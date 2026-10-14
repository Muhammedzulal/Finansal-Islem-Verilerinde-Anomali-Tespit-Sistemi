# Rastgele işlemler üretilecek
from faker import Faker
from aciklamalar import Desc
import random
from transfer import Transfer
from location import Locs

fake = Faker("tr_TR")
dsc = Desc()

hesap_turu_list = ["Bireysel", "Kurumsal", "Ticari"]
islem_turu_list = ["EFT", "HAVALE", "FAST", "SWIFT"]
cihaz_turu_list = ["iOS", "Android", "Windows", "MacOs", "Linux", "ChromeOS"]


class Simulator:
    def fake_veriler_olustur(self):
        #!--------Kimlik--------
        islem_id = random.randint(1, 1_000_000)
        islem_zamani = fake.date_time()
        #!-------Gönderen-------
        gonderen_id = random.randint(1, 1_000_000)
        gonderen_ad_soyad = f"{fake.first_name()} {fake.last_name()}"
        gonderen_iban = fake.iban()
        hesap_turu = hesap_turu_list[random.randint(0, 2)]

        #!---------Alıcı---------
        alici_ad_soyad = f"{fake.first_name()} {fake.last_name()}"
        alici_iban = fake.iban()
        alici_banka_kodu = f"BK_{random.randint(10, 99)}"

        #!---------Finansal Detay---------
        miktar = random.randint(0, 300_000)
        para_birimi = f"{fake.currency_name()} ({fake.currency_symbol()})"
        islem_turu = islem_turu_list[random.randint(0, 3)]
        aciklama = dsc.NORMAL_ACIKLAMALAR[random.randint(0, 15)]

        #!---------Cihaz & Ağ---------
        ip_adresi = fake.ipv4()
        cihaz_id = fake.uuid4()
        cihaz_turu = cihaz_turu_list[random.randint(0, 5)]
        isletim_sistemi = random.randint(0, 18)

        #!---------Konum---------
        rndNumber = random.randint(0, 32)
        ulke = Locs.locations[rndNumber].country
        sehir = Locs.locations[rndNumber].city
        enlem = Locs.locations[rndNumber].lat
        boylam = Locs.locations[rndNumber].lon

        #!---------Nesne---------
        # Transfer nesnesini oluşturuyoruz
        yeni_transfer = Transfer(
            islem_id=islem_id,
            islem_zamani=islem_zamani,
            gonderen_id=gonderen_id,
            gonderen_ad_soyad=gonderen_ad_soyad,
            gonderen_iban=gonderen_iban,
            gonderen_hesap_turu=hesap_turu,
            alici_ad_soyad=alici_ad_soyad,
            alici_iban=alici_iban,
            alici_banka_kodu=alici_banka_kodu,
            miktar=miktar,
            para_birimi=para_birimi,
            islem_turu=islem_turu,
            aciklama=aciklama,
            ip_adresi=ip_adresi,
            cihaz_id=cihaz_id,
            cihaz_turu=cihaz_turu,
            isletim_sistemi=isletim_sistemi,
            sehir=sehir,
            ulke=ulke,
            enlem=enlem,
            boylam=boylam,
        )

        # &------PRINT----------
        yeni_transfer.yazdir()
