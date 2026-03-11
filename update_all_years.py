import pandas as pd
import json
import os

def process_data():
    csv_file = 'Especializadas.csv'
    json_file = 'data.json'

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo {csv_file} não encontrado.")
        return

    print("Lendo CSV...")
    df = pd.read_csv(csv_file)

    # Limpeza básica
    df = df.dropna(subset=['Ano'])
    df['Ano'] = df['Ano'].astype(int)

    # Filtrar anos desejados (1997 a 2026)
    df = df[(df['Ano'] >= 1997) & (df['Ano'] <= 2026)]

    print(f"Processando {len(df)} registros...")

    global_by_year = {}
    esp_by_year = {}
    especializadas_totals = {}

    for _, row in df.iterrows():
        ano = str(row['Ano'])
        esp = str(row['Especializada'])
        
        if pd.isna(row['Especializada']) or esp.strip() == '':
            continue
            
        classe = str(row['Classe']) if not pd.isna(row['Classe']) else "A Definir"
        assunto = str(row['Assunto']) if not pd.isna(row['Assunto']) else "A Definir"
        
        # Agregado Global
        if ano not in global_by_year:
            global_by_year[ano] = {'total': 0, 'classes': {}, 'assuntos': {}}
        
        global_by_year[ano]['total'] += 1
        global_by_year[ano]['classes'][classe] = global_by_year[ano]['classes'].get(classe, 0) + 1
        global_by_year[ano]['assuntos'][assunto] = global_by_year[ano]['assuntos'].get(assunto, 0) + 1
        
        # Totais por Especializada
        especializadas_totals[esp] = especializadas_totals.get(esp, 0) + 1
        
        # Agregado por Especializada e Ano
        if esp not in esp_by_year:
            esp_by_year[esp] = {}
        if ano not in esp_by_year[esp]:
            esp_by_year[esp][ano] = {'total': 0, 'classes': {}, 'assuntos': {}}
            
        esp_by_year[esp][ano]['total'] += 1
        esp_by_year[esp][ano]['classes'][classe] = esp_by_year[esp][ano]['classes'].get(classe, 0) + 1
        esp_by_year[esp][ano]['assuntos'][assunto] = esp_by_year[esp][ano]['assuntos'].get(assunto, 0) + 1

    # Objeto final
    output_data = {
        'global_by_year': global_by_year,
        'esp_by_year': esp_by_year,
        'especializadas_totals': especializadas_totals
    }

    print(f"Salvando dados em {json_file}...")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("Sucesso! O dashboard lerá os novos dados automaticamente.")

if __name__ == "__main__":
    process_data()
