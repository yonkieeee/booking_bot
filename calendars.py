import requests
STANYTSIA_TEAMUP_CALENDAR_ID = "kstbv5srw3gter52zv"
STANYTSIA_TEAMUP_API_KEY = "b7f1db771ffa1ac9d41d196d17b946ca62ecc6325e379cbf4fcd925238303f4e"

VYNNYKY_TEAMUP_CALENDAR_ID = "ksnkruqk4d9xezc8r7"
VYNNYKY_TEAMUP_API_KEY = "b7f1db771ffa1ac9d41d196d17b946ca62ecc6325e379cbf4fcd925238303f4e"


def get_subcalendars(TEAMUP_CALENDAR_ID, TEAMUP_API_KEY):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/subcalendars"
    headers = {"Teamup-Token": TEAMUP_API_KEY, "Accept": "application/json"}
   
    response = requests.get(url, headers=headers)
    data=response.json()
    info=data['subcalendars']
    rooms={}
    for index in info:
        rooms[index['name']]=index["id"]
        
    return rooms
