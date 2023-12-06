import sqlite3
import streamlit as st
import pandas as pd
conn = sqlite3.connect('db_setik.db', check_same_thread=False)
curr = conn.cursor()
import base64
import streamlit_nested_layout
import numpy as np

if 'input_lowongan' not in st.session_state:
    st.session_state['input_lowongan'] = ""


def addData(idAdmin_inp,nama_inp,password_inp):
    curr.execute("INSERT INTO tb_akun VALUES (?,?,?)", (idAdmin_inp,nama_inp,password_inp))
    conn.commit()
    
def addDataPelamar (email_inp,nama_inp,jk_inp,usia_inp,pendidikan_inp,wawancara_inp,tpa_inp,keterampilan_inp,posisi_inp,tanggal_inp):
    try:
        curr.execute("""INSERT INTO tb_pelamar (nama_pelamar, email,
                    jenis_kelamin, usia, pendidikan, wawancara, tpa, keterampilan, posisi, tanggal)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""", (email_inp,nama_inp,jk_inp,usia_inp,pendidikan_inp,wawancara_inp,tpa_inp,keterampilan_inp,posisi_inp,tanggal_inp)) 
        conn.commit()
        return True
    except Exception:
        return False

def ubahDataPelamar(email_inp,nama_inp,jk_inp,usia_inp,pendidikan_inp,wawancara_inp,tpa_inp,keterampilan_inp,posisi_inp,tanggal_inp):
    curr.execute(f"""UPDATE tb_pelamar SET nama_pelamar='{nama_inp}', jenis_kelamin='{jk_inp}', usia='{usia_inp}', pendidikan='{pendidikan_inp}', wawancara='{wawancara_inp}', tpa='{tpa_inp}', keterampilan='{keterampilan_inp}', posisi='{posisi_inp}', tanggal='{tanggal_inp}'
    WHERE email='{email_inp}'""")
    conn.commit()

def hapusDataAkun(idAdmin_inp):
    curr.execute(f"DELETE FROM tb_akun WHERE id_admin={idAdmin_inp}")
    conn.commit()

def editDataAkun(nama_inp=None, pw_inp=None, idAdmin_inp=None) :
    curr.execute(f"UPDATE tb_akun SET nama='{nama_inp}', password='{pw_inp}' WHERE id_admin={idAdmin_inp}")
    conn.commit()

def hapusAllData():
    curr.execute("DELETE FROM tb_pelamar")
    conn.commit()

def hapusDataPelamar(email_inp):
    curr.execute(f"DELETE FROM tb_pelamar WHERE email='{email_inp}'")
    conn.commit()


def cek_login(id_admin,pw):
    try:
        curr.execute('SELECT*FROM tb_akun WHERE id_admin=? AND password=?',(id_admin,pw))
        data = curr.fetchone()
        st.session_state['session_login'] = data[0]
        return True
    except Exception:
        return False

def getData(category_inp = None):
    if category_inp == "All":
        statement = "SELECT * from tb_pelamar;"

    curr.execute(statement)
    rows = curr.fetchall()
    if not rows:
        return False
    else:
        data_empty = []
        for row in rows:
            data_empty.append(row)
        return data_empty
    
def getDataByFilter(posisi, start_date, end_date):
    curr.execute(f"SELECT*FROM tb_pelamar WHERE posisi='{posisi}' AND tanggal BETWEEN '{start_date}' AND '{end_date}';")
    data1 = curr.fetchall()
    if int(len(data1)) > 0:
        return data1
    else:
        return False

def getDataAkun(idAdmin_inp = None, category_inp = None):
    if category_inp == "All":
        statement = f"SELECT * from tb_akun;"
    else:
        statement = f"SELECT * from tb_akun WHERE id_admin = '{idAdmin_inp}';"

    curr.execute(statement)
    rows = curr.fetchall()
    if not rows:
        return False
    else:
        data_empty = []
        for row in rows:
            data_empty.append(row)
        return data_empty
    
