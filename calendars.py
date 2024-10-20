import requests
STANYTSIA_TEAMUP_CALENDAR_ID = "ksmr4o4huehb9n9sph"
STANYTSIA_TEAMUP_API_KEY = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"

VYNNYKY_TEAMUP_CALENDAR_ID = "kss1wi3w8rpsfzgjhz"
VYNNYKY_TEAMUP_API_KEY = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"


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
