District_reference_for_temperature = {
    'Tin Shui Wai': 'Lau Fau Shan',
    'Yuen Long': 'Yuen Long Park'
}
import requests
import json
from utility import twentyfourh_to_12h  # Assuming utility.py is in the same directory

class Current_Weather_Report():
  raw_data = None
  temperature = None
  last_update = None
  district = None

  def __init__(self, district: str) -> None:
    self.raw_data = None
    self.temperature = None
    self.last_update = None
    self.processed_data = None
    self.district = district

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
      return True

    except Exception as e:
      raise Exception(f"Error getting Current Weather Report data: {str(e)}")

  def fetch_lighting(self) -> list:
    messages = []
    raw_data_lighting = self.raw_data.get('lightning')

    if (not raw_data_lighting) or raw_data_lighting == "":
      messages.append("Lightning is not happening in Hong Kong right now.")
      return messages

    messages.append(f"Lightning has began at these location,\nstarting from {twentyfourh_to_12h(raw_data_lighting['startTime'][11:19])} to {twentyfourh_to_12h(raw_data_lighting['endTime'][11:19])}")

    for temp in raw_data_lighting['data']:
      if temp["occur"] == "true":
        messages.append(f"\t{temp['place']}")

    return messages

  def fetch_uv(self) -> list:
    messages = []
    try:
      raw_data_uvindex = self.raw_data.get('uvindex')

      if (not raw_data_uvindex) or raw_data_uvindex == "":
        messages.append("UV Index is unavailable at night.")
        return messages

      raw_data_uvindex = raw_data_uvindex['data'][0] #Only 1 place available for presenting uvindex data

      raw_data_uvindex['recordDesc'] = self.raw_data['uvindex']['recordDesc']
      raw_data_uvindex['updateTime'] = self.raw_data['updateTime'][11:19]

    except Exception as e:
      messages.append(f"Error getting uvindex: {str(e)}")
      return messages

    messages.append(f"{raw_data_uvindex['recordDesc']} of {twentyfourh_to_12h(raw_data_uvindex['updateTime'])}, the current uvindex recorded at {raw_data_uvindex['place']} is {raw_data_uvindex['value']}, classified as {raw_data_uvindex['desc']}")

    extra_message = raw_data_uvindex.get("message")
    if extra_message and extra_message != "":
      messages.append(f"Here is a special announcement from HKO regarding uv index: \n{extra_message}")

    return messages

  def fetch_temperature(self) -> list:
    messages = []
    try:
      raw_data_temperature = self.raw_data.get('temperature')

      if (not raw_data_temperature) or raw_data_temperature == "":
        messages.append(f"Received Null value in temperature. \nReport this error to the author.")
        return messages

      result = {
          'place': select_place(self.district, raw_data_temperature['data'], 'place', District_reference_for_temperature),
          'recordTime': raw_data_temperature['recordTime'][11:19]
      }

      for x in raw_data_temperature['data']:
        if x['place'] == result['place']:

          result['value'] = str(x['value']) + " "+ x['unit']

          messages.append(f"At {twentyfourh_to_12h(result['recordTime'])}, in {result['place']}, the temperature is {result['value']}")
          return messages

      messages.append(f"Data not available at requested district")
      return messages

    except Exception as e:
      messages.append(f"Error getting temperature: {str(e)}")
      return messages

  def fetch_humidity(self) -> list:
    messages = []
    raw_data_humidity = self.raw_data.get("humidity")
    if raw_data_humidity is None:
      messages.append("Humidity data unavailable")
      return messages

    temp = raw_data_humidity.get('data')
    if temp is None or temp == []:
      messages.append("Humidity data unavailable. Possible full maintenance of HKO")
      return messages
    temp = temp[0]

    result = {
        'place': temp['place'],
        'value': str(temp['value']) + " " + temp['unit'],
        'recordTime': raw_data_humidity['recordTime'][11:19]
    }

    messages.append(f"Humidity data recorded at {twentyfourh_to_12h(result['recordTime'])}: ")
    messages.append(f"\tAt {result['place']}, the humidity recorded is {result['value']}.")

    if (temp['unit'] == 'percent'):
      humidity_level = 'Low' if temp['value'] < 25 else 'Moderate' if temp['value'] < 75 else 'High'
      messages.append(f"\t Humidity Level is {humidity_level}")

    return messages

  def fetch_and_process_warning(self) -> list:
    messages = []
    result = self.raw_data.get('warningMessage', [])

    if not result:
      return messages

    n = len(result)
    messages.append(f"\nHere {'is 1' if n == 1 else f'are {n}'} warning message{'s' if n != 1 else ''} from Hong Kong Observatory:")
    for message in result:
      messages.append(f"\t{message}")
    return messages

  def fetch_and_process_ultil(self) -> list:
    messages = []
    # Special Weather Tips
    specialWxTips = self.raw_data.get('specialWxTips')
    if specialWxTips:
      messages.append("\nHere are some special Weather Tips from HKO: ")
      for message in specialWxTips:
        messages.append(f"\t{message}")

    # Tropical Cyclone Position
    tcmessage = self.raw_data.get('tcmessage')
    if tcmessage and tcmessage != "":
      n = len(tcmessage)
      messages.append("\nHere are some information relating to Tropical Cyclone from HKO: ")
      messages.append(f"Currently there {'is 1' if n == 1 else f'are {n}'} tropical cyclone{'s' if n != 1 else ''} near Hong Kong")
      for message in tcmessage:
        messages.append(f"\t{message}")

    # Others are always unavailable without any reason why
    return messages

  def fetch_bundle(self) -> list:
    messages = []
    try:
      if not self.fetch_data():
        messages.append("Failed to fetch data from HKO API.")
        return messages
      messages.extend(self.fetch_lighting())
      messages.extend(self.fetch_uv())
      messages.extend(self.fetch_temperature())
      messages.extend(self.fetch_humidity())
      messages.extend(self.fetch_and_process_warning())
      messages.extend(self.fetch_and_process_ultil())
    except Exception as e:
      messages.append(f"Error fetching data: {str(e)}")
    return messages
