"""Normal ve anomalili banka işlemlerini üretip CSV'ye kaydeder."""

from csv_olustur import veri_uret, csv_kaydet


def main():
    islemler = veri_uret()
    csv_kaydet(islemler)
    print(f"CSV oluşturuldu: {len(islemler)} işlem kaydedildi.")


if __name__ == "__main__":
    main()
