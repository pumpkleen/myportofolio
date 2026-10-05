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


### TUGAS 3

1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
Alasan Menggunakan ModelForm:
Kita menggunakan ModelForm karena ia menghilangkan beban untuk menulis kode berulang (boilerplate). Alih-alih mendefinisikan ulang setiap kolom isian, tipe data, dan batas karakter di HTML (seperti <input type="text" maxlength="255">), Django akan secara otomatis membaca struktur model Menfess di database dan membangun HTML form yang sesuai. Selain itu, ModelForm juga menyediakan validasi data otomatis. Jika pengguna mengirim pesan tanpa mengisi nama, atau mengunggah file yang bukan gambar, ModelForm akan otomatis memblokir data tersebut agar tidak merusak database, sesuatu yang sangat rumit jika harus diatur secara manual melalui HTML konvensional.

Mengapa wajib ada {% csrf_token %}:
{% csrf_token %} adalah mekanisme pertahanan utama Django melawan serangan Cross-Site Request Forgery (CSRF). Tanpa token ini, peretas dapat membuat form palsu di website lain dan menipu browser pengguna agar mengirimkan data modifikasi atau penghapusan secara diam-diam ke server kita saat pengguna sedang login. Token ini ibarat "stempel unik" yang hanya diketahui oleh server dan browser pengguna yang sah, memastikan bahwa setiap data POST yang masuk memang benar-benar dikirim dari halaman website kita sendiri.


2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
Dalam pengembangan aplikasi web modern, JSON (JavaScript Object Notation) jauh lebih disukai dibandingkan XML (eXtensible Markup Language) karena dua alasan utama: efisiensi ukuran dan kompatibilitas sintaks.

Efisiensi Ukuran dan Keterbacaan: JSON menggunakan struktur Key-Value yang sederhana (menggunakan kurung kurawal dan kurung siku), sehingga ukuran payload datanya jauh lebih ringan. Sebaliknya, XML mengharuskan setiap data dibungkus oleh tag pembuka dan penutup yang panjang (seperti <nama>Cheryl</nama>), yang memboroskan ruang (bandwidth) dan membuat proses pengiriman data antar server menjadi lebih lambat.

Kompatibilitas Langsung dengan JavaScript: Karena sebagian besar frontend modern dibangun dengan JavaScript, JSON dapat langsung dibaca dan diolah sebagai objek native JavaScript menggunakan fungsi JSON.parse() tanpa memerlukan proses parsing yang rumit, menjadikannya standar industri untuk komunikasi API dan arsitektur microservices.


3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
Alur saat fungsi view dipanggil:

Saat pengguna atau aplikasi (client) meminta URL endpoint (misalnya /json-menfess/), Django akan mengaktifkan fungsi view yang bertugas.
Fungsi view akan berkomunikasi dengan ORM (Object-Relational Mapping) Django untuk menarik seluruh data objek dari model Menfess di dalam database PostgreSQL.
Objek-objek data mentah tersebut kemudian dimasukkan ke dalam mesin Serializer Django.
Data yang sudah diubah formatnya menjadi bentuk struktur string JSON oleh serializer kemudian dibungkus di dalam kelas HttpResponse dengan header application/json dan dikirim kembali ke browser atau aplikasi peminta.

Mengapa butuh proses serialization:
Kita wajib melakukan proses serialization karena format objek database atau tipe data bawaan Python (seperti objek QuerySet Django atau objek tanggal datetime) tidak dapat dikirimkan secara langsung melalui protokol internet (HTTP). Proses serialization berfungsi sebagai penterjemah yang mengubah struktur kompleks tersebut menjadi format teks standar (JSON) yang dapat dipahami, dikirimkan melalui jaringan internet, dan disusun kembali oleh bahasa pemrograman apa pun yang berada di sisi penerima.


### Deklarasi Penggunaan AI (AI Disclosure)
Dalam pengerjaan Tugas 3 Pemrograman Berbasis Platform (PBP) ini, saya memanfaatkan Generative AI Gemini sebagai mitra diskusi dan asisten pemecahan masalah teknis. Berikut adalah rincian kontribusi AI dalam proses pengembangan:

1. Pemecahan Bug dan Error Debugging

Sistem Template Django: AI membantu menemukan dan menjelaskan penyebab error NoReverseMatch, yang bersumber dari ketiadaan iterasi {% for %} pada pemanggilan URL berparameter ID saat proses rendering data di halaman Menfess.

Penanganan TemplateDoesNotExist: AI membantu mengingatkan kerangka HTML dan attribute yang wajib ada (seperti enctype="multipart/form-data" dan {% csrf_token %}) saat membuat halaman Create dan Edit setelah error hilangnya file template terjadi.

