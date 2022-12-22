
from datetime import datetime
import json
import numbers
import requests
from constant.config import SEARCH_CITY_DISTRICT_WARD, UNIT_PRICE, YEAR_OF_REQUEST, SEARCH_CITY_DISTRICT_WARD_LOCAL
from constant.res_handing import ErrorHandling
from rest_framework import exceptions


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# convert currency: triệu đồng -> tỷ đồng
#  UNIT_PRICE 1000


def currency_converter_helper(money):
    return round(money/UNIT_PRICE, 2)

def get_map_data(city):
    if city.startswith('Tỉnh '):
        city = city[5:]
    if city.startswith('Thành phố '):
        city = city[10:]
    with open('gadm36_VNM_2.json','r', encoding='UTF-8') as file:
        json_map = json.load(file)
    # list(filter(lambda x: x['NAME_1'] == city, json_map))
    in_put_json_map = json_map['features']
    out_put_json_map = [x for x in in_put_json_map if x['properties']['NAME_1'] == city]
    return out_put_json_map

def get_list_district_of_city(city) -> dict:
    try:
        params = {}
        params.update({'city': city})
        data = requests.get(f'{SEARCH_CITY_DISTRICT_WARD}', params=params)
        data = data.json()
        return data['results']
    except:
        raise exceptions.APIException(ErrorHandling(
            message='The system is maintenance', code='SERVER ERROR', type="SERVER ERROR", lang='en').to_representation())

def remove_type_of_district(district):
    if district.startswith('Huyện '):
        district = district[6:]
    if district.startswith('Thị xã '):
        district = district[7:]
    if district.startswith('Thành phố '):
        district = district[10:]
    if district.startswith('Quận '):
        district = district[5:]
    return district


def get_data_vs_map_district_of_city(city=None) -> dict:
    try:
        # if city is None:
        #     raise exceptions.ValidationError(ErrorHandling(
        #         message='city required', code='DATA ERROR', type="DATA ERROR", lang='en').to_representation())
        data_map = get_map_data(city)
        params = {}
        params.update({'city': city})
        data = requests.get(f'{SEARCH_CITY_DISTRICT_WARD}', params=params)
        data = data.json()
        for i in data['results']:
            name_map = remove_type_of_district(i['district'])
            i.update({
                'name_map': name_map
            })
            
        return data['results'], data_map
    except:
        raise exceptions.APIException(ErrorHandling(
            message='The system is maintenance', code='SERVER ERROR', type="SERVER ERROR", lang='en').to_representation())


def get_list_ward_of_district(city, district) -> dict:
    if city is None or district is None:
        raise exceptions.ValidationError(ErrorHandling(
            message='City and District params required', code='DATA ERROR', type="DATA ERROR", lang='en').to_representation())
    try:
        params = {}
        params.update({'city': city})
        params.update({'district': district})
        data = requests.get(
            f'{SEARCH_CITY_DISTRICT_WARD}', params=params)
        data = data.json()
        return data['results']
    except:
        raise exceptions.APIException(ErrorHandling(
            message='The system is maintenance', code='SERVER ERROR', type="SERVER ERROR", lang='en').to_representation())


def is_integer_num(n):
    if isinstance(5, numbers.Number):
        return True
    raise exceptions.ValidationError(ErrorHandling(message="Không phải số nguyên / field must be an integer",
                                                   code="DATA ERROR",
                                                   type="DATA ERROR",
                                                   lang='en').to_representation())


def get_year_params(year, quarter):
    year = YEAR_OF_REQUEST
    st1_quarter = datetime.strptime(
        f'{year}-1-1', '%Y-%m-%d').date()
    st2_quarter = datetime.strptime(
        f'{year}-4-1', '%Y-%m-%d').date()
    st3_quarter = datetime.strptime(
        f'{year}-7-1', '%Y-%m-%d').date()
    st4_quarter = datetime.strptime(
        f'{year}-10-1', '%Y-%m-%d').date()
    end_quarter = datetime.strptime(
        f'{year}-1-1', '%Y-%m-%d').date()
    from_quarter = st1_quarter
    to_quarter = st2_quarter
    if quarter == '1':
        from_quarter = st1_quarter
        to_quarter = st2_quarter
    elif quarter == '2':
        from_quarter = st2_quarter
        to_quarter = st3_quarter
    elif quarter == '3':
        from_quarter = st3_quarter
        to_quarter = st4_quarter
    elif quarter == '4':
        from_quarter = st4_quarter
        to_quarter = end_quarter
    return from_quarter, to_quarter


def get_month_params_for_query(from_month, to_month):

    if from_month is None:
        raise exceptions.ValidationError(ErrorHandling(message="from_month must be exist",
                                                       code="DATA ERROR", type="DATA ERROR", lang='en').to_representation())
    is_integer_num(from_month)

    from_month = int(from_month)
    if from_month == 12:
        return from_month, from_month
    if from_month == 11:
        return from_month, 12
    if from_month <= 12 and from_month >= 1:
        if to_month:
            is_integer_num(to_month)
            to_month = int(to_month)
            if to_month > from_month and to_month <= 12 and to_month >= 1:
                return from_month, to_month
            raise exceptions.ValidationError(ErrorHandling(message="to_month must be more than from_month",
                                                           code="DATA ERROR", type="DATA ERROR", lang='en').to_representation())
        return from_month, from_month + 2
    raise exceptions.ValidationError(ErrorHandling(message="month must be integer 1 - 12",
                                                   code="DATA ERROR", type="DATA ERROR", lang='en').to_representation())


def is_integer(n):
    try:
        float(n)
    except:
        return False
    else:
        return float(n).is_integer()


def get_year_query_drf(year):
    if year is None:
        return 2022
    if is_integer(year) is True:
        year = int(year)
        if year == 2021:
            return year
        if year == 2022:
            return year
        else:
            return 2022
    return 2022


def valid_year_uda(year):
    if year and is_integer(year) is True:
        year = int(year)
        if year >= 1900 and year <= 2022:
            return year
