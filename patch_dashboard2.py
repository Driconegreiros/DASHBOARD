import json
import re

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\data_slider.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace data
pattern = re.compile(r'const rawData = \{.*?\};', re.DOTALL)
html = pattern.sub('const rawData = ' + json.dumps(data, ensure_ascii=False) + ';', html)

# Inject sidebar UI for year slider
old_sidebar_header = '''<div class="p-6 border-b border-white/10">
            <h2 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
                Filtrar</h2>
            <p class="text-white/50 text-xs mt-1">Selecione a Especializada</p>
        </div>'''
        
new_sidebar_header = '''<div class="p-6 border-b border-white/10">
            <h2 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
                Filtros</h2>
            <p class="text-white/50 text-xs mt-1 mb-4">Escolha o Período</p>
            <div class="space-y-4">
                <div>
                   <label class="text-xs text-white/50 flex justify-between mb-1"><span>Ano Inicial:</span> <span id="year-start-val" class="font-bold text-white">2010</span></label>
                   <input type="range" id="year-start" min="2010" max="2026" value="2010" class="w-full accent-purple-500 hover:accent-purple-400 cursor-pointer">
                </div>
                <div>
                   <label class="text-xs text-white/50 flex justify-between mb-1"><span>Ano Final:</span> <span id="year-end-val" class="font-bold text-white">2026</span></label>
                   <input type="range" id="year-end" min="2010" max="2026" value="2026" class="w-full accent-pink-500 hover:accent-pink-400 cursor-pointer">
                </div>
            </div>
            
            <p class="text-white/50 text-xs mt-6 mb-2">Selecione a Especializada</p>
        </div>'''

html = html.replace(old_sidebar_header, new_sidebar_header)

# New JS variables
js_addition = '''
        let currentEspecializada = 'Todas';
        const yearStartEl = document.getElementById('year-start');
        const yearEndEl = document.getElementById('year-end');
        const yearStartVal = document.getElementById('year-start-val');
        const yearEndVal = document.getElementById('year-end-val');

        function handleYearSlider(e) {
            let s = parseInt(yearStartEl.value);
            let e_val = parseInt(yearEndEl.value);
            if (s > e_val) {
                if (e.target.id === 'year-start') yearStartEl.value = e_val;
                else yearEndEl.value = s;
            }
            yearStartVal.innerText = yearStartEl.value;
            yearEndVal.innerText = yearEndEl.value;
            updateDashboard(currentEspecializada);
        }

        yearStartEl.addEventListener('input', handleYearSlider);
        yearEndEl.addEventListener('input', handleYearSlider);
        
        function getTop10Percent(countsObj) {
            let entries = Object.entries(countsObj).sort((a,b) => b[1] - a[1]).slice(0, 10);
            let topTotal = Object.values(countsObj).reduce((sum, val) => sum + val, 0);
            if (topTotal === 0) return { _labels: [], _data: [] };
            return {
                _labels: entries.map(x => x[0]),
                _data: entries.map(x => (x[1] / topTotal) * 100)
            };
        }
        
        function addCounts(target, source) {
            for(let k in source) {
                target[k] = (target[k] || 0) + source[k];
            }
        }
'''

# New updateDashboard function
new_update_dashboard = js_addition + '''
        function updateDashboard(esp) {
            currentEspecializada = esp;
            let start = parseInt(yearStartEl.value);
            let end = parseInt(yearEndEl.value);
            let validYears = [];
            for(let y=start; y<=end; y++) validYears.push(y.toString());

            let dataTotal = 0;
            let aggregatedClasses = {};
            let aggregatedAssuntos = {};
            let dataAnosObj = {};

            let allTimeTotal = 0; // For percentage of the esp
            Object.values(rawData.especializadas_totals).forEach(v => allTimeTotal += v);
            let totalOfEspAllTime = esp === 'Todas' ? allTimeTotal : rawData.especializadas_totals[esp];
            let ratio = totalOfEspAllTime / allTimeTotal;

            validYears.forEach(y => {
                let yData = esp === 'Todas' ? rawData.global_by_year[y] : (rawData.esp_by_year[esp] ? rawData.esp_by_year[esp][y] : null);
                dataAnosObj[y] = yData ? yData.total : 0;
                if(yData) {
                    dataTotal += yData.total;
                    addCounts(aggregatedClasses, yData.classes);
                    addCounts(aggregatedAssuntos, yData.assuntos);
                }
            });

            let dataClassesRes = getTop10Percent(aggregatedClasses);
            let dataAssuntosRes = getTop10Percent(aggregatedAssuntos);
            
            let dataAnos = validYears.map(y => dataAnosObj[y] || 0);

            let title2, liderText, picoText, classeText;

            if (esp === 'Todas') {
                title2 = "Especializada Líder";
                let topEspAllTime = Object.entries(rawData.especializadas_totals).sort((a,b)=>b[1]-a[1])[0];
                liderText = `${topEspAllTime[0]} <span class="text-sm font-normal text-white/50">(${(topEspAllTime[1]/allTimeTotal*100).toFixed(0)}%)</span>`;
                especializadasChart.data.datasets[0].backgroundColor = originalColorsDoughnut;
            } else {
                title2 = "Participação Histórica";
                liderText = `${(ratio * 100).toFixed(1)}% <span class="text-sm font-normal text-white/50">do total</span>`;
                const espIdx = Object.keys(rawData.especializadas_totals).indexOf(esp);
                especializadasChart.data.datasets[0].backgroundColor = originalColorsDoughnut.map((c, i) =>
                    i === espIdx ? c : hexToRgba(c, 0.15)
                );
            }

            let maxGlobalVal = Math.max(...dataAnos, 0);
            let picoAno = maxGlobalVal > 0 ? validYears[dataAnos.indexOf(maxGlobalVal)] : "N/A";
            picoText = `${picoAno} <span class="text-sm font-normal text-white/50">(${maxGlobalVal >= 1000 ? Math.round(maxGlobalVal / 1000) + 'k' : maxGlobalVal})</span>`;

            classeText = dataClassesRes._labels[0] || "N/A";

            // Update DOM Elements
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

            // Update Charts
            evolucaoChart.data.labels = validYears;
            evolucaoChart.data.datasets[0].data = dataAnos;
            evolucaoChart.update();

            classesChart.data.labels = dataClassesRes._labels;
            classesChart.data.datasets[0].data = dataClassesRes._data;
            classesChart.update();

            assuntosChart.data.labels = dataAssuntosRes._labels;
            assuntosChart.data.datasets[0].data = dataAssuntosRes._data;
            assuntosChart.update();

            // Doughnut is statically showing ALL-TIME distributions (filtering doughnut by year can be confusing, but let's keep it static)
            especializadasChart.update();
        }
'''

pattern_func = re.compile(r'function updateDashboard\(esp\)\s*\{.*?\}(?=\s*</script>)', re.DOTALL)
html = pattern_func.sub(new_update_dashboard, html)

# The doughnut initial dataset doesn't change, but it references rawData.especializadas_totals so no issue.

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
