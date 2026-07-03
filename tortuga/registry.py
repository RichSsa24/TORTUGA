from typing import List, Dict
from tortuga.action import Action
import platform

class ActionRegistry:
    def __init__(self):
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action):
        self._actions[action.id] = action

    def get_actions_for_level(self, module: str, level: int) -> List[Action]:
        """Returns applicable actions up to the specified level for the current OS."""
        current_os = self._get_os_shortname()
        applicable = []
        for act in self._actions.values():
            if act.module == module and act.min_level <= level and current_os in act.platforms:
                applicable.append(act)
        return applicable
    
    def get_action_by_id(self, action_id: str) -> Action:
        return self._actions.get(action_id)

    def _get_os_shortname(self) -> str:
        sysname = platform.system().lower()
        if sysname == "windows":
            return "win"
        elif sysname == "darwin":
            return "mac"
        elif sysname == "linux":
            import os
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    content = f.read().lower()
                    if "ubuntu" in content or "debian" in content:
                        return "lin"
            print("[WARNING] Non-Debian/Ubuntu Linux detected. Proceed with caution.")
            return "lin"
        return "unknown"

# Global registry instance
registry = ActionRegistry()
