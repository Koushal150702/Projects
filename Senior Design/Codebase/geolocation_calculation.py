from geopy.geocoders import Nominatim
import math

def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.reverse(f"{latitude}, {longitude}")

    if location:
        address_parts = location.raw['address']
        area = address_parts.get('suburb', '') or address_parts.get('city_district', '')
        city = address_parts.get('city', '') or address_parts.get('town', '')
        country = address_parts.get('country', '')

        return f"{area}, {city}, {country}"
        # return f"{city}, {country}"
    else:
        return "Unknown"
    

def calculate_geolocation(latitude, longitude, object_height, ymax, ymin): 
    obj_height = object_height
    real_h = 2133.6 + obj_height
    cam_frame = 1080
    focal = 5.6
    img_height = ymax-ymin # ymax - ymin (bounding box)
    sensor_height = 11.43
    
    distance_to_obj = (real_h * cam_frame * focal) / (img_height * sensor_height)
    distance_to_sign = distance_to_obj/1000

    # Conversion factor for estimating latitude and longitude change based on distance
    lat_factor = distance_to_sign / 111000  # 1 degree of latitude is approximately 111 kilometers
    lon_factor = distance_to_sign / (111000 * math.cos(math.radians(latitude)))

    # Calculate new latitude and longitude
    new_latitude = latitude + lat_factor
    new_longitude = longitude + lon_factor

    return new_latitude, new_longitude