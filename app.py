import streamlit as st  # Mengimport library Streamlit untuk membangun web dashboard
import pandas as pd     # Mengimport library Pandas untuk memproses dan memanipulasi data tabel
import plotly.express as px  # Mengimport Plotly Express untuk membuat grafik interaktif

# 1. KONFIGURASI HALAMAN
# Mengatur judul tab browser menjadi "FinTrackQ" dan tata letak melebar (wide) agar pas di layar
st.set_page_config(page_title="FinTrackQ", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS: MENTOK KIRI, ATAS, SERTA STYLE TOMBOL NAVIGASI 3D ---
# Menyisipkan kode CSS khusus ke dalam Streamlit untuk memodifikasi tampilan visual (user interface)
st.markdown("""
    <style>
    /* Menghilangkan padding utama agar posisi seluruh dashboard mentok ke paling atas dan kiri */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        margin-left: 0px;
    }
    
    /* Mengatur style kotak metrik: warna latar abu-biru terang, padding tipis, dan border melengkung */
    [data-testid="stMetric"] {
        background-color: #4e567d; 
        padding: 5px 12px;
        border-radius: 8px;
        border: 1px solid #7a84b8;
    }
    
    /* Mengatur ukuran teks label metrik di bagian atas agar kecil dan rapat */
    [data-testid="stMetricLabel"] { font-size: 12px !important; margin-bottom: -5px; }
    
    /* Mengatur ukuran angka metrik dan memberi warna hijau cyan cerah agar kontras */
    [data-testid="stMetricValue"] { font-size: 20px !important; color: #00ffd5 !important; }
    
    /* Memperkecil jarak (space) vertikal antar elemen widget Streamlit agar tidak renggang */
    div.element-container { margin-bottom: -0.8rem; }

    /* --- GAYA TOMBOL 3D DI SIDEBAR --- */
    /* Mengatur style khusus tombol navigasi di sidebar agar memiliki efek timbul (3D) dan jarak ideal */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: left;
        background-color: #2b304a;
        color: #ffffff;
        border: 1px solid #43496e;
        /* Memberikan efek bayangan (shadow border) tebal di bawah untuk kesan tombol 3D */
        box-shadow: 0px 4px 0px #181b2a;
        transition: all 0.1s ease;
    }

    /* Efek ketika tombol dilewati oleh kursor mouse */
    .stButton > button:hover {
        background-color: #353b5c;
        border-color: #555c8a;
        color: #00ffd5;
    }

    /* Efek ketika tombol sedang diklik (ditekan ke bawah layaknya tombol fisik) */
    .stButton > button:active {
        box-shadow: 0px 1px 0px #181b2a;
        transform: translateY(3px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIHAN DATA ---
# Fungsi untuk membersihkan teks mata uang/persen dari Google Sheets menjadi angka desimal (float) yang bisa dihitung
def clean_data(v):
    if pd.isna(v) or v == '': return 0.0  # Jika data kosong atau NaN, kembalikan nilai 0.0
    s = str(v).replace('Rp', '').replace('%', '').replace(' ', '').strip()  # Hapus simbol Rp, persen, dan spasi
    if '.' in s and ',' in s: s = s.replace('.', '').replace(',', '.')  # Jika format ribuan Indonesia (1.000,00) ubah ke format standar (1000.00)
    elif ',' in s: s = s.replace(',', '.')  # Jika hanya ada koma, anggap sebagai penanda desimal
    elif '.' in s:
        if len(s.split('.')[-1]) == 3: s = s.replace('.', '')  # Jika titik diikuti 3 angka, itu adalah penanda ribuan, maka hapus titiknya
    try: return float(s)  # Ubah string teks bersih menjadi angka desimal
    except: return 0.0  # Jika gagal konversi (misal teks tulisan), kembalikan 0.0

# Fungsi untuk memformat angka penuh utuh dengan pemisah ribuan titik tanpa ringkasan singkatan M (Permintaan No. 2)
def format_full_rp(val):
    return f"Rp {val:,.0f}".replace(',', '.')  # Memformat angka ke format ribuan rupiah utuh standar Indonesia

# 2. SIDEBAR (NAVIGASI CUSTOM TOMBOL 3D)
# --- 2. SIDEBAR (NAVIGASI CUSTOM TOMBOL 3D DENGAN LOGO) ---
with st.sidebar:
    
    # --- TAMBAHKAN LOGO BARU DI SINI ---
    # Menentukan nama file gambar logo Anda
    logo_filename = "Logo.png" # Sesuaikan nama filenya
    
    # Import library os untuk mengecek file
    import os
    
    # Mengecek keberadaan file logo
    if os.path.exists(logo_filename):
        # Menampilkan gambar logo. 
        # use_container_width=True memastikan lebar logo mengikuti lebar sidebar.
        st.image(logo_filename, use_container_width=True)
    else:
        # Teks cadangan jika file gambar tidak ditemukan
        st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 20px;'>FinTrackQ</h2>", unsafe_allow_html=True)

    # Menyisipkan jarak (space) di bawah logo agar proporsional
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Inisialisasi session state untuk menyimpan halaman aktif jika belum ada sistem pencatatan
    if 'page' not in st.session_state:
        st.session_state.page = "💰 Dividend"
        
    # Membuat tombol 3D untuk menu Dividend
    if st.button("💰 Dividend", key="btn_div", use_container_width=True):
        st.session_state.page = "💰 Dividend"
        
    # Menyisipkan jarak (space) antar tombol agar tidak terlalu berdekatan
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        
    # Membuat tombol 3D untuk menu Gold
    if st.button("🏆 Gold", key="btn_gold", use_container_width=True):
        st.session_state.page = "🏆 Gold"

# Alamat ID Google Sheets yang digunakan sebagai database
sheet_id = "1dq6pkbFbNPkgV4wtOBg15h4TM0xi-mKxDME2cPTTtq0"

# --- LOGIKA MENU 1: DIVIDEND ---
if st.session_state.page == "💰 Dividend":
    # Membuat URL khusus untuk menarik data dari tab bernama 'Dividend' dalam format CSV
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Dividend"
    
    try:
        df = pd.read_csv(export_url)  # Membaca data Google Sheets langsung ke dalam DataFrame Pandas
        # Daftar kolom yang berisi angka finansial dan perlu dibersihkan menggunakan fungsi clean_data
        cols = ['REALIZATION', 'BUDGET', 'DIV PREDICTION', 'DY PREDICTION', 'DY FROM AVERAGE', 'DY FROM PRICE NOW']
        for c in cols:
            if c in df.columns: df[c] = df[c].apply(clean_data)  # Terapkan pembersihan data per kolom jika kolomnya ada

        st.markdown("### Dividend Investment Monitoring")  # Menampilkan judul subheader menu
        
        # BARIS 1: KOTAK METRIK (Membagi layar menjadi 4 kolom sejajar)
        m1, m2, m3, m4 = st.columns(4)
        
        # Menampilkan metrik dengan menjabarkan angka penuh menggunakan fungsi format_full_rp (Permintaan No. 2)
        m1.metric("Total Investment", format_full_rp(df['REALIZATION'].sum()))  # Menampilkan angka penuh total REALIZATION
        m2.metric("Budget", format_full_rp(df['BUDGET'].sum()))                # Menampilkan angka penuh total BUDGET
        
        # Mengubah teks label menjadi "Dividend Prediction" dan "DY Prediction" (Permintaan No. 3)
        m3.metric("Dividend Prediction", format_full_rp(df['DIV PREDICTION'].sum())) # Menampilkan angka penuh Dividend Prediction
        m4.metric("DY Prediction", f"{df['DY PREDICTION'].mean():.1f}%")          # Menampilkan rata-rata persentase DY Prediction

        st.markdown("<br>", unsafe_allow_html=True)  # Memberikan jarak vertikal kecil sebelum baris grafik

        # BARIS 2: GRAFIK ALOKASI (PIE) & REALIZATION (BAR)
        col_pie, col_bar = st.columns([1, 1.2])  # Membagi layar menjadi 2 kolom dengan rasio lebar 1 banding 1.2

        with col_pie:
            st.caption("**Alokasi Saham**")  # Memberi teks judul kecil di atas grafik
            fig_pie = px.pie(df, values='REALIZATION', names='EMITTEN', hole=0.4, height=250)  # Membuat Donut Chart
            fig_pie.update_layout(
                margin=dict(t=10, b=10, l=0, r=0),  # Mengatur margin internal grafik agar pas
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0, font=dict(size=10))  # Legend vertikal di kanan
            )
            st.plotly_chart(fig_pie, use_container_width=True)  # Menampilkan grafik pie ke layar

        with col_bar:
            st.caption("**Realization by Ticker**")  # Memberi teks judul kecil di atas grafik bar
            df_sorted = df.sort_values('REALIZATION', ascending=True)  # Mengurutkan data dari nominal terkecil ke terbesar
            # Membuat grafik batang horizontal (orientation='h')
            fig_real = px.bar(df_sorted, x='REALIZATION', y='EMITTEN', orientation='h',
                              text='REALIZATION', color='REALIZATION', color_continuous_scale='Blues', height=250)
            fig_real.update_traces(texttemplate='Rp %{text:,.0f}', textposition='inside', textfont_size=9)  # Format teks rupiah di dalam bar
            fig_real.update_layout(margin=dict(t=10, b=10, l=0, r=0), xaxis_visible=False, yaxis_title="", coloraxis_showscale=False)  # Sembunyikan skala warna
            st.plotly_chart(fig_real, use_container_width=True)  # Menampilkan grafik bar ke layar

        # BARIS 3: YIELD COMPARISON (GRAFIK BATANG LEBAR PENUH)
        st.caption("**Yield Comparison: Average vs Price Now**")  # Judul grafik bar bawah
        df_melt = df.melt(id_vars='EMITTEN', value_vars=['DY FROM AVERAGE', 'DY FROM PRICE NOW'])  # Mengubah struktur tabel agar bisa dikelompokkan
        
        # Membuat grup bar chart dengan pemetaan warna pastel khusus (Hijau & Merah)
        fig_yield = px.bar(df_melt, x='EMITTEN', y='value', color='variable', barmode='group',
                           text='value', height=260, 
                           color_discrete_map={"DY FROM AVERAGE": "#A8E6CF", "DY FROM PRICE NOW": "#FF8B94"})
        fig_yield.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=10)  # Menampilkan angka persen di luar ujung bar
        fig_yield.update_layout(
            margin=dict(t=20, b=40, l=0, r=0), xaxis_title="", yaxis_title="",
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=10), title_text=""),  # Legend horizontal di bawah
            xaxis_tickfont_size=11
        )
        st.plotly_chart(fig_yield, use_container_width=True)  # Menampilkan grafik yield ke layar

    except Exception as e:
        st.error(f"Error: {e}")  # Tampilkan pesan error jika terjadi kegagalan sistem menarik data

# --- LOGIKA MENU 2: GOLD ---
elif st.session_state.page == "🏆 Gold":
    # Membuat URL khusus untuk menarik data dari tab bernama 'Gold' dalam format CSV dari Google Sheets
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Gold"
    
    try:
        df_gold = pd.read_csv(export_url)  # Membaca data Google Sheets tab Gold ke dalam DataFrame df_gold
        
        # Membersihkan kolom-kolom penting agar bertipe angka desimal (float)
        gold_cols = ['Jumlah', 'XAUUSD', 'Total Emas', 'Prakira Harga Emas', 'Profit', 'Close']
        for c in gold_cols:
            if c in df_gold.columns: 
                df_gold[c] = df_gold[c].apply(clean_data)

        st.markdown("### Gold Investment Monitoring")  # Menampilkan judul halaman utama untuk menu Gold
        
        # Membagi area metrik menjadi 5 kolom sejajar untuk menampung kotak Kurs USD IDR di depan
        g0, g1, g2, g3, g4 = st.columns(5)
        
        # --- PERBAIKAN SISTEM AMBIL DATA KURS PALING AKHIR/UPDATE (Permintaan No. 1) ---
        # Memfilter data baris kolom 'Close' yang valid (di atas angka 0)
        df_close_valid = df_gold[df_gold['Close'] > 0]
        # Menggunakan .iloc[-1] untuk mengambil nilai data pada baris PALING AKHIR (paling update = 17.603)
        val_close_akhir = df_close_valid['Close'].iloc[-1] if not df_close_valid.empty else 0.0
        # Menampilkan nilai terupdate Kurs USD IDR ke dalam kotak pertama (g0)
        g0.metric("Kurs USD IDR", format_full_rp(val_close_akhir))
        
        # METRIK 2: XAUUSD (Mencari baris pertama yang berisi angka > 0)
        df_xau_valid = df_gold[df_gold['XAUUSD'] > 0]
        val_xau = df_xau_valid['XAUUSD'].iloc[0] if not df_xau_valid.empty else 0.0
        g1.metric("XAUUSD", f"$ {val_xau:,.2f}")
        
        # METRIK 3: TOTAL GOLD
        total_emas = df_gold['Jumlah'].sum() if 'Jumlah' in df_gold.columns else 0.0
        g2.metric("Total Gold", f"{total_emas:,.2f} gram")
        
        # METRIK 4: GOLD PRICE (Menggunakan fungsi format_full_rp agar angka muncul utuh penuh)
        df_harga_valid = df_gold[df_gold['Prakira Harga Emas'] > 0]
        val_harga_emas = df_harga_valid['Prakira Harga Emas'].iloc[0] if not df_harga_valid.empty else 0.0
        g3.metric("Gold Price", format_full_rp(val_harga_emas))
        
        # METRIK 5: PROFIT PREDICTION (Menggunakan fungsi format_full_rp agar angka muncul utuh penuh)
        df_profit_valid = df_gold[df_gold['Profit'] > 0]
        val_profit_pred = df_profit_valid['Profit'].iloc[0] if not df_profit_valid.empty else 0.0
        g4.metric("Profit Prediction", format_full_rp(val_profit_pred))

        st.markdown("<br>", unsafe_allow_html=True)  # Menyisipkan jarak vertikal kecil

        # Membagi baris grafik menjadi 2 kolom sama besar
        col_left, col_right = st.columns([1, 1])
        
        # ISI KOLOM KIRI (GRAFIK KURS)
        with col_left:
            st.caption("**Kurs USD-IDR**")
            if 'Date' in df_gold.columns and 'Close' in df_gold.columns:
                
                df_kurs_clean = df_gold.copy()  # Mengkloning data agar tidak merusak data asli
                df_kurs_clean['Date'] = df_kurs_clean['Date'].astype(str).str.strip()  # Bersihkan spasi penulisan tanggal
                
                # Filter: Buang data baris kosong yang tidak valid
                df_kurs_clean = df_kurs_clean[
                    (df_kurs_clean['Date'] != '') & 
                    (df_kurs_clean['Date'] != 'nan') & 
                    (df_kurs_clean['Close'] > 0)
                ]
                
                if not df_kurs_clean.empty:
                    # Membuat objek grafik garis tren kurs
                    fig_kurs = px.line(df_kurs_clean, x='Date', y='Close', height=250)
                    
                    # Menampilkan Angka Langsung & Besar pada line chart harian
                    fig_kurs.update_traces(
                        line_color='#4facfe', 
                        line_width=2,
                        mode='lines+markers+text', # Menampilkan garis, titik penanda, sekaligus teks angka harian
                        text=df_kurs_clean['Close'].apply(lambda x: f"{x:,.0f}"), # Format angka teks tanpa desimal ribuan
                        textposition='top center', # Posisi teks berada tepat di atas titik koordinat
                        textfont=dict(size=11, color='white') # Mengatur ukuran text angka agar lebih besar dan jelas
                    )
                    
                    # Mengatur sumbu Y agar otomatis nge-zoom sesuai rentang data real harian
                    fig_kurs.update_yaxes(autorange=True, fixedrange=False)
                    fig_kurs.update_layout(margin=dict(t=25, b=10, l=0, r=0), xaxis_title="", yaxis_title="")
                    st.plotly_chart(fig_kurs, use_container_width=True)
                else:
                    st.warning("Tidak ada data Kurs (Date & Close) yang valid untuk ditampilkan.")
            else:
                st.warning("Kolom 'Date' atau 'Close' tidak ditemukan di sheet Gold.")

        # ISI KOLOM KANAN (GRAFIK PEMBELIAN EMAS)
        with col_right:
            st.caption("**Gold Purchase**")
            if 'Tahun' in df_gold.columns and 'Jumlah' in df_gold.columns:
                df_purchase = df_gold.dropna(subset=['Tahun', 'Jumlah'])  # Hapus baris kosong
                df_purchase = df_purchase[df_purchase['Jumlah'] > 0]       # Ambil pembelian di atas nol
                
                if not df_purchase.empty:
                    fig_purchase = px.bar(df_purchase, x='Tahun', y='Jumlah', text='Jumlah', height=250, color_discrete_sequence=['#FFD700'])
                    fig_purchase.update_traces(texttemplate='%{text:.2f}g', textposition='outside', textfont_size=9)
                    fig_purchase.update_layout(margin=dict(t=20, b=10, l=0, r=0), xaxis_title="", yaxis_title="", xaxis_type='category')
                    st.plotly_chart(fig_purchase, use_container_width=True)
                else:
                    st.warning("Tidak ada data pembelian emas untuk ditampilkan.")
            else:
                st.warning("Kolom 'Tahun' atau 'Jumlah' tidak ditemukan di sheet Gold.")

    except Exception as e:
        st.error(f"Error pada menu Gold: {e}")