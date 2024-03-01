import httpx
from os import environ as env
from datetime import datetime, timedelta,timezone
url = env.get("API_URL")

bot_username = env.get("BOT_USERNAME")
async def get_data(id):
    async with httpx.AsyncClient() as client:
        response = await client.get(url+id)
    print(response)
    print(url+id)
    return response.json()
def convert_date(date:str, n:int):
    current_date = datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]))
    next_day = current_date + timedelta(days=n)
    return next_day.strftime("%Y-%m-%d")
def get_time():
    utc_timezone = timezone.utc
    ist_offset = timedelta(hours=5, minutes=30)
    utc_now = datetime.now(utc_timezone)
    ist_now = utc_now + ist_offset
    time = ist_now.strftime("%Y-%m-%d %H:%M:%S IST")
    return time
async def generate_text(data:dict):
    response = data.get("body")
    quota = data.get("meta")['quota']
    text= f"**ℹ️ PNR Status Enquiry**\n\n"
    text += f"**PNR :**  `{response['pnr_number']}`\n"
    text += f"**👥 No of Passengers :**  `{response['no_of_passengers']}`\n"
    text += f"**🚆 Train :**  `{response['train_name']}` {response['train_number']}\n"
    text+= f"**🎟️ Booking Details :**  ` {response['class']}` `{quota[response['quota']]}`\n"
    text+=f"**📊 Chart Prepared :** `{'✅Prepared' if response['chart_prepared'] else '❌Not Yet'}`\n"
    day_count = int(response['boarding_station']['day_count'])
    date = response['date'] if day_count <=1 else convert_date(response['date'], day_count-1)
    text+= f"**🕒 Departure :** `{date}` | `{response['boarding_station']['departure_time']}` | **{response['boarding_station']['station_name']}**\n"
    text+=f"**⏱️ Journey Duration** : `{response['journey_duration']}`\n"
    day_count = int(response['reservation_upto']['day_count'])
    aravial_date = response['date'] if day_count <=1 else convert_date(response['date'], day_count-1)
    text+= f"**🛬 Arrival :** `{aravial_date}` | `{response['reservation_upto']['arrival_time']}` | **{response['reservation_upto']['station_name']}**\n\n"
    text+= "Name|Age|Booking Status|Current Status\n"
    for i, passenger in enumerate(response['pax_info'], start=1):
        text+= f"|-> 🤵 `P{i}` | `{passenger['passengerAge']}` | `{passenger['bookingStatus']}/{passenger['bookingBerthNo']}` | `{passenger['currentStatus']}/{passenger['currentBerthNo']}`    (**{passenger['currentStatusDisplayText']}**)\n"
    text+= f"\n**ℹ️ Pnr Message :** `{response['pnr_message']}`\n"
    text+= f"**🕰️ Last Updated :** `{get_time()}`\n"
    return text

    
error_message = """
Getting Error while processing your request.
You may find error message below.
❌**Error:** `{}`
`{}`
"""
