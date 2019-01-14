import pytest
import requests
import json

# Import the testing data.
import data.data as data

API_URL = 'http://localhost:5000'

workout_url = API_URL + '/workout/'
user_url = API_URL + '/user/'

def test_get_workout():
    object_id = '5c395e6dc62a663afe045e00'
    response = requests.get(workout_url + object_id)
    data = response.json()
    resource = data['resource']
    assert resource['distance'] == 3.69
    assert resource['title'] == 'Outdoor Run'
def test_get_all_workouts():
    pass

def test_get_user():
    object_id = '5c3c03c7c62a6647e3204792'
    response = requests.get(user_url + object_id)
    data = response.json()
    resource = data['resource']
    assert resource['first_name'] == 'Ethan'
    assert resource['last_name'] == 'Swan'
