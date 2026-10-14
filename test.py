# test.py
from location import Locs

# 1. Tüm sözlüğü gezmek ve ekrana düzgün yazdırmak:
for city_name, loc_obj in Locs.locationsDict.items():
    print(f"Konum-> {loc_obj.country}/{loc_obj.city}: ({loc_obj.lat},{loc_obj.lon})")
for konum in Locs.locations:
    print(konum.country, konum.city, konum.lat, konum.lon)
