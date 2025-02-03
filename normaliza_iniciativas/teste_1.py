import json
import pandas as pd
import os

def normalizar_para_excel(dados):
    """
    Função para normalizar os dados do GeoJSON e convertê-los em um DataFrame do Pandas.
    """
    def limpar_chave(chave):
        """Remove prefixos e melhora a legibilidade das colunas."""
        return chave.split('/')[-1].replace("__", "_").replace("_", " ").strip()

    def converter_valor(valor):
        """Converte valores específicos para melhor legibilidade."""
        if isinstance(valor, str):
            valor = valor.strip().lower()
            if valor in ["sim", "yes"]:
                return True
            elif valor in ["não", "n_o", "no"]:
                return False
        return valor

    lista_dados = []
    for item in dados["results"]:
        # Verifica se a geolocalização é válida
        latitude, longitude = item.get("_geolocation", [None, None])
        
        # Tratando valores 'null' para os campos de geolocalização
        latitude = None if latitude is None else latitude
        longitude = None if longitude is None else longitude

        # Processando propriedades
        propriedades = {limpar_chave(k): converter_valor(v) for k, v in item.items() if not k.startswith("_")}
        
        # Adiciona latitude e longitude separadamente
        propriedades["latitude"] = latitude
        propriedades["longitude"] = longitude

        lista_dados.append(propriedades)

    return pd.DataFrame(lista_dados)

# 📍 Defina aqui o caminho do arquivo GeoJSON:
caminho_geojson = r"C:/Users/admin/Documents/GitHub/normaliza_iniciativas2/data/cadastro_de_iniciativas_mapa_das_periferias_data.json"  # 🔄 Altere para o local correto do seu arquivo

# 🔄 Testa se o arquivo existe
if os.path.exists(caminho_geojson):
    print("✅ Arquivo encontrado! Processando...")
    
    # 🔹 Carregar os dados do GeoJSON
    try:
        with open(caminho_geojson, "r", encoding="latin-1") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o arquivo JSON: {e}")
        exit()  # Encerra a execução em caso de erro
    
    # 🔹 Normalizar e converter para DataFrame
    df = normalizar_para_excel(dados)
    
    # 🔹 Salvar como arquivo Excel (.xlsx)
    df.to_excel("dados_normalizados.xlsx", index=False)
    
    print("✅ Arquivo Excel gerado com sucesso: 'dados_normalizados.xlsx'")
else:
    print("❌ ERRO: Arquivo NÃO encontrado! Verifique o caminho.")
