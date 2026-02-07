# Instagram Multi-Tool

[Türkçe](#türkçe-kullanım-kılavuzu) | [English](#english-usage-guide)

---

<br>

## Türkçe Kullanım Kılavuzu

Bu script, Instagram hesapları üzerinde otomatize edilmiş işlemleri gerçekleştirmek, hesap bilgilerini analiz etmek ve çeşitli oturum yönetimi görevlerini yerine getirmek için tasarlanmış kapsamlı bir araçtır.

> **ÖNEMLİ YASAL UYARI:**  
> Bu yazılım yalnızca **eğitim, araştırma ve güvenlik testleri** amacıyla geliştirilmiştir. Başkalarına ait hesaplar üzerinde izinsiz işlem yapmak suç teşkil edebilir. Sorumluluk kullanıcıya aittir.

### Kurulum ve Hazırlık

**1. Gereksinimler**
- Python 3.x yüklü olmalıdır.

**2. Kütüphane Kurulumu**
Terminalde şu komutu çalıştırın:
```bash
python3 -m pip install requests
```

**3. Çalıştırma**
Scripti başlatmak için:
```bash
python3 script.py
```

### Menü ve Özellikler

Script çalıştırıldığında aşağıdaki menü açılır. İşte özellikleri:

#### Oturum (Session) İşlemleri
*   **1. GET SESSION (CODE):** Kullanıcı adı/şifre ile giriş yapıp Session ID alır. 2FA varsa kod ister.
*   **2. GET SESSION (ACCEPTIION):** Checkpoint (doğrulama) takılan hesaplar için alternatif giriş yöntemi.
*   **4. CONVERT SESSION (WEB TO API):** Web tarayıcısı oturumunu Mobil API uyumlu oturuma çevirir.
*   **5. CONVERT SESSION (WEB TO API VIA MID):** Web oturumunu Machine ID (MID) kullanarak API'ye çevirir.
*   **6. ACCEPT TERMS:** "Kullanım Koşullarını Kabul Et" ekranında takılan hesapları kurtarır.

#### Hesap Yönetimi
*   **7. REMOVING FORMER USERS:** Profil fotoğrafını sürekli değiştirerek hesap geçmişini/önbelleğini temizler.
*   **8. GET ACCOUNT INFO:** Session ID girilen hesabın tüm bilgilerini (mail, tel, takipçi vb.) gösterir.
*   **9. CHANGE NAME:** İsim değiştirir. Toplu isim değiştirme özelliği de vardır.
*   **10. CHANGE BIO:** Biyografiyi hızlıca değiştirir.

#### Şifre ve Güvenlik
*   **13. RESET PW (INACTIVE ACC):** Pasif hesaplara şifre sıfırlama maili gönderir.
*   **14. RESET PW (ACTIVE ACC):** Aktif hesaplara şifre sıfırlama linki gönderir.

#### Diğer Araçlar
*   **15. SKIPPING DISMISS:** "Otomatik davranış tespit edildi" uyarısını API üzerinden geçmeye çalışır.
*   **16. SESSIONS VALIDATOR:** Elinizdeki Session ID'lerin çalışıp çalışmadığını kontrol eder (Tekli veya Dosyadan toplu).
*   **17. RANDOM USER,PASS,MAIL:** Rastgele kullanıcı adı, şifre ve mail oluşturur.

---

### Türkçe Çıktı Açıklaması (Detaylı)

Script çalıştığında gördüğünüz menü maddelerinin ne anlama geldiğini aşağıda bulabilirsiniz:

**SESSION TOOLS (Oturum Araçları):**
Bu bölüm, Instagram hesabınıza giriş yapmanızı veya elinizdeki oturum bilgilerini dönüştürmenizi sağlar.
*   **GET SESSION (CODE):** Normal giriş yöntemidir. Kullanıcı adı ve şifrenizi girersiniz, sistem size bir "Session ID" verir. Bu ID, diğer araçları kullanmak için gereklidir.
*   **GET SESSION (ACCEPTIION):** Giriş yaparken sorun yaşıyorsanız (örneğin doğrulama ekranında kalıyorsanız) bu seçeneği deneyin. Farklı bir protokol kullanarak giriş yapmaya çalışır.
*   **CONVERT SESSION:** Eğer tarayıcıdan (Chrome vb.) aldığınız bir oturum kodunuz varsa, bu araç onu mobil uygulama formatına çevirir. Böylece scriptin diğer özellikleri daha stabil çalışır.
*   **ACCEPT TERMS:** Bazen hesaplara girildiğinde "Koşulları Kabul Et" butonu çıkmaz ve ekran kilitlenir. Bu araç, o onayı otomatik verip hesabın açılmasını sağlar.

**ACCOUNT MANAGEMENT (Hesap Yönetimi):**
Hesabın özelliklerini değiştirmek veya bilgi almak için kullanılır.
*   **REMOVING FORMER USERS:** Hesabın "eski sahibi" izlerini silmek için kullanılır. Arka arkaya profil fotoğrafı değiştirerek Instagram önbelleğini temizlemeye yarar.
*   **GET ACCOUNT INFO:** Bir Session ID girdiğinizde, o hesabın tüm detaylarını (gizli mi, telefon numarası ne, mail adresi ne vb.) listeler.
*   **CHANGE NAME / BIO:** İsim ve biyografi değiştirmek için kullanılır. Özellikle kilitlenmiş veya isim değiştirme hakkı dolmuş hesaplarda denenebilir.

**PASSWORD RESET (Şifre Sıfırlama):**
*   **INACTIVE ACC:** Uzun süredir girilmeyen hesaplara şifre sıfırlama postası atar.
*   **ACTIVE ACC:** Halen kullanılan hesaplara şifre sıfırlama bağlantısı gönderir.

**OTHER TOOLS (Diğer Araçlar):**
*   **SKIPPING DISMISS:** Hesabınızda "Otomasyon tespit edildi" uyarısı çıkıyorsa, bu araç o uyarıyı geçmenizi sağlar.
*   **SESSIONS VALIDATOR:** Elinizde yüzlerce hesap (Session ID) varsa, hangilerinin çalışıp hangilerinin patladığını (login olamadığını) tek tek kontrol eder ve ayırır.
*   **RANDOM USER,PASS,MAIL:** Yeni hesap açmak isterseniz, sizin için rastgele kullanıcı adı ve şifre üretir.

---

<br>

## English Usage Guide

This is a comprehensive tool designed to perform automated tasks on Instagram accounts, analyze account information, and handle various session management tasks.

> **IMPORTANT DISCLAIMER:**  
> This software is developed for **educational, research, and security testing** purposes only. Unauthorized actions on others' accounts may be illegal. The user is solely responsible.

### Installation & Setup

**1. Requirements**
- Python 3.x must be installed.

**2. Install Dependencies**
Run this command in your terminal:
```bash
python3 -m pip install requests
```

**3. Run the Script**
Start the tool with:
```bash
python3 script.py
```

### Menu & Features Explained

When you run the script, you will see the menu below. Here is what each option does:

#### Session Tools
*   **1. GET SESSION (CODE):** Log in with username/password to get the Session ID. Supports 2FA.
*   **2. GET SESSION (ACCEPTIION):** Alternative login method for accounts stuck at checkpoint/verification.
*   **4. CONVERT SESSION (WEB TO API):** Converts a Web Browser session to a Mobile API compatible session.
*   **5. CONVERT SESSION (WEB TO API VIA MID):** Converts Web session to API using Machine ID (MID).
*   **6. ACCEPT TERMS:** Automatically accepts "Terms of Service" for accounts stuck on that screen.

#### Account Management
*   **7. REMOVING FORMER USERS:** Repeatedly changes profile picture to clear account cache/history traces.
*   **8. GET ACCOUNT INFO:** Displays full details (email, phone, followers etc.) for a given Session ID.
*   **9. CHANGE NAME:** Changes the account name. Supports bulk name changing.
*   **10. CHANGE BIO:** Quickly updates the account biography.

#### Password & Security
*   **13. RESET PW (INACTIVE ACC):** Attempts to send password reset email to inactive accounts.
*   **14. RESET PW (ACTIVE ACC):** Sends password reset link to active accounts.

#### Other Tools
*   **15. SKIPPING DISMISS:** Attempts to bypass the "Automated behavior detected" warning via API.
*   **16. SESSIONS VALIDATOR:** Checks if Session IDs are valid or expired (Single or Bulk from file).
*   **17. RANDOM USER,PASS,MAIL:** Generates random username, password, and email.

---

### Script Output (Menu Preview)

The actual output when running the tool:

```text
======================================================================
INSTAGRAM MULTI-TOOL V3.01
 By: @suul community team
======================================================================

SESSION TOOLS:
 1. GET SESSION (CODE)
 2. GET SESSION (ACCEPTIION)
 4. CONVERT SESSION (WEB TO API)
 5. CONVERT SESSION (WEB TO API VIA MID)
 6. ACCEPT TERMS

ACCOUNT MANAGEMENT:
 7. REMOVING FORMER USERS
 8. GET ACCOUNT INFO
 9. CHANGE NAME
10. CHANGE BIO

PASSWORD RESET:
13. RESET PW (INACTIVE ACC)
14. RESET PW (ACTIVE ACC)

OTHER TOOLS:
15. SKIPPING DISMISS
16. SESSIONS VALIDATOR
17. RANDOM USER,PASS,MAIL

 0. EXIT
======================================================================
```
