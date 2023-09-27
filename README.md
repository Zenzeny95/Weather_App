# Weather app
#### Description:

Welcome to the Weather App! This application allows you to retrieve weather forecasts for a specific location and date. You can get detailed weather information, including temperature, humidity, wind speed, and more.

## How to Use the Weather App

1. **Date Selection**: You can choose a specific date in the format YYYY-MM-DD or press Enter to get the weather forecast for today.

2. **Time Selection**: Optionally, you can specify a particular hour of interest or press Enter to receive weather data for the entire day.

3. **Location Input**: Enter the location in one of the following formats:
   - City, Country (e.g., "New York, United States")
   - IP address (IPv4 or IPv6)

The app will then fetch and display weather information for your chosen date, time, and location.

## Features

- **Weather Details**: The Weather App provides you with various weather details, including temperature, apparent temperature, relative humidity, wind speed, wind gusts, wind direction, precipitation probability, weather description, and visibility.

- **Location Lookup**: For city and country input, the app can perform a location lookup in the provided database which has more than 44000 locations. It will provide the latitude and longitude coordinates for the selected location.

- **IP Location**: For IP address input, the app uses an external IP geolocation service to determine the location and fetch weather data.

- **Weather Codes**: The app translates weather codes into human-readable descriptions, making it easy to understand the weather conditions.

## Usage Notes

- Ensure you have an internet connection to fetch weather data.

- Make sure to use your own API keys (IP_API_HOST uses 'https://api.ipbase.com' and METEO_API_HOST uses "https://api.open-meteo.com")

- If you encounter any issues or incorrect data, please try again later as weather data availability may vary.

This Weather App is a handy tool to help you plan your day and stay informed about the weather conditions in your area or any other location of interest.

Enjoy using the Weather App!