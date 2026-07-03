from tortuga.action import Action, PreflightResult, ActionResult, ActionStrings
from tortuga.registry import registry
import json

class ActionUAC(Action):
    id = "SH-001"
    module = "system_hardening"
    min_level = 1
    platforms = ["win"]
    strings = ActionStrings(
        title_en="Enable UAC",
        title_es="Habilitar UAC",
        explain_en="User Account Control prevents unauthorized changes to the OS.",
        explain_es="User Account Control previene cambios no autorizados al SO."
    )

    def preflight(self) -> PreflightResult:
        # Checking if UAC is fully disabled
        script = "@{ value = (Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' -ErrorAction SilentlyContinue).EnableLUA }"
        res = self.run_ps(script)
        is_disabled = res.get("value") == 0
        return PreflightResult(
            is_active=False,
            impact_message="UAC will prompt for admin actions. Highly recommended.",
            demote_to_manual_confirm=False
        )

    def apply(self) -> ActionResult:
        # Capture current state
        check_script = """
        $val = (Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' -ErrorAction SilentlyContinue).EnableLUA
        if ($null -eq $val) { $val = 1 }
        @{ EnableLUA = $val }
        """
        prior_state = self.run_ps(check_script)
        
        # Apply change (EnableLUA = 1)
        apply_script = "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' -Value 1"
        self.run_ps(apply_script)
        
        return ActionResult(
            success=True, 
            prior_state=prior_state,
            undo_command=f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' -Value {prior_state.get('EnableLUA', 1)}"
        )

    def rollback(self, prior_state: dict) -> bool:
        val = prior_state.get("EnableLUA", 1)
        script = f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'EnableLUA' -Value {val}"
        res = self.run_ps(script)
        return "error" not in res

class ActionAutorun(Action):
    id = "SH-003"
    module = "system_hardening"
    min_level = 2
    platforms = ["win"]
    strings = ActionStrings(
        title_en="Disable Autorun",
        title_es="Deshabilitar Autorun",
        explain_en="Prevents malware on USB drives from automatically executing.",
        explain_es="Previene que el malware en unidades USB se ejecute automáticamente."
    )

    def preflight(self) -> PreflightResult:
        return PreflightResult(
            is_active=False,
            impact_message="USB drives will not automatically pop up or run programs when inserted.",
            demote_to_manual_confirm=False
        )

    def apply(self) -> ActionResult:
        check_script = """
        $val = (Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoDriveTypeAutoRun' -ErrorAction SilentlyContinue).NoDriveTypeAutoRun
        if ($null -eq $val) { $val = 0 }
        @{ NoDriveTypeAutoRun = $val }
        """
        prior_state = self.run_ps(check_script)
        
        # 255 (0xFF) disables AutoRun on all drives
        apply_script = """
        if (!(Test-Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer')) {
            New-Item -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Force | Out-Null
        }
        Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoDriveTypeAutoRun' -Value 255
        """
        self.run_ps(apply_script)
        
        return ActionResult(
            success=True, 
            prior_state=prior_state,
            undo_command=f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoDriveTypeAutoRun' -Value {prior_state.get('NoDriveTypeAutoRun', 0)}"
        )

    def rollback(self, prior_state: dict) -> bool:
        val = prior_state.get("NoDriveTypeAutoRun", 0)
        script = f"Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoDriveTypeAutoRun' -Value {val}"
        res = self.run_ps(script)
        return "error" not in res

# Register actions
registry.register(ActionUAC())
registry.register(ActionAutorun())
