from pymongo import MongoClient

def conectar():
    client = MongoClient("mongodb://localhost:27017/")  # Mongo local
    db = client["geo_db"]
    return db

def inserir_local(nome_local, cidade, latitude, longitude, descricao=""):
    db = conectar()
    locais = db["locais"]
    doc = {
        "nome_local": nome_local,
        "cidade": cidade,
        "coordenadas": {
            "latitude": latitude,
            "longitude": longitude
        },
        "descricao": descricao
    }
    locais.insert_one(doc)

def listar_locais():
    db = conectar()
    locais = db["locais"]
    return list(locais.find({}, {"_id": 0}))  # remove o _id na listagem
