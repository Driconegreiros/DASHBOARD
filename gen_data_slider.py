import pandas as pd
import json

df = pd.read_csv(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\Especializadas.csv')
df = df.dropna(subset=['Ano', 'Especializada'])
df['Ano'] = df['Ano'].astype(int).astype(str)

valid_years = [str(y) for y in range(2010, 2027)]
df = df[df['Ano'].isin(valid_years)]

def get_counts(series):
    return series.value_counts().to_dict()

def process_group(group_df):
    return {
        'total': len(group_df),
        'classes': get_counts(group_df['Classe']),
        'assuntos': get_counts(group_df['Assunto'])
    }

global_by_year = {}
for year in valid_years:
    year_df = df[df['Ano'] == year]
    global_by_year[year] = process_group(year_df)

esp_by_year = {}
especializadas = df['Especializada'].unique()
for esp in especializadas:
    esp_by_year[esp] = {}
    esp_df = df[df['Especializada'] == esp]
    for year in valid_years:
        ey_df = esp_df[esp_df['Ano'] == year]
        esp_by_year[esp][year] = process_group(ey_df)

data = {
    'global_by_year': global_by_year,
    'esp_by_year': esp_by_year,
    'especializadas_totals': get_counts(df['Especializada'])
}

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\data_slider.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
