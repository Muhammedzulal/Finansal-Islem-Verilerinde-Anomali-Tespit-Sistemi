# Simülatörün ürettiği Transfer nesnelerini basit kurallara göre kontrol eder
# ve her işleme iki etiket ekler:
#   is_anomaly   -> 0 (normal) / 1 (en az bir kurala takıldı)
#   anomali_turu -> takıldığı senaryolar, ör. "GECE_ISLEMI,YURT_DISI" (normalse boş)
from simulator_normal import Simulator
from transfer import Transfer

#!--------Eşik değerleri--------
YUKSEK_TUTAR_ESIGI = 200_000  # TL ve üzeri yüksek tutar sayılır
GECE_BASLANGIC = 2  # 02:00
GECE_BITIS = 5  # 05:00 (dahil değil)
EV_ULKESI = "Türkiye"
SUPHELI_ACIKLAMALAR = ["ACİL", "CRYPTO", "ÖNEMLİ ACİL BAKIYE", "TEST", "????", ""]


#!--------Senaryolar (Transfer alanlarına göre)--------
def yuksek_tutar_mi(transfer):
    # miktar alanı
    return transfer.miktar >= YUKSEK_TUTAR_ESIGI


def gece_islemi_mi(transfer):
    # islem_zamani alanı
    return GECE_BASLANGIC <= transfer.islem_zamani.hour < GECE_BITIS


def yurt_disi_mi(transfer):
    # ulke alanı
    return transfer.ulke != EV_ULKESI


def supheli_aciklama_mi(transfer):
    # aciklama alanı
    return transfer.aciklama.strip().upper() in SUPHELI_ACIKLAMALAR


def supheli_swift_mi(transfer):
    # islem_turu + gonderen_hesap_turu + ulke alanları
    return (
        transfer.islem_turu == "SWIFT"
        and transfer.gonderen_hesap_turu == "Bireysel"
        and transfer.ulke != EV_ULKESI
    )


# Senaryo adı -> kontrol fonksiyonu
SENARYOLAR = {
    "YUKSEK_TUTAR": yuksek_tutar_mi,
    "GECE_ISLEMI": gece_islemi_mi,
    "YURT_DISI": yurt_disi_mi,
    "SUPHELI_ACIKLAMA": supheli_aciklama_mi,
    "BIREYSEL_YURT_DISI_SWIFT": supheli_swift_mi,
}


#!--------Ana fonksiyon--------
def anomali_kontrol(transfer):
    """Transfer nesnesini kontrol eder, is_anomaly ve anomali_turu alanlarını ekler."""
    takilan = [ad for ad, kontrol in SENARYOLAR.items() if kontrol(transfer)]
    transfer.anomali_turu = ",".join(takilan)
    transfer.is_anomaly = 1 if takilan else 0
    return transfer


#!--------Deneme--------
if __name__ == "__main__":
    # Simülatör işlemleri sadece ekrana yazdırdığı için, yazdir() metodunu
    # geçici olarak "listeye ekle" yapıp üretilen Transfer nesnelerini topluyoruz.
    # (simulator.py ve transfer.py dosyalarına dokunulmuyor.)
    islemler = []
    Transfer.yazdir = lambda self: islemler.append(self)

    sim = Simulator()
    for i in range(0, 1000):
        sim.fake_veriler_olustur()

    for t in islemler:
        anomali_kontrol(t)

    #&------Özet----------
    anomali_sayisi = sum(t.is_anomaly for t in islemler)
    print(f"Toplam işlem       : {len(islemler)}")
    print(f"Anomali işaretlenen: {anomali_sayisi} (%{anomali_sayisi / len(islemler) * 100:.1f})")
    print("=" * 60)
    for ad in SENARYOLAR:
        sayi = sum(ad in t.anomali_turu.split(",") for t in islemler)
        print(f"{ad:<26}: {sayi}")
    print("=" * 60)
    print("Örnek işaretlenen işlemler:")
    for t in [t for t in islemler if t.is_anomaly][:5]:
        print(
            f"ID: {t.islem_id} | {t.islem_zamani:%Y-%m-%d %H:%M} | {t.miktar} | "
            f"{t.ulke} | '{t.aciklama}' -> {t.anomali_turu}"
        )