2. Eksplorasi Konsep UI/UX Tingkat Lanjut (Di Luar Silabus Dasar Tugas 3)

Implementasi Modal/Popup Murni CSS: Saya memiliki inisiatif desain UI/UX untuk menggunakan modal popup agar formulir Create, Edit, dan Delete tidak berpindah halaman. Karena AJAX belum diajarkan di Tugas 3, AI membantu saya merancang solusi alternatif yang efektif dengan memadukan ModelForm Django dan pseudo-class CSS :target (tanpa JavaScript) untuk menciptakan ilusi popup yang interaktif.

Integrasi Asset Desain Figma ke HTML/CSS: AI membantu menjelaskan strategi integrasi komponen UI kustom dari Figma, termasuk cara menempatkan SVG menggunakan Flexbox agar presisi di bawah grid layout portofolio, serta menangani masalah CSS background-size: cover versus penggunaan tag <img> yang lebih stabil.

3. Pendalaman Konsep Teoritis

AI membantu mengkurasi dan menguraikan pemahaman teknis terkait peran serialization, efisiensi JSON dibandingkan XML, serta fungsi keamanan dasar {% csrf_token %} sebagai referensi dalam penulisan jawaban di README.

Seluruh baris kode (terutama arsitektur model dan views), tata letak struktur layout, desain aset visual, serta penyusunan logika utama tetap merupakan karya orisinal dan arahan mandiri saya. AI murni berfungsi sebagai alat verifikasi, troubleshooter, dan fasilitator implementasi teknis.


### TUGAS 4

## Deklarasi Penggunaan AI (AI Disclosure)
Dalam pengerjaan tugas ini, saya menggunakan bantuan AI (Gemini) untuk beberapa hal spesifik:
Debugging CSS: AI membantu saya menemukan bug pada tata letak kartu proyek saya yang melebar, dengan menyarankan penggunaan `grid-template-columns: repeat(auto-fill, 300px)murni tanpa gabungan flexbox.
Pemahaman Konsep: Saya meminta bantuan AI untuk menjelaskan cara kerja Django Admin dan bagaimana menggunakannya untuk mengatur hak akses grup Editor tanpa harus melakukan hard-coding di views.py.
Troubleshooting API: AI membantu saya menemukan kesalahan routing path URL ketika saya mencoba mengakses endpoint JSON, serta memastikan implementasi `use_natural_foreign_keys=True` sudah benar agar ID database tidak bocor.


### TUGAS 5
Dalam pengerjaan Tugas 5 Pemrograman Berbasis Platform (PBP) ini, saya memanfaatkan Generative AI Gemini sebagai mitra diskusi dan asisten pemecahan masalah teknis. Berikut adalah rincian kontribusi AI dalam proses pengembangan:

1. Pemecahan Bug dan Error Debugging

Integrasi Frontend dan Backend: AI membantu menemukan missing link saat form gagal menambahkan data, dengan mengingatkan ketiadaan fungsi add_experience_ajax pada views dan membantu merakit kerangka blok try-catch di JavaScript agar Notifikasi Toast dapat menangkap pesan error spesifik dari server.

2. Eksplorasi Konsep Web Interactivity dan UI/UX

Implementasi Modal HTML5 Popover API: AI awalnya menyarankan solusi CSS/JS konvensional untuk modal, namun saya melakukan koreksi mandiri dan mengarahkan AI untuk mematuhi standar arsitektur modern (HTML5 Popover API) sesuai panduan tugas. AI kemudian membantu merapikan atribut popovertarget dan mengintegrasikan file HTML tersebut ke dalam struktur templates/components/.

Logika AJAX dan Debouncing: AI membantu menstrukturkan alur data asinkronus menggunakan fetch() dan await, serta merapikan logika debouncing pada search bar agar request ke server lebih efisien dan layar tidak berkedip (flicker) saat data di-refresh.

3. Pendalaman Konsep Teoritis dan Keamanan (Security)

Keamanan Anti-XSS: AI membantu mengingatkan penerapan keamanan lapis ganda, yaitu escaping karakter menggunakan JavaScript di sisi frontend dan pembersihan input menggunakan strip_tags pada kelas ModelForm di sisi backend.

Penyusunan Dokumentasi: AI membantu mengkurasi dan menguraikan pemahaman teknis terkait peran debouncing, fungsi krusial await pada proses asinkronus, serta rentannya manipulasi DOM terhadap serangan XSS sebagai referensi penulisan jawaban reflektif di README.

Seluruh baris kode (terutama arsitektur model dan views), tata letak struktur layout, desain aset visual, serta penyusunan logika utama tetap merupakan karya orisinal dan arahan mandiri saya. AI murni berfungsi sebagai alat verifikasi, troubleshooter, dan fasilitator implementasi teknis.