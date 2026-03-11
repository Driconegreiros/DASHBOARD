import json
import re

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_years(anos):
    return {k: v for k, v in anos.items() if 2010 <= int(k) <= 2026}

data['anos'] = clean_years(data['anos'])
for esp in data['especializadas_data']:
    data['especializadas_data'][esp]['anos'] = clean_years(data['especializadas_data'][esp]['anos'])

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'const rawData = \{.*?\};', re.DOTALL)
html = pattern.sub('const rawData = ' + json.dumps(data, ensure_ascii=False) + ';', html)

html = html.replace('Object.entries(rawData.especializadas).forEach', 'Object.entries(rawData.especializadas_totals).forEach')
html = html.replace('data: Object.values(rawData.especializadas),', 'data: Object.values(rawData.especializadas_totals),')
html = html.replace('labels: Object.keys(rawData.especializadas),', 'labels: Object.keys(rawData.especializadas_totals),')

new_update_dashboard = """function updateDashboard(esp) {
            let dataTotal, dataAnos, dataClasses, dataAssuntos;
            let liderText, picoText, classeText, title2;

            if (esp === 'Todas') {
                dataTotal = rawData.total;
                dataAnos = Object.values(rawData.anos);
                dataClasses = Object.values(rawData.classes).map(v => v * 100);
                dataAssuntos = Object.values(rawData.assuntos).map(v => v * 100);

                title2 = "Especializada Líder";
                liderText = `PPM <span class="text-sm font-normal text-white/50">(27%)</span>`;
                
                let maxGlobalVal = Math.max(...dataAnos);
                let maxAnoIdx = dataAnos.indexOf(maxGlobalVal);
                let picoAno = Object.keys(rawData.anos)[maxAnoIdx];
                picoText = `${picoAno} <span class="text-sm font-normal text-white/50">(${maxGlobalVal > 1000 ? Math.round(maxGlobalVal / 1000) + 'k' : maxGlobalVal})</span>`;
                
                let maxClasseIdx = dataClasses.indexOf(Math.max(...dataClasses));
                classeText = Object.keys(rawData.classes)[maxClasseIdx];

                especializadasChart.data.datasets[0].backgroundColor = originalColorsDoughnut;
                
                classesChart.data.labels = Object.keys(rawData.classes);
                assuntosChart.data.labels = Object.keys(rawData.assuntos);
                evolucaoChart.data.labels = Object.keys(rawData.anos);
            } else {
                let espData = rawData.especializadas_data[esp];
                dataTotal = espData.total;
                const ratio = dataTotal / rawData.total;

                // Sync anos with global x-axis
                const allAnos = Object.keys(rawData.anos);
                dataAnos = allAnos.map(ano => espData.anos[ano] || 0);
                
                let maxVal = Math.max(...dataAnos);
                let picoAno = allAnos[dataAnos.indexOf(maxVal)] || "N/A";

                dataClasses = Object.values(espData.classes).map(v => v * 100);
                dataAssuntos = Object.values(espData.assuntos).map(v => v * 100);

                title2 = "Participação";
                liderText = `${(ratio * 100).toFixed(1)}% <span class="text-sm font-normal text-white/50">do total</span>`;
                picoText = `${picoAno} <span class="text-sm font-normal text-white/50">(${maxVal >= 1000 ? Math.round(maxVal / 1000) + 'k' : maxVal})</span>`;
                
                let maxClasseIdx = dataClasses.indexOf(Math.max(...dataClasses));
                classeText = Object.keys(espData.classes)[maxClasseIdx] || "N/A";

                const espIdx = Object.keys(rawData.especializadas_totals).indexOf(esp);
                especializadasChart.data.datasets[0].backgroundColor = originalColorsDoughnut.map((c, i) =>
                    i === espIdx ? c : hexToRgba(c, 0.15)
                );
                
                classesChart.data.labels = Object.keys(espData.classes);
                assuntosChart.data.labels = Object.keys(espData.assuntos);
                evolucaoChart.data.labels = allAnos;
            }

            document.getElementById('kpi-total').innerText = dataTotal.toLocaleString('pt-BR');
            document.getElementById('kpi-title-2').innerText = title2;
            document.getElementById('kpi-lider').innerHTML = liderText;
            document.getElementById('kpi-pico').innerHTML = picoText;
            document.getElementById('kpi-classe').innerText = classeText;
            document.getElementById('kpi-classe').title = classeText;

            const kpiValues = document.querySelectorAll('.card-value, .card-title');
            kpiValues.forEach(el => {
                el.classList.add('opacity-50');
                setTimeout(() => el.classList.remove('opacity-50'), 300);
            });

            evolucaoChart.data.datasets[0].data = dataAnos;
            evolucaoChart.update();

            classesChart.data.datasets[0].data = dataClasses;
            classesChart.update();

            assuntosChart.data.datasets[0].data = dataAssuntos;
            assuntosChart.update();

            especializadasChart.update();
        }"""

pattern_func = re.compile(r'function updateDashboard\(esp\)\s*\{.*?\}(?=\s*</script>)', re.DOTALL)
html = pattern_func.sub(new_update_dashboard, html)

html = html.replace("""function pseudoRandom(seed) {
            let x = Math.sin(seed++) * 10000;
            return x - Math.floor(x);
        }""", "")

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
