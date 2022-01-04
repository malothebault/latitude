def dms2ddd(dms):
    lat, lon = dms.split(',')
    lat_deg, temp = lat.split('°')
    lat_min, temp = temp.split("'")
    lat_sec, lat_card = temp.split('"')
    lon_deg, temp = lon.split('°')
    lon_min, temp = temp.split("'")
    lon_sec, lon_card = temp.split('"')
    
    return ddd

def ddd2dms(ddd):
    
    return dms