def ubahHapusAkun():
    cek_data = getDataAkun(category_inp="All")
    id_admin, nama, pw = [],[],[]
    for i in range(len(cek_data)):
        id_admin.append(cek_data[i][0])
        nama.append(cek_data[i][1])
        pw.append(cek_data[i][2])
    data_df = {
        'ID_Admin' : id_admin,
        'Nama' : nama,
        'Password' : pw
    }
    df = pd.DataFrame(data_df)
    st.table(df)

    option = st.selectbox("Pilih Data Berdasarkan ID Admin", df.ID_Admin, 0)
    selected_id_admin = option
    selected_nama = df.loc[df.ID_Admin == option]["Nama"].iloc[0]
    selected_password = df.loc[df.ID_Admin == option]["Password"].iloc[0]
    

    placeholder = st.empty()
    with placeholder.form(key="data_akun"):
        nama = st.text_input("Nama", value=selected_nama)
        pw = st.text_input("Password", value=selected_password)
        hapus = st.form_submit_button("Hapus")
        edit = st.form_submit_button(label="Edit")

        if hapus==True:
            hapusDataAkun(selected_id_admin)
            st.success("Data berhasil dihapus")

        if edit==True:
            cek_edit = editDataAkun(nama, pw, selected_id_admin)
            if cek_edit != True:
                st.success("Edit Data Berhasil !")
            else:
                st.warning("Edit Data Gagal !")

def tambahAkun():
    cek_data = getDataAkun(category_inp="All")
    id_admin, nama, pw = [],[],[]
    for i in range(len(cek_data)):
        id_admin.append(cek_data[i][0])
        nama.append(cek_data[i][1])
        pw.append(cek_data[i][2])
    data_df = {
        'ID_Admin' : id_admin,
        'Nama' : nama,
        'Password' : pw
    }
    df = pd.DataFrame(data_df)
    st.table(df)

    placeholder = st.empty()
    with placeholder.form(key="data_akun"):
        id = st.text_input("ID Admin")
        nama = st.text_input("Nama")
        pw = st.text_input("Password")
        tambah = st.form_submit_button(label="Tambah")
        if tambah==True:
            addData(id,nama,pw)
            st.success("Akun berhasil ditambahkan")

