"""Normal ve anomalili banka işlemlerini üretip CSV'ye kaydeder."""

from csv_olustur import veri_uret, csv_kaydet
from anomali_uretec import AnomaliSimulator


def main():
    """islemler = veri_uret()
    csv_kaydet(islemler)
    print(f"CSV oluşturuldu: {len(islemler)} işlem kaydedildi.")
    sim = AnomaliSimulator("sifre")
    for i in range(0, 10):
        sim.fake_veriler_olustur()"""


if __name__ == "__main__":
    main()
