# Math ve Random kütüphaneleri import ediliyor
import math
import random

# 'a' ve 'b' arasında rastgele bir sayı döndüren bir fonksiyon tanımlanıyor
def rasgele(a, b):
    return (b-a)*random.random() + a

# Verilen boyutta ve dolgu değeri ile bir matris oluşturan bir fonksiyon tanımlanıyor
def matrisOlustur(I, J, fill=0.0):
    return [[fill]*J for _ in range(I)]

# Sigmoid aktivasyon fonksiyonu tanımlanıyor
def sigmoid(x):
    return math.tanh(x)

# Sigmoid fonksiyonunun türevi tanımlanıyor
def dsigmoid(y):
    return 1.0 - y**2

# Yapay Sinir Ağı (YSA) sınıfı tanımlanıyor
class YSA:
    # YSA başlatılıyor ve parametreler belirleniyor
    def __init__(self, gi, ga, co):
        self.gi, self.ga, self.co = gi + 1, ga, co
        self.giris, self.gizli, self.cikis = [1.0]*self.gi, [1.0]*self.ga, [1.0]*self.co
        
        # Ağırlıklar rastgele oluşturuluyor
        self.wgiris, self.wcikis = self.randomize_weights(self.gi, self.ga, -0.2, 0.2), self.randomize_weights(self.ga, self.co, -2.0, 2.0)
        
        # Değişiklikler için boş matrisler oluşturuluyor
        self.cgiris, self.ccikis = matrisOlustur(self.gi, self.ga), matrisOlustur(self.ga, self.co)

    # Rastgele ağırlıklar oluşturan bir fonksiyon tanımlanıyor
    def randomize_weights(self, n1, n2, low, high):
        matrix = matrisOlustur(n1, n2)
        for i in range(n1):
            for j in range(n2):
                matrix[i][j] = rasgele(low, high)
        return matrix

    # Giriş değerleri alınıyor ve çıkış hesaplanıyor
    def guncelle(self, girisler):
        if len(girisler) != self.gi - 1:
            raise ValueError('yanlış giris sayısı')

        self.giris[:self.gi-1] = girisler[:self.gi-1]

        # Gizli ve çıkış katmanındaki değerler hesaplanıyor
        self.gizli = [sigmoid(sum(self.giris[i] * self.wgiris[i][j] for i in range(self.gi))) for j in range(self.ga)]
        # Çıkış katmanındaki değerler sigmoid aktivasyon fonksiyonuna göre hesaplanıyor
                # Çıkış katmanındaki değerler sigmoid aktivasyon fonksiyonuna göre hesaplanıyor
        self.cikis = [sigmoid(sum(self.gizli[j] * self.wcikis[j][k] for j in range(self.ga))) for k in range(self.co)]
        
        # Hesaplanan çıkış değerleri döndürülüyor
        return self.cikis[:]

    # Geriye yayılım algoritması (backpropagation) tanımlanıyor
    def geriYayilim(self, hedefler, N, M):
        if len(hedefler) != self.co:
            raise ValueError('yanlış hedef değer sayısı')

        # Hedef ve çıkış arasındaki hata, çıkış katmanındaki nöronlar için hesaplanıyor
        cikis_deltas = [dsigmoid(self.cikis[k]) * (hedefler[k] - self.cikis[k]) for k in range(self.co)]
        
        # Hata, gizli katmandaki nöronlar için hesaplanıyor
        gizli_deltas = [dsigmoid(self.gizli[j]) * sum(cikis_deltas[k] * self.wcikis[j][k] for k in range(self.co)) for j in range(self.ga)]

        # Çıkış katmanındaki ağırlıklar güncelleniyor
        for j in range(self.ga):
            for k in range(self.co):
                degisim = cikis_deltas[k] * self.gizli[j]
                self.wcikis[j][k] += N * degisim + M * self.ccikis[j][k]
                self.ccikis[j][k] = degisim

        # Gizli katmandaki ağırlıklar güncelleniyor
        for i in range(self.gi):
            for j in range(self.ga):
                degisim = gizli_deltas[j] * self.giris[i]
                self.wgiris[i][j] += N * degisim + M * self.cgiris[i][j]
                self.cgiris[i][j] = degisim

        # Hata hesaplanıyor ve döndürülüyor
        hata = sum(0.5 * (hedefler[k] - self.cikis[k]) ** 2 for k in range(len(hedefler)))
        return hata

    # Test verisi ile ağın nasıl performans gösterdiğini kontrol etme fonksiyonu
    def test(self, ornekler):
        print("\n---------- Performans kontrol ----------")
        for p in ornekler:
            print(f"{p[0]} -----> {self.guncelle(p[0])}")
        print("----------------------------------------")

    # Eğitim fonksiyonu, belirli sayıda iterasyon ve belirli öğrenme hızları ile gerçekleşiyor
    def egit(self, ornekler, iterasyonlar=5000, N=0.5, M=0.2):
        print("\n---------- Hata Oranları ----------")
        for i in range(iterasyonlar):
            hata = 0.0
            for p in ornekler:
                girisler = p[0]
                hedefler = p[1]
                self.guncelle(girisler)
                hata = hata + self.geriYayilim(hedefler, N, M)
            if i % 500 == 0:
                print('Hata Oranı: %-.5f' % hata)

# Burada, bir demo fonksiyonu tanımlanıyor. Bu, YSA'nın XOR işlevini öğrenme yeteneğini gösterir.
def calistir():
    # XOR eğitim örnekleri
    ornekler = [[[0,0], [0]],[[0,1], [1]],[[1,0], [1]],[[1,1], [0]]]

    # YSA nesnesi oluşturuluyor
    n = YSA(2, 2, 1)
    
    # Ağ, eğitim örnekleri ile eğitiliyor
    n.egit(ornekler)
    
    # Eğitim sonrasında, ağın örnekler üzerinde nasıl performans gösterdiği test ediliyor
    n.test(ornekler)
    
# Bu Python dosyası doğrudan çalıştırılırsa, demo fonksiyonu çağrılır.

if __name__ == "__main__":
    calistir()