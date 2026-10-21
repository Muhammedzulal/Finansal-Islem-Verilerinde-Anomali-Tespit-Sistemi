import random
from datetime import datetime, timedelta

from faker import Faker

from location import Locs
from transfer import Transfer

fake = Faker("tr_TR")

HESAP_TURLERI = ["Bireysel", "Kurumsal", "Ticari"]
ISLEM_TURLERI = ["EFT", "HAVALE", "FAST", "SWIFT"]
CIHAZ_TURLERI = ["iOS", "Android", "Windows", "MacOs", "Linux", "ChromeOS"]
SUPHELI_ACIKLAMALAR = ["ACİL", "CRYPTO", "ÖNEMLİ ACİL BAKIYE", "TEST", "????", ""]
YURT_DISI_KONUMLAR = [yer for yer in Locs.locations if yer.country != "Türkiye"]
TURKIYE_KONUMLARI = [yer for yer in Locs.locations if yer.country == "Türkiye"]

# Ana anomali senaryoları ve dağılımları. Toplam 100.
SENARYO_AGIRLIKLARI = {
    "ASIRI_YUKSEK_TUTAR": 25,
    "GECE_YUKSEK_TUTAR": 20,
    "BIREYSEL_YURT_DISI_SWIFT": 20,
    "SUPHELI_ACIKLAMA": 15,
    "ARDISIK_HIZLI_TRANSFER": 10,
    "SIFRE_DEGISIMI_SONRASI_TRANSFER": 10,
}


