# Sistem Pendukung Keputusan Penerimaan Karyawan
Suatu sistem untuk membantu penyeleksian karyawan baru menggunakan algoritma Support Vector Machine dan metode SPK Simple Additive Weighting.

# Algoritma
## Support Vector Machine
![svm](https://github.com/khoirilannm/SPK-Penerimaan-Karyawan/assets/151839648/77055dcd-5a7c-4e88-b435-19e04fafc6c2)
Algoritma support vector machine (SVM) digunakan untuk membuat model klasifikasi berdasarkan pada label yang ada. SVM adalah salah satu algoritma dalam machine learning dan digunakan dalam penambangan data dan pengenalan pola. Konsep utama SVM dapat diilustrasikan pada gambar berikut.

![image](https://github.com/khoirilannm/SPK-Penerimaan-Karyawan/assets/151839648/7d750921-0455-4d48-8959-5b894a601af1)

Algoritma support vector machine (SVM) dapat dijelaskan sebagai proses pemisahan dua kelas yang berbeda dalam ruang fitur seperti positif dan negatif. Menemukan hyperplane yang dapat memisahkan kelas-kelas tersebut adalah masalah utama dalam proses klasifikasi menggunakan algoritma SVM, dimana hyperplane ini tergantung pada margin maksimal.
## Simple Additive Weighting
![normalisasi](https://github.com/khoirilannm/SPK-Penerimaan-Karyawan/assets/151839648/f6ddc63d-6afe-4743-9083-adba6ca0d1c3)

Metode Simple Additive Weighting (SAW) sering juga dikenal dengan penjumlahan terbobot. Konsep dasar metode Simple Additive Weighting disarankan untuk menyelesaikan masalah penyeleksian dalam sistem pengambilan keputusan multiproses. Konsep dasar metode SAW adalah mencari penjumlahan terbobot dari rating kinerja pada setiap alternatif pada semua atribut. Metode SAW membutuhkan proses normalisasi matriks keputusan (X) ke suatu skala yang dapat dibandingkan dengan semua rating alternatif yang ada.

# Teknologi dan bahasa yang digunakan
<ol>
  <li>Bahasa Pemrograman: Python</li>
  <li>Database: SQLite3</li>
  <li>Framework: Streamlit</li>
</ol>
