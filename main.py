import streamlit as st
from streamlit_option_menu import option_menu
from fungsi import getDataByFilter, perangkingan_saw, tambahAkun, ubahHapusAkun, getData, addDataPelamar, ubahDataPelamar, hapusAllData, form_login, change_data, hapusDataPelamar
import pandas as pd
from datetime import date
import time
from PIL import Image
import datetime
import pickle
import numpy as np

st.set_page_config(layout='wide')

if 'test_svm' not in st.session_state:
    st.session_state['test_svm'] = False

def klasifikasi_svm(df):
    data_new = change_data(df)
    df_new = data_new[0]

    file = open('model.pkl', 'rb')
    model = pickle.load(file)

    list_predict = []
    for i in range(len(df_new)):
        data = df_new.iloc[i, :].values
        predict = model.predict([data])

        if predict == 1:
            list_predict.append(1)
        else:
            list_predict.append(0)

    df_new['predict_svm'] = list_predict

    return df_new

if 'session_login' not in st.session_state: st.session_state['session_login'] = ''

st.markdown("""
            <style>
            .visimisi {
                width: 100%;
                background-color: #639cd9;
                text-align: center;
                border-radius: 15px;
                color: white;
                font-size:20px;
                font-family: Arial;
                padding-bottom:20px;
                padding-right: 20px;
                padding-left: 20px;
            }
            .title {
                
            }
            .big-font {
                font-family: Arial;
                font-size:22px;
            }
            [data-testid=stSidebar] {
                background-color: #639cd9;
            }
            .iv {
                background-color: #639cd9;
                text-align: center;
                margin-bottom:20px;
            }
            [data-testid="stForm"] {
                background-color: rgba(255, 255, 255, .7);
                border-radius: 15px;
            }
            [data-baseweb="base-input"] {
                font-family: Roboto;
                border-radius: 10px;
                color: white;
                background-color: #639cd9;
            }
            [data-baseweb="input"] {
                color: white;
                background-color: #639cd9;
                border-radius: 10px;
            }
            [aria-label=" "] {
                color: white;
                font-size: 23px;
            }
            [kind="secondaryFormSubmit"]{
                font-size: 25px;
                background-color: #639cd9;
                color: white;
                width: 100%;
            }
            .css-1a32fsj{
                background-color: rgba(255, 255, 255, .9);
                border-radius: 10px;
            }
            [aria-label="Password"] {
                color: white;
                font-size: 25px;
            }
            [aria-label="Nama"] {
                color: white;
                font-size: 25px;
            }
            p {
                color: black;
            }
            div.stButton > button:first-child {
                background-color: #a9d7f6;
                color:white;
            }
            div.stButton > button:hover {
                background-color: #354abf;
                color:white;
                }
            </style>
            """, unsafe_allow_html=True)

if st.session_state['session_login'] == '':
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Utama",
            options=["Profil Instansi", "Login"],
            menu_icon='truck',
            icons=['house', 'door-open'],
            styles={
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "18px", "text-align": "left", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#354abf"},
            })

   
    if selected == "Login":
        form_login()
    
    else:
        st.markdown('<h1 class="iv"> Profil Instansi </h1>', unsafe_allow_html=True)
        buffer, col1, col2 = st.columns([.1, 4, 5], gap='large')
        buffer_2, col1_2, col2_2 = st.columns([1, 4, 1])
        with col1:
            st.write("")
            st.markdown('<h1 class="title">PT. KALIBARU JAYA ABADI</h1>', unsafe_allow_html=True)
            st.write("")
            
            st.markdown('''<p class='big-font'; align='justify'>
                PT. Kalibaru Jaya Abadi merupakan perusahaan ekspedisi yang bergerak dalam bidang usaha jasa pengiriman barang dengan berbagai tujuan di pulau jawa melalui jalur darat yang mulai beroperasi sejak tahun 2013. PT. Kalibaru Jaya Abadi menciptakan sinergi yang positif serta siap merubah tantangan menjadi harapan baru dan terus maju untuk menjadi perusahaan nomor satu di bidang jasa pengiriman barang. Perusahaan ini berlokasi di Rawa Aren RT.002, RW.024. Desa Setiamekar, Kecamatan Tambun Selatan, Kabupaten Bekasi, Provinsi Jawa Barat.</p>''', unsafe_allow_html=True)

        with col2:
            img = Image.open('gambar/download.png')
            st.image(img)
        
        with col1_2:
            st.write("")
            st.markdown("<hr style='border: 0.5px solid white';>", unsafe_allow_html=True)
            st.markdown("<h1 align='center'; class='title'>VISI - MISI</h1>", unsafe_allow_html=True)
            st.markdown("<div class='visimisi'> <h2>VISI</h2>\n PT. Kalibaru Jaya Abadi memiliki visi untuk menjadi perusahaan yang terdepan dan berintegritas dalam layanan jasa angkut barang (cargo).\n <h2>MISI</h2> \nMemberikan solusi logistik yang efisien dan terintegrasi bagi pelanggan serta mendukung daya saing logistik nasional. Membangun kemitraan usaha dengan mitra kerja strategis yang saling menguntungkan. Terus berupaya mengembangkan kompetensi karyawan dan organisasi agar memiliki daya saing nasional.</div>", unsafe_allow_html=True)

