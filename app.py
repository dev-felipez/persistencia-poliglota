import streamlit as st
import db_sqlite
import db_mongo
import geoprocessamento
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="🌍 Persistência Poliglota", layout="wide")

st.title("🌍 Persistência Poliglota com MongoDB + SQLite")

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "🏙️ Cidades", 
    "📍 Locais", 
    "📋 Listagem", 
    "🗺️ Mapa", 
    "📡 Proximidade"
])

with aba1:
    st.subheader("Cadastrar Cidade")
    nome = st.text_input("Nome da cidade")
    estado = st.text_input("Estado")

    if st.button("Salvar Cidade"):
        if nome and estado:
            db_sqlite.inserir_cidade(nome, estado)
            st.success(f"✅ Cidade {nome} - {estado} cadastrada com sucesso!")
        else:
            st.error("⚠️ Preencha o nome da cidade e o estado antes de salvar.")

    st.divider()
    st.subheader("Cidades Cadastradas")
    cidades = db_sqlite.listar_cidades()
    if cidades:
        df = pd.DataFrame(cidades, columns=["ID", "Cidade", "Estado"])
        st.dataframe(df, width="stretch")
    else:
        st.info("Nenhuma cidade cadastrada ainda.")

with aba2:
    st.subheader("Cadastrar Local")
    nome_local = st.text_input("Nome do local")
    cidade = st.text_input("Cidade relacionada")
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", format="%.6f")
    with col2:
        longitude = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição do local")

    if st.button("Salvar Local"):
        db_mongo.inserir_local(nome_local, cidade, latitude, longitude, descricao)
        st.success("✅ Local cadastrado com sucesso!")

with aba3:
    st.subheader("📋 Lista de Locais")
    locais = db_mongo.listar_locais()
    if locais:
        df = pd.DataFrame(locais)
        st.dataframe(df, width="stretch")
    else:
        st.info("Nenhum local cadastrado ainda.")

with aba4:
    st.subheader("🗺️ Mapa Interativo dos Locais")
    locais = db_mongo.listar_locais()
    if locais:
        lat_centro = locais[0]["coordenadas"]["latitude"]
        lon_centro = locais[0]["coordenadas"]["longitude"]
        mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=13)

        for loc in locais:
            popup_html = f"""
            <b>{loc['nome_local']}</b><br>
            <i>{loc['cidade']}</i><br>
            <span style='color:gray;'>{loc['descricao']}</span>
            """
            folium.Marker(
                [loc["coordenadas"]["latitude"], loc["coordenadas"]["longitude"]],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=loc["cidade"],
                icon=folium.Icon(color="darkgreen", prefix="fa", icon="map-marker")
            ).add_to(mapa)

        st_folium(mapa, width=900, height=500)
    else:
        st.warning("Nenhum local para exibir no mapa.")

import streamlit.components.v1 as components
from streamlit_folium import folium_static

with aba5:
    st.subheader("📡 Consultar Locais Próximos")
    lat_ref = st.number_input("Latitude de referência", format="%.6f", key="latref")
    lon_ref = st.number_input("Longitude de referência", format="%.6f", key="lonref")
    raio = st.slider("Raio em km", 1, 50, 10, key="raio")

    if st.button("Buscar Locais Próximos"):
        locais = db_mongo.listar_locais()
        proximos = geoprocessamento.locais_proximos(locais, (lat_ref, lon_ref), raio)

        if proximos:
            df = pd.DataFrame([{
                "Nome": loc["nome_local"],
                "Cidade": loc["cidade"],
                "Descrição": loc["descricao"],
                "Distância (km)": round(dist, 2)
            } for loc, dist in proximos])

            st.dataframe(df, width="stretch")

            mapa = folium.Map(location=[lat_ref, lon_ref], zoom_start=13)
            folium.Marker([lat_ref, lon_ref], icon=folium.Icon(color="red"), popup="Referência").add_to(mapa)

            for loc, dist in proximos:
                popup_html = f"""
                <b>{loc['nome_local']}</b><br>
                <i>{loc['cidade']}</i><br>
                <span style='color:gray;'>Distância: {round(dist,2)} km</span>
                """
                folium.Marker(
                    [loc["coordenadas"]["latitude"], loc["coordenadas"]["longitude"]],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=loc["cidade"],
                    icon=folium.Icon(color="green", icon="ok")
                ).add_to(mapa)

            st.session_state["mapa_html"] = mapa._repr_html_()
        else:
            st.info("Nenhum local encontrado nesse raio.")
            st.session_state.pop("mapa_html", None)

    if "mapa_html" in st.session_state:
        components.html(st.session_state["mapa_html"], height=500)