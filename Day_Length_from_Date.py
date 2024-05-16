from datetime import datetime
from datetime import timedelta 
import numpy as np

lat=20
date="01-01-2020"

def day_year(date):
    date=datetime.strptime(date,'%d-%m-%Y')
    day_of_year = date.timetuple().tm_yday
    return day_of_year

def daylength(dayOfYear, lat):
    latInRad = np.deg2rad(lat)
    declinationOfEarth = 23.45*np.sin(np.deg2rad(360.0*(283.0+dayOfYear)/365.0))
    if -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) <= -1.0:
        return 24.0
    elif -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) >= 1.0:
        return 0.0
    else:
        hourAngle = np.rad2deg(np.arccos(-np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth))))
        return 2.0*hourAngle/15.0
    

# date1=datetime.strptime(date,'%d-%m-%Y')
day=np.arange(0,2*366,1)
for i in range(0,len(day)):
    day_y=day_year(date)
    day_l=daylength(day_y,lat)
    date=datetime.strptime(date,'%d-%m-%Y')
    print("Date : {} , Day : {:3}  , Length {}".format(date,day_y,day_l))
    date = date + timedelta(days=1)
    date=date.strftime('%d-%m-%Y')