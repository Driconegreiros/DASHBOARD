import pandas as pd
import json
import re

print("Leitura do CSV...")
df = pd.read_csv('Especializadas.csv')

# Drop NA years and convert to int
df = df.dropna(subset=['Ano'])
df['Ano'] = df['Ano'].astype(int)

# Fit into new range
df = df[(df['Ano'] >= 1997) & (df['Ano'] <= 2026)]

min_ano = df['Ano'].min()
max_ano = df['Ano'].max()

print(f"Ano Min: {min_ano}, Ano Max: {max_ano}")

# Build global dict
global_by_year = {}
esp_by_year = {}
especializadas_totals = {}

for index, row in df.iterrows():
    ano = str(row['Ano'])
    esp = str(row['Especializada'])
    
    # Ignorar Especializada "nan" ou vazia
    if pd.isna(row['Especializada']) or esp.strip() == '':
        continue
        
    classe = str(row['Classe']) if not pd.isna(row['Classe']) else "A Definir"
    assunto = str(row['Assunto']) if not pd.isna(row['Assunto']) else "A Definir"
    
    # Global
    if ano not in global_by_year:
        global_by_year[ano] = {'total': 0, 'classes': {}, 'assuntos': {}}
    
    global_by_year[ano]['total'] += 1
    global_by_year[ano]['classes'][classe] = global_by_year[ano]['classes'].get(classe, 0) + 1
    global_by_year[ano]['assuntos'][assunto] = global_by_year[ano]['assuntos'].get(assunto, 0) + 1
    
    # Especializadas Totals
    especializadas_totals[esp] = especializadas_totals.get(esp, 0) + 1
    
    # Especializadas By Year
    if esp not in esp_by_year:
        esp_by_year[esp] = {}
        
    if ano not in esp_by_year[esp]:
        esp_by_year[esp][ano] = {'total': 0, 'classes': {}, 'assuntos': {}}
        
    esp_by_year[esp][ano]['total'] += 1
    esp_by_year[esp][ano]['classes'][classe] = esp_by_year[esp][ano]['classes'].get(classe, 0) + 1
    esp_by_year[esp][ano]['assuntos'][assunto] = esp_by_year[esp][ano]['assuntos'].get(assunto, 0) + 1

# Montar JSON final
raw_data_dict = {
    'global_by_year': global_by_year,
    'esp_by_year': esp_by_year,
    'especializadas_totals': especializadas_totals
}

print("Salvando no HTML...")

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir rawData
pattern = re.compile(r'const rawData = \{.*?\};', re.DOTALL)
html = pattern.sub('const rawData = ' + json.dumps(raw_data_dict, ensure_ascii=False) + ';', html)

# Substituir minimo, maximo e defaults na interface
html = re.sub(r'id="year-start" min="\d+" max="\d+" value="\d+"', f'id="year-start" min="{min_ano}" max="{max_ano}" value="{min_ano}"', html)
html = re.sub(r'id="year-end" min="\d+" max="\d+" value="\d+"', f'id="year-end" min="{min_ano}" max="{max_ano}" value="{max_ano}"', html)
html = re.sub(r'<span id="year-val" class="font-bold text-white">\d+ - \d+</span>', f'<span id="year-val" class="font-bold text-white">{min_ano} - {max_ano}</span>', html)

# Change the text "Evolução Temporal de Processos (2010 - 2026)" into dynamic
html = re.sub(r'Evolução Temporal de Processos \(\d+ - \d+\)', f'Evolução Temporal de Processos ({min_ano} - {max_ano})', html)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Finalizado!")
