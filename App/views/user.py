import click
from flask.cli import with_appcontext, AppGroup
from App.controllers import (
    create_user_interactive,
    list_users_grouped,
)

#cretae user
@click.command("create-user", help="Interactively create a user")
@with_appcontext
def create_user():
    username = click.prompt("Enter username")
    password = click.prompt("Enter password", hide_input=True)
    role = click.prompt("Is this user a DRIVER or RESIDENT?",
                        type=click.Choice(["DRIVER", "RESIDENT"], case_sensitive=False)).upper()

    street = None
    if role == "RESIDENT":
        street = click.prompt('Enter street (e.g., "street")')
        s = street.strip()
        if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
            s = s[1:-1].strip()
        street = s

    out = create_user_interactive(username, password, role, street)
    click.echo(out)

#list them
list_cli = AppGroup("list", help="List helpers")

@list_cli.command("users", help="List all users grouped by role with role-specific IDs")
@with_appcontext
def list_users():
    out = list_users_grouped()

    click.echo("DRIVERS:")
    if out["drivers"]:
        for d in out["drivers"]:
            click.echo(f'  id={d["driverNo"]}  username={d["username"]}')
    else:
        click.echo("  (none)")

    click.echo("\nRESIDENTS:")
    if out["residents"]:
        for r in out["residents"]:
            click.echo(f'  id={r["residentNo"]}  username={r["username"]}  street={r["street"]}')
    else:
        click.echo("  (none)")

def register(app):
    app.cli.add_command(create_user)
    app.cli.add_command(list_cli)