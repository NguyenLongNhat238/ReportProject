# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RealEstate2021(models.Model):
    id_client = models.CharField(db_column='ID_CLIENT', max_length=255)  # Field name made lowercase.
    site = models.CharField(db_column='SITE', max_length=100)  # Field name made lowercase.
    ads_link = models.TextField(db_column='ADS_LINK')  # Field name made lowercase.
    for_sale = models.IntegerField(db_column='FOR_SALE', blank=True, null=True)  # Field name made lowercase.
    for_lease = models.IntegerField(db_column='FOR_LEASE', blank=True, null=True)  # Field name made lowercase.
    to_buy = models.IntegerField(db_column='TO_BUY', blank=True, null=True)  # Field name made lowercase.
    to_lease = models.IntegerField(db_column='TO_LEASE', blank=True, null=True)  # Field name made lowercase.
    land_type = models.CharField(db_column='LAND_TYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ads_date = models.DateField(db_column='ADS_DATE', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='PRICE', blank=True, null=True)  # Field name made lowercase.
    price_m2 = models.FloatField(db_column='PRICE_M2', blank=True, null=True)  # Field name made lowercase.
    surface = models.FloatField(db_column='SURFACE', blank=True, null=True)  # Field name made lowercase.
    used_surface = models.FloatField(db_column='USED_SURFACE', blank=True, null=True)  # Field name made lowercase.
    pro_width = models.FloatField(db_column='PRO_WIDTH', blank=True, null=True)  # Field name made lowercase.
    pro_length = models.FloatField(db_column='PRO_LENGTH', blank=True, null=True)  # Field name made lowercase.
    legal_status = models.CharField(db_column='LEGAL_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pro_current_status = models.CharField(db_column='PRO_CURRENT_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pro_direction = models.CharField(db_column='PRO_DIRECTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    frontage = models.FloatField(db_column='FRONTAGE', blank=True, null=True)  # Field name made lowercase.
    alley_access = models.FloatField(db_column='ALLEY_ACCESS', blank=True, null=True)  # Field name made lowercase.
    nb_lots = models.FloatField(db_column='NB_LOTS', blank=True, null=True)  # Field name made lowercase.
    pro_utilities = models.TextField(db_column='PRO_UTILITIES', blank=True, null=True)  # Field name made lowercase.
    nb_rooms = models.FloatField(db_column='NB_ROOMS', blank=True, null=True)  # Field name made lowercase.
    nb_floors = models.FloatField(db_column='NB_FLOORS', blank=True, null=True)  # Field name made lowercase.
    kitchen = models.FloatField(db_column='KITCHEN', blank=True, null=True)  # Field name made lowercase.
    bedroom = models.FloatField(db_column='BEDROOM', blank=True, null=True)  # Field name made lowercase.
    bathroom = models.FloatField(db_column='BATHROOM', blank=True, null=True)  # Field name made lowercase.
    garage = models.IntegerField(db_column='GARAGE', blank=True, null=True)  # Field name made lowercase.
    toilet = models.FloatField(db_column='TOILET', blank=True, null=True)  # Field name made lowercase.
    full_address = models.CharField(db_column='FULL_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    split_hs = models.TextField(db_column='SPLIT_HS', blank=True, null=True)  # Field name made lowercase.
    format_hs = models.TextField(db_column='FORMAT_HS', blank=True, null=True)  # Field name made lowercase.
    split_street = models.TextField(db_column='SPLIT_STREET', blank=True, null=True)  # Field name made lowercase.
    format_street = models.TextField(db_column='FORMAT_STREET', blank=True, null=True)  # Field name made lowercase.
    split_ward = models.CharField(db_column='SPLIT_WARD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    split_district = models.CharField(db_column='SPLIT_DISTRICT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    split_city = models.CharField(db_column='SPLIT_CITY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    street = models.TextField(db_column='STREET', blank=True, null=True)  # Field name made lowercase.
    ward = models.CharField(db_column='WARD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='DISTRICT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='LON', blank=True, null=True)  # Field name made lowercase.
    lat_os = models.FloatField(db_column='LAT_OS', blank=True, null=True)  # Field name made lowercase.
    lon_os = models.FloatField(db_column='LON_OS', blank=True, null=True)  # Field name made lowercase.
    photos = models.IntegerField(db_column='PHOTOS', blank=True, null=True)  # Field name made lowercase.
    ads_title = models.TextField(db_column='ADS_TITLE', blank=True, null=True)  # Field name made lowercase.
    brief = models.TextField(db_column='BRIEF', blank=True, null=True)  # Field name made lowercase.
    detailed_brief = models.TextField(db_column='DETAILED_BRIEF', blank=True, null=True)  # Field name made lowercase.
    pro_width_text = models.FloatField(db_column='PRO_WIDTH_TEXT', blank=True, null=True)  # Field name made lowercase.
    pro_length_text = models.FloatField(db_column='PRO_LENGTH_TEXT', blank=True, null=True)  # Field name made lowercase.
    alley_text = models.FloatField(db_column='ALLEY_TEXT', blank=True, null=True)  # Field name made lowercase.
    frontage_text = models.FloatField(db_column='FRONTAGE_TEXT', blank=True, null=True)  # Field name made lowercase.
    surface_text = models.FloatField(db_column='SURFACE_TEXT', blank=True, null=True)  # Field name made lowercase.
    price_text = models.FloatField(db_column='PRICE_TEXT', blank=True, null=True)  # Field name made lowercase.
    dealer_name = models.CharField(db_column='DEALER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    dealer_type = models.CharField(db_column='DEALER_TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dealer_address = models.CharField(db_column='DEALER_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealer_email = models.CharField(db_column='DEALER_EMAIL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dealer_tel = models.CharField(db_column='DEALER_TEL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dealer_joined_date = models.DateField(db_column='DEALER_JOINED_DATE', blank=True, null=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_name = models.CharField(db_column='AGENCY_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_address = models.CharField(db_column='AGENCY_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_city = models.CharField(db_column='AGENCY_CITY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_tel = models.CharField(db_column='AGENCY_TEL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    agency_website = models.CharField(db_column='AGENCY_WEBSITE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    check_convert = models.IntegerField(db_column='CHECK_CONVERT', blank=True, null=True)  # Field name made lowercase.
    pro_flag = models.IntegerField(db_column='PRO_FLAG', blank=True, null=True)  # Field name made lowercase.
    created_date = models.DateField(db_column='CREATED_DATE')  # Field name made lowercase.
    date_original = models.DateField(db_column='DATE_ORIGINAL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REAL_ESTATE_2021'



class RealEstate2022(models.Model):
    id_client = models.CharField(db_column='ID_CLIENT', max_length=255)  # Field name made lowercase.
    site = models.CharField(db_column='SITE', max_length=100)  # Field name made lowercase.
    ads_link = models.TextField(db_column='ADS_LINK')  # Field name made lowercase.
    for_sale = models.IntegerField(db_column='FOR_SALE', blank=True, null=True)  # Field name made lowercase.
    for_lease = models.IntegerField(db_column='FOR_LEASE', blank=True, null=True)  # Field name made lowercase.
    to_buy = models.IntegerField(db_column='TO_BUY', blank=True, null=True)  # Field name made lowercase.
    to_lease = models.IntegerField(db_column='TO_LEASE', blank=True, null=True)  # Field name made lowercase.
    land_type = models.CharField(db_column='LAND_TYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ads_date = models.DateField(db_column='ADS_DATE', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='PRICE', blank=True, null=True)  # Field name made lowercase.
    price_m2 = models.FloatField(db_column='PRICE_M2', blank=True, null=True)  # Field name made lowercase.
    surface = models.FloatField(db_column='SURFACE', blank=True, null=True)  # Field name made lowercase.
    used_surface = models.FloatField(db_column='USED_SURFACE', blank=True, null=True)  # Field name made lowercase.
    pro_width = models.FloatField(db_column='PRO_WIDTH', blank=True, null=True)  # Field name made lowercase.
    pro_length = models.FloatField(db_column='PRO_LENGTH', blank=True, null=True)  # Field name made lowercase.
    legal_status = models.CharField(db_column='LEGAL_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pro_current_status = models.CharField(db_column='PRO_CURRENT_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pro_direction = models.CharField(db_column='PRO_DIRECTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    frontage = models.FloatField(db_column='FRONTAGE', blank=True, null=True)  # Field name made lowercase.
    alley_access = models.FloatField(db_column='ALLEY_ACCESS', blank=True, null=True)  # Field name made lowercase.
    pro_utilities = models.TextField(db_column='PRO_UTILITIES', blank=True, null=True)  # Field name made lowercase.
    nb_rooms = models.FloatField(db_column='NB_ROOMS', blank=True, null=True)  # Field name made lowercase.
    nb_floors = models.FloatField(db_column='NB_FLOORS', blank=True, null=True)  # Field name made lowercase.
    full_address = models.CharField(db_column='FULL_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    format_hs = models.TextField(db_column='FORMAT_HS', blank=True, null=True)  # Field name made lowercase.
    format_street = models.TextField(db_column='FORMAT_STREET', blank=True, null=True)  # Field name made lowercase.
    split_ward = models.CharField(db_column='SPLIT_WARD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    split_district = models.CharField(db_column='SPLIT_DISTRICT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    split_city = models.CharField(db_column='SPLIT_CITY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='LON', blank=True, null=True)  # Field name made lowercase.
    ads_title = models.TextField(db_column='ADS_TITLE', blank=True, null=True)  # Field name made lowercase.
    detailed_brief = models.TextField(db_column='DETAILED_BRIEF', blank=True, null=True)  # Field name made lowercase.
    dealer_name = models.CharField(db_column='DEALER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    dealer_address = models.CharField(db_column='DEALER_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealer_email = models.CharField(db_column='DEALER_EMAIL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dealer_type = models.CharField(db_column='DEALER_TYPE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dealer_tel = models.CharField(db_column='DEALER_TEL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    project_name = models.CharField(db_column='PROJECT_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_name = models.CharField(db_column='AGENCY_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_address = models.CharField(db_column='AGENCY_ADDRESS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_city = models.CharField(db_column='AGENCY_CITY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agency_tel = models.CharField(db_column='AGENCY_TEL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    agency_website = models.CharField(db_column='AGENCY_WEBSITE', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REAL_ESTATE_2022'