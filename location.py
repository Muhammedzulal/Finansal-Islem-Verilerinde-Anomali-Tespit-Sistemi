class Location:
    def __init__(self, country, city, lat, lon):
        self.country = country
        self.city = city
        self.lat = lat
        self.lon = lon

    # Nesne print edildiğinde veya listede gösterildiğinde nasıl görüneceğini belirler
    def __repr__(self):
        return f"Location({self.city}, {self.lat}, {self.lon})"


class Locs:
    # Türkiye
    loc1 = Location(country="Türkiye", city="İstanbul", lat=41.0082, lon=28.9784)
    loc2 = Location(country="Türkiye", city="Ankara", lat=39.9334, lon=32.8597)
    loc3 = Location(country="Türkiye", city="İzmir", lat=38.4237, lon=27.1428)
    loc4 = Location(country="Türkiye", city="Antalya", lat=36.8969, lon=30.7133)
    loc5 = Location(country="Türkiye", city="Bursa", lat=40.1885, lon=29.0610)

    # Avrupa
    loc6 = Location(country="Fransa", city="Paris", lat=48.8566, lon=2.3522)
    loc7 = Location(country="Birleşik Krallık", city="Londra", lat=51.5074, lon=-0.1278)
    loc8 = Location(country="İtalya", city="Roma", lat=41.9028, lon=12.4964)
    loc9 = Location(country="Almanya", city="Berlin", lat=52.5200, lon=13.4050)
    loc10 = Location(country="İspanya", city="Madrid", lat=40.4168, lon=-3.7038)
    loc11 = Location(country="Hollanda", city="Amsterdam", lat=52.3676, lon=4.9041)
    loc12 = Location(country="Çekya", city="Prag", lat=50.0755, lon=14.4378)

    # Asya
    loc13 = Location(country="Japonya", city="Tokyo", lat=35.6762, lon=139.6503)
    loc14 = Location(country="Çin", city="Pekin", lat=39.9042, lon=116.4074)
    loc15 = Location(country="Güney Kore", city="Seul", lat=37.5665, lon=126.9780)
    loc16 = Location(country="Hindistan", city="Yeni Delhi", lat=28.6139, lon=77.2090)
    loc17 = Location(
        country="Birleşik Arap Emirlikleri", city="Dubai", lat=25.2048, lon=55.2708
    )
    loc18 = Location(country="Singapur", city="Singapur", lat=1.3521, lon=103.8198)

    # Kuzey Amerika
    loc19 = Location(country="ABD", city="New York", lat=40.7128, lon=-74.0060)
    loc20 = Location(country="ABD", city="Los Angeles", lat=34.0522, lon=-118.2437)
    loc21 = Location(country="ABD", city="San Francisco", lat=37.7749, lon=-122.4194)
    loc22 = Location(country="ABD", city="Chicago", lat=41.8781, lon=-87.6298)
    loc23 = Location(country="Kanada", city="Toronto", lat=43.6532, lon=-79.3832)
    loc24 = Location(country="Meksika", city="Mexico City", lat=19.4326, lon=-99.1332)

    # Güney Amerika
    loc25 = Location(
        country="Brezilya", city="Rio de Janeiro", lat=-22.9068, lon=-43.1729
    )
    loc26 = Location(
        country="Arjantin", city="Buenos Aires", lat=-34.6037, lon=-58.3816
    )
    loc27 = Location(country="Kolombiya", city="Bogotá", lat=4.7110, lon=-74.0721)

    # Afrika
    loc28 = Location(country="Mısır", city="Kahire", lat=30.0444, lon=31.2357)
    loc29 = Location(
        country="Güney Afrika", city="Cape Town", lat=-33.9249, lon=18.4241
    )
    loc30 = Location(country="Fas", city="Kazablanka", lat=33.5731, lon=-7.5898)

    # Okyanusya
    loc31 = Location(country="Avustralya", city="Sydney", lat=-33.8688, lon=151.2093)
    loc32 = Location(country="Avustralya", city="Melbourne", lat=-37.8136, lon=144.9631)
    loc33 = Location(
        country="Yeni Zelanda", city="Auckland", lat=-36.8485, lon=174.7633
    )

    # Tüm konumları listelemek için
    locations = [
        loc1,
        loc2,
        loc3,
        loc4,
        loc5,
        loc6,
        loc7,
        loc8,
        loc9,
        loc10,
        loc11,
        loc12,
        loc13,
        loc14,
        loc15,
        loc16,
        loc17,
        loc18,
        loc19,
        loc20,
        loc21,
        loc22,
        loc23,
        loc24,
        loc25,
        loc26,
        loc27,
        loc28,
        loc29,
        loc30,
        loc31,
        loc32,
        loc33,
    ]
    # Şehir adına göre hızlıca Location nesnesine ulaşabileceğin Dict yapısı
    locationsDict = {"İstanbul": loc1, "Ankara": loc2, "İzmir": loc3}
