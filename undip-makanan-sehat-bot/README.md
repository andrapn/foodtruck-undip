# UNDIP Food Truck Helper

Bot untuk mengambil kupon makanan sehat/food truck UNDIP.

Jangan rame ya, nanti malah di-patch sistemnya 🤫


Requirements:
```
Python 3.8+
```

## Instalasi

1. Buka terminal dan ganti direktori ke folder project
2. Install pipenv melalui terminal (jika belum ada)
```PowerShell
pip install pipenv
```
3. Buat virtual environment dengan pipenv
```PowerShell
pipenv install
```
4. Aktivasi virtual environment
```PowerShell
pipenv shell
```
5. Jalankan bot (test)
```PowerShell
python get-coupon.py -t
```
Nonaktifkan virtual environment dengan perintah `exit`

#### Terdapat juga file `requirements.txt` bagi yang ingin setup dengan `virtualenv` atau tanpa virtual environment.

---

## Contoh Kasus Penggunaan

### Penggunaan Standar (Input Data Manual)

```PowerShell
python get-coupon.py
```

### Penggunaan dengan Command Line Argument / Flag

* Lengkap

```PowerShell
python get-coupon.py -e "jeff@students.undip.ac.id" -p "pw123" -l 1
```

* Tanpa flag `-p` (jika ingin input password secara tertutup)

```PowerShell
python get-coupon.py -e "jeff@students.undip.ac.id" -l 2
```

>Index Lokasi: (1) Student Center, (2) SA-MWA, (3) FPIK, (4) Imam Bardjo

Disarankan menjalankan bot **sebelum** jam 10:00 WIB. Bot akan stand-by di halaman form sampai jam 10:00 WIB.

### Eksekusi Paralel

Jika ingin menjalankan 2 bot atau lebih secara bersamaan, disarankan menambahkan **delay** refresh yang berbeda untuk setiap bot.

Contoh: menambahkan delay 0.2s dengan argumen **-d 0.2**

```PowerShell
python get-coupon.py -e "jeff@students.undip.ac.id" -p "pw123" -l 3 -d 0.2
```

### Sentry Mode

Untuk kasus ketika pilihan kupon tidak muncul setelah jam 10:00 WIB.

Dalam sentry mode, bot akan refresh halaman form secara berkala sesuai dengan interval waktu yang diberikan.

Contoh: mengaktifkan sentry mode dengan interval refresh 30s dengan flag **-S 30**

```PowerShell
python get-coupon.py -e "jeff@students.undip.ac.id" -p "pw123" -l 3 -S 30
```

---

* Info lebih lanjut

```PowerShell
python get-coupon.py -h
```