elif st.session_state['session_login'] != '':
    with st.sidebar:
        choose = option_menu(
            menu_title="Menu", 
            options=["Input Data", "Klasifikasi", "Perangkingan", "Hasil","Data Akun", 'Logout'],
            icons=['plus-lg', 'receipt', 'sort-down' ,'activity', "list-task",'door-closed'],
            menu_icon='truck',
            styles={
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "18px", "text-align": "left", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#354abf"},
            })
            
    if choose == 'Input Data':
        st.markdown('<h1 class="iv">Data Pelamar Kerja</h1>', unsafe_allow_html=True)
        cek_data = getData(category_inp="All")
        email, nama, jenis_kelamin, usia, pendidikan, tes_wawancara, tpa, tes_keterampilan, posisi, tanggal = [],[],[],[],[],[],[],[],[],[]
        if cek_data == False:
            data_df = {
                    'Email' : email,
                    'Nama Pelamar' : nama,
                    'Jenis Kelamin' : jenis_kelamin,
                    'Usia' : usia,
                    'Pendidikan' : pendidikan,
                    'Tes Wawancara' : tes_wawancara,
                    'Tes Potensi Akademik' : tpa,
                    'Tes Keterampilan Teknis' : tes_keterampilan,
                    'Posisi yang dilamar' : posisi,
                    'Tanggal' : tanggal
                }

            df = pd.DataFrame(data_df)
            st.table(df)

            placeholder = st.empty()
            with placeholder.form(key="tambah data"):
                nama = st.text_input("Nama Pelamar")
                email = st.text_input("Email")
                jenis_kelamin = st.selectbox(
                    'Jenis Kelamin',
                ('Laki-laki', 'Perempuan'))
                usia = st.number_input("Usia", min_value=19, step=1, max_value=28)
                pendidikan = st.selectbox(
                    'Pendidikan Terakhir',
                    ('SMA/SMK', 'D3', 'S1'))
                posisi = st.selectbox(
                    'Posisi yang dilamar',
                    ('Staf Administrasi', 'Staf Operasional'))
                tanggal = st.date_input('Tanggal Apply Lamaran', value=date.today())
                wawancara = int(st.number_input("Nilai Tes Wawancara", min_value=0, step=1, max_value=35))
                tpa = int(st.number_input("Nilai Tes Potensi Akademik", min_value=0, step=1, max_value=20))
                keterampilan = int(st.number_input("Nilai Tes Keterampilan Teknis", min_value=0, step=1, max_value=20))
                st.write(" ")
                submit = st.form_submit_button(label="Tambah Data")
                if submit==True:
                    addDataPelamar(nama,email,jenis_kelamin,usia,pendidikan,wawancara,tpa,keterampilan,posisi,tanggal)
                    st.success("Data berhasil ditambahkan")
                    

        else:
            option = st.selectbox('',('Tambah Akun Pelamar', 'Ubah & Hapus Akun Pelamar'))
            if option == 'Tambah Akun Pelamar':
                for i in range(len(cek_data)):
                    email.append(cek_data[i][0])
                    nama.append(cek_data[i][1])
                    jenis_kelamin.append(cek_data[i][2])
                    usia.append(cek_data[i][3])
                    pendidikan.append(cek_data[i][4])
                    tes_wawancara.append(cek_data[i][5])
                    tpa.append(cek_data[i][6])
                    tes_keterampilan.append(cek_data[i][7])
                    posisi.append(cek_data[i][8])
                    tanggal.append(cek_data[i][9])
                    data_df = {
                        'Email' : email,
                        'Nama Pelamar' : nama,
                        'Jenis Kelamin' : jenis_kelamin,
                        'Usia' : usia,
                        'Pendidikan' : pendidikan,
                        'Tes Wawancara' : tes_wawancara,
                        'Tes Potensi Akademik' : tpa,
                        'Tes Keterampilan Teknis' : tes_keterampilan,
                        'Posisi yang dilamar' : posisi,
                        'Tanggal' : tanggal
                    }

                df = pd.DataFrame(data_df)
                st.table(df)

                placeholder = st.empty()
                with placeholder.form(key="input data"):
                    nama = st.text_input("Nama Pelamar")
                    email = st.text_input("Email")
                    jenis_kelamin = st.selectbox(
                        'Jenis Kelamin',
                    ('Laki-laki', 'Perempuan'))
                    usia = st.number_input("Usia", min_value=19, max_value=28)
                    pendidikan = st.selectbox(
                        'Pendidikan Terakhir',
                        ('SMA/SMK', 'D3', 'S1'))
                    posisi = st.selectbox(
                        'Posisi yang dilamar',
                        ('Staf Administrasi', 'Staf Operasional'))
                    tanggal = st.date_input('Tanggal Apply Lamaran', value=date.today())
                    wawancara = int(st.number_input("Nilai Tes Wawancara", min_value=0, step=1, max_value=35))
                    tpa = int(st.number_input("Nilai Tes Potensi Akademik", min_value=0, step=1, max_value=20))
                    keterampilan = int(st.number_input("Nilai Tes Keterampilan Teknis", min_value=0, step=1, max_value=20))
                    st.write(" ")
                    submit = st.form_submit_button(label="Submit")
                    if submit==True:
                        if addDataPelamar(nama,email,jenis_kelamin,usia,pendidikan,wawancara,tpa,keterampilan,posisi,tanggal) == True:
                            st.success("Nilai berhasil ditambahkan")
                        else:
                            st.warning("Data gagal ditambahkan")
                        
            if option == 'Ubah & Hapus Akun Pelamar':
                for i in range(len(cek_data)):
                    email.append(cek_data[i][0])
                    nama.append(cek_data[i][1])
                    jenis_kelamin.append(cek_data[i][2])
                    usia.append(cek_data[i][3])
                    pendidikan.append(cek_data[i][4])
                    tes_wawancara.append(cek_data[i][5])
                    tpa.append(cek_data[i][6])
                    tes_keterampilan.append(cek_data[i][7])
                    posisi.append(cek_data[i][8])
                    tanggal.append(cek_data[i][9])
                    data_df = {
                        'Email' : email,
                        'Nama Pelamar' : nama,
                        'Jenis Kelamin' : jenis_kelamin,
                        'Usia' : usia,
                        'Pendidikan' : pendidikan,
                        'Tes Wawancara' : tes_wawancara,
                        'Tes Potensi Akademik' : tpa,
                        'Tes Keterampilan Teknis' : tes_keterampilan,
                        'Posisi yang dilamar' : posisi,
                        'Tanggal' : tanggal
                    }
                df = pd.DataFrame(data_df)
                st.table(df)

                option = st.selectbox("Pilih Data Berdasarkan Email", df.Email, 0)
                selected_id_admin = option
                selected_nama = df.loc[df.Email == option]["Nama Pelamar"].iloc[0]
                selected_email = df.loc[df.Email == option]["Email"].iloc[0]
                selected_jk = df.loc[df.Email == option]["Jenis Kelamin"].iloc[0]
                selected_usia = df.loc[df.Email == option]["Usia"].iloc[0]
                selected_pendidikan = df.loc[df.Email == option]["Pendidikan"].iloc[0]
                selected_wawancara = df.loc[df.Email == option]["Tes Wawancara"].iloc[0]
                selected_tpa = df.loc[df.Email == option]["Tes Potensi Akademik"].iloc[0]
                selected_keterampilan = df.loc[df.Email == option]["Tes Keterampilan Teknis"].iloc[0]
                selected_posisi = df.loc[df.Email == option]["Posisi yang dilamar"].iloc[0]
                if selected_jk == "Laki-laki":
                    selected_jk = 0
                else:
                    selected_jk = 1

                if selected_pendidikan == "SMA/SMK":
                    selected_pendidikan = 0

                elif selected_pendidikan == "D3":
                    selected_pendidikan = 1

                elif selected_pendidikan == "S1":
                    selected_pendidikan = 2
                
                
                if selected_posisi == "Staf Administrasi":
                    selected_posisi = 0
                if selected_posisi == "Staf Operasional":
                    selected_posisi = 1

                placeholder = st.empty()
                with placeholder.form(key="edit data"):
                    nama = st.text_input("Nama Pelamar", value=selected_nama)
                    jenis_kelamin = st.selectbox(
                        'Jenis Kelamin',
                    ('Laki-laki', 'Perempuan'), index=selected_jk)
                    usia = st.number_input("Usia", value=selected_usia)
                    pendidikan = st.selectbox(
                        'Pendidikan Terakhir',
                        ('SMA/SMK', 'D3', 'S1'), index=selected_pendidikan)
                    posisi = st.selectbox(
                        'Posisi yang dilamar',
                        ('Staf Administrasi', 'Staf Operasional'))
                    tanggal = st.date_input('Tanggal Apply Lamaran', value=date.today())
                    wawancara = int(st.number_input("Nilai Tes Wawancara", min_value=0, step=1, max_value=35, value=selected_wawancara))
                    tpa = int(st.number_input("Nilai Tes Potensi Akademik", min_value=0, step=1, max_value=20, value=selected_tpa))
                    keterampilan = int(st.number_input("Nilai Tes Keterampilan Teknis", min_value=0, step=1, max_value=20, value=selected_keterampilan))
                    st.write(" ")
                    editdata = st.form_submit_button(label="Edit")
                    hapusData = st.form_submit_button(label="Hapus")
                    if hapusData==True:
                        hapusDataPelamar(selected_email)
                        st.success("Data berhasil dihapus")
                    elif editdata==True:
                        st.success("Data berhasil diubah")
                        ubahDataPelamar(nama,jenis_kelamin,usia,pendidikan,wawancara,tpa,keterampilan,posisi,tanggal,selected_email)
            
    
    elif choose == "Klasifikasi":
        st.markdown('<h1 class="iv">Data Training SVM </h1>', unsafe_allow_html=True)
        df = pd.read_csv("dataset/datatrain-final.csv")
        df = df.iloc[:10, 1:]
        st.table(df)


        st.markdown('<h1 class="iv">Perhitungan SVM </h1>', unsafe_allow_html=True)
        st.image('gambar/rumus svm.png')

        target_svm = np.where(df['Target'] <= 0, -1, 1)
        features = df.iloc[:, :-1].values
        data_kondisi = []
        data_bobot = []
        data_bias = []
        bobot = np.zeros(features.shape[1])
        bias = 0
        learning_rate = 0.001
        ParamLambda = 0.01
        iter = 1

        for _ in range(iter):
            for idx, x in enumerate(features):
                kondisi = target_svm[idx] * (np.dot(x, bobot) - bias) >= 1
                if kondisi == True:
                    data_kondisi.append("True")
                    bobot = bobot - learning_rate * (2 * ParamLambda * bobot)
                    bias = bias
                    data_bobot.append(bobot)
                    data_bias.append(bias)
                else:
                    data_kondisi.append("False")

                    bobot = bobot - learning_rate * (
                        2 * ParamLambda * bobot - np.dot(x, target_svm[idx])
                    )
                    bias = bias - learning_rate * target_svm[idx]

                    data_bobot.append(bobot)
                    data_bias.append(bias)

        bobot_usia, bobot_pendidikan, bobot_wawancara, bobot_tpa, bobot_keterampilan = [], [], [], [], []    
        for i in range(len(data_bobot)):
            bobot_usia.append(data_bobot[i][0])
            bobot_pendidikan.append(data_bobot[i][1])
            bobot_wawancara.append(data_bobot[i][2])
            bobot_tpa.append(data_bobot[i][3])
            bobot_keterampilan.append(data_bobot[i][4])
        
        df_new = pd.DataFrame()
        df_new['Kondisi'] = data_kondisi
        df_new['Bobot Usia'] = bobot_usia
        df_new['Bobot Pendidikan'] = bobot_pendidikan
        df_new['Bobot Wawancara'] = bobot_wawancara
        df_new['Bobot Tpa'] = bobot_tpa
        df_new['Bobot Keterampilan'] = bobot_keterampilan
        df_new['Bias'] = data_bias
        st.table(df_new)
    

        st.markdown('<h1 class="iv">Form Testing Model</h1>', unsafe_allow_html=True)
        form_klasifikasi = st.empty()
        with form_klasifikasi.form("Klasifikasi"):
            usia = st.number_input("Usia", min_value=19, max_value=28, step=1)
            pendidikan = st.selectbox("Pendidikan", ['SMA/SMK', 'D3', 'S1'])
            nilai_wawancara = st.number_input("Wawancara", min_value=0, max_value=35, step=1)
            nilai_tpa = st.number_input("Tes Potensi Akademik", min_value=0, max_value=20, step=1)
            nilai_keterampilan = st.number_input("Keterampilan", min_value=0, max_value=20, step=1)

            submit = st.form_submit_button("Submit")

            if submit:
                if pendidikan == "SMA/SMK":
                    pendidikan = 1
                elif pendidikan == "D3":
                    pendidikan = 2
                elif pendidikan == "S1":
                    pendidikan = 3

                st.session_state['test_svm'] = [usia, pendidikan, nilai_wawancara, nilai_tpa, nilai_keterampilan]

        if st.session_state['test_svm'] != False:
            data_test = st.session_state['test_svm']
            prediksi = np.dot(data_test, bobot) - bias
            if prediksi > 0 :
                prediksi = "Lolos"
            else:
                prediksi = "Tidak Lolos"

            st.write("Hasil Prediksi : {}".format(prediksi))
            st.session_state['test_svm'] = False
        
        else:
            st.write(f"Hasil Prediksi : None")

    elif choose == "Perangkingan":
        cek_data = getData(category_inp="All")

        email, nama, jenis_kelamin, usia, pendidikan, tes_wawancara, tpa, tes_keterampilan = [],[],[],[],[],[],[],[]
        if cek_data == False:
            data_df = {
                    'Email' : email,
                    'Nama Pelamar' : nama,
                    'Jenis Kelamin' : jenis_kelamin,
                    'Usia' : usia,
                    'Pendidikan' : pendidikan,
                    'Tes Wawancara' : tes_wawancara,
                    'Tes Potensi Akademik' : tpa,
                    'Tes Keterampilan Teknis' : tes_keterampilan
                }

            df = pd.DataFrame(data_df)
            st.table(df)
        else:
            for i in range(len(cek_data)):
                email.append(cek_data[i][0])
                nama.append(cek_data[i][1])
                jenis_kelamin.append(cek_data[i][2])
                usia.append(cek_data[i][3])
                pendidikan.append(cek_data[i][4])
                tes_wawancara.append(cek_data[i][5])
                tpa.append(cek_data[i][6])
                tes_keterampilan.append(cek_data[i][7])
                data_df = {
                    'Email' : email,
                    'Nama Pelamar' : nama,
                    'Jenis Kelamin' : jenis_kelamin,
                    'Usia' : usia,
                    'Pendidikan' : pendidikan,
                    'Tes Wawancara' : tes_wawancara,
                    'Tes Potensi Akademik' : tpa,
                    'Tes Keterampilan Teknis' : tes_keterampilan,
                }

            df = pd.DataFrame(data_df)

        data_svm = klasifikasi_svm(df)

        df['Klasifikasi SVM'] = data_svm['predict_svm']

        df['Klasifikasi SVM'] = df['Klasifikasi SVM'].replace({0 : 'Tidak Lolos', 1 : 'Lolos'})

        df_saw = df.loc[df['Klasifikasi SVM'] == "Lolos"]
        st.markdown('<h1 class="iv">Data Calon Karyawan Yang Lolos</h1>', unsafe_allow_html=True)
        st.table(df_saw)
        st.markdown('<h1 class="iv">Perangkingan SAW</h1>', unsafe_allow_html=True)
        if df_saw.empty == False:
            data_new = change_data(df)
            df = data_new[0]
            df = df.loc[df['Klasifikasi SVM'] == "Lolos"]

            # Menentukan Cost/Benefit
            min_usia = int(min(df['Usia']))
            max_pendidikan = int(max(df['Pendidikan']))
            max_wawancara = int(max(df['Tes Wawancara']))
            max_tpa = int(max(df['Tes Potensi Akademik']))
            max_keterampilan = int(max(df['Tes Keterampilan Teknis']))
            st.markdown("<h2 align='center'> ===== Menentukan Nilai Kriteria Cost & Benefit =====</h2>", unsafe_allow_html=True)
            buffer, col1, col2 = st.columns([.5, 6, 4])
            with col1:
                st.write("### == Kriteria Benefit")
                st.write(f"- Pendidikan : {max_pendidikan}\n- Wawancara : {max_wawancara}\n- TPA : {max_tpa}\n- Keterampilan : {max_keterampilan}")

                st.write("### == Kriteria Cost")
                st.write(f"- Usia : {min_usia}")

            # Normalisasi (Cost)
            st.markdown("<h2 align='center'> ===== Normalisasi =====</h2>", unsafe_allow_html=True)
            st.image('gambar/normalisasi.jpg')
            st.write("### == Normalisasi Cost")
            df['Usia'] = (min_usia / df['Usia'])
            st.table(df['Usia'])

            # Normalisasi (Benefit)
            st.write("### == Normalisasi Benefit")
            df['Pendidikan'] = (df['Pendidikan'] / max_pendidikan)
            df['Tes Wawancara'] = (df['Tes Wawancara'] / max_wawancara)
            df['Tes Potensi Akademik'] = (df['Tes Potensi Akademik'] / max_tpa)
            df['Tes Keterampilan Teknis'] = (df['Tes Keterampilan Teknis'] / max_keterampilan)
            st.table(df.iloc[:, 1:-1])

            st.markdown("<h2 align='center'> ===== Hasil Normalisasi =====</h2>", unsafe_allow_html=True)
            st.table(df)
            
            st.markdown("<h2 align='center'> ===== Bobot Kriteria =====</h2>", unsafe_allow_html=True)
            st.write("1. Usia : 0.2\n2. Pendidikan : 0.2\n3. Tes Wawancara : 0.2\n4. Tes Potensi Akademik : 0.2\n5. Tes Keterampilan Teknis : 0.2")
            
            df['Usia'] = df['Usia'] * 0.2
            df['Pendidikan'] = df['Pendidikan'] * 0.2
            df['Tes Wawancara'] = df['Tes Wawancara'] * 0.2
            df['Tes Potensi Akademik'] = df['Tes Potensi Akademik'] * 0.2
            df['Tes Keterampilan Teknis'] = df['Tes Keterampilan Teknis'] * 0.2

            df_saw['Total'] = df.iloc[:, :5].sum(axis = 1)
            st.markdown("<h2 align='center'> ===== Total Data =====</h2>", unsafe_allow_html=True)
            st.table(df)

            st.markdown("<h2 align='center'> ===== Perangkingan =====</h2>", unsafe_allow_html=True)

            df_saw['Rangking'] = df_saw['Total'].rank(ascending=0)
            df_saw['Rangking'] = df_saw['Rangking'].astype('int')
            df_saw = df_saw.sort_values(by=['Rangking'])
            st.table(df_saw)

    elif choose == 'Hasil':
        st.markdown('<h1 class="iv">Data Pelamar Kerja</h1>', unsafe_allow_html=True)

        # Dapatkan tanggal hari ini
        today = date.today()

        # Tambahkan input untuk memilih tanggal
        start_date = st.date_input('Tampilkan data dari tanggal', value=today)
        end_date = st.date_input('Sampai tanggal', value=today)

        
        filter_posisi = st.selectbox('Tampilkan data berdasarkan',('Staf Administrasi', 'Staf Operasional'))
        if st.button('Tampilkan Data'):
            cek_data = getDataByFilter(filter_posisi, start_date, end_date)
            if cek_data == False:
                st.warning("Data kosong")
        else:
            cek_data = getData(category_inp="All")


        email, nama, jenis_kelamin, usia, pendidikan, tes_wawancara, tpa, tes_keterampilan, posisi, tanggal = [],[],[],[],[],[],[],[],[],[]
        if cek_data == False:
            data_df = {
                    'Email' : email,
                    'Nama Pelamar' : nama,
                    'Jenis Kelamin' : jenis_kelamin,
                    'Usia' : usia,
                    'Pendidikan' : pendidikan,
                    'Tes Wawancara' : tes_wawancara,
                    'Tes Potensi Akademik' : tpa,
                    'Tes Keterampilan Teknis' : tes_keterampilan,
                    'Posisi yang dilamar' : posisi,
                    'Tanggal' : tanggal
                }

            df = pd.DataFrame(data_df)
            st.table(df)

        else:
            for i in range(len(cek_data)):
                email.append(cek_data[i][0])
                nama.append(cek_data[i][1])
                jenis_kelamin.append(cek_data[i][2])
                usia.append(cek_data[i][3])
                pendidikan.append(cek_data[i][4])
                tes_wawancara.append(cek_data[i][5])
                tpa.append(cek_data[i][6])
                tes_keterampilan.append(cek_data[i][7])
                posisi.append(cek_data[i][8])
                tanggal.append(cek_data[i][9])
                data_df = {
                    'Email' : email,
                    'Nama Pelamar' : nama,
                    'Jenis Kelamin' : jenis_kelamin,
                    'Usia' : usia,
                    'Pendidikan' : pendidikan,
                    'Tes Wawancara' : tes_wawancara,
                    'Tes Potensi Akademik' : tpa,
                    'Tes Keterampilan Teknis' : tes_keterampilan,
                    'Posisi yang dilamar' : posisi,
                    'Tanggal' : tanggal
                }

            df = pd.DataFrame(data_df)
            st.table(df)


        st.markdown('<h1 class="iv">Klasifikasi Data Pelamar</h1>', unsafe_allow_html=True)

        data_svm = df.iloc[: , :-2]
        data_svm = klasifikasi_svm(data_svm)

        df['Klasifikasi SVM'] = data_svm['predict_svm']

        df['Klasifikasi SVM'] = df['Klasifikasi SVM'].replace({0 : 'Tidak Lolos', 1 : 'Lolos'})

        st.table(df)

        df_saw = df.loc[df['Klasifikasi SVM'] == "Lolos"]
        

        st.markdown('<h1 class="iv">Perangkingan SAW</h1>', unsafe_allow_html=True)
        if df_saw.empty == False:
            rangking = perangkingan_saw(df_saw)

            st.table(rangking)
        else:
            st.markdown('<h1 align="center">Tidak ada peserta yang lolos',unsafe_allow_html=True)

        st.button("Hapus Semua Data", on_click=hapusAllData)
        
    

    # HALAMAN DATA AKUN
    elif choose == 'Data Akun':
        st.markdown('<h1 class="iv">Data Akun</h1>', unsafe_allow_html=True)
        
        option = st.selectbox('',
        ('Ubah & Hapus Akun', 'Tambah Akun'))
        if option == 'Ubah & Hapus Akun':
            ubahHapusAkun()
        if option == 'Tambah Akun':
            tambahAkun()
        
    # HALAMAN LOGOUT
    elif choose == 'Logout':
        st.session_state['session_login'] = ''
        st.success("Logout Berhasil")

