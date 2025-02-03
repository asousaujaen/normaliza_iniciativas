import pandas as pd

# Caminho do arquivo original
caminho_arquivo = r'C:\Users\admin\Documents\GitHub\normaliza_iniciativas2\data\cadastro_de_iniciativas_mapa_das_periferias_data.xlsx'

# Carregar os dados do arquivo Excel
df = pd.read_excel(caminho_arquivo)

# Unpivot para as redes sociais
df_rede_social = pd.melt(df, id_vars=["_id", "grupo_dados_iniciativa/nome_iniciativa"], 
                         value_vars=["grupo_dados_iniciativa/facebook_iniciativa", 
                                      "grupo_dados_iniciativa/instagram_iniciativa", 
                                      "grupo_dados_iniciativa/tiktok_iniciativa", 
                                      "grupo_dados_iniciativa/youtube_iniciativa", 
                                      "grupo_dados_iniciativa/site_iniciativa"], 
                         var_name="rede_social", value_name="link_rede_social")

# Unpivot para o endereço (combinar as colunas em uma única)
df_endereco = pd.melt(df, id_vars=["_id", "grupo_dados_iniciativa/nome_iniciativa"], 
                      value_vars=["grupo_dados_iniciativa/estado_iniciativa",
                                   "grupo_dados_iniciativa/municipio_iniciativa",
                                   "grupo_dados_iniciativa/possui_endereco_completo_inici",
                                   "grupo_dados_iniciativa/logradouro_iniciativa",
                                   "grupo_dados_iniciativa/nome_logradouro_iniciativa",
                                   "grupo_dados_iniciativa/sn_iniciativa",
                                   "grupo_dados_iniciativa/complemento_iniciativa",
                                   "grupo_dados_iniciativa/bairro_comunidade_iniciativa",
                                   "grupo_dados_iniciativa/cep_iniciativa"], 
                      var_name="endereco_component", value_name="endereco")

# Combinar as colunas de endereço em uma só (separando por vírgula)
df_endereco["endereco"] = df_endereco.groupby(["_id", "grupo_dados_iniciativa/nome_iniciativa"])["endereco"].transform(lambda x: ', '.join(x.dropna().astype(str)))

# Remover as linhas duplicadas para não ter múltiplos valores para o mesmo _id
df_endereco_unificado = df_endereco.drop_duplicates(subset=["_id", "grupo_dados_iniciativa/nome_iniciativa"])

# Concatenar os dataframes de redes sociais e endereço
df_unpivotado = pd.concat([df_rede_social, df_endereco_unificado], axis=0)

# Diagnóstico: checando valores nulos nas colunas 'link_rede_social' e 'endereco'
print("Valores nulos em 'link_rede_social':")
print(df_unpivotado["link_rede_social"].isnull().sum())
print("Valores nulos em 'endereco':")
print(df_unpivotado["endereco"].isnull().sum())

# Remover as linhas onde 'link_rede_social' ou 'endereco' estão vazias ou contêm apenas espaços em branco
df_unpivotado = df_unpivotado[df_unpivotado["link_rede_social"].str.strip().astype(bool)]
df_unpivotado = df_unpivotado[df_unpivotado["endereco"].str.strip().astype(bool)]

# Caminho para salvar o resultado final em formato Excel
caminho_saida_excel = r'C:\Users\admin\Documents\GitHub\normaliza_iniciativas2\data\dados_unpivotados.xlsx'

# Salvar o resultado final em um novo arquivo Excel
df_unpivotado.to_excel(caminho_saida_excel, index=False)

print(f"Arquivo salvo em: {caminho_saida_excel}")
