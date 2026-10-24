# Rastgele işlemler üretilecek
from faker import Faker
from aciklamalar import Desc
import random
from transfer import Transfer
from location import Locs
from datetime import datetime

fake = Faker("tr_TR")
dsc = Desc()

hesap_turu_list = ["Bireysel", "Kurumsal", "Ticari"]
islem_turu_list = ["EFT", "HAVALE", "FAST", "SWIFT"]
cihaz_turu_list = ["iOS", "Android", "Windows", "MacOs", "Linux", "ChromeOS"]


class Simulator:

    def __init__(self):
        # Benzersizlik kontrolleri için hafıza kümeleri
        self.uretilmis_ad_soyadlar = set()
        self.uretilmis_ibanlar = set()

    def benzersiz_ad_soyad_uret(self):
        deneme = 0
        while True:
            ad_soyad = f"{fake.first_name()} {fake.last_name()}"

            # Eğer henüz üretilmediyse kümeye ekle ve döndür
            if ad_soyad not in self.uretilmis_ad_soyadlar:
                self.uretilmis_ad_soyadlar.add(ad_soyad)
                return ad_soyad

            # Havuz dolmaya başladıysa ve sürekli çakışıyorsa (10 denemeden sonra)
            # isimlerin sonuna benzersizliği garanti edecek minik bir ek yapıyoruz
            deneme += 1
            if deneme > 10:
                benzersiz_ek = random.randint(100, 999)
                yeni_ad_soyad = f"{ad_soyad}{benzersiz_ek}"
                if yeni_ad_soyad not in self.uretilmis_ad_soyadlar:
                    self.uretilmis_ad_soyadlar.add(yeni_ad_soyad)
                    return yeni_ad_soyad

    def benzersiz_iban_uret(self):
        while True:
            iban = fake.iban()
            if iban not in self.uretilmis_ibanlar:
                self.uretilmis_ibanlar.add(iban)
                return iban

    def sifre_degisim_tarihi_uret(self):
        rastgele_dt = fake.date_time_between(start_date="-180d", end_date="-1m")
        return rastgele_dt

    def fake_veriler_olustur(self):
        #!--------Kimlik--------
        islem_id = random.randint(1, 1_000_000)
        islem_zamani = datetime.now()
        #!-------Gönderen-------
        gonderen_id = random.randint(1, 1_000_000)
        gonderen_ad_soyad = self.benzersiz_ad_soyad_uret()
        gonderen_iban = self.benzersiz_iban_uret()
        hesap_turu = hesap_turu_list[random.randint(0, 2)]
        son_sifre_degisimtarihi = self.sifre_degisim_tarihi_uret()

        #!---------Alıcı---------
        alici_ad_soyad = self.benzersiz_ad_soyad_uret()
        alici_iban = self.benzersiz_iban_uret()
        alici_banka_kodu = f"BK_{random.randint(10, 99)}"

        #!---------Finansal Detay---------
        miktar = random.randint(0, 300_000)
        para_birimi = f"{fake.currency_symbol()}"
        islem_turu = islem_turu_list[random.randint(0, 3)]
        aciklama = dsc.NORMAL_ACIKLAMALAR[random.randint(0, 10)]

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
            gonderen_son_sifre_degisimi=son_sifre_degisimtarihi,
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
        return yeni_transfer
