import requests
import json
import csv
import regex as re
import datetime
from key import IP_API_KEY, IP_API_HOST, METEO_API_HOST


def main():
    print()
    print("Welcome to weather app!\nForcast available for the following 7 days!\n"
          "Please enter information for desired location.\n")
    try:
        while True:
            date = input("Enter date (YYYY-MM-DD format) or press Enter for today's date: ")
            if not date:
                break
            elif date_validation(date) is True:
                break
            else:
                print("Wrong date format")
                continue

        while True:
            time = input("Enter hour of interest or press Enter for whole day: ")
            if not time:
                break
            elif time_validation(time) is True:
                break
            elif time_validation(time) == 'Bad Date':
                print('Possible data only for next 7 days')
            else:
                print("Wrong time format")
                continue

        while True:
            place = input("City, Country or IP address: ")
            if not place:
                print("Invalid location or IP address")
                continue
            elif location_validation(place) == "Place":
                try:
                    city, country = place.split(",")
                    long, latt = location_by_place(city.title(), country.title())
                    print()
                except ValueError:
                    print("Unfortunately, the location is not in our database")
                    return
                if not date and not time:
                    meteoapi(long, latt)
                elif not date:
                    meteoapi(long, latt, hour=time.zfill(2))
                elif not time:
                    meteoapi(long, latt, day=date)
                else:
                    meteoapi(long, latt, day=date, hour=time.zfill(2))
                break
            elif location_validation(place) == "Ip":
                long, latt = location_by_ip(place)
                print()
                if not date and not time:
                    meteoapi(long, latt)
                elif not date:
                    meteoapi(long, latt, hour=time.zfill(2))
                elif not time:
                    meteoapi(long, latt, day=date)
                else:
                    meteoapi(long, latt, day=date, hour=time.zfill(2))
                break
            else:
                print("Invalid location or IP address")
                continue
    except TypeError:
        print("Couldn't retrieve information for this data")
        return


def location_validation(location):
    pattern_place = r"^[\p{L}\s.'-]{1,50}, ?[\p{L}\s.'-]{1,50}$"
    pattern_ip = r"^(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                 r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|" \
                 r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4})$"
    match_place = re.match(pattern_place, location)
    match_ip = re.match(pattern_ip, location)
    if match_place:
        return 'Place'
    elif match_ip:
        return 'Ip'
    else:
        return 'Invalid'


def date_validation(d):
    pattern_date = r"^\d{4}-\d{2}-\d{2}$"
    match_date = re.match(pattern_date, d)
    if not match_date:
        return False
    try:
        input_date = datetime.datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return False
    today = datetime.datetime.today()
    next_week = today + datetime.timedelta(days=7)
    if today.date() <= input_date <= next_week.date():
        return True
    return 'Bad Date'


def time_validation(t):
    pattern_time = r"^(?:[0-9]|1[0-9]|2[0-3])$"
    match_time = re.match(pattern_time, t)
    if match_time:
        return True
    return False


def date_time():
    now = datetime.datetime.now()
    date = f"{now.year:04}-{now.month:02}-{now.day:02}"
    hour = f"{now.hour}:00"
    return date, hour


