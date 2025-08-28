# Flask-Terraform AiWebSite Deployment Platformu

## 1. Ürün Tanımı

Bu proje, kullanıcıların tek tuş ile web sitesi oluşturmasını ve yayınlamasını sağlayan bir platformdur. Flask tabanlı web uygulaması üzerinden üç farklı yöntemle site üretilebilir:

- Prompt + Görselden Web Sitesi Üretme
- Sadece Prompt’tan Web Sitesi Üretme
- Mevcut GitHub Linkinden Web Sitesi Alma

Oluşturulan siteler platformun yan tarafında desktop, tablet ve mobil cihazlar için preview olarak görüntülenir. Kullanıcı “Deploy AI Site” butonu ile siteyi canlıya alabilir.

---

## 2. Kullanılan Teknolojiler

- Python / Flask: Web uygulamasının temel framework’ü, API ve UI işlemleri için.
- Docker: Uygulamanın containerize edilmesi ve ortam bağımsız çalışması için.
- Terraform: Kullanıcının deploy tuşuna bastığında otomatik olarak VM oluşturulması ve Apache ile site yayınlanması için.
- Azure App Services: Flask uygulamasının barındırıldığı ana ortam.
- Apache: VM üzerinde HTML siteyi serve etmek için.
- GitHub: Oluşturulan sitelerin depolanması ve pull işlemleri için.
- Bash (.sh script): VM içinde Apache kurulumunu, site indirmeyi ve yayına almayı otomatikleştiren script.
- Environment Variables: API anahtarları, GitHub tokenleri ve Terraform Service Principal bilgileri güvenli şekilde saklanır.

---

## 3. Çalışma Mantığı

### 3.1 Flask Uygulaması

Kullanıcı web arayüzünden site oluşturma yöntemini seçer.

Oluşturulan site, platformda ön izleme olarak gösterilir.

Kullanıcı “Deploy AI Site” butonuna bastığında Terraform pipeline tetiklenir.

### 3.2 Terraform & Bash Script

Terraform deploy süreci sadece user tarafından tetiklendiğinde çalışır. Ve site için şu şekilde bir mimari oluşturulur:

Scriptin işlevleri:

- VM oluşturur (Azure üzerinde).
- Apache kurar.
- GitHub üzerinden siteyi download eder ve /var/www/html/ dizinine yerleştirir.
- Apache servisini restart ederek siteyi yayınlar.

Deployment sonucu, VM IP’si Terraform output üzerinden Flask uygulamasına iletilir.

### 3.3 Yayın ve Destroy

Kullanıcı deploy butonuna bastığında site VM üzerinde canlıya alınır ve linki UI’da “VM Live” olarak gösterilir.

Sitenin kullanımı bittikten sonra veya sonuç beğenilmez ise Destroy buttonu kullanılır ve ai website için oluşturulmuş resource group silinir. Site yayından kalkmış olur

---

## 4. Kullanım

- Kullanıcı web uygulamasını açar
- Web sitesini oluşturmak için bir yöntem seçer (Prompt + Görsel, Prompt veya GitHub Linki).
- Platform preview kısmında siteyi görüntüler.
- Beğenirse Deploy AI Site butonuna tıklar.
- Site Azure VM üzerinde Apache ile yayınlanır.
- Kullanıcı, canlı siteye sağlanan link üzerinden erişebilir.
- İşlem sonunda Destroy VM buttonu ile siteyi silebilir.

---

## 5. Mevcut Workflow Özet

- Otomatik GitHub Push: Flask uygulaması, oluşturulan siteleri otomatik olarak GitHub deposuna pushlar.
- Terraform Deploy: Deploy butonuna basıldığında arka planda script çalışır, VM hazırlanır ve site canlıya alınır.
- Containerized Flask: Flask ve Terraform işlemleri aynı Docker container içinde çalışır, böylece bağımsız ve taşınabilir bir ortam sağlanır.
- Port & Networking: Flask App Service, Azure App Service port 80 üzerinden erişilebilir.
- Diyagram: Diyagram

---

## 6. Future Work / İyileştirme Önerileri

**Scaling & Concurrency**  
Birden fazla kullanıcı aynı anda deploy yaparsa, Azure Container Apps veya Kubernetes ile ölçeklenebilirlik sağlanabilir.

**Monitoring & Logging**  
VM sağlık kontrolleri ve deploy süreçlerinin izlenmesi.

**Custom Domain & SSL**  
Kullanıcının kendi domain’i ile deploy etme ve SSL sertifikası entegrasyonu.

**Enhanced Preview**  
Gerçek zamanlı HTML/CSS düzenlemeleri ile preview deneyiminin iyileştirilmesi.

**Template HTML**  
HTML çeşitliliğini ve detayları arttırmak adına html templateleri oluşturulabilir bunları AI doldurur ve temperature ayarına göre kendi yaratıcılığı ile düzenler.

---

## 7. Güvenlik ve Konfigürasyon

- API tokenleri, GitHub tokenleri ve Terraform Service Principal bilgileri Azure App Services Environment Variables kısmında saklanır.
- VM üzerindeki script yalnızca deploy sürecinde çalışır; kullanıcı sistemi doğrudan değiştiremez.
- Container izolasyonu sayesinde tüm bağımlılıklar ve scriptler kontrollü bir şekilde çalışır.

---

## Bağlantılar

- Web Uygulaması: https://flask-terraform-webapp-2025.azurewebsites.net
- GitHub HTML Storage: https://github.com/barisMarathon/html-pages-storage
- Drive demo: https://drive.google.com/drive/u/0/folders/17Da9h1GquZIYc5FNkXXOp7G4H1tMI-W0
- Mimari çizim: https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=flask-terraform-2.drawio&dark=auto#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1OijOf67aDZlETFq5YyN8Gm1oKuuAhyJs%26export%3Ddownload#%7B%22pageId%22%3A%22-jeOLZyow7tsawBEThXN%22%7D
- Mimari çizim 2: https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=flask-terraform-DSD.drawio&dark=auto#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1ztAJDR5qAF_eMeMvzznUh19GX44ez9jg%26export%3Ddownload
