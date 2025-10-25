import pytest

@pytest.mark.integration
def test_login_and_protected_routes(client):
    from App.controllers import create_user
    app = client.application
    with app.app_context():
        try:
            create_user("bob","bobpass","DRIVER")
        except Exception:
            pass

    res = client.post("/api/auth/login", json={"username":"bob","password":"bobpass"})
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get("/api/users", headers=headers)
    assert r.status_code == 200
    assert "drivers" in r.get_json()
    
@pytest.mark.integration
def test_full_flow(client, auth_header):
    r = client.post("/api/users", headers=auth_header, json={
        "username":"alice","password":"alicepass","role":"RESIDENT","street":"High Street"
    })
    assert r.status_code in (200,201)

    d = client.post("/api/users", headers=auth_header, json={
        "username":"rob","password":"robpass","role":"DRIVER"
    })
    assert d.status_code in (200,201)

    s = client.post("/api/drives", headers=auth_header, json={"driverNo":1, "street":"High Street"})
    assert s.status_code in (200,201)

    u = client.put("/api/drivers/1/status", headers=auth_header, json={"status":"EN_ROUTE","location":"Gas station"})
    assert u.status_code == 200
    assert u.get_json()["driver"]["status"] == "EN_ROUTE"

    q = client.post("/api/requests", headers=auth_header, json={
        "residentNo":1,"driverNo":1,"confirm":True,"note":"Please stop by #42"
    })
    assert q.status_code in (200,201)