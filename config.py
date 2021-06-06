# Fill out the information below and then run 'bot.py' to use the resy bot
# Make sure to create a .env file with 'DISCORD_WEBHOOK_URL' before running

# * MAKE SURE VALUE MATCHES VALUE IN URL

# Example Resy URL:
# https://resy.com/cities/{RESTAURANT_URL_CITY}/{RESTAURANT_URL_NAME}


TIMEZONE = "America/New_York"

VERBOSE = True

STOP_AFTER_FIRST_SUCCESS = False


# Restaurant Name (no default)
RESTAURANT_NAME = ""

# Restaurant URL Name (no default)*
# Look at example URL above
RESTAURANT_URL_NAME = ""

# Restaurant URL City (no default)*
# Look at example URL above
RESTAURANT_URL_CITY = ""

# Reservation Window Search Start Date (no default)
# The date in the reservation window where you want the search to begin (inclusive)
# FORMAT: (YEAR, MONTH, DAY)
RESERVATION_WINDOW_SEARCH_START_DATE = ()

# Reservation Window Search Start Date (default: None)
# The date in the reservation window where you want the search to end (inclusive)
# If no date is included, the bot will only search for reservations on RESERVATION_WINDOW_SEARCH_START_DATE
# FORMAT: (YEAR: int, MONTH: int, DAY: int)
RESERVATION_WINDOW_SEARCH_END_DATE = None

# Reservation Window Search Start Date (default: [])
# Dates in the reservation window that you do not want the search (e.g. you're busy that day, so you don't want to book a reservation)
# FORMAT: [(YEAR: int, MONTH: int, DAY: int), (YEAR: int, MONTH: int, DAY: int)]
RESERVATION_WINDOW_SEARCH_DATES_TO_SKIP = []

# RESERVATION PARTY SIZE (default: 2)
# Number of people in the reservation
RESERVATION_PARTY_SIZE = 2

# REFRESH INTERVAL (default: 60)
# Amount of time (in seconds) the bot should wait before checking resy again





####~~~~EXAMPLE SETUP~~~~####
# RESTAURANT_NAME = "Jeju Noodle Bar"
# RESTAURANT_URL_NAME = "jeju-noodle-bar"
# RESTAURANT_URL_CITY = "ny"
# RESERVATION_WINDOW_SEARCH_START_DATE = (2021, 6, 10)
# RESERVATION_WINDOW_SEARCH_END_DATE = (2021, 6, 20)
# RESERVATION_WINDOW_SEARCH_DATES_TO_SKIP = [(2021, 6, 17), (2021, 6, 18), (2021, 6, 19)]
# RESERVATION_PARTY_SIZE = 4
# REFRESH_INTERVAL = 60
# RANDOMIZE_REFRESH_INTERVAL = True
