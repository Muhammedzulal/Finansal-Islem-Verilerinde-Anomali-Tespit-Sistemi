from csv_olustur import veri_uret, csv_kaydet


def main():
    islemler = veri_uret()
    csv_kaydet(islemler)
    print(
        f"Başarılı! CSV dosyası oluşturuldu ve toplam {len(islemler)} işlem kaydedildi."
    )


if __name__ == "__main__":
    main()
