import requests
from key import SHEETY_USERNAME, BEARER_AUTHENTICATION
from pprint import pprint

SHEETY_PRICES_ENDPOINT = f"https://api.sheety.co/{SHEETY_USERNAME}/flightDeals"
SHEETY_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {BEARER_AUTHENTICATION}"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.user_data = {}

    def get_destination_data(self):
        response = requests.get(url=f"{SHEETY_PRICES_ENDPOINT}/prices", headers=SHEETY_HEADERS)
        self.destination_data = response.json()["prices"]
        # pprint(self.destination_data)
        return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/prices/{city['id']}", json=new_data, headers=SHEETY_HEADERS)
            print(response.text)

    def get_email_list(self):
        response = requests.get(url=f"{SHEETY_PRICES_ENDPOINT}/users", headers=SHEETY_HEADERS)
        self.user_data = response.json()["users"]
        # pprint(self.destination_data)
        return self.user_data
