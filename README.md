Nama: Cheryl Mahira Indarto
Npm: 2506606093
Kelas: PBP A

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 dalam merancang struktur website ini.
Saya menggunakan <section> untuk memisahkan area About Me dan Experience agar pembagian halamannya jelas sesuai tema
secara garis besar. Selain itu saya juga jadi bisa membuat tombol di navbar yang mengarahkan langsung ke section-section
yang dituju. Selain itu saya juga menggunakan elemen <article> untuk membungkus setiap experiences saya. Elemen-elemen ini membantu saya memberikan struktur pada web saya. Selain itu elemen semantik ini juga membuat kode saya terlihat lebih rapih. Pada static web seperti ini, update sangat mengandalkan pembaharuan kode secara manual, maka sangat penting untuk memastikan kode mudah dibaca dan dipahami. Karena elemen semantik sangat deksriptif mengenai fungsinya, saya tidak akan bingung jika harus membuka kode saya lagi dalam waktu lama.
2. Tantangan utamanya adalah memastikan konten tidak terasa sesak saat layar menyempit, sekaligus mempertahankan white space yang cukup agar nyaman di mata. Tantangan ini saya temukan saat membuat experience-card. Dalam mengevaluasi elemen, saya memprioritaskan keterbacaan teks dan proporsi kartu. Saya memanfaatkan CSS Grid dengan properti repeat(auto-fit, minmax(300px, 1fr)). Pendekatan ini memungkinkan kartu-kartu pengalaman berbaris rapi secara horizontal di desktop, dan secara otomatis menyusut lalu turun menjadi satu kolom vertikal di layar yang lebih sempit (termasuk pada layar mobile). Saya juga menyesuaikan nilai padding dan gap agar konten di dalam kartu tidak menempel ke tepi layar pada layar yang lebih kecil.
3. Batasan yang saya rasakan saat mencoba menyajikan informasi pada portofolio saya adalah pemeliharaan konten sebagaimana telah saya sampaikan sebelumnya bahwasannya pada static web untuk mengupdate konten diperlukan pembaharuan konten secara manual. Tentu saja ini bukan proses yang efektif karena saya harus mengubah konten html lagi secara terus menerus. Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya persiapkan adalah menu dashboard dimana saya bisa mengelola portfolio melalui menu admin.

Pekan ini pada tugas mandiri 1 saya menambahkan fitur baru yaitu Experience. Untuk section ini, saya membuat section baru yang berisi card-card kecil bertuliskan pengalaman-pengalaman saya. Dalam mengerjakan refleksi, saya tidak menggunakan AI, tetapi saya tetap mencari di internet terkait istilah-istilah yang belum saya pahami seperti semantik HTML5 (ternyata yang dimaksud semantik HTML5 adalah yang isinya lugas). Selain itu saya juga memastikan apakah pemahaman saya sudah benar terkait perbedaan static web dan dynamic web. Untuk mengerjakan codingnya sendiri saya banyak menonton tutorial youtube agar memahami penggunaan elemen HTML dan CSS dan melihat bagaimana biasanya orang membuat web dengan HTML CSS. Terkadang saya bertanya ke AI jika ada tutorial yang sulit dipahami agar lebih menangkap konsepnya. Misalnya penggunaan repeat() itu kayak gimana. Ada banyak elemen yang baru saya ketahui setelah berkelana di internet. Saya juga memberikan banyak komentar pada kode saya agar tidak lupa format serta cara pemakaiannya.

### Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

Ketika klien mengetik URL di browser, alur yang terjadi adalah:
Browser mengirimkan HTTP Request ke server Django. Kemudian, Django akan mengecek routing di berkas urls.py untuk mencari fungsi mana yang cocok dengan alamat /projects/. Setelah cocok, Django akan memanggil fungsi terkait di views.py. Kalau fungsi view butuh data (seperti daftar project milikku), view akan meminta data tersebut dari database melalui perantara models.py. Setelah data terkumpul, view akan menggabungkan data tersebut dengan berkas template HTML (aku pakai projects.html). Terakhir, Django akan mengirimkan kembali dokumen HTML yang sudah dirender seutuhnya ke browser pengguna sebagai HTTP Response, sehingga tampilan halamannya bisa dilihat.


2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Karena ketika data dalam portfolio disimpan secara hard-coded di dalam template, kita akan kesulitan dalam memelihara website kita. Sebagai contoh jika saya memiliki 100 projects kemudian suatu hari saya ingin mengedit satu judul, saya harus mengacak-acak lagi kode html yang saya miliki. Pada saat itu mungkin saja saya sudah lupa mengenai struktur kode saya.
Semakin sering kita membongkar berkas HTML untuk mengganti data, semakin tinggi kemungkinan merusak struktur desain (seperti CSS Grid/Flexbox) yang sudah dibangun.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
makemigrations adalah proses di mana Django mencatat setiap perubahan yang kita buat pada berkas models.py (seperti saat saya menambahkan kelas Project). Hasilnya adalah sebuah berkas cetak biru (skema/instruksi) yang berisi detail apa saja yang berubah.

Migrate adalah proses eksekusi. Django akan membaca berkas cetak biru yang dibuat oleh makemigrations tadi, lalu menerapkannya secara fisik ke dalam struktur database kita yang sesungguhnya (seperti benar-benar membuat tabel Project baru atau menambah kolom image).