import requests

CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=aec14afce2de44d0b37d56d171675ec8"

def get_rates(frm, to):
    all_currency = requests.get(CURRENCY_URL)
    parsed = all_currency.json()['rates']
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate

get_rates('GBP','USD')