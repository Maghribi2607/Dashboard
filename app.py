import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Dividend Investment", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS: MENTOK KIRI & ATAS ---
st.markdown("""
    <style>
    /* Menghilangkan padding utama agar mentok ke atas dan kiri */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        margin-left: 0px;
    }
    
    /* Box Metrik Compact */
    [data-testid="stMetric"] {
        background-color: #4e567d; 
        padding: 5px 12px;
        border-radius: 8px;
        border: 1px solid #7a84b8;
    }
    
    [data-testid="stMetricLabel"] { font-size: 12px !important; margin-bottom: -5px; }
    [data-testid="stMetricValue"] { font-size: 20px !important; color: #00ffd5 !important; }
    
    /* Menghilangkan space antar elemen */
    div.element-container { margin-bottom: -0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIHAN DATA ---
def clean_data(v):
    if pd.isna(v) or v == '': return 0.0
    s = str(v).replace('Rp', '').replace('%', '').replace(' ', '').strip()
    if '.' in s and ',' in s: s = s.replace('.', '').replace(',', '.')
    elif ',' in s: s = s.replace(',', '.')
    elif '.' in s:
        if len(s.split('.')[-1]) == 3: s = s.replace('.', '')
    try: return float(s)
    except: return 0.0

def format_short(val):
    if val >= 1_000_000: return f"Rp {val / 1_000_000:.1f} M"
    return f"Rp {val:,.0f}"

# 2. SIDEBAR
with st.sidebar:
    st.title("📊 Navigasi")
    menu = st.radio("Pilih Menu:", ["💰 Dividend"])

# 3. KONEKSI DATA
sheet_id = "1dq6pkbFbNPkgV4wtOBg15h4TM0xi-mKxDME2cPTTtq0"
export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Dividend"

try:
    df = pd.read_csv(export_url)
    cols = ['REALIZATION', 'BUDGET', 'DIV PREDICTION', 'DY PREDICTION', 'DY FROM AVERAGE', 'DY FROM PRICE NOW']
    for c in cols:
        if c in df.columns: df[c] = df[c].apply(clean_data)

    if menu == "💰 Dividend":
        # Header kecil mentok atas
        st.markdown("### Dividend Investment Monitoring")
        
        # --- BARIS 1: KOTAK METRIK (Compact & Rapat) ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Investment", format_short(df['REALIZATION'].sum()))
        m2.metric("Budget", format_short(df['BUDGET'].sum()))
        m3.metric("Div Pred", format_short(df['DIV PREDICTION'].sum()))
        m4.metric("DY Pred", f"{df['DY PREDICTION'].mean():.1f}%")

        st.markdown("<br>", unsafe_allow_html=True) # Jarak kecil

        # --- BARIS 2: PIE & BAR REALIZATION (Sejajar Tinggi & Lebar) ---
        col_pie, col_bar = st.columns([1, 1.2])

        with col_pie:
            st.caption("**Alokasi Saham**")
            fig_pie = px.pie(df, values='REALIZATION', names='EMITTEN', hole=0.4, height=250)
            fig_pie.update_layout(
                margin=dict(t=10, b=10, l=0, r=0),
                legend=dict(
                    orientation="v",
                    yanchor="middle", y=0.5, 
                    xanchor="left", x=1.0,
                    font=dict(size=10)
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar:
            st.caption("**Realization by Ticker**")
            df_sorted = df.sort_values('REALIZATION', ascending=True)
            fig_real = px.bar(df_sorted, x='REALIZATION', y='EMITTEN', orientation='h',
                              text='REALIZATION', color='REALIZATION', 
                              color_continuous_scale='Blues', height=250)
            fig_real.update_traces(
                texttemplate='Rp %{text:,.0f}', textposition='inside', textfont_size=9
            )
            fig_real.update_layout(
                margin=dict(t=10, b=10, l=0, r=0),
                xaxis_visible=False, yaxis_title="", coloraxis_showscale=False
            )
            st.plotly_chart(fig_real, use_container_width=True)

        # --- BARIS 3: YIELD COMPARISON (Legend di bawah & Warna Pastel) ---
        st.caption("**Yield Comparison: Average vs Price Now**")
        df_melt = df.melt(id_vars='EMITTEN', value_vars=['DY FROM AVERAGE', 'DY FROM PRICE NOW'])
        
        # Penyesuaian warna pastel: Hijau untuk Average, Merah untuk Price Now
        fig_yield = px.bar(df_melt, x='EMITTEN', y='value', color='variable', barmode='group',
                           text='value', height=260, 
                           color_discrete_map={
                               "DY FROM AVERAGE": "#A8E6CF",  # Hijau Pastel
                               "DY FROM PRICE NOW": "#FF8B94" # Merah Pastel
                           })
        
        fig_yield.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=10)
        fig_yield.update_layout(
            margin=dict(t=20, b=40, l=0, r=0),
            xaxis_title="", yaxis_title="",
            # Legend dipindah ke bawah (bottom)
            legend=dict(
                orientation="h", 
                yanchor="top", y=-0.2, 
                xanchor="center", x=0.5, 
                font=dict(size=10),
                title_text=""
            ),
            xaxis_tickfont_size=11
        )
        st.plotly_chart(fig_yield, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")