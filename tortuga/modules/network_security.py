from tortuga.action import Action, PreflightResult, ActionResult, ActionStrings
from tortuga.registry import registry

class ActionDisableSMBv1(Action):
    id = "NS-003"
    module = "network_security"
    min_level = 3
    platforms = ["win"]
    strings = ActionStrings(
        title_en="Disable SMBv1",
        title_es="Deshabilitar SMBv1",
        explain_en="SMBv1 is an obsolete protocol vulnerable to ransomware like WannaCry.",
        explain_es="SMBv1 es un protocolo obsoleto vulnerable a ransomware como WannaCry."
    )

    def preflight(self) -> PreflightResult:
        # Check if SMBv1 is currently active or has sessions
        script = """
        $hasSessions = @(Get-SmbSession | Where-Object Dialect -eq '1.0.2').Count -gt 0
        @{ InUse = $hasSessions }
        """
        res = self.run_ps(script)
        in_use = res.get("InUse", False)
        
        return PreflightResult(
            is_active=in_use,
            impact_message="Breaks connection to very old NAS devices (pre-2010)." + (" ACTIVE SMBv1 SESSIONS DETECTED!" if in_use else ""),
            demote_to_manual_confirm=in_use
        )

    def apply(self) -> ActionResult:
        # Capture current feature state (this is for Windows 10/11)
        check_script = """
        $state = (Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -ErrorAction SilentlyContinue).State
        if ($null -eq $state) { $state = 'Disabled' } else { $state = $state.ToString() }
        @{ SMB1State = $state }
        """
        prior_state = self.run_ps(check_script)
        
        # Disable SMBv1
        apply_script = "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"
        res = self.run_ps(apply_script)
        
        return ActionResult(
            success="error" not in res, 
            prior_state=prior_state,
            error_message=res.get("error", ""),
            undo_command="Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"
        )

    def rollback(self, prior_state: dict) -> bool:
        state = prior_state.get("SMB1State", "Disabled")
        if state == "Enabled":
            script = "Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"
        else:
            script = "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"
        res = self.run_ps(script)
        return "error" not in res

registry.register(ActionDisableSMBv1())
