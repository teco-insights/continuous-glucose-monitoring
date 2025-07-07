import pandas as pd
import numpy as np

# --- Criando um DataFrame de exemplo com um hiato ---
data = {
    'timedata': pd.to_datetime(['2025-01-01 10:00:00', '2025-01-01 10:15:00', '2025-01-01 10:30:00',
                               '2025-01-01 10:45:00', '2025-01-01 11:00:00',
                               # Hiato aqui (2025-01-02, 2025-01-03 e parte de 2025-01-04)
                               '2025-01-04 09:00:00', '2025-01-04 09:15:00',
                               '2025-01-04 09:30:00']),
    'valor_medicao': [10, 12, 15, 13, 11, 20, 22, 18]
}
df = pd.DataFrame(data)

print("DataFrame Original:")
print(df)
print("-" * 50)

# 1. Certificar-se de que 'timedata' é do tipo datetime
df['timedata'] = pd.to_datetime(df['timedata'])

# 2. Identificar os hiatos
# Calculamos a diferença de tempo entre medições consecutivas.
# Usamos `dt.total_seconds()` para obter a diferença em segundos para facilitar a comparação.
df['diff_seconds'] = df['timedata'].diff().dt.total_seconds()

# Um hiato é identificado quando a diferença é maior que 15 minutos (900 segundos)
# e também maior que a menor frequência de medição observada (se houver, para evitar falsos positivos)
# Vamos considerar 15 minutos como a frequência normal para este exemplo.
hiato_threshold_seconds = 15 * 60 # 15 minutos em segundos

# Encontrar os índices onde um hiato começa (a medição anterior é a última antes do hiato)
# e onde um hiato termina (a medição atual é a primeira depois do hiato).
# Excluímos o primeiro elemento do diff porque ele será NaN.
indices_fim_hiato_anterior = df[df['diff_seconds'] > hiato_threshold_seconds].index - 1
indices_inicio_hiato_proximo = df[df['diff_seconds'] > hiato_threshold_seconds].index

linhas_a_adicionar = []

# Iterar sobre cada hiato encontrado
for i in range(len(indices_fim_hiato_anterior)):
    idx_fim_anterior = indices_fim_hiato_anterior[i]
    idx_inicio_proximo = indices_inicio_hiato_proximo[i]

    # Obter o último timestamp antes do hiato
    start_time = df.loc[idx_fim_anterior, 'timedata']

    # Obter o primeiro timestamp depois do hiato
    end_time = df.loc[idx_inicio_proximo, 'timedata']

    print(f"Hiato encontrado entre {start_time} e {end_time}")

    # Gerar uma série de timestamps de 15 em 15 minutos dentro do hiato
    # O `start_time + pd.Timedelta(minutes=15)` garante que a primeira nova entrada
    # não duplique a última antes do hiato.
    # O `end_time` não é incluído para evitar duplicar a primeira medição após o hiato.
    range_preenchimento = pd.date_range(start=start_time + pd.Timedelta(minutes=15),
                                        end=end_time - pd.Timedelta(minutes=1), # -1 minuto para garantir que não inclui end_time se for exato
                                        freq='15min')

    # Para cada novo timestamp, criar uma nova linha.
    # A coluna 'valor_medicao' será preenchida com NaN inicialmente.
    for timestamp in range_preenchimento:
        linhas_a_adicionar.append({'timedata': timestamp, 'valor_medicao': np.nan})

# Criar um DataFrame a partir das novas linhas
df_novas_linhas = pd.DataFrame(linhas_a_adicionar)

# Combinar o DataFrame original com as novas linhas
df_final = pd.concat([df.drop(columns=['diff_seconds']), df_novas_linhas], ignore_index=True)

# Opcional: Ordenar o DataFrame pela coluna 'timedata'
df_final = df_final.sort_values(by='timedata').reset_index(drop=True)

print("\nDataFrame Preenchido (com valores NaN nos pontos interpolados):")
print(df_final)
print("-" * 50)

# --- Opcional: Preencher os valores de medição (NaN) interpolando ---
# Se você quer preencher os valores NaN usando interpolação, por exemplo, linear:
df_final['valor_medicao_interpolado'] = df_final['valor_medicao'].interpolate(method='linear')

print("\nDataFrame com 'valor_medicao' interpolado (linearmente):")
print(df_final)
print("-" * 50)

# Opcional: Se você quiser descartar a coluna original 'valor_medicao' e manter apenas a interpolada
# df_final = df_final.drop(columns=['valor_medicao']).rename(columns={'valor_medicao_interpolado': 'valor_medicao'})
# print("\nDataFrame com apenas a coluna 'valor_medicao' interpolada:")
# print(df_final)