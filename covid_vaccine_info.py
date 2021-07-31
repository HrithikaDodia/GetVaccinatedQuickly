import requests
from datetime import datetime
from collections import OrderedDict
from fake_useragent import UserAgent
import json


def get_api_header():
    ua = UserAgent()
    header = {'User-Agent': ua.random}
    return header

def prepare_info(vaccine_response, area, min_age_limit):
    vaccine_response = vaccine_response.json()
    result = []
    centers = vaccine_response['centers']
    for i in range(len(centers)):
        info = centers[i]
        for session in info['sessions']:
            if session['min_age_limit'] == int(min_age_limit) and session['available_capacity_dose1'] > 0 and area in info['address'].lower():
                vaccine_fee = {}
                vaccine_info = {}
                if not info['fee_type'] == 'Free':
                    for vacc in info['vaccine_fees']:
                        vaccine_fee[vacc['vaccine']] = vacc['fee']
            
                vaccine_info['center_id'] = info['center_id']
                vaccine_info['name'] = info['name']
                # vaccine_info['address'] = info['address'] + ' ' + str(info['pincode'])
                vaccine_info['date'] = session['date']
                # vaccine_info['slots'] = session['slots']
                vaccine_info['min_age_limit'] = session['min_age_limit']
                vaccine_info['available_capacity_dose1'] = session['available_capacity_dose1']
                
                # print('Center ID | Name | Address: ', info['center_id'], ' | ', info['name'], ' | ', info['address'], ' | ', info['pincode'])
                # print('Date | Slots: ', session['date'], ' | ', session['slots'])
                # print('Age Limit: ', session['min_age_limit'])
                # print('Available Capacity Dose1: ', session['available_capacity_dose1'])
                # print('Available Capacity Dose2: ', session['available_capacity_dose2'])        
                
                vaccine_info['vaccine'] = {}
                if bool(vaccine_fee):
                    for vacc_fee in vaccine_fee:
                        vaccine_info['vaccine'][vacc_fee] = vaccine_fee[vacc_fee]
                else:
                    vaccine_info['vaccine'][session['vaccine']] = 'Free'
                

                if vaccine_info not in result:
                    result.append(vaccine_info)
                    
    print('Successfully created result dictionary')
    # print(len(result))
    return result


def get_vaccine_details(district, area, min_age_limit):
    date_today = datetime.now()
    date_today = f'{date_today.day}-{date_today.month}-{date_today.year}'

    header = get_api_header()
    vaccine_response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district}&date={date_today}', headers = header)
    
    result = prepare_info(vaccine_response, area, min_age_limit)
    return result
