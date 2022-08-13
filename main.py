import requests
import datetime as dt
import smtplib
import time

MY_LAT = 20.976750  # Set Your Latitude
MY_LONG = 155.575280  # Set Your Longitude


def is_iss_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss = iss_response.json()
    iss_long = float(iss["iss_position"]['longitude'])
    iss_lat = float(iss["iss_position"]['latitude'])
    print(iss_lat, iss_long)
    if (MY_LAT - 5 <= iss_lat <= MY_LAT + 5) and (MY_LONG - 5 <= iss_long <= MY_LONG + 5):
        return True


def is_night():
    dn_params = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    dn_resp = requests.get("http://api.sunrise-sunset.org/json", dn_params)
    dn_resp.raise_for_status()
    day_night_data = dn_resp.json()
    sn = day_night_data['results']['sunrise']
    sun_rise = int(day_night_data['results']['sunrise'].split("T")[1].split(":")[0])
    sun_set = int(day_night_data['results']['sunset'].split("T")[1].split(":")[0])
    if dt.datetime.utcnow().hour > sun_set:
        return True

# You Can add your SMTP HOST and Credentials Here
def send_mail():
    host = "smtp.gmail.com"
    user = "xyz@gmail.com"
    password = "Gmail_app_password"
    with smtplib.SMTP(host, port=587) as connection:
        connection.starttls()
        connection.login(user=user, password=password)
        message = "Subject: ISS is Near You\n\n Hi User, The ISS is Now Visible From Your Location. Please Go Outside To See It.\nThank You"
        connection.sendmail(from_addr=user, to_addrs=user, msg=message)


def send_telegram_msg_via_ifttt():
    ifttt_key = "your ifttt key"
    requests.get(f"https://maker.ifttt.com/trigger/iss_overhead/json/with/key/{ifttt_key}")


def run_each_5min():
    if is_iss_overhead() and is_night():
        send_mail()
        send_telegram_msg_via_ifttt()

    time.sleep(300)  # Run Each 5 Minute
    run_each_5min()


run_each_5min()
