"""Normal ve anomali transferlerini olasılıksal (rastgele) olarak tek CSV dosyasında birleştirir."""

import csv
import io
import random
from contextlib import redirect_stdout
from pathlib import Path

# Artık tüm işlemleri tek simülatörden çekiyoruz
from anomali_uretec import AnomaliSimulator

DONGU_SAYISI = 10000  # Üretilecek temel işlem/olay döngüsü
CSV_DOSYASI = Path(__file__).resolve().parent / "banka_islemleri.csv"

ALANLAR = [
    "islem_id",
    "islem_zamani",
    "gonderen_id",
    "gonderen_ad_soyad",
    "gonderen_iban",
    "gonderen_hesap_turu",
    "gonderen_son_sifre_degisimi",
    "alici_ad_soyad",
    "alici_iban",
    "alici_banka_kodu",
    "miktar",
    "para_birimi",
    "islem_turu",
    "aciklama",
    "ip_adresi",
    "cihaz_id",
    "cihaz_turu",
    "isletim_sistemi",
    "sehir",
    "ulke",
    "enlem",
    "boylam",
]
CSV_ALANLARI = ALANLAR + ["is_anomaly", "uretim_senaryosu"]


def veri_uret():
    sim = AnomaliSimulator()
    islemler = []

    anomali_sayaci = 0
    normal_sayaci = 0

    for _ in range(DONGU_SAYISI):
        # 1-100 arası zar atıyoruz (Gerçek dünyadaki gibi %2 anomali ihtimali)
        zar = random.randint(1, 100)

        # Simülatör içindeki print() komutlarının konsolu dondurmasını engelliyoruz
        with redirect_stdout(io.StringIO()):

            # Eğer zar 99 veya 100 gelirse (Yaklaşık %2 ihtimal) Anomali üret
            if zar >= 99:
                secilen_anomali = random.choice(["sifre", "structuring"])
                sim.anomali_turu = secilen_anomali
                sonuc = sim.fake_veriler_olustur()

                if secilen_anomali == "structuring":
                    # Structuring bir liste döner, içindeki her işlemi CSV'ye ekliyoruz
                    for transfer in sonuc:
                        islemler.append((transfer, 1, secilen_anomali.upper()))
                        anomali_sayaci += 1
                else:
                    # Şifre değişimi anomalisi tek bir nesne döner
                    islemler.append((sonuc, 1, secilen_anomali.upper()))
                    anomali_sayaci += 1

            # Geri kalan durumlarda (%98 ihtimal) Normal işlem üret
            else:
                sim.anomali_turu = None  # Anomali yok
                sonuc = sim.fake_veriler_olustur()
                islemler.append((sonuc, 0, "NORMAL"))
                normal_sayaci += 1

    # Structuring çoklu veri eklediği veya aynı anlarda üretildiği için ID çakışmaları olabilir
    # Çakışmaları engellemek için yeniden numaralandırıyoruz
    kullanilan_idler = set()
    for transfer, _, _ in islemler:
        if transfer.islem_id in kullanilan_idler:
            yeni_id = random.randint(1, 2_147_483_647)
            while yeni_id in kullanilan_idler:
                yeni_id = random.randint(1, 2_147_483_647)
            transfer.islem_id = yeni_id
        kullanilan_idler.add(transfer.islem_id)

    # Verileri kronolojik çakışma gibi görünmesin diye karıştırıyoruz
    random.shuffle(islemler)

    # Oranları Konsola Bilgi Olarak Ver
    toplam_islem = len(islemler)
    anomali_orani = (anomali_sayaci / toplam_islem) * 100
    print(f"Toplam Üretilen İşlem: {toplam_islem}")
    print(f"Normal İşlem: {normal_sayaci} | Anormal İşlem: {anomali_sayaci}")
    print(f"Gerçekleşen Anomali Oranı: %{anomali_orani:.2f}")

    return islemler


def csv_kaydet(islemler):
    with CSV_DOSYASI.open("w", newline="", encoding="utf-8-sig") as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=CSV_ALANLARI)
        yazici.writeheader()
        for transfer, etiket, senaryo in islemler:
            satir = {alan: getattr(transfer, alan) for alan in ALANLAR}
            satir["is_anomaly"] = etiket
            satir["uretim_senaryosu"] = senaryo
            yazici.writerow(satir)
