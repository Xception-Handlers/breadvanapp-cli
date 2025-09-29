import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (
    initialize,

    # Users
    create_user_interactive,
    list_users_grouped,

    # Driver ops
    schedule_drive_by_driver_no,
    set_status_by_driver_no,
    inbox_for_driver,

    #Resident ops
    inbox_for_resident,
    request_stop_flow,
)

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def init_cmd():
    out = initialize()
    print(out.get("message", "database initialized"))
    if "seed" in out:
        print(out["seed"])

#user
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user (prompts)")
def user_create_cmd():
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
    print(out)

@user_cli.command("list", help="Lists users in the database (grouped)")
@click.argument("format", default="string")
def list_user_command(format):
    out = list_users_grouped()
    if format == 'string':
        print("DRIVERS:")
        if out["drivers"]:
            for d in out["drivers"]:
                print(f'  id={d["driverNo"]}  username={d["username"]}')
        else:
            print("  (none)")
        print("\nRESIDENTS:")
        if out["residents"]:
            for r in out["residents"]:
                print(f'  id={r["residentNo"]}  username={r["username"]}  street={r["street"]}')
        else:
            print("  (none)")
    else:
        print(out)

app.cli.add_command(user_cli)

# schedudle
schedule_cli = AppGroup("schedule", help="Scheduling commands")

@schedule_cli.command("drive", help="Schedule a drive for a driver to a street")
def schedule_drive_cmd():
    driver_no = click.prompt("Enter DRIVER user id", type=int)
    street = click.prompt("Enter street name")
    s = street.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        s = s[1:-1].strip()
    out = schedule_drive_by_driver_no(driver_no, s)
    print(out)

app.cli.add_command(schedule_cli)

#driver stauts
driver_cli = AppGroup("driver", help="Driver utilities")

@driver_cli.command("status", help="Update or view a driver's status/location OR view inbox")
def driver_status_cmd():
    driver_no = click.prompt("Enter DRIVER user id", type=int)
    action = click.prompt("Type 'set' to update status/location or 'get' to view inbox",
                          type=click.Choice(["set", "get"], case_sensitive=False)).lower()

    if action == "get":
        out = inbox_for_driver(driver_no)
        print(out)
        return

    status = click.prompt("Status", type=click.Choice(["OFF_DUTY", "EN_ROUTE", "DELIVERING"], case_sensitive=False)).upper()
    location = click.prompt("Location note", default="", show_default=False)
    out = set_status_by_driver_no(driver_no, status, location or None)
    print(out)

app.cli.add_command(driver_cli)

#request
request_cli = AppGroup("request", help="Resident request commands")

@request_cli.command("stop", help="Resident requests a stop from a chosen driver")
def request_stop_cmd():
    resident_no = click.prompt("Enter RESIDENT user id", type=int)

    listing = request_stop_flow(resident_no, confirm=False, chosen_driver_no=None)
    msg = listing.get("message", "")
    print(msg)
    drivers = listing.get("drivers", [])
    if not drivers:
        return

    print("Drivers scheduled to your street:")
    for d in drivers:
        print(f'  driver id={d["driverNo"]}  username={d["username"]}')

    yn = click.prompt("Would you like to request a stop? (y/n)", type=str).strip().lower()
    if yn != "y":
        print("Cancelled.")
        return

    chosen_driver_no = click.prompt("Enter DRIVER user id to request", type=int)
    note = click.prompt("Optional note", default="", show_default=False)
    out = request_stop_flow(resident_no, confirm=True, chosen_driver_no=chosen_driver_no, note=note)
    print(out)

app.cli.add_command(request_cli)

#inbox
@app.cli.command("inbox", help="View inbox as driver or resident")
def inbox_cmd():
    from App.controllers import inbox_for_resident, inbox_for_driver
    role = click.prompt("Are you a DRIVER or RESIDENT?",
                        type=click.Choice(["DRIVER", "RESIDENT"], case_sensitive=False)).upper()
    if role == "RESIDENT":
        resident_no = click.prompt("Enter RESIDENT user id", type=int)
        out = inbox_for_resident(resident_no)
        print(out)
        return
    driver_no = click.prompt("Enter DRIVER user id", type=int)
    out = inbox_for_driver(driver_no)
    print(out)

#tests
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)