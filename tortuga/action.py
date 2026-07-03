import json
import subprocess # nosec B404
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ActionStrings:
    title_en: str
    title_es: str
    explain_en: str
    explain_es: str

@dataclass
class PreflightResult:
    is_active: bool
    impact_message: str
    demote_to_manual_confirm: bool = False

@dataclass
class ActionResult:
    success: bool
    prior_state: Dict[str, Any]
    error_message: str = ""
    undo_command: str = ""

class Action:
    """Base class for all TORTUGA actions."""
    
    id: str = ""
    module: str = ""  # system_hardening, network_security, privacy
    min_level: int = 1
    platforms: List[str] = field(default_factory=list) # "win", "lin", "mac"
    strings: ActionStrings = None
    risk_note: str = ""
    framework_refs: List[str] = field(default_factory=list)

    def check(self) -> Dict[str, Any]:
        """Returns the current state of the configuration."""
        raise NotImplementedError

    def preflight(self) -> PreflightResult:
        """Dynamically detects active usage to predict impact and require confirmation if in use."""
        raise NotImplementedError

    def apply(self) -> ActionResult:
        """Idempotently applies the hardening change and returns the prior state snapshot."""
        raise NotImplementedError

    def rollback(self, prior_state: Dict[str, Any]) -> bool:
        """Restores the system to the exact prior state."""
        raise NotImplementedError

    def _run_subprocess(self, cmd: list[str]) -> subprocess.CompletedProcess:
        """Helper to run a subprocess safely without shell execution."""
        return subprocess.run(cmd, capture_output=True, text=True, check=False) # nosec B603
        
    def run_ps(self, script_block: str) -> Dict[str, Any]:
        """Runs a PowerShell script block and parses the JSON output."""
        # Wrap the script block to force JSON output
        wrapped = f"try {{ $Result = & {{ {script_block} }}; if ($Result -ne $null) {{ $Result | ConvertTo-Json -Compress }} else {{ '{{}}' }} }} catch {{ @{{ error = $_.Exception.Message }} | ConvertTo-Json -Compress }}"
        cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", wrapped]
        res = self.run_command(cmd)
        if res.returncode != 0 and not res.stdout.strip():
            return {"error": res.stderr.strip() or f"PowerShell exited with code {res.returncode}"}
        try:
            return json.loads(res.stdout.strip() or "{}")
        except json.JSONDecodeError:
            return {"error": "Failed to parse PowerShell output", "raw": res.stdout}

    def run_bash(self, script_block: str) -> Dict[str, Any]:
        """Runs a bash script block and parses the JSON output."""
        # The bash script is expected to output a JSON string at the end.
        cmd = ["bash", "-c", script_block]
        res = self.run_command(cmd)
        if res.returncode != 0 and not res.stdout.strip():
            return {"error": res.stderr.strip() or f"Bash exited with code {res.returncode}"}
        try:
            return json.loads(res.stdout.strip() or "{}")
        except json.JSONDecodeError:
            return {"error": "Failed to parse Bash output as JSON", "raw": res.stdout}
