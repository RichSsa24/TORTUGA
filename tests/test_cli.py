from click.testing import CliRunner
from tortuga.cli import cli

def test_cli_harden_dry_run():
    runner = CliRunner()
    result = runner.invoke(cli, ['harden', '--module', 'system_hardening', '--level', '1'])
    assert result.exit_code == 0
    assert "DRY RUN COMPLETE" in result.output

def test_cli_harden_apply():
    runner = CliRunner()
    # Apply with an unknown module to test graceful failure or just execution path
    result = runner.invoke(cli, ['harden', '--module', 'system_hardening', '--level', '1', '--apply'])
    # Since we are mocking or just running basic actions, it might try to run.
    # We should expect exit code 0 or check output
    assert result.exit_code == 0
    assert "APPLYING CHANGES" in result.output
    
def test_cli_rollback_invalid():
    runner = CliRunner()
    result = runner.invoke(cli, ['rollback', 'invalid_id.json'])
    # Should fail nicely instead of traceback
    assert result.exit_code != 0

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "TORTUGA" in result.output
