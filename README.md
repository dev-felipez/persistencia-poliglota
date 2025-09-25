# persistencia-poliglota
Projeto acadêmico de Persistência Poliglota utilizando SQLite + MongoDB, com interface em Streamlit e recursos de geoprocessamento.
# Persistência Poliglota — Projeto Acadêmico

## Descrição do Projeto
Este projeto tem como objetivo demonstrar a aplicação de **persistência poliglota**, integrando dois modelos distintos de banco de dados dentro de um mesmo sistema:  
- **SQLite (relacional)**: usado para armazenar cidades e estados em tabelas estruturadas.  
- **MongoDB (NoSQL)**: usado para armazenar pontos de interesse (locais), permitindo flexibilidade no armazenamento de coordenadas geográficas e descrições.  

A aplicação foi desenvolvida em **Python** com interface web em **Streamlit**, possibilitando que o usuário cadastre, consulte, visualize e pesquise dados de forma simples e intuitiva.  

Além da listagem de dados tabulares, o sistema permite a **visualização geográfica** em mapas interativos (com **Folium**) e a **análise de proximidade** utilizando bibliotecas de geoprocessamento (como **Geopy**).  

---

## Componentes do Projeto

### `db_sqlite.py` — Banco Relacional (SQLite) para Cidades
Gerencia cidades em um banco relacional com suporte a tabelas.  
- Criação da tabela de cidades.  
- Inserção de novos registros.  
- Listagem de cidades existentes.  

**Exemplo de inserção:**
```
inserir_cidade("João Pessoa", "PB")
inserir_cidade("Recife", "PE")
db_mongo.py — Banco de Documentos (MongoDB) para Locais
Gerencia locais de interesse em formato JSON.
Cada local contém:

Nome do local

Cidade vinculada

Latitude e longitude

Descrição

Exemplo de documento no MongoDB:

{
  "_id": ObjectId("..."),
  "nome_local": "Praça da Independência",
  "cidade": "João Pessoa",
  "coordenadas": {"latitude": -7.11532, "longitude": -34.861},
  "descricao": "Ponto turístico central"
}
Exemplo de inserção em Python:

inserir_local(
    "Farol do Cabo Branco",
    "João Pessoa",
    -7.15100,
    -34.79472,
    "Ponto mais oriental das Américas"
)
geoprocessamento.py — Funções de Geolocalização
Implementa cálculos de distância e consultas por proximidade.

Usa Geopy para calcular a distância entre dois pontos.

Permite buscar locais dentro de um raio específico a partir de uma coordenada.

Exemplo de cálculo de distância:

coord_origem = (-7.120, -34.850)
coord_destino = (-7.11768, -34.83239)

distancia = geodesic(coord_origem, coord_destino).km
print(f"Distância: {distancia:.2f} km")
Saída esperada:

Distância: 1.80 km
app.py — Interface em Streamlit
Integra todos os módulos e exibe a interface gráfica interativa.

Abas para cadastrar cidades, cadastrar locais, listar dados, visualizar no mapa e buscar por proximidade.

Integração com SQLite e MongoDB.
Visualização interativa de dados com tabelas e mapas.

Exemplo de tabela no Streamlit:

import streamlit as st
import pandas as pd

locais = [
    {"nome": "Praia de Tambaú", "cidade": "João Pessoa", "lat": -7.11768, "lon": -34.83239},
    {"nome": "Farol do Cabo Branco", "cidade": "João Pessoa", "lat": -7.15100, "lon": -34.79472}
]

df = pd.DataFrame(locais)
st.dataframe(df, width="stretch")
Fluxo de Dados (detalhado)
Cadastro de Cidade (SQLite)
Usuário insere nome e estado.

Dados são persistidos em tabela no banco relacional.

Essas cidades servem de referência para vincular locais no MongoDB.

Cadastro de Local (MongoDB)
Usuário escolhe uma cidade já existente (via SQLite).

Informa nome, latitude, longitude e descrição.

Dados são salvos no MongoDB como documento JSON.

Listagem
O sistema recupera:

Todas as cidades do SQLite.

Todos os locais do MongoDB.

Exibe em tabelas interativas (Streamlit DataFrame).

Mapa
Os locais armazenados no MongoDB são plotados em mapa Folium.

Cada ponto tem popup com nome e descrição.

O mapa é interativo, permitindo zoom e movimentação.

Busca por Proximidade
Usuário informa uma coordenada (lat/lon) e raio em km.

O sistema calcula distância entre o ponto informado e cada local.

Exibe apenas os locais encontrados dentro do raio especificado.

Funcionalidades Principais
Cadastro de Cidades (SQLite): Registra cidades com nome e estado em banco relacional.

Cadastro de Locais (MongoDB): Armazena locais com informações flexíveis, vinculados a cidades cadastradas.

Listagem Completa: Exibe dados tabulares de forma clara e organizada.

Mapa Interativo (Folium): Visualização geográfica dos locais cadastrados com marcadores e popups.

Busca de Proximidade (Geopy): Localiza pontos próximos a uma coordenada definida pelo usuário, retornando a distância em km.

Tecnologias Utilizadas
Linguagem: Python 3.10+

Banco de Dados Relacional: SQLite

Banco de Dados NoSQL: MongoDB (local ou Atlas)

Framework Web: Streamlit

Mapas Interativos: Folium + streamlit-folium

Geoprocessamento: Geopy

Manipulação de dados: Pandas

Autores
Felipe Gabriel Mendes de Sousa

Yasmin Carvalho dos Santos

Vitória Gabrielly das Chagas Moreira
