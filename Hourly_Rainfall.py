import requests
import json

PRIORITY_STATIONS = {'Tuen Mun': ["RF019", "RF002", "RF001" , "N12"], #屯門，#濕地公園，流浮山，元朗水邊圍
                     'Tin Shui Wai': ["RF002", "RF001", "N12", "RF019"], #濕地公園，流浮山，元朗水邊圍，屯門
                     'Yuen Long': ["N12", "RF002","RF003", "RF001"]} #元朗水邊圍, 濕地公園，石崗，流浮山

# A way to check if the station is still close to the district user mentioend (within 3.0 km)
PRIORITY_STATIONS_bool = {
    'Tuen Mun': [True, False, False, False],
    'Tin Shui Wai': [True, True, True, False],
    'Yuen Long': [True, False, False, False]
}

class Hourly_Rainfall():
  raw_data = None
  processed_data = None
  last_update = None
  district = None
  # Manual approach identifier
  manual = False

  def __init__(self, district: str) -> None:
    self.raw_data = None
    self.processed_data = None
    self.last_update = None
    self.district = district
    self.manual = False

  def fetch_data(self) -> bool:
    try:
      response = requests.get('https://data.weather.gov.hk/weatherAPI/opendata/hourlyRainfall.php?lang=en', timeout = 10)
      response.raise_for_status() # For HTTP error

      if not response:
        raise Exception("Received empty data from API")

      self.raw_data = response.json()

      if not self.raw_data['obsTime']:
        raise Exception("No obsTime. Possible update on Hong Kong Observatory")

      self.last_update = self.raw_data['obsTime'][11:19]
      return True

    except Exception as e:
      raise Exception(f"Error getting hourlyRainfall data: {str(e)}")

  # Extract data for all priority stations
  def filter_data(self) -> list:
    # Result = [None, None, None, None] normally
    try:

      # If hourlyRainfall doesn't exist on raw_data (the data from API request, raise an exception)
      if not (self.raw_data.get('hourlyRainfall')):
        raise Exception(f"Possible Full Maintenance on Hong Kong Observatory. ")

      hourlyRainfall_data = self.raw_data['hourlyRainfall']

      # Manual approach
      if (self.district not in PRIORITY_STATIONS.keys()):
        self.manual = True
        # In Streamlit context, we can't use input(), so raise error instead
        raise Exception("District not supported for automatic selection. Please choose a supported district.")

      result = [None for i in range(len(PRIORITY_STATIONS[self.district]))]

      for data in hourlyRainfall_data:
        if ((data['automaticWeatherStationID'] in PRIORITY_STATIONS[self.district]) and data['value'] != 'M'):
          index = PRIORITY_STATIONS[self.district].index(data['automaticWeatherStationID'])
          result[index] = [data['automaticWeatherStation'] , data['value'] + " " + data['unit']]

      if any(result):
        self.processed_data = result
        return result
      else:
        return None # return none if all 4 of them is not working


    except Exception as e:
      raise Exception(f"Error filtering hourlyRainfall data: {str(e)}")

  def get_nearest_rainfall_data(self) -> list:
    messages = []
    if self.processed_data is None:
      return messages

    for i in range(len(self.processed_data)):
      nearest_rainfall_data = self.processed_data[i]
      if (nearest_rainfall_data):

        if (PRIORITY_STATIONS_bool[self.district][i] == False):
          messages.append("As all the automatic weather station next to you is under maintenance, we will present data from other weather station.\nThe data retrieved might be less accurate. We are sorry for such inconvenience.")

        messages.append(f"During last hour of {self.last_update}, in {nearest_rainfall_data[0]}, the rainfall amount is {nearest_rainfall_data[1]}")
        return messages

    messages.append(f"All 4 nearest automatic weather station is not available/ under maintenance. Please try again later.") # This shouldn't be used normally. Just a redundant command for just incase.
    return messages

  def fetch_bundle(self) -> list:
    messages = []
    try:
      if not self.fetch_data():
        messages.append("Hong Kong Observatory API is currently unavailable")
        return messages

      filtered = self.filter_data()
      if filtered is None:
        messages.append("All 4 nearest automatic weather station is not available/ under maintenance. Please try again later.")
        return messages

      if not self.manual:
        messages.extend(self.get_nearest_rainfall_data())

    except Exception as e:
      messages.append(f"Error: {str(e)}")
    return messages
