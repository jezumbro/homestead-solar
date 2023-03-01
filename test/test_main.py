def test_main_app_starts(client):
    resp = client.get("/docs")
    assert resp.status_code == 200, "should get 200 code"
