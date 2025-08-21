# SaDx Terraform Project

---

## 1. Terraform init, terraform plan, terraform apply komutları nedir neden kullanılırlar?

Terraform init --> Projeyi başlatır, Provider (Azure, Aws, Google Cloud) eklentilerini indirir, Backend operasyonlarını başlatır (Bu projede vm oluştuğunda Apache yi başlatma operasyonu olabilir ?)  
Terraform plan --> GÜncel terraform dosyasından nelerin değiştiğini ön izlemek için kullanılır.  
Terraform apply --> Önizlenmiş değişiklikleri uygulamaya koyar

---

## 2. Terraform fmt, terraform validate ve terraform refresh komutlarının işlevleri nelerdir?

Terraform fmt --> Düzenleme sağlıyor kod tek tip kurallarla format olarak tek tip hale gelmiş oluyor. (Zaten Vscode içerisinden düzenleyici seçilebildiği için bir faydasını göremedim)  
Terraform validate --> Değerlerin yazımsal olarak doğruluğunu kontrol ediyor ama gerçekten bulutta var olup olamayacağını (değerlerin anlamlı olup olmadığını) kontrol etmiyor. İstisnai olarak bazı değerlerin var olup olmayacağını biliyor düzeltme istiyor.  
Terraform refresh --> Terraformu kullanmadan azure portal üzerinden yapılan değişiklikleri terraformun görebilmesi için terraform state dosyasını günceller

---

## 3. main.tf, variables.tf ve outputs.tf dosyaları ne işe yarar?

main.tf --> Ana tercihlerin belirlendiği yer infrastuctre'ın kurulduğu yerdir.  
variables.tf --> Burada variableları tutarız bunun sebebi de tekrarlı kullanılacak belirlenmiş variableları tek yerden değiştirebilmek kolayca tek yerden tercihlerimizi düzenleyebilmek örn: subscription_id = sub_id yaptığında aynı template'i başka hesapta da kullanmak için variables kısmında sub_id = "xxxxxxx" veya sub_id = "yyyyyyy" yaparak hesaplar arasında template'ini kullanabilirsin.  
outputs.tf --> terraform apply yaptıktan sonra karşına çıkacak değerleri belirlediğin yer örn: vm kaldırdın outputs kısmına ip'sini eklersen apply'dan sonra sana çıktısını verecektir. ip = xxxxxxx

---

## 4. HCL nedir ve nasıl bir yazımı vardır?

Daha okunabilir JSON a benzeyen bir listeleme dili.

---

## 5. Terraform’da bir resource bloğu nasıl yazılır ve hangi bileşenleri içerir?

## 6. Modül yapısı nedir, ne zaman ve neden kullanılır?

---

## 7. Terraform’da provider nedir?

---

## 8. Terraform state dosyası (terraform.tfstate) nedir ve neden önemlidir?

---

## 9. variables.tf ve terraform.tfvars dosyalarının farkı nedir?

---

## 10. VNet, Subnet, NSG nedir?

---

## 11. Public ve Private IP nedir?

---

## 12. NSG’nin doğrudan sanal makineye değil, subnet’e atanması ne anlama gelir?

---

## Build-Step Notları

1. `az login`
2. `az account show` (bilgilerini görüntüle)
3. Yukarıdaki bilgileri kullanarak aşağıdaki komutu doldur.

```bash
$env:ARM_SUBSCRIPTION_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
$env:ARM_TENANT_ID="yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"


```
