# ana sınıf
from simulator import Simulator
import time
import random

if __name__ == "__main__":
    sim = Simulator()
    baslangic = time.time()

    for i in range(0, 100_000):
        nesne = sim.fake_veriler_olustur()
        print(nesne.gonderen_ad_soyad)
        # bekleme_saniyesi = random.uniform(0.001, 0.007)
        # time.sleep(bekleme_saniyesi)
    bitis = time.time()
    print(f"{bitis-baslangic:.2f} sn geçti toplam {i+1} adet veri transferi oldu")
