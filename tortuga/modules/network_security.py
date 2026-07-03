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

class ActionUFWEnable(Action):
    id = "NS-001-Lin"
    module = "network_security"
    min_level = 1
    platforms = ["lin"]
    strings = ActionStrings(
        title_en="Enable OS Firewall (UFW)",
        title_es="Habilitar Cortafuegos (UFW)",
        explain_en="Enables the Uncomplicated Firewall to block inbound connections.",
        explain_es="Habilita UFW para bloquear conexiones entrantes."
    )

    def preflight(self) -> PreflightResult:
        script = '''
        if command -v ufw >/dev/null; then
            echo '{"installed": true}'
        else
            echo '{"installed": false}'
        fi
        '''
        res = self.run_bash(script)
        if not res.get("installed", False):
            return PreflightResult(False, "UFW is not installed. Action will fail.", False)
        return PreflightResult(False, "UFW will be enabled. All inbound connections blocked by default.", False)

    def apply(self) -> ActionResult:
        check_script = '''
        if ufw status | grep -q "Status: active"; then
            echo '{"status": "active"}'
        else
            echo '{"status": "inactive"}'
        fi
        '''
        prior_state = self.run_bash(check_script)
        self.run_bash("ufw --force enable && echo '{}'")
        return ActionResult(True, prior_state, undo_command="ufw disable")

    def rollback(self, prior_state: dict) -> bool:
        if prior_state.get("status") == "inactive":
            res = self.run_bash("ufw disable && echo '{}'")
        else:
            res = self.run_bash("ufw --force enable && echo '{}'")
        return "error" not in res

class ActionCloseTelnetFTP(Action):
    id = "NS-004-Lin"
    module = "network_security"
    min_level = 4
    platforms = ["lin"]
    strings = ActionStrings(
        title_en="Close Telnet/FTP Ports",
        title_es="Cerrar puertos Telnet/FTP",
        explain_en="Disables insecure plaintext services.",
        explain_es="Deshabilita servicios inseguros de texto plano."
    )

    def preflight(self) -> PreflightResult:
        script = '''
        sessions=$(ss -tn | awk '$4 ~ /:(21|23)$/ {print $0}' | wc -l)
        echo "{\\"sessions\\": $sessions}"
        '''
        res = self.run_bash(script)
        sessions = res.get("sessions", 0)
        return PreflightResult(
            is_active=sessions > 0,
            impact_message=f"Disables FTP/Telnet. Active sessions: {sessions}",
            demote_to_manual_confirm=sessions > 0
        )

    def apply(self) -> ActionResult:
        # Note: A real implementation would parse systemctl status for inetd, vsftpd, etc.
        # This is a representative mock for the phase 3 proof of concept.
        prior_state = {"telnet_disabled": True, "ftp_disabled": True}
        return ActionResult(True, prior_state, undo_command="echo 'Re-enable services manually'")

    def rollback(self, prior_state: dict) -> bool:
        return True

registry.register(ActionUFWEnable())
registry.register(ActionCloseTelnetFTP())

class ActionDisableRemoteLoginMac(Action):
    id = "NS-005-Mac"
    module = "network_security"
    min_level = 4
    platforms = ["mac"]
    strings = ActionStrings(
        title_en="Disable Remote Login (SSH)",
        title_es="Deshabilitar Inicio de sesión remoto (SSH)",
        explain_en="Closes SSH to prevent remote unauthorized access.",
        explain_es="Cierra SSH para prevenir el acceso remoto no autorizado."
    )

    def preflight(self) -> PreflightResult:
        script = '''
        if systemsetup -getremotelogin | grep -q "On"; then
            echo '{"status": "on"}'
        else
            echo '{"status": "off"}'
        fi
        '''
        res = self.run_bash(script)
        is_on = res.get("status") == "on"
        return PreflightResult(is_on, "Disabling SSH will terminate existing remote sessions.", is_on)

    def apply(self) -> ActionResult:
        script_check = '''
        if systemsetup -getremotelogin | grep -q "On"; then
            echo '{"status": "on"}'
        else
            echo '{"status": "off"}'
        fi
        '''
        prior_state = self.run_bash(script_check)
        self.run_bash("systemsetup -setremotelogin off && echo '{}'")
        return ActionResult(True, prior_state, undo_command="systemsetup -setremotelogin on")

    def rollback(self, prior_state: dict) -> bool:
        if prior_state.get("status") == "on":
            res = self.run_bash("systemsetup -setremotelogin on && echo '{}'")
        else:
            res = self.run_bash("systemsetup -setremotelogin off && echo '{}'")
        return "error" not in res

registry.register(ActionDisableRemoteLoginMac())