def form_login():
    st.markdown("""
            <style>
            .iv {
                background-color: #639cd9;
                color: white;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
    st.markdown('<h1 class="iv"> Form Login </h1>', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    buffer, col1, col2 = st.columns([2.5, 5, 2.5])
    with col1:
        placeholder = st.empty()
        with placeholder.form(key="form login"):
            col3, col4= st.columns([.7,9.3])
            with col3:
                st.write(" ")
                st.write(" ")
                st.markdown('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/></svg>', unsafe_allow_html=True)
                st.write(" ")
                st.write(" ")
                st.markdown('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-lock-fill" viewBox="0 0 16 16"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>', unsafe_allow_html=True)
            with col4:
                id_admin = st.text_input(" ", placeholder="ID Admin")
                pw = st.text_input(" ",type='password', placeholder='Password')
                st.write(" ")
                btn_login = st.form_submit_button(label="Login")
                st.write(" ")
                if btn_login == True and id_admin != "" and pw != "":
                    result = cek_login(id_admin,pw)
                    if result:
                        st.success("Berhasil Login")
                    else:
                        st.warning("Data Salah")
                elif btn_login == True and (id_admin == "" or pw == ""):
                    st.warning("Data Belum Diisi Lengkap!")
            

def change_data(df):
        df_new = df.iloc[:, 3:]

        for i in range(len(df_new)):

            if df_new['Pendidikan'][i] == "SMA/SMK":
                df_new['Pendidikan'][i] = 1
            elif df_new['Pendidikan'][i] == "D3":
                df_new['Pendidikan'][i] = 2
            elif df_new['Pendidikan'][i] == "S1":
                df_new['Pendidikan'][i] = 3

        return [df_new]


def perangkingan_saw(df):
    # merubah dataframe ke dictionary
    df_dict = df.to_dict(orient='list')
    data_saw = {
        'Usia' : df_dict['Usia'],
        'Pendidikan' : df_dict['Pendidikan'],
        'Tes Wawancara' : df_dict['Tes Wawancara'],
        'Tes Potensi Akademik' : df_dict['Tes Potensi Akademik'],
        'Tes Keterampilan Teknis' : df_dict['Tes Keterampilan Teknis'],
    }

    # Merubah data string ke numeric
    for index, data in enumerate(data_saw['Pendidikan']):
        if str(data) == "SMA/SMK":
            data_saw['Pendidikan'][index] = 1
        
        elif str(data)  == "D3":
            data_saw['Pendidikan'][index] = 2

        elif str(data)  == "S1":
            data_saw['Pendidikan'][index] = 3


    # Menentukan nilai Cost dan Benefit
    min_usia = min(data_saw['Usia'])
    max_pendidikan = max(data_saw['Pendidikan'])
    max_wawancara = max(data_saw['Tes Wawancara'])
    max_tpa = max(data_saw['Tes Potensi Akademik'])
    max_keterampilan = max(data_saw['Tes Keterampilan Teknis'])

    # Normalisasi Cost dan benefit
    columns = ['Usia', 'Pendidikan', 'Tes Wawancara', 'Tes Potensi Akademik', 'Tes Keterampilan Teknis']
    for column in columns:
        if column == "Usia":
            data_saw["Usia"] = [min_usia / x for x in data_saw["Usia"]]

        elif column == "Pendidikan":
            data_saw["Pendidikan"] = [x / max_pendidikan for x in data_saw["Pendidikan"]]

        elif column == "Tes Wawancara":
            data_saw["Tes Wawancara"] = [x / max_wawancara for x in data_saw["Tes Wawancara"]]

        elif column == "Tes Potensi Akademik":
            data_saw["Tes Potensi Akademik"] = [x / max_tpa for x in data_saw["Tes Potensi Akademik"]]

        elif column == "Tes Keterampilan Teknis":
            data_saw["Tes Keterampilan Teknis"] = [x / max_keterampilan for x in data_saw["Tes Keterampilan Teknis"]]   

    # Menginisialisasi bobot tiap kriteria
    bobot_usia = 0.2
    bobot_pendidikan = 0.2 
    bobot_wawancara = 0.2
    bobot_tpa = 0.2
    bobot_keterampilan = 0.2
    
    # Mengalikan hasil normalisasi nilai dengan masing-masing bobot
    for column in data_saw.keys():
        if column == "Usia":
            data_saw["Usia"] = [x * bobot_usia for x in data_saw["Usia"]]

        elif column == "Pendidikan":
            data_saw["Pendidikan"] = [x * bobot_pendidikan for x in data_saw["Pendidikan"]]

        elif column == "Tes Wawancara":
            data_saw["Tes Wawancara"] = [x * bobot_wawancara for x in data_saw["Tes Wawancara"]]

        elif column == "Tes Potensi Akademik":
            data_saw["Tes Potensi Akademik"] = [x * bobot_tpa for x in data_saw["Tes Potensi Akademik"]]

        elif column == "Tes Keterampilan Teknis":
            data_saw["Tes Keterampilan Teknis"] = [x * bobot_keterampilan for x in data_saw["Tes Keterampilan Teknis"]]

    #  Menjumlahkan nilai pada tiap alternatif
    data_row = []
    for i in range(len(data_saw['Pendidikan'])):
        value = 0
        for key in data_saw.keys():
            value += data_saw[key][i]
        data_row.append(value)
    
    data_saw['Total'] = data_row

    rank = sorted(data_saw['Total'], reverse=True)
    new_rank = {}

    for idx, i in enumerate(rank):
        new_rank[idx + 1] = i

    rank = []
    for i in data_saw['Total']:
        for j in new_rank.items():
            if i == j[1]:
                print(j)
                rank.append(j[0])

    
    # # Menambahkan kolom Ranking ke dala
    data_saw['Rangking'] = rank
    df_dict['Total'] = data_row
    df_dict['Rangking'] = rank



    # Menggabungkan semua kolom menjadi satu set data yang bisa diurutkan
    combined_data = list(zip(df_dict['Email'], df_dict['Nama Pelamar'], df_dict['Jenis Kelamin'], df_dict["Usia"], df_dict["Pendidikan"], df_dict["Tes Wawancara"],
                            df_dict["Tes Potensi Akademik"], df_dict["Tes Keterampilan Teknis"], df_dict["Total"],
                            df_dict["Rangking"]))

    # Mengurutkan berdasarkan kolom Rangking
    sorted_data = sorted(combined_data, key=lambda x: x[-1])

    # Memisahkan kembali kolom-kolom setelah diurutkan
    sorted_columns = list(zip(*sorted_data))

    # Mengubah kembali menjadi dictionary
    sorted_dict = {
        "Email": sorted_columns[0],
        "Nama Pelamar": sorted_columns[1],
        "Jenis Kelamin": sorted_columns[2],
        "Usia": sorted_columns[3],
        "Pendidikan": sorted_columns[4],
        "Tes Wawancara": sorted_columns[5],
        "Tes Potensi Akademik": sorted_columns[6],
        "Tes Keterampilan Teknis": sorted_columns[7],
        "Total" : sorted_columns[8],
        "Rangking": sorted_columns[9]
    }

    return pd.DataFrame(sorted_dict)