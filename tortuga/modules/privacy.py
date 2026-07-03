from tortuga.action import Action, PreflightResult, ActionResult, ActionStrings
from tortuga.registry import registry

class ActionDisableTelemetry(Action):
    id = "PR-001"
    module = "privacy"
    min_level = 2
    platforms = ["win"]
    strings = ActionStrings(
        title_en="Disable OS Telemetry",
        title_es="Deshabilitar Telemetría",
        explain_en="Reduces the diagnostic data Windows sends to Microsoft.",
        explain_es="Reduce los datos de diagnóstico que Windows envía a Microsoft."
    )

    def preflight(self) -> PreflightResult:
        return PreflightResult(
            is_active=False,
            impact_message="OS provides less crash data to vendor.",
            demote_to_manual_confirm=False
        )

    def apply(self) -> ActionResult:
        check_script = """
        $val = (Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -ErrorAction SilentlyContinue).AllowTelemetry
        if ($null -eq $val) { $val = 3 } # Default Full
        @{ AllowTelemetry = $val }
        """
        prior_state = self.run_ps(check_script)
        
        # Set telemetry to 0 (Security) or 1 (Basic)
        apply_script = """
        if (!(Test-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection')) {
            New-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Force | Out-Null
        }
        Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Value 0
        """
        self.run_ps(apply_script)
        
        return ActionResult(
            success=True, 
            prior_state=prior_state,
            undo_command=f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Value {prior_state.get('AllowTelemetry', 3)}"
        )

    def rollback(self, prior_state: dict) -> bool:
        val = prior_state.get("AllowTelemetry", 3)
        script = f"Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Value {val}"
        res = self.run_ps(script)
        return "error" not in res

registry.register(ActionDisableTelemetry())
