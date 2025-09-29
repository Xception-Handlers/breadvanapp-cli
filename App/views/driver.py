import click
from flask.cli import with_appcontext, AppGroup
from App.controllers import set_status_by_driver_no, inbox_for_driver

driver_cli = AppGroup("driver", help="Driver utilities")

@driver_cli.command("status", help="Update or view a driver's status/location OR view inbox")
@with_appcontext
def driver_status():
    driver_no = click.prompt("Enter DRIVER user id", type=int)
    action = click.prompt("Type 'set' to update status/location or 'get' to view inbox",
                          type=click.Choice(["set", "get"], case_sensitive=False)).lower()

    if action == "get":
        out = inbox_for_driver(driver_no)
        click.echo(out)
        return

    status = click.prompt("Status", type=click.Choice(["OFF_DUTY", "EN_ROUTE", "DELIVERING"], case_sensitive=False)).upper()
    location = click.prompt("Location note", default="", show_default=False)
    out = set_status_by_driver_no(driver_no, status, location or None)
    click.echo(out)

def register(app):
    app.cli.add_command(driver_cli)