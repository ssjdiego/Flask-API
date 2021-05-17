import requests
import json

def test_create_first_person():
    url = "http://127.0.0.1:5000/api/persons"
    headers = {"Content-Type": "application/json" } 
    payload = { "person_id": 1,
                "first_name":"Diego",
                "middle_name": "",
                "last_name": "Ortega",
                "email": "test1@test.com",
                "age": 28
                }
    response = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    assert response.status_code == 201

def test_create_second_person():
    url = "http://127.0.0.1:5000/api/persons"
    headers = {"Content-Type": "application/json" } 
    payload = { "person_id": 2,
                "first_name":"Test",
                "middle_name": "",
                "last_name": "User",
                "email": "test2@test.com",
                "age": 27
                }
    response = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))
    assert response.status_code == 201

def test_get_all_persons():
    url = "http://127.0.0.1:5000/api/persons"
    response = requests.get(url)
    assert response.status_code == 200


def test_get_second_person():
     response = requests.get("http://127.0.0.1:5000/api/persons/2")
     assert response.status_code == 200

def test_update_first_person():
    url = "http://127.0.0.1:5000/api/persons/1"
    headers = {"Content-Type": "application/json" } 
    payload = {"first_name":"NEW_NAME"}
    response = requests.put(url, headers=headers, data=json.dumps(payload,indent=4))
    assert response.status_code == 200

def test_get_first_person_first_version():
    url = "http://127.0.0.1:5000/api/persons/1/1"
    response = requests.get(url)
    assert response.status_code == 200


def test_delete_first_person():
    url = "http://127.0.0.1:5000/api/persons/1"
    response = requests.delete(url)
    assert response.status_code == 200


def test_delete_second_person():
    url = "http://127.0.0.1:5000/api/persons/2"
    response = requests.delete(url)
    assert response.status_code == 200