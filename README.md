# Data-Vizualitation - List of Busiest Airports by Passenger Traffic 2022 With Streamlit

## Group Project
- Syehan Fariz Gustomo - 1301210530
- Naufal Geo Pastrana - 1301213083
- Akmal Sidki Razaka - 1301210547

##

This application is an interactive dashboard built using Streamlit to visualize data on the 50 busiest airports in the world for 2022. The dashboard allows users to explore statistics, geographic distribution, and global trends related to these airports.

## Features
- Airport Rankings: Information on airport rankings based on passenger numbers.
- Geographic Distribution: Visualization of airport locations on a world map.
- Regional Statistics: Data analysis based on regions or countries.
- Dynamic Visualizations: Interactive charts using Pydeck, Plotly, and Matplotlib.

## Dataset
The dataset used is modified_busiest_airports_2022.csv, which contains the following information:
- Airport Name: Official name of the airport.
- Location: City and country where the airport is located.
- Passenger Numbers: Passenger statistics.
- Latitude and Longitude: Geographic coordinates for map visualization.

## File Structure
- (`application.py`): Main code for the Streamlit application.
- (`modified_busiest_airports_2022.csv`): Dataset of the world's busiest airports in 2022.

## How To Run the Application
- Ensure Python 3.x is installed:
  - Download and install Python from [python.org](https://www.python.org/)
- Install the required depedencies:
  ```bash
  pip install -r requirements.txt
  ```
  Note: Create a (`requirements.txt`) file if it doesn't exist with the following
  ```bash
  streamlit
  pandas
  pydeck
  plotly
  ```
- Run the Application:
  - Open (`http://localhost:8888`) in your web browser.
