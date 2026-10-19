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
        isletim_sistemi,
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
        self.isletim_sistemi = isletim_sistemi
        self.sehir = sehir
        self.ulke = ulke
        self.enlem = enlem
        self.boylam = boylam

    def yazdir(self):
        """Transfer nesnesinin detaylarını terminale basar."""
        print(f"🆔 İşlem ID      : {self.islem_id} |  Zaman: {self.islem_zamani}")
        print(
            f"👤 Gönderen      : {self.gonderen_ad_soyad} (ID: {self.gonderen_id}) [{self.gonderen_hesap_turu}]"
        )
        print(f"💳 Gönderen IBAN : {self.gonderen_iban}")
        print(
            f"🎯 Alıcı         : {self.alici_ad_soyad} | Banka Kodu: {self.alici_banka_kodu}"
        )
        print(f"💳 Alıcı IBAN    : {self.alici_iban}")
        print(
            f"💰 Finansal      : {self.miktar} {self.para_birimi} | Tür: {self.islem_turu}"
        )
        print(
            f"📝 Açıklama      : {self.aciklama if self.aciklama else '(Açıklama Yok)'}"
        )
        print(
            f"🌐 Ağ & Cihaz    : IP: {self.ip_adresi} | ID: {self.cihaz_id} | {self.cihaz_turu} ({self.isletim_sistemi})"
        )
        print(
            f"📍 Konum         : {self.ulke}, {self.sehir} (Enlem: {self.enlem}, Boylam: {self.boylam})"
        )
        print("=" * 90)
