from ismn.interface import ISMN_Interface
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#data path with current directory and the ISMN data folder starting with name Data_separate_files_header
data_path = os.path.join(os.getcwd(), "Data_separate_files_header_20100101_20240102_9781_ykEo_20240102")

# Function to calculate daily mean soil moisture
def calculate_daily_mean_soil_moisture(lat, lon, start_date, end_date, depth_from, depth_to, remove_flag=True):
    ismn_data = ISMN_Interface(data_path, parallel=True)
    
    station, dist = ismn_data.collection.get_nearest_station(lon, lat)
    station_name = station.name
    network_name = ismn_data.network_for_station(station.name, name_only=False).name
    
    print(f'Station {station.name} is {int(dist)} metres away from the passed coordinates:')
    print("Network name:", network_name)
    print("Station name:", station.name)
    
    sensor_data_list = []
    
    # Iterate over sensors and filter by station name and depth
    for network, station, sensor in ismn_data.collection.iter_sensors(variable='soil_moisture', depth=[depth_from, depth_to]):
        if station.name == station_name:
            sensor_data = sensor.read_data()
            sensor_data = sensor_data[(sensor_data.index >= start_date) & (sensor_data.index <= end_date)]
            sensor_data.replace(-9999, np.nan, inplace=True)
            if remove_flag:
                sensor_data.loc[sensor_data['soil_moisture_flag'] != 'G', 'soil_moisture'] = np.nan
            sensor_data_list.append(sensor_data['soil_moisture'])
    
    if not sensor_data_list:
        print("No matching sensors found for the specified station and depth.")
        return None, None
    
    combined_data = pd.concat(sensor_data_list, axis=1)
    average_soil_moisture = combined_data.mean(axis=1)
    daily_mean_soil_moisture = average_soil_moisture.resample('D').mean()
    daily_mean_soil_moisture_filtered = daily_mean_soil_moisture[start_date:end_date]
    daily_mean_soil_moisture_filtered = daily_mean_soil_moisture_filtered.to_frame(name= station_name + " "+ 'soil_moisture')
    
    # Store metadata separately
    metadata = {
        "network": network_name,
        "station_name": station_name,
        "latitude": lat,
        "longitude": lon
    }
    
    return daily_mean_soil_moisture_filtered, metadata

lat, lon = 50.5, 6.3
start_date = "2011-07-03"
end_date = "2013-12-31"

daily_mean_soil_moisture, metadata = calculate_daily_mean_soil_moisture(lat, lon, start_date, end_date, 0.0, 0.05, True)

if daily_mean_soil_moisture is not None:
    # Plot the data
    plt.figure(figsize=(10, 6))
    daily_mean_soil_moisture.plot(title="Daily Mean Soil Moisture")
    plt.xlabel("Date")
    plt.ylabel("Soil Moisture")
    plt.title(f"Daily Mean Soil Moisture\nNetwork: {metadata['network']}, "
              f"Station: {metadata['station_name']}\n"
              f"Lat: {metadata['latitude']}, Lon: {metadata['longitude']}")
    plt.show()

    # Print the DataFrame and metadata
    print(daily_mean_soil_moisture)
    print(metadata)