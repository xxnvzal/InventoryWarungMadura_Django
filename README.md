# Proyek UTS Backend Sistem Manajemen Inventory

Proyek ini adalah sistem manajemen inventory yang dibangun menggunakan Django, Docker, dan PostgreSQL. Berikut adalah petunjuk cara menjalankan proyek di mesin lokal Anda.

## Langkah-langkah untuk Menjalankan Proyek

### 1. **Clone Repository**
Pertama, clone repositori ini ke dalam direktori lokal Anda dengan menggunakan perintah berikut:

2. Sesuaikan Versi PostgreSQL di docker-compose.yml
Pastikan versi PostgreSQL yang ada di file docker-compose.yml sesuai dengan versi yang Anda miliki di mesin lokal Anda. Buka file docker-compose.yml dan sesuaikan versi PostgreSQL jika diperlukan.

Contoh:

yaml
Copy
Edit
services:
  db:
    image: postgres:12 # Sesuaikan dengan versi yang Anda inginkan
3. Menjalankan Docker Compose
Setelah file docker-compose.yml disesuaikan, buka terminal dan jalankan perintah berikut untuk membangun dan menjalankan kontainer Docker:

bash
Copy
Edit
docker-compose up -d
Perintah ini akan membangun dan menjalankan dua kontainer: satu untuk aplikasi web (Django) dan satu untuk database PostgreSQL.

4. Cek Kontainer Docker
Periksa apakah kedua kontainer (untuk aplikasi dan PostgreSQL) sudah berjalan dengan benar. Jalankan perintah berikut untuk melihat status kontainer:

bash
Copy
Edit
docker ps
Pastikan kedua kontainer hidup. Jika kontainer PostgreSQL tidak hidup, Anda perlu menyesuaikan versi PostgreSQL di file docker-compose.yml.

5. Jika PostgreSQL Tidak Berjalan
Jika kontainer PostgreSQL tidak berjalan, lakukan langkah berikut:

Jalankan perintah untuk mematikan semua kontainer dan menghapus volume:

bash
Copy
Edit
docker-compose down -v
Kemudian, bangun ulang kontainer dengan perintah:

bash
Copy
Edit
docker-compose build
Jalankan kembali perintah untuk menjalankan kontainer:

bash
Copy
Edit
docker-compose up -d
6. Masuk ke Kontainer Web
Setelah kontainer berjalan, kita perlu masuk ke dalam kontainer inventory_web_uts. Jika Anda menggunakan Docker Extension (misalnya di Visual Studio Code), Anda bisa langsung attach shell ke kontainer.

Jika tidak menggunakan Docker Extension, gunakan perintah berikut untuk masuk ke dalam kontainer menggunakan terminal:

bash
Copy
Edit
docker exec -it inventory_web_uts /bin/bash
7. Migrasi Database
Setelah berhasil masuk ke dalam kontainer, jalankan perintah berikut untuk melakukan migrasi database:

bash
Copy
Edit
python manage.py migrate
8. Import Data
Setelah migrasi selesai, jalankan perintah berikut untuk mengimpor data yang diperlukan ke dalam database:

bash
Copy
Edit
python importer.py
9. Menjalankan Aplikasi
Jika database sudah terimpor, jalankan perintah berikut untuk menjalankan server Django:

bash
Copy
Edit
python manage.py runserver 0.0.0.0:8000
10. Akses Aplikasi
Buka browser dan akses aplikasi melalui URL berikut:

arduino
Copy
Edit
http://localhost:8000/
