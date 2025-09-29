import click
from flask.cli import with_appcontext, AppGroup
from App.controllers import request_stop_flow

request_cli = AppGroup("request", help="Resident request commands")

@request_cli.command("stop", help="Resident requests a stop from a chosen driver")
@with_appcontext
def request_stop():
    resident_no = click.prompt("Enter RESIDENT user id", type=int)

    #list drivers scheduled to the street
    listing = request_stop_flow(resident_no, confirm=False, chosen_driver_no=None)
    msg = listing.get("message", "")
    click.echo(msg)
    drivers = listing.get("drivers", [])
    if not drivers:
        return

    click.echo("Drivers scheduled to your street:")
    for d in drivers:
        click.echo(f'  driver id={d["driverNo"]}  username={d["username"]}')

    yn = click.prompt("Would you like to request a stop? (y/n)", type=str).strip().lower()
    if yn != "y":
        click.echo("Cancelled.")
        return

    chosen_driver_no = click.prompt("Enter DRIVER user id to request", type=int)
    note = click.prompt("Optional note", default="", show_default=False)
    out = request_stop_flow(resident_no, confirm=True, chosen_driver_no=chosen_driver_no, note=note)
    click.echo(out)

def register(app):
    app.cli.add_command(request_cli)