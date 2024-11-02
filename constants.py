# Weather API response keys
WEATHER_API_LOCATION_NAME = 'location.name'
WEATHER_API_LOCATION_REGION = 'location.region'
WEATHER_API_LOCATION_COUNTRY = 'location.country'
WEATHER_API_FORECAST_DATE = 'forecast.forecastday[0].date'
WEATHER_API_AVGTEMP_C = 'forecast.forecastday[0].day.avgtemp_c'
WEATHER_API_CONDITION = 'forecast.forecastday[0].day.condition.text'
WEATHER_API_MAXTEMP_C = 'forecast.forecastday[0].day.maxtemp_c'
WEATHER_API_MINTEMP_C = 'forecast.forecastday[0].day.mintemp_c'
WEATHER_API_MAXWIND_KPH = 'forecast.forecastday[0].day.maxwind_kph'
WEATHER_API_AVGHUMIDITY = 'forecast.forecastday[0].day.avghumidity'

# Gemini API response keys
GEMINI_API_CANDIDATES = 'candidates'

# Error messages
ERROR_LOCATION_REQUIRED = 'Location parameter is required.'
ERROR_DATE_REQUIRED = 'Date parameter is required.'
ERROR_INVALID_DATE_FORMAT = 'Invalid date format. Use "YYYY-MM-DD".'

# Default values
DEFAULT_STYLE = 'facts'
DEFAULT_LANGUAGE = 'en'
