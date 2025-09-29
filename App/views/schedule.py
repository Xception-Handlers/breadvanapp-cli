import click
from flask.cli import with_appcontext, AppGroup
from App.controllers import schedule_drive_by_driver_no

schedule_cli = AppGroup("schedule", help="Scheduling commands")

@schedule_cli.command("drive", help="Schedule a drive for a driver to a street")
@with_appcontext
def schedule_drive():
    driver_no = click.prompt("Enter DRIVER user id", type=int)
    street = click.prompt("Enter street name")
    s = street.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        s = s[1:-1].strip()
    street = s

    out = schedule_drive_by_driver_no(driver_no, street)
    click.echo(out)

def register(app):
    app.cli.add_command(schedule_cli)