import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

st.title("Tugas Kelompok Python")

st.write("""
         # Dashboard Kelompok Sampurasun

         **Nama Kelompok:**
         - Andreas Rhemadanu        <span style="float:right;">210103088</span>
         - Muhammad Hafid Krisna    <span style="float:right;">210103106</span>
         - Muhammad Yusuf           <span style="float:right;">210103110</span>
         - Rafif Rizqy Alfiansyah   <span style="float:right;">210103114</span>

         ### Dashboard Jaminan Kesehatan di Provinsi Jawa Barat.
         """, unsafe_allow_html=True)

st.text("")
# Load data from Excel
excel_file = "Jaminan Kesehatan Jabar.xlsx"
df = pd.read_excel(excel_file)

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
# Load data from Excel
excel_file = "Jumlah Faskes Jabar.xlsx"
df = pd.read_excel(excel_file)

plt.legend(wedges, labels_out, title="Jaminan Kesehatan", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Increase the label font size
plt.setp(autotexts, size=14)

# Show the pie chart in the main content area
st.pyplot(fig)

st.text("")
st.text("")

spacer = st.empty()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Posyanadu",
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
          'PUSKESMAS': '#d62728', 'POSYANDU': '#1f77b4'}  # POSYANDU will be blue

# Sidebar for data selection
st.sidebar.header('Pilihan Data')
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

