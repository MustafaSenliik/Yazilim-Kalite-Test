from models import Location
from geopy.distance import geodesic

class LocationService:
    def __init__(self):
        self.district_boundaries = {
            'ADALAR': {'north': 40.9333, 'south': 40.9000, 'east': 29.0000, 'west': 29.0000},
            'ARNAVUTKOY': {'north': 41.0500, 'south': 41.0000, 'east': 28.7500, 'west': 28.6000},
            'ATASEHIR': {'north': 41.0000, 'south': 40.9800, 'east': 29.2000, 'west': 29.1000},
            'SILIVRI': {'north': 41.0000, 'south': 40.9600, 'east': 28.6500, 'west': 28.5000},
            'AVCILAR': {'north': 41.0700, 'south': 40.9700, 'east': 28.7400, 'west': 28.6400},
            'BAGCILAR': {'north': 41.0600, 'south': 41.0100, 'east': 28.8700, 'west': 28.8300},
            'BAHCELIEVLER': {'north': 41.0200, 'south': 40.9900, 'east': 28.8700, 'west': 28.8400},
            'BAKIRKOY': {'north': 40.9900, 'south': 40.9600, 'east': 28.9000, 'west': 28.8100},
            'BASAKSEHIR': {'north': 41.1200, 'south': 41.0300, 'east': 28.8000, 'west': 28.6000},
            'BAYRAMPASA': {'north': 41.0500, 'south': 41.0000, 'east': 28.9200, 'west': 28.8800},
            'BESIKTAS': {'north': 41.0600, 'south': 41.0100, 'east': 29.0400, 'west': 29.0000},
            'BEYKOZ': {'north': 41.1800, 'south': 41.0600, 'east': 29.2700, 'west': 29.0300},
            'BEYLIKDUZU': {'north': 41.0100, 'south': 40.9700, 'east': 28.6400, 'west': 28.6000},
            'BEYOGLU': {'north': 41.0400, 'south': 41.0200, 'east': 28.9700, 'west': 28.9400},
            'BUYUKCEKMECE': {'north': 41.0000, 'south': 40.9600, 'east': 28.6500, 'west': 28.5000},
            'CATALCA': {'north': 41.1600, 'south': 41.1000, 'east': 28.4600, 'west': 28.2000},
            'CEKMEKOY': {'north': 41.0300, 'south': 41.0000, 'east': 29.2300, 'west': 29.1700},
            'ESENLER': {'north': 41.0500, 'south': 41.0200, 'east': 28.8800, 'west': 28.8300},
            'ESENYURT': {'north': 41.0300, 'south': 40.9900, 'east': 28.7000, 'west': 28.6200},
            'EYUPSULTAN': {'north': 41.1400, 'south': 41.0400, 'east': 28.9300, 'west': 28.8000},
            'FATIH': {'north': 41.0300, 'south': 41.0100, 'east': 28.9700, 'west': 28.9000},
            'GAZIOSMANPASA': {'north': 41.0800, 'south': 41.0300, 'east': 28.9200, 'west': 28.8500},
            'GUNGOREN': {'north': 41.0200, 'south': 41.0000, 'east': 28.8800, 'west': 28.8500},
            'KADIKOY': {'north': 40.9900, 'south': 40.9700, 'east': 29.1000, 'west': 29.0300},
            'KAGITHANE': {'north': 41.0800, 'south': 41.0300, 'east': 28.9700, 'west': 28.9400},
            'KARTAL': {'north': 40.9900, 'south': 40.9600, 'east': 29.2000, 'west': 29.1700},
            'KUCUKCEKMECE': {'north': 41.0300, 'south': 41.0100, 'east': 28.8000, 'west': 28.7400},
            'MALTEPE': {'north': 40.9800, 'south': 40.9500, 'east': 29.1700, 'west': 29.1200},
            'PENDIK': {'north': 41.0000, 'south': 40.9800, 'east': 29.3000, 'west': 29.2400},
            'SARIYER': {'north': 41.2000, 'south': 41.1200, 'east': 29.0300, 'west': 28.9300},
            'SILIVRI': {'north': 41.1000, 'south': 40.9600, 'east': 28.3000, 'west': 28.0000},
            'SULTANBEYLI': {'north': 41.0000, 'south': 40.9600, 'east': 29.3200, 'west': 29.2300},
            'SULTANGAZI': {'north': 41.1100, 'south': 41.0400, 'east': 28.8500, 'west': 28.8000},
            'SILE': {'north': 41.2000, 'south': 41.0000, 'east': 29.8500, 'west': 29.6000},
            'SISLI': {'north': 41.0700, 'south': 41.0300, 'east': 28.9800, 'west': 28.9400},
            'TUZLA': {'north': 41.0000, 'south': 40.9600, 'east': 29.3000, 'west': 29.2300},
            'UMRANIYE': {'north': 41.0300, 'south': 41.0000, 'east': 29.2000, 'west': 29.1000},
            'USKUDAR': {'north': 41.0400, 'south': 41.0100, 'east': 29.0600, 'west': 29.0100},
            'ZEYTINBURNU': {'north': 41.0200, 'south': 41.0000, 'east': 28.9000, 'west': 28.8500}
        }

    def get_all_filtered_locations(self):
        all_locations = Location.query.all()
        filtered_locations = []
        for location in all_locations:
            town_boundary = self.district_boundaries.get(location.town_id.upper(), None)
            if not town_boundary:
                continue
            try:
                lat = float(location.latitude.replace(',', '.'))
                lng = float(location.longitude.replace(',', '.'))
                if self.is_within_boundary(lat, lng, town_boundary):
                    filtered_locations.append(location)
            except ValueError:
                print(f"Hatalı koordinatlar: {location.latitude}, {location.longitude}")
                continue

        return filtered_locations

    def get_locations_by_town_id(self, town_id):
        town_boundary = self.district_boundaries.get(town_id.upper(), None)
        if not town_boundary:
            return []

        locations = Location.query.filter_by(town_id=town_id.upper()).all()
        filtered_locations = []
        for location in locations:
            try:
                lat = float(location.latitude.replace(',', '.'))
                lng = float(location.longitude.replace(',', '.'))
                if self.is_within_boundary(lat, lng, town_boundary):
                    filtered_locations.append(location)
            except ValueError:
                print(f"Hatalı koordinatlar: {location.latitude}, {location.longitude}")
                continue

        return filtered_locations

    def is_within_boundary(self, lat, lng, boundary):
        return (boundary['south'] <= lat <= boundary['north'] and
                boundary['west'] <= lng <= boundary['east'])

    def find_nearest_locations(self, latitude, longitude, count=3):
        locations = self.get_all_filtered_locations()
        location_distances = []

        for location in locations:
            try:
                loc_coords = (float(location.latitude.replace(',', '.')), float(location.longitude.replace(',', '.')))
                dist = geodesic((latitude, longitude), loc_coords).meters
                location_distances.append((location, dist))
            except ValueError:
                print(f"Hatalı koordinatlar: {location.latitude}, {location.longitude}")
                continue

        location_distances.sort(key=lambda x: x[1])
        nearest_locations = [location[0] for location in location_distances[:count]]
        return nearest_locations

    def get_all_locations(self):
        return Location.query.all()
