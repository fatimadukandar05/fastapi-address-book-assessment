import math
import logging

logger = logging.getLogger(__name__)

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    earth_radius = 6371.0
    distance = earth_radius * c
    
    logger.debug(f"Distance between ({lat1}, {lng1}) and ({lat2}, {lng2}): {distance:.2f}km")
    return distance
