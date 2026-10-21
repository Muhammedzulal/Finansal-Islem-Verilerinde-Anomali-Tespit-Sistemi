"""Normal ve anomali transferlerini tek CSV dosyasında birleştirir."""

import csv
import io
import random
from contextlib import redirect_stdout
from pathlib import Path

from simulator_normal import Simulator as NormalSimulator
from simulator_anomali import Simulator as AnomaliSimulator, SENARYO_AGIRLIKLARI

# 100:5 dağılımı ölçeklendi: 10.000 işlem, yaklaşık %95,24 / %4,76.
NORMAL_ADET = 9524
ANOMALI_ADET = 476
CSV_DOSYASI = Path(__file__).resolve().parent / "banka_islemleri.csv"

ALANLAR = [
    "islem_id", "islem_zamani", "gonderen_id", "gonderen_ad_soyad",
    "gonderen_iban", "gonderen_hesap_turu", "gonderen_son_sifre_degisimi",
    "alici_ad_soyad", "alici_iban", "alici_banka_kodu", "miktar",
    "para_birimi", "islem_turu", "aciklama", "ip_adresi", "cihaz_id",
    "cihaz_turu", "isletim_sistemi", "sehir", "ulke", "enlem", "boylam",
]
CSV_ALANLARI = ALANLAR + ["is_anomaly", "uretim_senaryosu"]


def veri_uret():
    normal_sim = NormalSimulator()
    anomali_sim = AnomaliSimulator()
    islemler = []

    for _ in range(NORMAL_ADET):
        # Eski normal simülatör her işlemde yazdırıyor; CSV üretirken çıktıyı gizle.
        with redirect_stdout(io.StringIO()):
            transfer = normal_sim.fake_veriler_olustur()
        islemler.append((transfer, 0, "NORMAL"))

    # Altı senaryonun hepsinden en az bir örnek: ağırlıklara göre kesin adetler.
    agirlik_toplami = sum(SENARYO_AGIRLIKLARI.values())
    hedefler = {ad: ANOMALI_ADET * agirlik / agirlik_toplami
               for ad, agirlik in SENARYO_AGIRLIKLARI.items()}
    adetler = {ad: int(deger) for ad, deger in hedefler.items()}
    kalan = ANOMALI_ADET - sum(adetler.values())
    for ad in sorted(hedefler, key=lambda x: hedefler[x] - adetler[x], reverse=True)[:kalan]:
        adetler[ad] += 1
    if any(adet < 1 for adet in adetler.values()):
        raise ValueError("Her anomali türünden en az bir işlem üretilmeli.")

    for senaryo, adet in adetler.items():
        for _ in range(adet):
            transfer = anomali_sim.fake_veriler_olustur(yazdir=False, senaryo=senaryo)
            islemler.append((transfer, 1, transfer.uretim_senaryosu))

    # Ayrı simülatörlerin oluşturduğu ID'ler çakışırsa yeniden numaralandır.
    kullanilan_idler = set()
    for transfer, _, _ in islemler:
        if transfer.islem_id in kullanilan_idler:
            yeni_id = random.randint(1, 2_147_483_647)
            while yeni_id in kullanilan_idler:
                yeni_id = random.randint(1, 2_147_483_647)
            transfer.islem_id = yeni_id
        kullanilan_idler.add(transfer.islem_id)

    random.shuffle(islemler)
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


if __name__ == "__main__":
    islemler = veri_uret()
    csv_kaydet(islemler)
    toplam = len(islemler)
    print(f"CSV oluşturuldu: {CSV_DOSYASI}")
    print(f"Toplam: {toplam} | Normal: {NORMAL_ADET} | Anomali: {ANOMALI_ADET}")
    print(f"Anomali oranı: %{ANOMALI_ADET / toplam * 100:.2f}")
