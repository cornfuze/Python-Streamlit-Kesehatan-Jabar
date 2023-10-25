import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import plotly.express as px

st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("""
         # Python Kelompok Sampurasun

         **Nama Anggota :**
         - Andreas Rhemadanu        <span style="float:right;">210103088</span>
         - Muhammad Hafid Krisna    <span style="float:right;">210103106</span>
         - Muhammad Yusuf           <span style="float:right;">210103110</span>
         - Rafif Rizqy Alfiansyah   <span style="float:right;">210103114</span>

         ## Dashboard Jaminan Kesehatan di Provinsi Jawa Barat.
         """, unsafe_allow_html=True)

st.markdown("---")

st.text("")
# Function to display the Home page
def show_home_page():
    
    # Load data from Excel
    excel_file = "Jaminan Kesehatan Jabar.xlsx"
    df = pd.read_excel(excel_file)

    st.markdown("<h2 class='centered'>Proporsi Jaminan Kesehatan</h2>", unsafe_allow_html=True)

    # Create a sidebar to select data
    st.sidebar.header('Sidebar Data Selection')
    selected_data = st.sidebar.multiselect('Pie Chart:', df['jaminan_kesehatan'].unique())

    # Check if no selection is made, and if not, use all data
    if not selected_data:
        filtered_data = df 
    else:
        # Filter the data based on the selected data
        filtered_data = df[df['jaminan_kesehatan'].isin(selected_data)]

    # Group data by 'jaminan_kesehatan' and calculate the total population for each category
    grouped = filtered_data.groupby('jaminan_kesehatan')['jumlah_penduduk'].sum()

    # Define custom colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c2f0c2']

    # Create labels with both category and percentage
    labels = [f"{category} ({(population/sum(grouped)*100):.1f}%)"
            for category, population in zip(grouped.index, grouped)]

    # Create an 'explode' list with the same length as the number of categories
    explode = [0.1] * len(grouped)

    # Plot a pie chart with customizations
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(grouped, labels=None, startangle=140, colors=colors, shadow=True, explode=explode,
                                    autopct=lambda p: f'{p:.1f}%' if p > 1 else '')
    ax.set_title('Proporsi Jaminan Kesehatan terhadap Jumlah Penduduk')

    # Add custom labels outside of the pie chart
    labels_out = [f"{category}: {(population/sum(grouped)*100):.1f}%" for category, population in zip(grouped.index, grouped)]

    plt.legend(wedges, labels_out, title="Jaminan Kesehatan", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Increase the label font size
    plt.setp(autotexts, size=14)

    # Show the pie chart in the main content area
    st.pyplot(fig)



    # Load data from Excel
    excel_file = "Jumlah Faskes Jabar.xlsx"
    df = pd.read_excel(excel_file)

    st.text("")
    st.text("")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Posyandu",
            value=df[df['jenis_faskes'] == 'POSYANDU']['jumlah_faskes'].sum(),
        )
    with col2:
        st.metric(
            label="Puskesmas",
            value=df[df['jenis_faskes'] == 'PUSKESMAS']['jumlah_faskes'].sum(),
        )
    with col3:
        st.metric(
            label="Rumah Sakit Bersalin",
            value=df[df['jenis_faskes'] == 'RUMAH SAKIT BERSALIN']['jumlah_faskes'].sum(),
        )
    with col4:
        st.metric(
            label="Rumah Sakit Khusus",
            value=df[df['jenis_faskes'] == 'RUMAH SAKIT KHUSUS']['jumlah_faskes'].sum(),
        )
    with col5:
        st.metric(
            label="Rumah Sakit Umum",
            value=df[df['jenis_faskes'] == 'RUMAH SAKIT UMUM']['jumlah_faskes'].sum(),
        )

    st.text("")
    st.text("")

    # Define colors for each jenis_faskes
    colors = {'RUMAH SAKIT UMUM': '#1f77b4', 'RUMAH SAKIT KHUSUS': '#ff7f0e', 'RUMAH SAKIT BERSALIN': '#2ca02c',
            'PUSKESMAS': '#d62728', 'POSYANDU': '#8f14b8'}

    st.markdown("<h2 class='centered'>Jumlah Fasilitas Kesehatan</h2>", unsafe_allow_html=True)

    # Sidebar for data selection
    selected_data = st.sidebar.multiselect('Bar Chart:', df['jenis_faskes'].unique(), [])

    # Filter data based on user selection
    if not selected_data:
        filtered_data = df  # Jika tidak ada yang dipilih, tampilkan semua data
    else:
        filtered_data = df[df['jenis_faskes'].isin(selected_data)]

    # Group filtered data by 'jenis_faskes' and calculate the total number of facilities for each category
    grouped = filtered_data.groupby('jenis_faskes')['jumlah_faskes'].sum()

    # Create a bar chart with customizations
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = grouped.plot(kind='bar', ax=ax, color=[colors[jenis] for jenis in grouped.index])
    ax.set_xlabel('Jenis Fasilitas Kesehatan')
    ax.set_ylabel('Jumlah Fasilitas Kesehatan')
    ax.set_title('Jumlah Fasilitas Kesehatan berdasarkan Jenis')
    ax.set_yscale('log')
    ax.set_ylim(0.1, 1000)  # Adjust the lower limit for log scale
    plt.xticks(rotation=45, ha='right')

    # Create a custom legend with the same colors as the bars
    legend_labels = [f"{jenis}: {jumlah}" for jenis, jumlah in zip(grouped.index, grouped)]
    legend_handles = [Patch(color=colors[jenis], label=l) for jenis, l in zip(grouped.index, legend_labels)]

    # Add the custom legend outside the chart
    legend = ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1, 1))
    legend.set_title("Legenda")

    # Show the bar chart in the main content area
    st.pyplot(fig)

    # Load data
    df_kesehatan = pd.read_excel("Jaminan Kesehatan Jabar.xlsx")
    df_faskes = pd.read_excel("Jumlah Faskes Jabar.xlsx")

    st.text("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Jumlah Kabupaten/Kota",
            value=df_kesehatan['nama_kabupaten_kota'].nunique(),
    )

    with col2:
        st.metric(
            label="Jumlah Penduduk Terdaftar",
            value=df_kesehatan['jumlah_penduduk'].sum(),
    )

    with col3:
        st.metric(
            label="Jumlah Faskes",
            value=df_faskes['jumlah_faskes'].sum(),
    )

    st.text("")
    st.text("")

    # menghapus data duplikat berdasarkan kolom 'nama_kabupaten_kota' dan 'jenis_faskes'
    df_faskes = df_faskes.drop_duplicates(subset=['nama_kabupaten_kota', 'jenis_faskes'])

    # Pivot the data to create a DataFrame suitable for a stacked bar chart
    pivot_df = df_faskes.pivot(index='nama_kabupaten_kota', columns='jenis_faskes', values='jumlah_faskes')

    # Fill missing values with 0
    pivot_df.fillna(0, inplace=True)

    # Create a stacked bar chart
    st.markdown("<h2 class='centered'>Distribusi Fasilitas Kesehatan</h2>", unsafe_allow_html=True)

    # Create an interactive stacked bar chart using Plotly Express
    fig = px.bar(pivot_df, x=pivot_df.index, y=pivot_df.columns, title="Distribusi Fasilitas Kesehatan", 
                labels={'index': "Nama Kabupaten/Kota", 'value': 'Jumlah Fasilitas Kesehatan'}, 
                hover_name=pivot_df.index)

    # Configure the layout for better readability
    fig.update_layout(barmode='stack', xaxis_tickangle=-45, xaxis_title="Nama Kabupaten/Kota", yaxis_title="Jumlah Fasilitas Kesehatan")

    # Display the interactive chart using Streamlit
    st.plotly_chart(fig)

    st.text("")
    st.text("")

    st.markdown("<h2 class='centered'>Jumlah Penduduk Terdaftar Jaminan Kesehatan</h2>", unsafe_allow_html=True)

    st.text("")

    # Create a bar chart for the number of registered population in each kabupaten
    fig, ax = plt.subplots(figsize=(10, 6))
    df_kesehatan = df_kesehatan.sort_values(by='jumlah_penduduk', ascending=False)

    bars = ax.barh(df_kesehatan['nama_kabupaten_kota'], df_kesehatan['jumlah_penduduk'], color='skyblue')

    # Show the bar chart in Streamlit
    st.pyplot(fig)

# Function to display the Excel data page
def show_excel_data():
    st.title("Data Jaminan Kesehatan Di Jawa Barat")
    excel_file = "Jaminan Kesehatan Jabar.xlsx" 
    df = pd.read_excel(excel_file)
    st.write(df)

    st.title("Data  Fasilitas Kesehatan di Jawa Barat")
    excel_file = "Jumlah Faskes Jabar.xlsx" 
    df = pd.read_excel(excel_file)
    st.write(df)
   
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Chart", "Data"],
        icons=["clipboard2-data", "database"],
        default_index=0,
)

if selected == "Chart":
    show_home_page()
else:
    show_excel_data()

    