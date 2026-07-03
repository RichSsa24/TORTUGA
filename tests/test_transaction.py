import os
import json
from tortuga.transaction import TransactionLog

def test_transaction_creation_and_load(tmp_path):
    log_dir = tmp_path / "rollback"
    tx = TransactionLog(str(log_dir))
    
    # Record a state
    tx.record("TEST-01", {"setting": "on"}, "undo_cmd_1")
    tx.record("TEST-02", {"setting": "off"}, "undo_cmd_2")
    
    # Ensure it writes correctly
    log_file = os.path.join(str(log_dir), f"{tx.current_run_id}.json")
    assert os.path.exists(log_file)
    
    # Load and verify
    data = TransactionLog.load(log_file)
    assert len(data["actions"]) == 2
    
    assert data["actions"][0]["action_id"] == "TEST-01"
    assert data["actions"][0]["prior_state"]["setting"] == "on"
    assert data["actions"][0]["undo_command"] == "undo_cmd_1"

    assert data["actions"][1]["action_id"] == "TEST-02"
    assert data["actions"][1]["undo_command"] == "undo_cmd_2"

def test_transaction_load_invalid():
    # Attempting to load a non-existent file
    data = TransactionLog.load("does_not_exist.json")
    assert data is None
