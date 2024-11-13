🛠️ Odoo Development Repository

📜 Deskripsi

Repositori ini berisi panduan dan contoh implementasi berbagai aspek pengembangan di Odoo, termasuk:

✨ Pembuatan Modul <br>
🗂️ Pembuatan Model <br>

Repositori ini dirancang untuk membantu pengembang memahami konsep dasar dan lanjutan dalam membangun modul dan antarmuka di Odoo, 
serta memberikan contoh kode yang dapat digunakan sebagai referensi.

untuk <br>

📊 Membuat Laporan QWeb <br>
🖼️ Membuat Template QWeb menggunakan Python dan JavaScript <br>
🦉 Penggunaan OWL Framework untuk membuat Template QWeb <br>

ada di branch selanjutnya.


-----------------------------------------------------------------------------------------------------

🧩 Persyaratan

Pastikan Anda telah menginstal Odoo dan dependensi lain yang diperlukan untuk menjalankan modul dan template yang disediakan. Berikut adalah beberapa persyaratan:

<b>Odoo versi terbaru</b> (misalnya, Odoo 14 atau lebih baru)
<b>Python 3.x</b> <br>
<b>Node.js dan NPM</b> (untuk pengembangan OWL framework) <br>
<b>wkhtmltopdf</b> (untuk rendering laporan PDF QWeb)

-----------------------------------------------------------------------------------------------------

🚀 Instalasi
Folder yang digunakan hanya folder addons di dalam folder server!

1. unduh / download ZIP jangan di clone karena komponen yang penting hanyalah folder addons
2. taruh folder / module yang kalian inginkan di dalam folder custom addons kalian
3. update applist aplikasi odoo kalian
4. kalau muncul tinggal install modulenya. contoh: master_data dan master_purchasing

CAUTION!!!
hanya pindahkan atau download module yang kalian ingin gunakan tidak usah mengclone semua resource di repository ini
clone hanya dari folder addons nya saja

-----------------------------------------------------------------------------------------------------

🛠️ Penggunaan

1. 🔧 Pembuatan Modul
Lihat folder modules/ untuk memahami cara membuat modul Odoo dari awal. Modul ini mencakup pengaturan __manifest__.py, __init__.py, serta file konfigurasi untuk models, views, dan controllers.

2. 🗂️ Pembuatan Model
Di dalam folder models/, terdapat contoh model dengan penjelasan setiap field dan metode utama yang digunakan. Contoh model ini dapat digunakan sebagai referensi untuk operasi CRUD (Create, Read, Update, Delete) di Odoo.
