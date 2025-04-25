
# Proyek UTS Backend Sistem Manajemen Inventory
===========================

Proyek ini menggunakan Django dengan PostgreSQL sebagai database, dan dijalankan menggunakan Docker.

Cara Menjalankan Proyek
------------------------

1. Clone repository ini

2. Sesuaikan versi PostgreSQL:
Buka file `docker-compose.yml` dan pastikan versi PostgreSQL sesuai dengan versi yang kamu miliki di lokal.

3. Jalankan Docker Compose:
```bash
docker-compose up -d
```

4. Cek kontainer:
Pastikan dua kontainer aktif (`inventory_web_uts` dan `postgres`).

5. Jika kontainer PostgreSQL tidak aktif:
- Sesuaikan versi PostgreSQL di file `docker-compose.yml`.
- Jika sudah menyesuaikan lalu jalankan perintah berikut:
```bash
docker-compose down -v
docker-compose up -d
```

6. Masuk ke dalam shell kontainer `inventory_web_uts`:
- Jika menggunakan Docker Extension (misalnya di VS Code), bisa langsung attach shell.
- Jika tidak, gunakan perintah:
```bash
docker exec -it inventory_web_uts bash
```

7. Jalankan migrasi database:
```bash
python manage.py migrate
```

8. Import data ke database:
```bash
python importer.py
```

9. Jalankan server Django:
```bash
python manage.py runserver 0.0.0.0:8000
```

10. Akses aplikasi melalui browser:
```
http://localhost:8000/
```
