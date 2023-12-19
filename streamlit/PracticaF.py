import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import logging

@st.cache_data
def load_data(url: str):
    r = requests.get(url, verify=False)
    if r.status_code != 200:
        logging.error(r.status_code)
        return None
    mijson = r.json()
    logging.info(str(mijson))
    listado = mijson['tracks']
    data = pd.DataFrame.from_records(listado)
    return data

# Assuming you have a URL from which you want to load data
data_url = "http://fastapi:8000/retrieve_data"

# Load data using the load_data function
data = load_data(data_url)

# Título del dashboard
st.markdown("<h1 style='text-align: center; color: lightgreen;'>Spotify-2023</h1>", unsafe_allow_html=True)

# Información detallada de la canción seleccionada
selected_track = st.selectbox("Selecciona una canción:", data['track_name'])
selected_track_info = data[data['track_name'] == selected_track]

# Organizar los gráficos en filas de tres
col1, col2, col3 = st.columns(3)

# Primer gráfico: Información detallada
with col1:
    st.markdown(f"<h2 style='color: lightgreen;'>Información detallada para '{selected_track}'</h2>", unsafe_allow_html=True)
    st.write(selected_track_info)

# Segundo gráfico: Tabla con información detallada
with col2:
    st.markdown("<h2 style='color: lightgreen;'>Tabla de canciones</h2>", unsafe_allow_html=True)
    st.write(data)

# Tercer gráfico: Gráfico de pastel para la distribución de modos
with col3:
    st.markdown("<h2 style='color: lightgreen;'>Distribución de Modos</h2>", unsafe_allow_html=True)
    fig_modos = px.pie(data, names='mode', title='Distribución de Modos')
    st.plotly_chart(fig_modos, use_container_width=True)

# Cuarta fila
col4, col5, col6 = st.columns(3)

# Cuarto gráfico: Gráfico de Radar para Características Musicales
with col4:
    st.markdown("<h2 style='color: lightgreen;'>Gráfico de Radar para Características Musicales</h2>", unsafe_allow_html=True)
    fig_radar = px.line_polar(selected_track_info, r=['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%'],
                              theta=['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%'],
                              line_close=True, title=f"Características Musicales para '{selected_track}'")
    st.plotly_chart(fig_radar, use_container_width=True)

# Quinto gráfico: Histograma para la distribución de BPM
with col5:
    st.markdown("<h2 style='color: lightgreen;'>Histograma de BPM</h2>", unsafe_allow_html=True)
    fig_bpm = px.histogram(data, x='bpm', nbins=20, title='Distribución de BPM')
    st.plotly_chart(fig_bpm, use_container_width=True)

# Gráfico de dispersión para las reproducciones en listas de reproducción en Spotify y Apple
with col6:
    st.markdown("<h2 style='color: lightgreen; text-align: center;'>Reproducciones en Listas de Reproducción</h2>", unsafe_allow_html=True)
    fig_playlist = px.scatter(data, x='in_spotify_playlists', y='in_apple_playlists',
                              title='Reproducciones en Listas de Reproducción',
                              labels={'in_spotify_playlists': 'Reproducciones en Spotify',
                                      'in_apple_playlists': 'Reproducciones en Apple'})
    st.plotly_chart(fig_playlist, use_container_width=True)





# Análisis de Género basado en características musicales
st.markdown("<h2 style='color: lightgreen;'>Análisis de Género basado en Características Musicales</h2>", unsafe_allow_html=True)

# Agrupar por modo y calcular el promedio de las características musicales
genre_analysis = data.groupby('mode').agg({
    'danceability_%': 'mean',
    'valence_%': 'mean',
    'energy_%': 'mean',
    'acousticness_%': 'mean',
    'instrumentalness_%': 'mean'
}).reset_index()

# Graficar el análisis de género
fig_genre_analysis = px.bar(genre_analysis, x='mode', y=['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%'],
                            title='Análisis de Género basado en Características Musicales',
                            labels={'value': 'Promedio de Características Musicales'})
st.plotly_chart(fig_genre_analysis)
