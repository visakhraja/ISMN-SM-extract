# Reading and plotting ISMN data for specific latitude and longitude (ismn.interface.ISMN_Interface)

Data for your study area can be selected and downloaded for free from http://ismn.earth after registration.
ISMN files are downloaded as a compressed .zip file after selecting the data from the website. You can extract it (with any zip software) locally into one (root) folder (in this case ‘Data_separate_files’).

Keep this data in the current working directory

To run the code the following packages have to be installed:

ismn.interface
os
numpy
pandas
matplotlib.pyplot

Please change the latitude, longitude, depth_from, depth_to, start_date and end_date according to your study

This script extracts the daily soil moisture for a particular location, depth and time range




