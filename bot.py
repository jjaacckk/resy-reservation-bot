from typing import List, Generator
from time import sleep
from random import random
from datetime import datetime, date, timedelta
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from os import getenv
import notify
import config


TIMEZONE = timezone(config.TIMEZONE)

HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Accept-Language': 'en-US, en;q=0.5'
})

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"

BASE_URL = "https://resy.com/cities/"

load_dotenv()
DISCORD_WEBHOOK_URL = getenv("DISCORD_WEBHOOK_URL")


class PrintColors:
    reset = '\033[0m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    pink = '\033[95m'
    cyan = '\033[96m'
    underline = '\33[04m'


def send_message(title: str, content: str, color: str = notify.Colors.blue) -> None:
    if config.VERBOSE:
        print(f"{time_now(True)}: sending: '",
              content.replace('\n', ' '), "'", sep="")
    nd = notify.discord_embed(DISCORD_WEBHOOK_URL, title, content, color)
    if config.VERBOSE:
        print(f"{time_now(True)}: discord notify response: {nd}")


def check_time(t: datetime) -> bool:
    current_time = datetime.now(tz=TIMEZONE)
    if current_time >= t:
        return True
    return False


def time_now(pretty: bool = False) -> str:
    if pretty:
        return f'{PrintColors.pink}[{datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S:%f UTC%z")}]{PrintColors.reset}'
    return f'[{datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S:%f UTC%z")}]'


def date_range(start_date: date, end_date: date, dates_to_skip: List[date] = []) -> Generator[date, None, None]:
    for n in range(int((end_date - start_date).days + 1)):
        if start_date + timedelta(days=n) not in dates_to_skip:
            yield start_date + timedelta(days=n)


def start_browser() -> WebDriver:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", USER_AGENT)
    profile.set_preference("browser.privatebrowsing.autostart", True)
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(
        executable_path="./geckodriver", options=options, firefox_profile=profile)
    return browser


def check_resy(browser: WebDriver, restaurant_url_name: str, restaurant_url_city: str, start_date: date, end_date: date = None, party_size: int = 2, dates_to_skip: List[date] = []) -> set:
    full_availability = set()
    availability = list()

    url = BASE_URL + \
        f"{restaurant_url_city}/{restaurant_url_name}?seats={party_size}"

    if config.VERBOSE:
        print(f"{time_now(True)}: checking {url}....")

    xpath = '//*[@id="page-content"]/div[2]/div/article/section[1]/resy-inline-booking/div/div/resy-date-select/div/div[2]/resy-calendar[1]/div/div/div[2]/div[1]/button'

    browser.get(url)
    WebDriverWait(driver=browser, timeout=3).until(
        expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    for m in range(2):
        for w in range(5):
            for d in range(7):
                element = browser.find_element_by_xpath(
                    f'//*[@id="page-content"]/div[2]/div/article/section[1]/resy-inline-booking/div/div/resy-date-select/div/div[2]/resy-calendar[{m+1}]/div/div/div[{w+2}]/div[{d+1}]/button')
                class_list = element.get_attribute("class").split(' ')
                if 'outside-month' not in class_list and 'available' in class_list:
                    date_now = datetime.now(TIMEZONE)
                    day = int(element.get_attribute('innerText'))
                    month = (int(date_now.strftime('%m'))+m)
                    year = int(date_now.strftime('%Y'))
                    res_date = date(year, month, day)
                    # print(res_date.strftime('%Y-%m-%d'), class_list, sep='\t')
                    full_availability.add(res_date)

    dr = None
    if end_date == None:
        dr = date_range(start_date, start_date, dates_to_skip)
    else:
        dr = date_range(start_date, end_date, dates_to_skip)

    for d in dr:
        if d in full_availability:
            availability.append(
                BASE_URL + f"{restaurant_url_name}?date={d.strftime('%Y-%m-%d')}&seats={party_size}")

    return availability


def run(restaurant_name: str, restaurant_url_name: str, restaurant_url_city: str, start_date: date, end_date: date = None, party_size: int = 2, dates_to_skip: List[date] = [], refresh_interval: int = 60, randomize_refresh_interval: bool = True) -> None:
    try:
        print((f"{time_now(True)}: running resy bot...."))
        send_message(restaurant_name, f"{time_now()}\nrunning resy bot....")

        if config.VERBOSE:
            print(f"{time_now(True)}: starting browser....")
        browser = start_browser()

        count = 1

        while True:
            if config.VERBOSE:
                print(
                    f"\n{time_now(True)}:{PrintColors.blue} on loop {count}{PrintColors.reset}")

            resy_update = check_resy(browser=browser, restaurant_url_name=restaurant_url_name, restaurant_url_city=restaurant_url_city,
                                     start_date=start_date, end_date=end_date, party_size=party_size, dates_to_skip=dates_to_skip)

            if len(resy_update) > 0:
                pretty_resy_update = '\n\t- ' + '\n\t- '.join(resy_update)
                print(f"{time_now(True)}: {PrintColors.green}{restaurant_name} has reservations in your time-frame: {pretty_resy_update}{PrintColors.reset}")
                send_message(
                    restaurant_name, f"{time_now()}\nnew reservations in your time-frame:\n{pretty_resy_update}", notify.Colors.success)
                if config.STOP_AFTER_FIRST_SUCCESS:
                    raise KeyboardInterrupt
            else:
                if config.VERBOSE:
                    print(f"{time_now(True)}: no update.")

            s = refresh_interval
            if randomize_refresh_interval == True:
                s += int((10 * random()))
            if config.VERBOSE:
                print(f"{time_now(True)}: sleeping for {s} seconds (until {(datetime.now(tz=TIMEZONE) + timedelta(seconds=s)).strftime('%H:%M:%S')})....")
            sleep(s)

            count += 1

    except Exception as e:
        print(f"{time_now(True)}: ERROR: {e}")
        send_message(
            restaurant_name, f"{time_now()}\nERROR:\nRESY BOT HAS STOPPED ON COUNT {count}!\nMESSAGE: {e}", notify.Colors.failure)

    except KeyboardInterrupt:
        print(f"\r  \r\n{time_now(True)}: goodbye.")
        send_message(
            restaurant_name, f"{time_now()}\nresy bot has been stopped on count {count}.")

    finally:
        browser.quit()


def load_params() -> tuple:
    params = (
        config.RESTAURANT_NAME,
        config.RESTAURANT_URL_NAME,
        config.RESTAURANT_URL_CITY,
        date(*config.RESERVATION_WINDOW_SEARCH_START_DATE),
        date(*config.RESERVATION_WINDOW_SEARCH_END_DATE),
        config.RESERVATION_PARTY_SIZE,
        [date(*d) for d in config.RESERVATION_WINDOW_SEARCH_DATES_TO_SKIP],
        config.REFRESH_INTERVAL,
        config.RANDOMIZE_REFRESH_INTERVAL
        )
    return params


run(*load_params())
