import json
import os
from datetime import datetime
from typing import Dict, Any, List

class TransactionLog:
    def __init__(self, log_dir: str = "rollback"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        self.current_run_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.log_path = os.path.join(self.log_dir, f"{self.current_run_id}.json")
        self.entries: List[Dict[str, Any]] = []

    def record(self, action_id: str, prior_state: Dict[str, Any], undo_cmd: str):
        entry = {
            "action_id": action_id,
            "timestamp": datetime.now().isoformat(),
            "prior_state": prior_state,
            "undo_command": undo_cmd
        }
        self.entries.append(entry)
        self._flush()

    def _flush(self):
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump({"run_id": self.current_run_id, "actions": self.entries}, f, indent=2)
        # Ensure restrictive permissions (600) on UNIX, Windows uses ACLs but we do our best via Python
        if os.name != 'nt':
            os.chmod(self.log_path, 0o600)

    @classmethod
    def load(cls, log_path: str) -> Dict[str, Any]:
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
