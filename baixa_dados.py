from dotenv import load_dotenv

load_dotenv()
import requests
import pandas as pd
import geopandas as gpd
import os
import json
from normaliza_iniciativas.normalizer import clear_string

KOBO_API_KEY = os.getenv("KOBO_API_KEY")
KOBO_USERNAME = os.getenv("KOBO_USERNAME")
KOBO_PASSWORD = os.getenv("KOBO_PASSWORD")
KOBO_URL = os.getenv("KOBO_URL")
FROM_UID = "atUcxaKhdkAJsHhiPzXJ2E"

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

kobo_endpoints = {
    "token": f"{KOBO_URL}/token/",
    "assets_json": f"{KOBO_URL}/api/v2/assets.json",
}
auth = (KOBO_USERNAME, KOBO_PASSWORD)
opts = {
    "format": "json",
}

result = requests.post(kobo_endpoints["token"], auth=auth, params=opts)
API_TOKEN = result.json()["token"]
headers = {"Authorization": f"Token {API_TOKEN}"}
#Aqui pegamos as informções de todos os formulários que estão no kobotoolbox, e salvamos em um arquivo json.
result_assets = requests.get(kobo_endpoints["assets_json"], headers=headers)
result_assets = result_assets.json()
print(f"Quantidade de resultados {result_assets['count']}")
print(f'Next: {result_assets["next"]}')
with open(os.path.join('.',data_folder, "kobo_assets.json"), "w") as f:
    json.dump(result_assets, f, indent=2, ensure_ascii=False)

results = result_assets["results"]

#Baixando todos os dados do formulário que desejamos

form_to_download = next(filter(lambda x: x["uid"] == FROM_UID, results))
form_name = clear_string(form_to_download["name"])
print(f"Baixando {form_name}")
# * Salvando arquivo de metadados do formulário
filename_form_metadata = f"{form_name}_metadata.json"
with open(os.path.join(".", data_folder, filename_form_metadata), "w") as f:
    json.dump(form_to_download, f, indent=2, ensure_ascii=False)
# * Baixando o arquivo xls do formulário
print("Baixando arquivo xls do formulário")
download_url = next(filter(lambda x: x["format"] == "xls", form_to_download["downloads"]))
form_configs_filename = f"{form_name}_configs.xlsx"
form_configs = requests.get(download_url["url"], headers=headers)
with open(os.path.join(".", data_folder, form_configs_filename), "wb") as f:
    f.write(form_configs.content)
# * Baixando os dados do formulário
print("Baixando dados do formulário")
url_data = form_to_download["data"]
data_filename = f"{form_name}_data.json"
data = requests.get(url_data, headers=headers)
data = data.json()
with open(os.path.join(".", data_folder, data_filename), "w",  encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# === ADICIONADO: Convertendo os dados para um DataFrame e salvando como Excel ===

# Converte os dados JSON para um DataFrame
df = pd.json_normalize(data['results'])  # 'results' contém os dados do formulário

# Salva o DataFrame em um arquivo Excel
excel_filename = f"{form_name}_data.xlsx"
df.to_excel(os.path.join(".", data_folder, excel_filename), index=False)

# === FIM DO CÓDIGO ADICIONADO ===

print(f"Dados baixados e salvos como {data_filename} (JSON) e {excel_filename} (Excel)!")

print("Dados Baixados com sucesso!")
