from pprint import pprint


def test_insert_zero_records(client):
    resp = client.post("/day/values", json=[])
    pprint(resp.json())
    assert resp.status_code == 200
    assert resp.json() == {}


def test_insert_single_record_new_day(client, solar_repo):
    resp = client.post(
        "/day/values",
        json=[
            {
                "start_date": "2023-03-01T06:00+00:00",
                "end_date": "2023-03-01T06:15+00:00",
                "value": None,
            },
            {
                "start_date": "2023-03-01T06:15+00:00",
                "end_date": "2023-03-01T06:30+00:00",
                "value": 100,
            },
        ],
    )
    json = resp.json()
    pprint(json)
    assert resp.status_code == 200
    assert json["nInserted"] == 1
    day = solar_repo.find_one_by({})
    assert day.date.isoformat() == "2023-03-01T00:00:00"
    assert day.values


def test_respond_with_date(client, solar_day_3_10):
    resp = client.get("/day/2023-03-10")
    json = resp.json()
    pprint(json)
    assert resp.status_code == 200
