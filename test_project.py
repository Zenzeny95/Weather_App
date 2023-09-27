import project


def test_date_validation_valid():
    assert project.date_validation("2023-08-31") == True

def test_date_validation_invalid():
    assert project.date_validation("2023/08/31") == False
    assert project.date_validation("2023-08/31") == False
    assert project.date_validation("2023/08-31") == False
    assert project.date_validation("2023.08.31") == False

def test_time_validation_valid():
    assert project.time_validation("18") == True

def test_time_validation_invalid():
    assert project.time_validation("25") == False
    assert project.time_validation("-1") == False

def test_weather_code_valid():
    assert project.weather_code(0) == "Clear sky"
    assert project.weather_code(61) == "Rain: Slight intensity"

def test_wind_direction_valid():
    assert project.wind_direction(0) == "North"
    assert project.wind_direction(340) == "North"
    assert project.wind_direction(120) == "Southeast"
    assert project.wind_direction(180.1) == "South"

def test_location_validation_valid_place():
    assert project.location_validation("Los Angeles, USA") == "Place"
    assert project.location_validation("new york, united states") == "Place"

def test_location_validation_invalid_place():
    assert project.location_validation("") == "Invalid"
    assert project.location_validation("City") == "Invalid"
    assert project.location_validation("Los Angeles USA") == "Invalid"

def test_location_validation_valid_ip():
    assert project.location_validation("192.168.1.1") == "Ip"

def test_location_validation_invalid_ip():
    assert project.location_validation("254.168.256.1") == "Invalid"
    assert project.location_validation("256.168.1.1") == "Invalid"
    assert project.location_validation("192.168.1") == "Invalid"
