import pytest
import os
import json
from tortuga.engine import Engine
from tortuga.action import Action, PreflightResult, ActionResult, ActionStrings
from tortuga.registry import registry
from tortuga.transaction import TransactionLog

class MockSafeAction(Action):
    id = "SH-MOCK1"
    module = "system_hardening"
    min_level = 1
    platforms = ["win", "lin", "mac"]
    strings = ActionStrings("Mock 1", "Mock 1 ES", "Explain 1", "Explain 1 ES")

    def preflight(self):
        return PreflightResult(is_active=False, impact_message="No impact expected")
        
    def apply(self):
        return ActionResult(success=True, prior_state={"test": 1}, undo_command="echo undo1")
        
    def rollback(self, prior_state):
        return prior_state.get("test") == 1

class MockRiskyAction(Action):
    id = "SH-MOCK2"
    module = "system_hardening"
    min_level = 3
    platforms = ["win", "lin", "mac"]
    strings = ActionStrings("Mock 2", "Mock 2 ES", "Explain 2", "Explain 2 ES")

    def preflight(self):
        return PreflightResult(is_active=True, impact_message="Service is actively in use!", demote_to_manual_confirm=True)
        
    def apply(self):
        return ActionResult(success=True, prior_state={"test": 2}, undo_command="echo undo2")

@pytest.fixture(autouse=True)
def setup_registry():
    registry._actions.clear()
    registry.register(MockSafeAction())
    registry.register(MockRiskyAction())

def test_dry_run_plan():
    engine = Engine(dry_run=True)
    plan = engine.plan("system_hardening", 5)
    
    # Check that we got 2 actions because both min_level <= 5
    assert len(plan) == 2
    
    safe_plan = [p for p in plan if p["action"].id == "SH-MOCK1"][0]
    assert not safe_plan["preflight"].demote_to_manual_confirm
    
    risky_plan = [p for p in plan if p["action"].id == "SH-MOCK2"][0]
    assert risky_plan["preflight"].demote_to_manual_confirm

def test_transaction_log(tmp_path):
    log_dir = tmp_path / "rollback"
    tx = TransactionLog(str(log_dir))
    tx.record("SH-MOCK1", {"test": 1}, "echo undo1")
    
    log_file = os.path.join(str(log_dir), f"{tx.current_run_id}.json")
    assert os.path.exists(log_file)
    
    data = TransactionLog.load(log_file)
    assert len(data["actions"]) == 1
    assert data["actions"][0]["action_id"] == "SH-MOCK1"
    assert data["actions"][0]["undo_command"] == "echo undo1"
