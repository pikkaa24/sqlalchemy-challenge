# sqlalchemy-challenge

This jupyter notebook takes data from the station and measurement csv files for analysis using SQLAlchemy and pandas. Precipitation data from the most recent 12 months was gathered to show the precipitation in inches for each date of the year. Then the station with the most recorded data was identified and the temperature observastions were plotted into a histogram for the most recent 12 months. 

The python app has routes to list the precipitation and temperature data gathered in the jupyter notebook. One route also provides the list of stations in the dataset. A route is also provided to calculate the min, max, and avg temperature a date range or from a specific date. 

References:

-Adapted following code given by Xpert Learning Assistant.
    station_names = session.query(station.station).all()
    station_list = [name[0] for name in station_names]