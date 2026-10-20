"""# test.py
from location import Locs

# 1. Tüm sözlüğü gezmek ve ekrana düzgün yazdırmak:
for city_name, loc_obj in Locs.locationsDict.items():
    print(f"Konum-> {loc_obj.country}/{loc_obj.city}: ({loc_obj.lat},{loc_obj.lon})")
for konum in Locs.locations:
    print(konum.country, konum.city, konum.lat, konum.lon)"""

"""from datetime import datetime

# Tarih ve saat birlikte
simdi = datetime.now()

# Sadece saat kısmı
sadece_saat = datetime.now().time()
print(simdi)
print(sadece_saat)"""

from faker import Faker

fake = Faker("tr_TR")
print(type(fake.date()))
print(fake.date_time_between(start_date="-1y", end_date="now"))
