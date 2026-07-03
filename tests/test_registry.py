from tortuga.registry import ActionRegistry
from tortuga.action import Action

class MockWinAction(Action):
    id = "WIN-1"
    module = "test"
    min_level = 1
    platforms = ["win"]
    def preflight(self): pass
    def apply(self): pass
    def rollback(self, prior_state): pass

class MockLinAction(Action):
    id = "LIN-1"
    module = "test"
    min_level = 1
    platforms = ["lin"]
    def preflight(self): pass
    def apply(self): pass
    def rollback(self, prior_state): pass

def test_registry_registration():
    registry = ActionRegistry()
    registry.register(MockWinAction())
    registry.register(MockLinAction())
    
    assert len(registry._actions) == 2
    assert "WIN-1" in registry._actions
    assert "LIN-1" in registry._actions

def test_registry_filtering(monkeypatch):
    registry = ActionRegistry()
    registry.register(MockWinAction())
    registry.register(MockLinAction())
    
    # Force OS to 'win'
    monkeypatch.setattr(registry, "_get_os_shortname", lambda: "win")
    
    actions = registry.get_actions_for_level(module="test", level=5)
    assert len(actions) == 1
    assert actions[0].id == "WIN-1"
    
    # Force OS to 'lin'
    monkeypatch.setattr(registry, "_get_os_shortname", lambda: "lin")
    actions = registry.get_actions_for_level(module="test", level=5)
    assert len(actions) == 1
    assert actions[0].id == "LIN-1"
