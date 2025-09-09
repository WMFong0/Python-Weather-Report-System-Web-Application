def twentyfourh_to_12h(time: str) -> str:
  splitted_time = time.split(':')
  hour = int(splitted_time[0])
  if hour >= 12:
    splitted_time.append("PM")
    if (hour > 12):
      splitted_time[0] = str(hour - 12)
  else:
    splitted_time.append("AM")
    if (hour == 0):
      splitted_time[0] = str(12)

  return ":".join(splitted_time[:-1]) + " " + splitted_time[-1]

def No_empty_string(received_data):
  return None if received_data == "" else received_data

'''disbanded
def select_place(original_selection, raw_data_temperature_datasection: list, variable_name_for_station: str, supported_station: dict = {}):
    # Predefined
    if original_selection in supported_station.keys():
      return District_reference_for_temperature[original_selection]

    available_station = []
    # Fetch available station
    for station_data in raw_data_temperature_datasection:
      available_station.append( station_data[variable_name_for_station] )

    # Remove supported station
    for station in supported_station.values():
      available_station.remove(station)

    # Same Name Case
    if original_selection in available_station:
      return original_selection


    # Required Manual Case
    print("Since we currently doesn't support automatic selection of weather station at your district\n Please select the nearest weather station from the list below: ")
    station = ""

    while True:
      print("Available Station: ")
      for i in range(len(available_station)):
        if (i != 0 and i % 4 == 0):
          print("\t" + available_station[i], end = '\n')
        else:
          print("\t" + available_station[i], end = '')

      station = format_string(input("\nKey in your nearest Weather Station: "))
      # Just in case operation
      if (station in available_station):
        print()
        break
      print("You have input a unavailable station. Please input a available Station." + "\n"*2)

    return station
'''

def lazy_list_message(message_list: list = []):
  full_message = ""
  for message in message_list:
    message = message.replace('a.m.', 'am').replace('p.m.','pm').replace("No.", "No")
    small_message = [part.strip() for part in message.split('. ') if part.strip()]
    # message = ""
    if not small_message:
      continue

    full_message += f"<ul><li>{small_message[0]}"
    for part in small_message[1:]:
      if part != "":
        if ';' in part:
          smaller_part = part.split(';')
          for text in smaller_part:
            full_message += f"<li>{text}</li>"
        else:
          full_message += f"<li>{part}</li>"
    full_message += "</li></ul>"
    return full_message

def format_string(string: str = "") -> str:
  string = string.strip()
  splitted_string = string.split(" ")
  for i in range(len(splitted_string)):
    splitted_string[i] = splitted_string[i].lower().capitalize()
  return " ".join(splitted_string)


# disbanding
def lazy_print_option(message, option_list: list):
  option_list = list(set(option_list))

  if not option_list:
    return None
  elif len(option_list) == 1:
    return option_list[0]

  if len(option_list) <= 5:
    for item in option_list:
      message += f"{item}, " if item != option_list[-1] else item
  else:
    message += (("\n") + ("  "))
    for item_index, item in enumerate(option_list, start=1):
        message += item if item == option_list[-1] else ((item + "\n  ") if item_index % 4 == 0 else f"{item}, ")

  while True:
    print("\n" + message)
    user_input = format_string(input(" "))
    if user_input in option_list:
      break
    print("Sorry. You have input a option that is out of the list, please check your input", "\n")

  return user_input