import click
from typing import List, Optional
from tortuga.registry import registry
from tortuga.transaction import TransactionLog

class Engine:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.tx_log = TransactionLog() if not dry_run else None

    def plan(self, module: str, level: int) -> List[dict]:
        """Generates an execution plan by checking preflight for all actions."""
        actions = registry.get_actions_for_level(module, level)
        plan_results = []
        for act in actions:
            try:
                pf_result = act.preflight()
                plan_results.append({
                    "action": act,
                    "preflight": pf_result
                })
            except Exception as e:
                plan_results.append({
                    "action": act,
                    "preflight": None,
                    "error": str(e)
                })
        return plan_results

    def apply_plan(self, plan: List[dict]):
        """Executes the plan, asking for confirmation if needed."""
        for item in plan:
            act = item["action"]
            pf = item["preflight"]
            
            if pf and pf.demote_to_manual_confirm:
                click.secho(f"\n[WARNING] Action {act.id} requires explicit confirmation:", fg="yellow")
                click.echo(f"Impact: {pf.impact_message}")
                if not click.confirm("Do you want to proceed with this action?"):
                    click.secho(f"Skipping {act.id}", fg="yellow")
                    continue
                    
            if not self.dry_run:
                click.echo(f"Applying {act.id}...")
                try:
                    res = act.apply()
                    if res.success:
                        self.tx_log.record(act.id, res.prior_state, res.undo_command)
                        click.secho(f"Success: {act.id}", fg="green")
                        click.echo(f"Undo Command: {res.undo_command}")
                    else:
                        click.secho(f"Failed {act.id}: {res.error_message}", fg="red")
                except Exception as e:
                    click.secho(f"Exception in {act.id}: {e}", fg="red")

    def rollback_run(self, run_id_path: str):
        """Rolls back an entire transaction log."""
        data = TransactionLog.load(run_id_path)
        # Rollback in reverse order
        actions_to_rollback = reversed(data.get("actions", []))
        for entry in actions_to_rollback:
            act_id = entry["action_id"]
            act = registry.get_action_by_id(act_id)
            if not act:
                click.secho(f"Action {act_id} not found in registry. Manual rollback needed.", fg="red")
                continue
                
            click.echo(f"Rolling back {act_id}...")
            try:
                success = act.rollback(entry["prior_state"])
                if success:
                    click.secho(f"Successfully rolled back {act_id}", fg="green")
                else:
                    click.secho(f"Failed to rollback {act_id}", fg="red")
            except Exception as e:
                click.secho(f"Exception rolling back {act_id}: {e}", fg="red")
