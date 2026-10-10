class Transfer:
    def __init__(
        self,
        islem_id,
        islem_zamani,
        gonderen_id,
        gonderen_ad_soyad,
        gonderen_iban,
        gonderen_hesap_turu,
        alici_ad_soyad,
        alici_iban,
        alici_banka_kodu,
        miktar,
        para_birimi,
        islem_turu,
        aciklama,
        ip_adresi,
        cihaz_id,
        cihaz_turu,
        sehir,
        ulke,
        enlem,
        boylam,
    ):

        self.islem_id = islem_id
        self.islem_zamani = islem_zamani
        self.gonderen_id = gonderen_id
        self.gonderen_ad_soyad = gonderen_ad_soyad
        self.gonderen_iban = gonderen_iban
        self.gonderen_hesap_turu = gonderen_hesap_turu
        self.alici_ad_soyad = alici_ad_soyad
        self.alici_iban = alici_iban
        self.alici_banka_kodu = alici_banka_kodu
        self.miktar = miktar
        self.para_birimi = para_birimi
        self.islem_turu = islem_turu
        self.aciklama = aciklama
        self.ip_adresi = ip_adresi
        self.cihaz_id = cihaz_id
        self.cihaz_turu = cihaz_turu
        self.sehir = sehir
        self.ulke = ulke
        self.enlem = enlem
        self.boylam = boylam
