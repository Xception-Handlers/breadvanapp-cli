import click
from flask.cli import with_appcontext
from App.controllers import inbox_for_resident, inbox_for_driver

@click.command("inbox", help="View inbox as driver or resident")
@with_appcontext
def inbox():
    role = click.prompt("Are you a DRIVER or RESIDENT?",
                        type=click.Choice(["DRIVER", "RESIDENT"], case_sensitive=False)).upper()
    if role == "RESIDENT":
        resident_no = click.prompt("Enter RESIDENT user id", type=int)
        out = inbox_for_resident(resident_no)
        click.echo(out)
        return

    driver_no = click.prompt("Enter DRIVER user id", type=int)
    out = inbox_for_driver(driver_no)
    click.echo(out)

def register(app):
    app.cli.add_command(inbox)