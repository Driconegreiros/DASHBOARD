import re

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS for multi-range slider
css = '''
        .range-slider {
            position: relative;
            width: 100%;
            height: 6px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin-top: 1rem;
        }
        .range-slider .progress {
            position: absolute;
            height: 100%;
            left: 0%;
            right: 0%;
            background: linear-gradient(to right, #a855f7, #ec4899);
            border-radius: 4px;
        }
        .range-slider input[type="range"] {
            position: absolute;
            width: 100%;
            height: 6px;
            top: 0;
            background: none;
            pointer-events: none;
            -webkit-appearance: none;
            outline: none;
            margin: 0;
        }
        .range-slider input[type="range"]::-webkit-slider-thumb {
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: #fff;
            pointer-events: auto;
            -webkit-appearance: none;
            cursor: pointer;
            box-shadow: 0 0 4px rgba(0,0,0,0.5);
        }
'''
if '.range-slider' not in html:
    html = html.replace('</style>', css + '    </style>')

# 2. Update HTML
old_html = '''                <div>
                   <label class="text-xs text-white/50 flex justify-between mb-1"><span>Ano:</span> <span id="year-val" class="font-bold text-white">Todos</span></label>
                   <input type="range" id="year-slider" min="2009" max="2026" value="2009" class="w-full accent-purple-500 hover:accent-purple-400 cursor-pointer">
                </div>'''
                
new_html = '''                <div>
                   <label class="text-xs text-white/50 flex justify-between mb-1"><span>Ano:</span> <span id="year-val" class="font-bold text-white">2010 - 2026</span></label>
                   <div class="range-slider">
                        <div class="progress" id="slider-progress"></div>
                        <input type="range" id="year-start" min="2010" max="2026" value="2010" step="1">
                        <input type="range" id="year-end" min="2010" max="2026" value="2026" step="1">
                   </div>
                </div>'''
                
html = html.replace(old_html, new_html)

# 3. Update JS declarations
old_js_vars = '''        let currentEspecializada = 'Todas';
        const yearSliderEl = document.getElementById('year-slider');
        const yearVal = document.getElementById('year-val');'''

new_js_vars = '''        let currentEspecializada = 'Todas';
        const yearStartEl = document.getElementById('year-start');
        const yearEndEl = document.getElementById('year-end');
        const sliderProgress = document.getElementById('slider-progress');
        const yearVal = document.getElementById('year-val');'''

html = html.replace(old_js_vars, new_js_vars)

# 4. Update handle logic
old_handle_logic = '''        function handleYearSlider(e) {
            let y = parseInt(yearSliderEl.value);
            if (y === 2009) {
                yearVal.innerText = 'Todos';
            } else {
                yearVal.innerText = y.toString();
            }
            updateDashboard(currentEspecializada);
        }

        yearSliderEl.addEventListener('input', handleYearSlider);'''

new_handle_logic = '''        function updateSliderUI() {
            let start = parseInt(yearStartEl.value);
            let end = parseInt(yearEndEl.value);
            let min = parseInt(yearStartEl.min);
            let max = parseInt(yearStartEl.max);

            if (start > end) {
                let tmp = start;
                start = end;
                end = tmp;
            }

            yearVal.innerText = (start === end) ? start.toString() : start + " - " + end;

            let leftPercent = ((start - min) / (max - min)) * 100;
            let rightPercent = 100 - ((end - min) / (max - min)) * 100;
            
            sliderProgress.style.left = leftPercent + "%";
            sliderProgress.style.right = rightPercent + "%";
        }

        function handleYearSlider(e) {
            let start = parseInt(yearStartEl.value);
            let end = parseInt(yearEndEl.value);
            
            if(e.target.id === 'year-start' && start > end) {
                yearStartEl.value = end;
            }
            if(e.target.id === 'year-end' && end < start) {
                yearEndEl.value = start;
            }
            
            updateSliderUI();
            updateDashboard(currentEspecializada);
        }

        yearStartEl.addEventListener('input', handleYearSlider);
        yearEndEl.addEventListener('input', handleYearSlider);
        
        updateSliderUI();'''

html = html.replace(old_handle_logic, new_handle_logic)

# 5. Update updateDashboard
old_ud_logic = '''        function updateDashboard(esp) {
            currentEspecializada = esp;
            let year = parseInt(yearSliderEl.value);
            let validYears = [];
            if (year === 2009) {
                for(let y=2010; y<=2026; y++) validYears.push(y.toString());
            } else {
                validYears.push(year.toString());
            }'''

new_ud_logic = '''        function updateDashboard(esp) {
            currentEspecializada = esp;
            let start = parseInt(yearStartEl.value);
            let end = parseInt(yearEndEl.value);
            let validYears = [];
            for (let y = start; y <= end; y++) {
                validYears.push(y.toString());
            }'''

html = html.replace(old_ud_logic, new_ud_logic)

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
