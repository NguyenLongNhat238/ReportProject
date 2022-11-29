
import requests
from constant.config import SEARCH_CITY_DISTRICT, UNIT_PRICE
from rest_framework import exceptions

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

#### convert currency: triệu đồng -> tỷ đồng
#  UNIT_PRICE 1000
def currency_converter_helper(money):
    return round(money/UNIT_PRICE,2)



def get_list_district_of_city(city) -> dict:
    params = {}
    params.update({'city': city})
    data = requests.get(f'{SEARCH_CITY_DISTRICT}', params=params)
    data = data.json()
    return data['results']


