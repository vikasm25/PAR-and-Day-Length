import numpy as np
import matplotlib.pyplot as plt


# Constants
I0 = 1361  # Solar constant in W/m²
e = 0.0167  # Orbital eccentricity
days_in_year = 365.25
tp = 3  # Approximate day of perihelion (January 3)
par_fraction = 0.45  # Fraction of total solar irradiance that is PAR

def day_length(latitude, declination):
    latitude_rad = np.radians(latitude)
    declination_rad = np.radians(declination)
    cos_h0 = -np.tan(latitude_rad) * np.tan(declination_rad)
    
    if cos_h0 >= 1:
        return 0  # Polar night
    elif cos_h0 <= -1:
        return 24  # Midnight sun

    h0 = np.degrees(np.arccos(cos_h0))
    return 2 * h0 / 15  # Day length in hours

def solar_irradiance_at_time(t, latitude, time_of_day):
    distance_factor = (1 - e * np.cos(2 * np.pi * (t - tp) / days_in_year))**-2
    declination_angle = 23.44 * np.sin(2 * np.pi * (t - 80) / days_in_year)
    
    latitude_rad = np.radians(latitude)
    declination_rad = np.radians(declination_angle)
    
    # Calculate the hour angle (H)
    solar_noon = 12  # Assuming solar noon is at 12:00 local time
    hour_angle = 15 * (time_of_day - solar_noon)  # 15 degrees per hour
    hour_angle_rad = np.radians(hour_angle)
    
    cos_zenith_angle = (np.sin(latitude_rad) * np.sin(declination_rad) +
                        np.cos(latitude_rad) * np.cos(declination_rad) * np.cos(hour_angle_rad))
    
    if cos_zenith_angle < 0:
        return 0  # No irradiance when the sun is below the horizon
    
    irradiance = I0 * distance_factor * cos_zenith_angle
    return irradiance

def average_par_on_surface(t, latitude):
    declination_angle = 23.44 * np.sin(2 * np.pi * (t - 80) / days_in_year)
    day_length_hours = day_length(latitude, declination_angle)
    if day_length_hours == 0:
        return 0  # No PAR if there is no daylight
    
    total_par = 0
    time_steps = int(day_length_hours * 4)  # 15-minute intervals
    time_of_day_start = 12 - day_length_hours / 2
    time_of_day_end = 12 + day_length_hours / 2
    
    for time_step in np.linspace(time_of_day_start, time_of_day_end, time_steps):
        irradiance = solar_irradiance_at_time(t, latitude, time_step)
        par = irradiance * par_fraction
        total_par += par

    if time_steps==0:
        average_par=0
    else:
        average_par = total_par / time_steps
    return average_par

# Example usage: Calculate average PAR for day 100 at latitude 45 degrees
day_of_year = 100
days=np.arange(1,365)
lat=30
irr=[]
for t in range(0,len(days)):
    par = average_par_on_surface(t, lat)
    print(f'Average PAR on day {t} at latitude {lat}°: {par:.2f} W/m²')
    irr.append(par)
    
plt.clf()
plt.plot(days,irr)
# plt.show()
plt.savefig("G:/Test/Output/"+str(lat)+".png")


