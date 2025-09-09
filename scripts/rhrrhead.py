# cwr.py
# uvindex, temp, humid

import csv
import requests
import json
import streamlit as st
from scripts import utility
class Current_Weather_Report():
    raw_data = None
    last_update = None
    available_weather_station = None
    district = None
    
    # Switch to list when done
    weather_station_temperature = "Tuen Mun"
    weather_station_rainfall = None

    def __init__(self) -> None:
        self.raw_data = None
        self.last_update = None
        self.available_weather_station = []
        self.district = None
        self.weather_station_temperature = "Tuen Mun"
        self.weather_station_rainfall = None
        self.fetch_data()

    def update_user_data(self) -> None:
        self.district = st.session_state['selected_district']
        self.weather_station_rainfall = st.session_state['selected_weather_station']

    def fetch_data(self) -> bool:
        try:
            response = requests.get('https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en', timeout = 10)
            response.raise_for_status()
            if not response:
                raise Exception("Received empty data from API")
            self.raw_data = response.json()
            if not self.raw_data['updateTime']:
                raise Exception("No updateTime. Possible update on Hong Kong Observatory")
            self.last_update = self.raw_data['updateTime'][11:19]
            self.available_weather_station = [data['place'] for data in self.raw_data['temperature']['data']]
            return True

        except Exception as e:
            raise Exception(f"Error getting Current Weather Report data: {str(e)}")

    def fetch_lighting(self):
        raw_data_lighting = self.raw_data.get('lightning')
        if (not raw_data_lighting) or raw_data_lighting == "":
            return "Lightning is not happening in Hong Kong right now."

        full_message = "Lightning has began at these location,<br>" + \
            f"starting from {utility.twentyfourh_to_12h(raw_data_lighting['startTime'][11:19])} " + \
            f"to {utility.twentyfourh_to_12h(raw_data_lighting['endTime'][11:19])}"

        full_message += "<ul>"
        for temp in raw_data_lighting['data']:
            if temp["occur"] == "true": #redundant loc, can be removed 
                full_message += (f"<li>{temp['place']}</li>")

        full_message += "</ul>"
        return full_message
    
    def fetch_uv(self) -> str:
        try:
            raw_data_uvindex = self.raw_data.get('uvindex')

            if (not raw_data_uvindex) or raw_data_uvindex == "":
                return "UV Index is unavailable at night."

            raw_data_uvindex = raw_data_uvindex['data'][0] #Only 1 place available for presenting uvindex data

            raw_data_uvindex['recordDesc'] = self.raw_data['uvindex']['recordDesc']
            raw_data_uvindex['updateTime'] = self.raw_data['updateTime'][11:19]

        except Exception as e:
            raise Exception(f"Error getting uvindex: {str(e)}")

        full_message = f"{raw_data_uvindex['recordDesc']} of {utility.twentyfourh_to_12h(raw_data_uvindex['updateTime'])}, " + \
            f"the current uvindex recorded at {raw_data_uvindex['place']} is {raw_data_uvindex['value']}, " + \
            f"classified as {raw_data_uvindex['desc']}"


        extra_message = raw_data_uvindex.get("message")
        if extra_message != None and extra_message != "":
            full_message += (f"\nHere is a special announcement from HKO regarding uv index: \n" + \
                    extra_message)

        return full_message

    def fetch_temperature(self) -> str:
        try:
            raw_data_temperature = self.raw_data.get('temperature')
            if (not raw_data_temperature) or raw_data_temperature == "":
                raise Exception(f"Received Null value in temperature. \nReport this error to the author.")
            result = {
                'place': self.weather_station_temperature,
                'recordTime': raw_data_temperature['recordTime'][11:19]
            }
            for x in raw_data_temperature['data']:
                if x['place'] == result['place']:
                    result['value'] = str(x['value']) + " "+ x['unit']
                    return (f"At {utility.twentyfourh_to_12h(result['recordTime'])}, in {result['place']}, " + \
                        f"the temperature is {result['value']}\n")
            raise Exception("Data not available at requested district")
        except Exception as e:
            raise Exception(f"Error getting uvindex: {str(e)}")

    def fetch_humidity(self) -> str:
        raw_data_humidity = self.raw_data.get("humidity")
        if raw_data_humidity is None:
            return "Humidity data unavailable"
        temp = raw_data_humidity.get('data')
        if temp is None or temp == []:
            return ("Humidity data unavailable. Possible full mainatance of HKO")
        temp = temp[0]
        result = {
            'place': temp['place'],
            'value': str(temp['value']) + " " + temp['unit'],
            'recordTime': raw_data_humidity['recordTime'][11:19]
        }

        full_message = (f"Humidity data recorded at {utility.twentyfourh_to_12h(result['recordTime'])}: <br>" + \
            f"<ul><li>At {result['place']}, the humudity recorded is {result['value']}.")

        if (temp['unit'] == 'percent'):
            full_message += ("</li><li> Humidity Level is ")
            if (temp['value'] < 25):
                full_message += ('Low')
            elif (temp['value'] < 75):
                full_message += ('Moderate')
            else:
                full_message += ('High')

        full_message += "</li></ul>"
        return full_message

    def fetch_and_process_warning(self) -> str:
        result = self.raw_data['warningMessage']

        if result == "":
            return "Received error in warning message."

        full_message = ("\nHere "+
            f"{'is 1' if len(result) == 1 else f'are {len(result)}'} warning message"+
            f"{'s' if len(result)!= 1 else ''} from Hong Kong Observatory:<br>")
        full_message += utility.lazy_list_message(result)
        return full_message

# Above fixed
# Below Temp fixed
    def fetch_and_process_ultil(self) -> str:
        # Special Weather Tips
        specialWxTips = self.raw_data.get('specialWxTips')
        if specialWxTips != None:
            full_message = "<br>Here are some special Weather Tips from HKO: " + utility.lazy_list_message(specialWxTips)
        else:
            full_message = ""
        # Tropical Cyclone Position
        tcmessage = list(self.raw_data.get('tcmessage'))
        number_of_typhoon = len(tcmessage)
        if (tcmessage != ""):
            full_message += ("<br>Here are some information relating to Tropical Cyclone from HKO: <br>" +
                f"Currently there {'is 1' if number_of_typhoon == 1 else f'are {number_of_typhoon}'} tropical cyclone" +
                f"{'s' if number_of_typhoon != 1 else ''}"+
                "near Hong Kong")

        for typhoon in tcmessage:
            typhoon = typhoon.replace("\n", "<br><ul><li>")
            full_message += (f"<li>{typhoon}</li>")

        full_message += "</li></ul>"

        # Others are always unavailable without any reason why
        return full_message