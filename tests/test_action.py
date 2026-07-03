import pytest
import platform
from tortuga.action import Action

class DummyAction(Action):
    id = "TEST-01"
    module = "test"
    min_level = 1
    platforms = ["win", "lin", "mac"]
    
    def preflight(self): pass
    def apply(self): pass
    def rollback(self, prior_state): pass

def test_run_command_success():
    action = DummyAction()
    # Cross-platform simple command
    res = action.run_command(["python", "-c", "print('hello')"])
    assert res.returncode == 0
    assert "hello" in res.stdout

def test_run_command_failure():
    action = DummyAction()
    res = action.run_command(["python", "-c", "import sys; sys.exit(1)"])
    assert res.returncode == 1

@pytest.mark.skipif(platform.system() != "Windows", reason="Requires PowerShell")
def test_run_ps_success():
    action = DummyAction()
    # Execute a simple PS script that returns a dict/hashtable
    res = action.run_ps("@{ status = 'ok'; code = 200 }")
    assert "error" not in res
    assert res.get("status") == "ok"
    assert res.get("code") == 200

@pytest.mark.skipif(platform.system() != "Windows", reason="Requires PowerShell")
def test_run_ps_error_handling():
    action = DummyAction()
    # Invalid script
    res = action.run_ps("Throw 'Simulated error'")
    assert "error" in res
    assert "Simulated error" in res["error"]

@pytest.mark.skipif(platform.system() == "Windows", reason="Requires Bash")
def test_run_bash_success():
    action = DummyAction()
    res = action.run_bash("echo '{\"status\": \"ok\", \"code\": 200}'")
    assert "error" not in res
    assert res.get("status") == "ok"
    assert res.get("code") == 200

@pytest.mark.skipif(platform.system() == "Windows", reason="Requires Bash")
def test_run_bash_error_handling():
    action = DummyAction()
    res = action.run_bash("exit 1")
    assert "error" in res
