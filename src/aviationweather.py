# Module:
# aviationweather.py
#
# Description:
# An aviation weather bot module based on NOAA data (https://aviationweather.gov/)
# using the third-party API AVWX (https://avwx.rest/) for acquisition.
#
# Author:
# Michael V. Coppola <prenetic@gmail.com>, 2019

from sopel import module
import requests

protocol = "https"
endpoint = "avwx.rest"
timeout = 10  # Denoted in seconds


def request(urn, key):
    response = requests.get(
        protocol + "://" + endpoint + "/" + urn,
        timeout=timeout,
    )
    json = response.json()

    if response.status_code == 200:
        return json.get(key)
    elif response.status_code == 400:
        if "help" in json:
            return (
                "Status code 400: "
                + json.get("error")
                + ". "
                + json.get("help")
                + "."
            )
        else:
            return (
                "Status code 400: "
                + json.get("error")
                + "."
            )
    else:
        return "Status code " + response.status_code


@module.commands("metar")
def metar(bot, trigger):
    urn = "api/metar/" + trigger.group(2)
    key = "raw"

    message = request(urn, key)
    bot.say(message)


@module.commands("taf")
def taf(bot, trigger):
    urn = "api/taf/" + trigger.group(2)
    key = "raw"

    message = request(urn, key)
    bot.say(message)
