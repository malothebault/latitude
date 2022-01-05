class Converter:
    def __init__(self):
        pass

    def dms2ddd(self, dms):
        ddd = {}
        lat = dms.get('lat')
        lon = dms.get('lon')    
        ddd['lat'] = (lat[0] + lat[1]/60 + lat[2]/3600, lat[3])
        ddd['lon'] = (lon[0] + lon[1]/60 + lon[2]/3600, lon[3])
        return ddd

    def ddd2dms(self, ddd):
        dms = {}
        lat = ddd.get('lat')
        lon = ddd.get('lon')    
        dms['lat'] = (int(lat[0]), int(60*(lat[0]%1)), ((60*(lat[0]%1))%1)*60, lat[1])
        dms['lon'] = (int(lon[0]), int(60*(lon[0]%1)), ((60*(lon[0]%1))%1)*60, lon[1])
        return dms
    
    def ddd2dmm(self, ddd):
        dmm = {}
        lat = ddd.get('lat')
        lon = ddd.get('lon')    
        dmm['lat'] = (int(lat[0]), 60*(lat[0]%1), lat[1])
        dmm['lon'] = (int(lon[0]), 60*(lon[0]%1), lon[1])
        return dmm
    
    def dmm2dms(self, dmm):
        dms = {}
        lat = dmm.get('lat')
        lon = dmm.get('lon')    
        dms['lat'] = (lat[0], int(lat[1]), int(60*(lat[1]%1)), lat[1])
        dms['lon'] = (lon[0], int(lon[1]), int(60*(lon[1]%1)), lon[1])
        return dms
    
    def dmm2ddd(self, dmm):
        dms = self.dmm2dms(dmm)
        ddd = self.dms2ddd(dms)
        return ddd
    
    def dms2dmm(self, dms):
        ddd = self.dms2ddd(dms)
        dmm = self.ddd2dmm(ddd)
        print(dmm)
        return dmm

