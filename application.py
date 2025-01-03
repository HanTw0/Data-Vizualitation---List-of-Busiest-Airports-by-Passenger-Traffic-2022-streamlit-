import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Memuat dataset
file_path = 'modified_busiest_airports_2022.csv'  # Sesuaikan dengan path Anda
data = pd.read_csv(file_path)

# Mengubah nama kolom agar kompatibel dengan Streamlit map dan Pydeck
data = data.rename(columns={'lat': 'latitude', 'long': 'longitude'})

# Judul aplikasi Streamlit
st.title("Dashboard Bandara Tersibuk di Dunia (2022)")

st.markdown("""
Dashboard ini memberikan wawasan tentang 50 bandara tersibuk di dunia, termasuk peringkat, statistik penumpang, distribusi geografis, tren global, dan analisis mendalam berdasarkan negara.
""")

# Konten sidebar
st.sidebar.header("Tentang Dashboard Ini")
st.sidebar.markdown("""
Dashboard ini menyoroti:
- **Bandara Tersibuk**: Mengidentifikasi bandara yang menjadi hub utama perjalanan udara global.
- **Distribusi Geografis**: Menunjukkan pola aktivitas bandara di seluruh dunia.
- **Fokus Regional**: Memberikan analisis terperinci berdasarkan negara pilihan Anda.
- **Tren Global**: Menyoroti distribusi total penumpang berdasarkan peringkat.
- **Perbandingan Bandara**: Menganalisis bandara dengan ukuran relatif.
""")

st.sidebar.header("Statistik Utama")
st.sidebar.metric("Jumlah Bandara", data.shape[0])
st.sidebar.metric("Total Penumpang", f"{data['Total passengers'].sum():,}")

# Dropdown filter di halaman utama
st.subheader("Filter berdasarkan Negara")
negara_dipilih = st.selectbox(
    "Pilih Negara",
    options=["Semua"] + list(data['Country'].unique()),
    index=0
)

# Menerapkan filter
if negara_dipilih == "Semua":
    data_terfilter = data
else:
    data_terfilter = data[data['Country'] == negara_dipilih]

# Highlight Insights
st.markdown("## 📊 Highlight Insights")
if negara_dipilih == "Semua":
    bandara_terbanyak = data.loc[data['Total passengers'].idxmax()]
    st.markdown(f"""
    - **Bandara Tersibuk Secara Global**: {bandara_terbanyak['Airport']} dengan {bandara_terbanyak['Total passengers']:,} penumpang.
    - **Jumlah Total Penumpang Global**: {data['Total passengers'].sum():,} penumpang.
    """)
else:
    bandara_terbanyak = data_terfilter.loc[data_terfilter['Total passengers'].idxmax()]
    st.markdown(f"""
    - **Bandara Tersibuk di {negara_dipilih}**: {bandara_terbanyak['Airport']} dengan {bandara_terbanyak['Total passengers']:,} penumpang.
    - **Jumlah Total Penumpang di {negara_dipilih}**: {data_terfilter['Total passengers'].sum():,} penumpang.
    """)

