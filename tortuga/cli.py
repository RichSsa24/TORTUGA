import click
from tortuga.engine import Engine
from tortuga.i18n import i18n

@click.group()
def cli():
    """TORTUGA - OS Hardening, Simplified and Safe."""
    pass

@cli.command()
@click.option('--module', required=True, type=click.Choice(['system_hardening', 'network_security', 'privacy']))
@click.option('--level', required=True, type=click.IntRange(1, 5))
@click.option('--apply', is_flag=True, help="Actually apply the changes. Without this, it's a dry-run.")
def harden(module, level, apply):
    """Scan and apply hardening actions."""
    click.echo(f"Initializing TORTUGA for module: {module}, level: {level}")
    
    engine = Engine(dry_run=not apply)
    click.echo("Generating plan...")
    plan = engine.plan(module, level)
    
    click.echo("\n--- EXECUTION PLAN ---")
    for item in plan:
        act = item["action"]
        pf = item["preflight"]
        title, why = i18n.get(act.strings)
        click.secho(f"\nAction: {act.id} - {title}", fg="cyan")
        click.echo(f"Why: {why}")
        if pf:
            if pf.demote_to_manual_confirm:
                click.secho(f"Impact: {pf.impact_message} [REQUIRES CONFIRMATION]", fg="yellow")
            else:
                click.echo(f"Impact: {pf.impact_message}")
        else:
            click.secho(f"Error checking preflight: {item.get('error')}", fg="red")
            
    if not apply:
        click.secho("\nDRY RUN COMPLETE. Use --apply to execute.", fg="green")
        return

    click.echo("\n--- APPLYING CHANGES ---")
    engine.apply_plan(plan)

@cli.command()
@click.argument('log_path', type=click.Path(exists=True))
def rollback(log_path):
    """Rollback a specific transaction log."""
    click.echo(f"Rolling back transaction: {log_path}")
    engine = Engine()
    engine.rollback_run(log_path)

if __name__ == '__main__':
    cli()
