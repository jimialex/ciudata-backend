import utm


def coordinates_conversor(coordenadas, utm_zone):
    """Create a list of latitude-longitude pairs"""
    array_lat_long = []
    for easting, northing in coordenadas:
        # Convert coordinates to latitude and longitude
        latitud, longitud = utm.to_latlon(easting, northing, utm_zone, northern=False)

        # Format the latitude and longitude values to 7 decimal places
        data = {
            "lat": f"{latitud:.7f}",
            "lng": f"{longitud:.7f}"
        }
        array_lat_long.append(data)

    return array_lat_long