def wind_direction(degrees):
    directions = ["Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
    degree_ranges = [(22.5, 67.5), (67.5, 112.5), (112.5, 157.5), (157.5, 202.5), (202.5, 247.5), (247.5, 292.5),
                     (292.5, 337.5)]
    for i, (start, end) in enumerate(degree_ranges):
        if start < degrees <= end:
            return directions[i]
    return "North"


def weather_code(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog and depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight intensity",
        81: "Rain showers: Moderate intensity",
        82: "Rain showers: Violent intensity",
        85: "Snow showers: Slight intensity",
        86: "Snow showers: Heavy intensity",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes[code]


def location_by_place(city, country):
    with open('worldcities.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if city.title().strip() == row[0].strip() and (country.title().strip() == row[4] or
                                                           country.upper().strip() == row[5] or
                                                           country.upper().strip() == row[6]):
                print()
                print(f"Location - {row[0]}, {row[4]}")
                return row[3], row[2]
        return f"Location is not found"


def location_by_ip(ip):
    try:
        payload = {"apikey": IP_API_KEY, "language": "en", "ip": ip}
        endpoint = '/v2/info'
        r = requests.get(IP_API_HOST + endpoint, params=payload)
        res = json.loads(r.text)['data']['location']
        print()
        print(f"Location - {res['city']['name']}, {res['country']['name']}")
        return res['longitude'], res['latitude']
    except (KeyError, ValueError):
        print("Cannot locate this IP address")
    except requests.exceptions.RequestException:
        print("An error occurred while making the API request")


def meteoapi(long, latt, day=None, hour=None):
    endpoint = "/v1/forecast"
    payload = {"latitude": latt, "longitude": long, "timezone": "auto",
               "hourly": "temperature_2m,relativehumidity_2m,apparent_temperature,windspeed_10m,"
                         "winddirection_10m,windgusts_10m,precipitation_probability,weathercode,visibility"}
    r = requests.get(METEO_API_HOST + endpoint, params=payload)
    try:
        res = json.loads(r.text)
        if day is None and hour is None:
            for i in range(24):
                temperatura = res['hourly']['temperature_2m'][i]
                dregnumas = res['hourly']['relativehumidity_2m'][i]
                jutimine = res['hourly']['apparent_temperature'][i]
                vejo_greitis = res['hourly']['windspeed_10m'][i]
                vejo_gusiai = res['hourly']['windgusts_10m'][i]
                kryptis = res['hourly']['winddirection_10m'][i]
                tikimybe = res['hourly']['precipitation_probability'][i]
                kodas = res['hourly']['weathercode'][i]
                matomumas = res['hourly']['visibility'][i]
                print(f"Date: {date_time()[0]}.\nTime: {str(i).zfill(2)}:00 h.")
                print(
                    f"Temperature - {temperatura}°C\nFeelable temperature - {jutimine}°C\n"
                    f"Relative humidity - {dregnumas}%\nWind speed - {vejo_greitis}km/h")
                print(
                    f"Wind gusts - {vejo_gusiai}km/h\nWind direction - {wind_direction(kryptis)}\n"
                    f"Rain probability - {tikimybe}%")
                print(f"Weather description - {weather_code(kodas)}\nVisibility - {matomumas / 1000}km")
                print()

        elif day is None and hour is not None:
            index = res['hourly']['time'].index(f"{date_time()[0]}T{hour}:00")
            temperatura = res['hourly']['temperature_2m'][index]
            dregnumas = res['hourly']['relativehumidity_2m'][index]
            jutimine = res['hourly']['apparent_temperature'][index]
            vejo_greitis = res['hourly']['windspeed_10m'][index]
            vejo_gusiai = res['hourly']['windgusts_10m'][index]
            kryptis = res['hourly']['winddirection_10m'][index]
            tikimybe = res['hourly']['precipitation_probability'][index]
            kodas = res['hourly']['weathercode'][index]
            matomumas = res['hourly']['visibility'][index]
            print(f"Date: {date_time()[0]}.\nTime: {hour.zfill(2)}:00 h.")
            print(
                f"Temperature - {temperatura}°C\nFeelable temperature - {jutimine}°C\n"
                f"Relative humidity - {dregnumas}%\nWind speed - {vejo_greitis}km/h")
            print(
                f"Wind gusts - {vejo_gusiai}km/h\nWind direction - {wind_direction(kryptis)}\n"
                f"Rain probability - {tikimybe}%")
            print(f"Weather description - {weather_code(kodas)}\nVisibility - {matomumas / 1000}km")
            print()

        elif day is not None and hour is None:
            for i in range(24):
                index = res['hourly']['time'].index(f"{day}T{str(i).zfill(2)}:00")
                temperatura = res['hourly']['temperature_2m'][index]
                dregnumas = res['hourly']['relativehumidity_2m'][index]
                jutimine = res['hourly']['apparent_temperature'][index]
                vejo_greitis = res['hourly']['windspeed_10m'][index]
                vejo_gusiai = res['hourly']['windgusts_10m'][index]
                kryptis = res['hourly']['winddirection_10m'][index]
                tikimybe = res['hourly']['precipitation_probability'][index]
                kodas = res['hourly']['weathercode'][index]
                matomumas = res['hourly']['visibility'][index]
                print(f"Date: {day}.\nTime: {str(i).zfill(2)}:00 h.")
                print(
                    f"Temperature - {temperatura}°C\nFeelable temperature - {jutimine}°C\n"
                    f"Relative humidity - {dregnumas}%\nWind speed - {vejo_greitis}km/h")
                print(
                    f"Wind gusts - {vejo_gusiai}km/h\nWind direction - {wind_direction(kryptis)}\n"
                    f"Rain probability - {tikimybe}%")
                print(f"Weather description - {weather_code(kodas)}\nVisibility - {matomumas / 1000}km")
                print()

        else:
            index = res['hourly']['time'].index(f"{day}T{hour}:00")
            temperatura = res['hourly']['temperature_2m'][index]
            dregnumas = res['hourly']['relativehumidity_2m'][index]
            jutimine = res['hourly']['apparent_temperature'][index]
            vejo_greitis = res['hourly']['windspeed_10m'][index]
            vejo_gusiai = res['hourly']['windgusts_10m'][index]
            kryptis = res['hourly']['winddirection_10m'][index]
            tikimybe = res['hourly']['precipitation_probability'][index]
            kodas = res['hourly']['weathercode'][index]
            matomumas = res['hourly']['visibility'][index]
            print(f"Date: {day}.\nTime: {hour.zfill(2)}:00 h.")
            print(
                f"Temperature - {temperatura}°C\nFeelable temperature - {jutimine}°C\n"
                f"Relative humidity - {dregnumas}%\nWind speed - {vejo_greitis}km/h")
            print(
                f"Wind gusts - {vejo_gusiai}km/h\nWind direction - {wind_direction(kryptis)}\n"
                f"Rain probability - {tikimybe}%")
            print(f"Weather description - {weather_code(kodas)}\nVisibility - {matomumas / 1000}km")
            print()

    except json.JSONDecodeError:
        print("An error occurred while decoding the weather data. Please try again later.")
    except KeyError:
        print("The requested weather data is not available. Please check your parameters.")
    except ValueError:
        print("An error occurred while processing the weather data. Please try again later.")
    except IndexError:
        print("An error occurred while accessing the weather data. Please try again later.")
    except requests.exceptions.RequestException:
        print("An error occurred while making the API request")


if __name__ == "__main__":
    main()
