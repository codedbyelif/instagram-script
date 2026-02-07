# Instagram Multi-Tool - Detaylı Kullanım Kılavuzu

Bu script, Instagram hesapları üzerinde otomatize edilmiş işlemleri gerçekleştirmek, hesap bilgilerini analiz etmek ve çeşitli oturum yönetimi görevlerini yerine getirmek için tasarlanmış kapsamlı bir araçtır. Özellikle hesap güvenliği testleri ve oturum yönetimiyle ilgilenen kullanıcılar için güçlü özellikler sunar.

> **ÖNEMLİ YASAL UYARI:**  
> Bu yazılım yalnızca **eğitim, araştırma ve güvenlik testleri** amacıyla geliştirilmiştir. Başkalarına ait hesaplar üzerinde izinsiz işlem yapmak, taciz etmek veya Instagram Hizmet Koşullarını ihlal etmek suç teşkil edebilir. Yazılımın kötüye kullanımından doğacak tüm yasal sorumluluk kullanıcıya aittir.

---

## Kurulum ve Hazırlık

Bu aracı sorunsuz çalıştırmak için aşağıdaki adımları takip edin.

### 1. Gereksinimler
Bilgisayarınızda **Python 3.x** sürümünün yüklü olması gerekmektedir.
- **Python İndir:** [python.org/downloads](https://www.python.org/downloads/)

### 2. Kütüphane Kurulumu
Script, internet üzerinden veri alışverişi yaptığı için `requests` kütüphanesine ihtiyaç duyar. Terminal veya komut satırını açıp şu komutu çalıştırın:

```bash
pip install requests
```

### 3. Çalıştırma
Terminale aşağıdaki komutu yazarak aracı başlatabilirsiniz:

```bash
python script.py
```

---

## Menü ve Özelliklerin Detaylı Açıklaması

Script çalıştırıldığında ana menü üzerinden numaralarla işlem seçebilirsiniz. İşte her bir özelliğin ne işe yaradığı ve nasıl kullanılacağı:

### Oturum (Session) İşlemleri

Bu bölüm, Instagram'a giriş yapmanızı ve oturum bilgilerinizi (Session ID) almanızı sağlar.

#### **1. GET SESSION (CODE)**
*   **Ne İşe Yarar?** Kullanıcı adı ve şifrenizle giriş yaparak size **Session ID** (Oturum Kimliği) verir. 
*   **Nasıl Çalışır?** 
    1. Kullanıcı adı ve şifrenizi girersiniz.
    2. Eğer hesabınızda İki Faktörlü Doğrulama (2FA) varsa, size SMS veya E-posta kodunu sorar.
    3. Başarılı girişte size `sessionid` ve `mid` gibi değerleri verir. Bu değerleri kopyalayıp saklayın, diğer işlemlerde lazım olacaktır.

#### **2. GET SESSION (ACCEPTIION)**
*   **Ne İşe Yarar?** Normal giriş yöntemlerinin takıldığı durumlarda (örneğin "Şüpheli Giriş Denemesi"), alternatif bir mobil cihaz simülasyonu ile giriş yapmayı dener.
*   **Kullanım:** "Checkpoint" hatası alan hesaplar için önerilir.

#### **4. CONVERT SESSION (WEB TO API)**
*   **Ne İşe Yarar?** Tarayıcıdan (Chrome, Firefox vb.) aldığınız oturum bilgisini, bu scriptin (Mobil API'nin) anlayacağı formata çevirir.
*   **Neden Gerekli?** Bazı işlemler (ör. İsim Değiştirme) sadece mobil uygulama üzerinden yapılabilir gibi davranır. Web oturumunuzu bu formata çevirmezseniz o işlemler çalışmayabilir.

#### **5. CONVERT SESSION (WEB TO API VIA MID)**
*   **Ne İşe Yarar?** Session ID'nize ek olarak `MID` (Machine ID) değerini de kullanarak daha kararlı bir oturum dönüşümü sağlar.

#### **6. ACCEPT TERMS (Kullanım Koşullarını Kabul Et)**
*   **Ne İşe Yarar?** Uzun süre girilmeyen veya politika değişikliği sonrası giriş yapılan hesaplarda çıkan "Kullanım Koşullarını Kabul Et" ekranını otomatik olarak geçer.
*   **Kullanım:** Hesaba giriyorsunuz ama ekranda hiçbir şey yapamıyorsanız bu seçeneği deneyin. Hesabın kilidini açabilir.

---

### Hesap Yönetimi (Account Management)

Hesap üzerindeki bilgileri görme ve değiştirme işlemleridir.

#### **7. REMOVING FORMER USERS (Eski Kullanıcı İzlerini Silme)**
*   **Ne İşe Yarar?** Hesabın profil fotoğrafını art arda (4-5 kez) değiştirerek Instagram önbelleğindeki "Eski Kullanıcı" bilgilerini temizlemeyi amaçlar. Bu işlem genellikle hesabın önceki sahipleriyle olan bağını (önerilenlerde çıkma vb.) koparmak için kullanılır.
*   **Dikkat:** İşleme başlamadan önce mevcut profil fotoğrafınızı kaldırın. İşlem sırasında rastgele profil fotoğrafları yüklenecektir.

#### **8. GET ACCOUNT INFO (Hesap Bilgisi Sorgulama)**
*   **Ne İşe Yarar?** Elinizdeki Session ID'nin hangi hesaba ait olduğunu ve detaylarını gösterir.
*   **Hangi Bilgileri Verir?**
    - Kullanıcı Adı, Tam İsim, Kullanıcı ID (PK)
    - E-posta Adresi ve Telefon Numarası
    - Takipçi ve Takip Edilen Sayıları
    - Hesap Türü (Gizli, Onaylı, İşletme vb.)

#### **9. CHANGE NAME (İsim Değiştirme)**
*   **Ne İşe Yarar?** Hesabın "Ad Soyad" (Name) kısmını değiştirir. 
*   **Seçenekler:**
    1.  **Set a new name:** Yeni bir isim belirlersiniz.
    2.  **Remove current name:** Mevcut ismi siler.
    3.  **Change multiple names (Toplu Değişim):** Birden fazla isim girersiniz ve script bunları sırayla dener. (Örn: İsim alma denemeleri için).

#### **10. CHANGE BIO (Biyografi Değiştirme)**
*   **Ne İşe Yarar?** Hesabın biyografi kısmını hızlıca günceller.
*   **Kullanım:** Session ID ve yeni biyografi metnini girmeniz yeterlidir.

---

### Şifre ve Güvenlik (Password Reset)

Şifre sıfırlama işlemleri için kullanılır.

#### **13. RESET PW (INACTIVE ACC - Pasif Hesaplar)**
*   **Ne İşe Yarar?** Uzun süredir kullanılmayan veya erişimi kaybedilen hesaplar için "Kurtarma E-postası" göndermeyi dener.
*   **Kullanım:** Sadece kullanıcı adını girersiniz. Script, Instagram'ın kurtarma API'sine istek atar.

#### **14. RESET PW (ACTIVE ACC - Aktif Hesaplar)**
*   **Ne İşe Yarar?** Aktif kullanılan bir hesap için şifre sıfırlama bağlantısı gönderir.
*   **Kullanım:** Kullanıcı adı veya e-posta adresi ile çalışır. Başarılı olursa kayıtlı e-postaya Instagram'dan link gider.

---

### Diğer Araçlar (Other Tools)

#### **15. SKIPPING DISMISS (Otomasyon Uyarısını Geç)**
*   **Ne İşe Yarar?** Instagram'da bazen "Otomatik davranış tespit edildi" uyarısı çıkar ve ekranı kilitler. Bu araç, o uyarıyı "Tamam" diyip geçmek yerine API üzerinden "Görmezden Gel" (Dismiss) sinyali göndererek kilidi açmaya çalışır.

#### **16. SESSIONS VALIDATOR (Oturum Kontrolcü)**
*   **Ne İşe Yarar?** Elinizdeki Session ID'lerin hala çalışıp çalışmadığını (Patlayıp patlamadığını) kontrol eder.
*   **Seçenekler:**
    - **Single Session:** Tek bir ID yapıştırıp kontrol edersiniz.
    - **Multi Sessions (Dosyadan):** Bir `.txt` dosyası içindeki yüzlerce Session ID'yi tek seferde tarar.
*   **Dosya Formatı:** Dosyanızda her satırda bir Session ID olmalıdır.
*   **Çıktı Dosyaları:** İşlem bitince çalışanları `valid_sessions_[tarih].txt`, çalışmayanları `invalid_sessions_[tarih].txt` dosyasına kaydeder.

#### **17. RANDOM USER,PASS,MAIL (Rastgele Veri Oluşturucu)**
*   **Ne İşe Yarar?** Yeni hesap açarken kullanabileceğiniz rastgele (random) bilgiler üretir.
*   **Neleri Oluşturur?**
    - Benzersiz bir Kullanıcı Adı
    - Güçlü bir Şifre
    - Geçici bir Gmail adresi (Format olarak, gerçek değil)
*   **Çıktı:** Oluşturulan bilgileri `generated_data_[tarih].txt` dosyasına kaydeder.

---

## Sorun Giderme (Sıkça Sorulan Sorular)

**S: "Session ID is valid" diyor ama işlem yapamıyorum.**
**C:** Oturumunuz "Web" oturumu olabilir. Menüden **4. CONVERT SESSION** seçeneğini kullanarak onu mobil API formatına çevirmeyi deneyin.

**S: "Checkpoint Required" hatası alıyorum.**
**C:** Instagram hesabınızda olağandışı bir giriş fark etti. Tarayıcıdan veya uygulamadan girip "Bendim" onayı vermeniz veya şifrenizi değiştirmeniz gerekebilir.

**S: Toplu işlem yaparken hata alıyorum.**
**C:** Instagram seri işlemlere (spam) karşı önlem alır. İşlemler arasında en az 30-60 saniye beklemek veya VPN/Proxy kullanmak gerekebilir.

**S: "Module not found: requests" hatası.**
**C:** `pip install requests` komutunu çalıştırmamışsınız. Lütfen "Kurulum" adımına dönün.

---

## Dosya Yapısı ve Çıktılar

Script çalışırken oluşturduğu dosyalar şunlardır:
- `script.py`: Ana program dosyası.
- `valid_sessions_YYYYMMDD.txt`: Çalışan oturumların kaydedildiği dosya.
- `invalid_sessions_YYYYMMDD.txt`: Bozuk oturumların kaydedildiği dosya.
- `generated_data_YYYYMMDD.txt`: Rastgele oluşturulan kullanıcı bilgilerini içeren dosya.