class Simulator:
    """Normal simülatörle aynı çağrı arayüzünü sunan anomali üreticisi."""

    def __init__(self):
        self.uretilmis_ad_soyadlar = set()
        self.uretilmis_ibanlar = set()
        self.uretilmis_islem_idleri = set()
        self._son_zaman = None
        self._tekrar_gonderen = None

    def benzersiz_ad_soyad_uret(self):
        while True:
            ad_soyad = f"{fake.first_name()} {fake.last_name()}"
            if ad_soyad not in self.uretilmis_ad_soyadlar:
                self.uretilmis_ad_soyadlar.add(ad_soyad)
                return ad_soyad
            if len(self.uretilmis_ad_soyadlar) > 200:
                ad_soyad += str(random.randint(100000, 999999))
                if ad_soyad not in self.uretilmis_ad_soyadlar:
                    self.uretilmis_ad_soyadlar.add(ad_soyad)
                    return ad_soyad

    def benzersiz_iban_uret(self):
        while True:
            iban = fake.iban()
            if iban not in self.uretilmis_ibanlar:
                self.uretilmis_ibanlar.add(iban)
                return iban

    def sifre_degisim_tarihi_uret(self):
        return datetime.now() - timedelta(days=random.randint(7, 365))

    def _benzersiz_islem_id_uret(self):
        while True:
            islem_id = random.randint(1, 2_147_483_647)
            if islem_id not in self.uretilmis_islem_idleri:
                self.uretilmis_islem_idleri.add(islem_id)
                return islem_id

    def fake_veriler_olustur(self, yazdir=True, senaryo=None):
        """Anomali içeren bir Transfer üretir ve döndürür.

        senaryo: SENARYO_AGIRLIKLARI içindeki senaryo adlarından biri,
                 None ise ağırlıklara göre rastgele seçilir.
        yazdir:  True ise üretilen transferi terminale basar.
        """
        if senaryo is None:
            senaryo = random.choices(
                list(SENARYO_AGIRLIKLARI),
                weights=list(SENARYO_AGIRLIKLARI.values()),
                k=1,
            )[0]
        if senaryo not in SENARYO_AGIRLIKLARI:
            raise ValueError(f"Bilinmeyen senaryo: {senaryo}")

        simdi = datetime.now()
        # Çoğu işlem son 30 gün içinde oluşur.
        islem_zamani = simdi - timedelta(
            days=random.randint(0, 29),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        gonderen_id = random.randint(1, 1_000_000)
        gonderen_ad_soyad = self.benzersiz_ad_soyad_uret()
        gonderen_iban = self.benzersiz_iban_uret()
        hesap_turu = random.choice(HESAP_TURLERI)
        sifre_degisim_tarihi = islem_zamani - timedelta(days=random.randint(10, 365))
        alici_ad_soyad = self.benzersiz_ad_soyad_uret()
        alici_iban = self.benzersiz_iban_uret()
        alici_banka_kodu = f"BK_{random.randint(10, 99)}"
        miktar = random.randint(1_000, 80_000)
        para_birimi = "Türk Lirası (₺)"
        islem_turu = random.choice(["EFT", "HAVALE", "FAST"])
        aciklama = random.choice(["Ödeme", "Kira ödemesi", "Alışveriş", "Borç transferi"])
        konum = random.choice(TURKIYE_KONUMLARI)
        ip_adresi = fake.ipv4()
        cihaz_id = fake.uuid4()
        cihaz_turu = random.choice(CIHAZ_TURLERI)
        isletim_sistemi = random.randint(0, 18)

        # Her senaryo en az bir mevcut anomali_kontrol.py kuralını tetikler.
        if senaryo == "ASIRI_YUKSEK_TUTAR":
            miktar = random.randint(500_000, 10_000_000)

        elif senaryo == "GECE_YUKSEK_TUTAR":
            islem_zamani = islem_zamani.replace(
                hour=random.randint(2, 4), minute=random.randint(0, 59)
            )
            miktar = random.randint(200_000, 2_000_000)

        elif senaryo == "BIREYSEL_YURT_DISI_SWIFT":
            hesap_turu = "Bireysel"
            islem_turu = "SWIFT"
            konum = random.choice(YURT_DISI_KONUMLAR)
            miktar = random.randint(200_000, 5_000_000)
            para_birimi = random.choice(["ABD Doları ($)", "Euro (€)"])

        elif senaryo == "SUPHELI_ACIKLAMA":
            aciklama = random.choice(SUPHELI_ACIKLAMALAR)
            miktar = random.randint(20_000, 199_999)

        elif senaryo == "ARDISIK_HIZLI_TRANSFER":
            # Aynı gönderen kısa aralıklarla farklı alıcılara transfer yapar.
            if self._tekrar_gonderen is None:
                self._tekrar_gonderen = (
                    gonderen_id, gonderen_ad_soyad, gonderen_iban
                )
            gonderen_id, gonderen_ad_soyad, gonderen_iban = self._tekrar_gonderen
            if self._son_zaman is not None:
                islem_zamani = self._son_zaman + timedelta(seconds=random.randint(2, 20))
            self._son_zaman = islem_zamani
            miktar = random.randint(200_000, 700_000)
            aciklama = "ACİL"

        elif senaryo == "SIFRE_DEGISIMI_SONRASI_TRANSFER":
            # Şifre değişiminden dakikalar sonra çok büyük tutarlı işlem.
            sifre_degisim_tarihi = islem_zamani - timedelta(minutes=random.randint(1, 10))
            miktar = random.randint(300_000, 3_000_000)
            cihaz_id = fake.uuid4()

        yeni_transfer = Transfer(
            islem_id=self._benzersiz_islem_id_uret(),
            islem_zamani=islem_zamani,
            gonderen_id=gonderen_id,
            gonderen_ad_soyad=gonderen_ad_soyad,
            gonderen_iban=gonderen_iban,
            gonderen_hesap_turu=hesap_turu,
            gonderen_son_sifre_degisimi=sifre_degisim_tarihi,
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
            sehir=konum.city,
            ulke=konum.country,
            enlem=konum.lat,
            boylam=konum.lon,
        )
        # Eğitimde etiket olarak kullanılabilir; Transfer modelini değiştirmez.
        yeni_transfer.beklenen_anomali = 1
        yeni_transfer.uretim_senaryosu = senaryo
        if yazdir:
            yeni_transfer.yazdir()
            print("Üretim senaryosu:", senaryo)
        return yeni_transfer


if __name__ == "__main__":
    sim = Simulator()
    for _ in range(10):
        sim.fake_veriler_olustur()