# Visualisasi Geospasial dengan Heatmap dan Scatterplot
st.markdown("## 🌍 Visualisasi Geospasial")
if not data_terfilter.empty:
    view_state = pdk.ViewState(
        latitude=data_terfilter['latitude'].mean(),
        longitude=data_terfilter['longitude'].mean(),
        zoom=2 if negara_dipilih == "Semua" else 5,
        pitch=40
    )

    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=data_terfilter,
        get_position=["longitude", "latitude"],
        get_fill_color=[255, 0, 0],
        get_radius=100000,
        pickable=True,
    )

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=data_terfilter,
        get_position=["longitude", "latitude"],
        get_weight="Total passengers",
        radius=50000,
    )

    deck = pdk.Deck(
        layers=[scatterplot_layer, heatmap_layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Bandara:</b> {Airport} <br/>"
                    "<b>Jumlah Penumpang:</b> {Total passengers}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    st.pydeck_chart(deck)
else:
    st.write("Tidak ada data geografis untuk negara yang dipilih.")

st.markdown("""
**Wawasan Penting**:
- **Scatterplot** menunjukkan lokasi bandara tersibuk secara individual.
- **Heatmap** menunjukkan konsentrasi aktivitas perjalanan udara berdasarkan jumlah penumpang.
""")

# Bubble Chart Perbandingan Bandara
st.markdown("## 🛬 Perbandingan Bandara dengan Bubble Chart")
if not data_terfilter.empty:
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(
        x=data_terfilter['Rank'],
        y=data_terfilter['Total passengers'],
        mode='markers',
        marker=dict(
            size=data_terfilter['Total passengers'] / 1000000,
            sizemode='diameter',
            color=data_terfilter['Total passengers'],
            showscale=True
        ),
        text=data_terfilter['Airport']
    ))
    fig7.update_layout(
        title="Perbandingan Bandara Berdasarkan Peringkat dan Penumpang",
        xaxis_title="Peringkat",
        yaxis_title="Total Penumpang",
    )
    st.plotly_chart(fig7)
else:
    st.write("Tidak ada data untuk negara yang dipilih.")

st.markdown("""
**Wawasan Penting**: Bandara dengan volume penumpang lebih tinggi cenderung berada di peringkat atas, menunjukkan ukuran relatif aktivitas.
""")

# Visualisasi Kontribusi Negara Terbesar
st.markdown("## 🏳️ Kontribusi Negara dengan Penumpang Terbanyak")
if negara_dipilih == "Semua":
    data_negara = data.groupby('Country')['Total passengers'].sum().reset_index().sort_values(by='Total passengers', ascending=False)
    if not data_negara.empty:
        fig8 = go.Figure(data=[
            go.Bar(
                x=data_negara['Country'][:10],
                y=data_negara['Total passengers'][:10],
                text=data_negara['Total passengers'][:10],
                marker=dict(color='green'),
                textposition='outside'
            )
        ])
        fig8.update_layout(
            title="10 Negara dengan Total Penumpang Terbanyak",
            xaxis_title="Negara",
            yaxis_title="Total Penumpang",
            xaxis=dict(tickangle=-45),
            height=600,
            margin=dict(l=40, r=40, t=40, b=150)
        )
        st.plotly_chart(fig8)
    else:
        st.write("Tidak ada data untuk negara.")
else:
    st.write("Analisis kontribusi negara hanya tersedia untuk data global.")

st.markdown("""
**Wawasan Penting**: Negara dengan total penumpang terbesar, seperti Amerika Serikat, memiliki kontribusi signifikan terhadap perjalanan udara global.
""")


# Donut Chart Kontribusi dari 5 Bandara Teratas
st.markdown("## 🍩 Kontribusi 5 Bandara Teratas dalam Total Penumpang")
if not data_terfilter.empty:
    bandara_teratas = data_terfilter.nlargest(5, 'Total passengers')
    fig2 = go.Figure(data=[
        go.Pie(
            labels=bandara_teratas['Airport'],
            values=bandara_teratas['Total passengers'],
            hole=0.5
        )
    ])
    fig2.update_layout(title="Kontribusi 5 Bandara Teratas terhadap Total Penumpang")
    st.plotly_chart(fig2)
else:
    st.write("Tidak ada data untuk negara yang dipilih.")

st.markdown("""
**Wawasan Penting**: Bandara-bandara teratas memiliki kontribusi signifikan terhadap total volume penumpang di wilayah tertentu.
""")

# Bar Chart Distribusi Bandara Berdasarkan Wilayah
st.markdown("## 🌍 Distribusi Bandara Berdasarkan Wilayah")
if negara_dipilih == "Semua":
    data_wilayah = data.groupby('Country').size().reset_index(name='Jumlah Bandara').sort_values(by='Jumlah Bandara', ascending=False)
    if not data_wilayah.empty:
        fig3 = go.Figure(data=[
            go.Bar(
                x=data_wilayah['Country'],
                y=data_wilayah['Jumlah Bandara'],
                text=data_wilayah['Jumlah Bandara'],
                marker=dict(color='purple'),
                textposition='outside'
            )
        ])
        fig3.update_layout(
            title="Distribusi Bandara Berdasarkan Wilayah",
            xaxis_title="Negara",
            yaxis_title="Jumlah Bandara",
            xaxis=dict(tickangle=-45),
            height=600,
            margin=dict(l=40, r=40, t=40, b=150)
        )
        st.plotly_chart(fig3)
    else:
        st.write("Tidak ada data untuk wilayah global.")
else:
    st.write("Distribusi bandara per wilayah hanya tersedia untuk data global.")

st.markdown("""
**Wawasan Penting**: Negara-negara dengan jumlah bandara yang lebih tinggi biasanya memiliki kontribusi signifikan terhadap jaringan penerbangan global.
""")


# Kesimpulan
st.markdown("## ✈️ Kesimpulan")
st.markdown("""
1. **Bandara Tersibuk Global**: Bandara Hartsfield–Jackson Atlanta di Amerika Serikat memimpin sebagai bandara tersibuk di dunia.
2. **Distribusi Geografis**: Aktivitas perjalanan udara terkonsentrasi di wilayah Amerika Utara, Eropa, dan Timur Tengah.
3. **Kontribusi Negara**: Amerika Serikat memiliki kontribusi terbesar terhadap total perjalanan udara global.
4. **Tren Aktivitas Bandara**: Bandara dengan peringkat atas melayani volume penumpang yang jauh lebih besar dibandingkan peringkat bawah.
5. **Analisis Visual**: Heatmap dan Bubble Chart menunjukkan lokasi bandara dan kontribusi relatifnya terhadap aktivitas global.
""")
