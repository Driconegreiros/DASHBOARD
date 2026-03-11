import re

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. btnTodas initialization
html = html.replace("rawData.total.toLocaleString('pt-BR')", "Object.values(rawData.especializadas_totals).reduce((a, b) => a + b, 0).toLocaleString('pt-BR')")

# 2. Charts initialization (Data fields)
html = html.replace('Object.keys(rawData.anos)', '[]')
html = html.replace('Object.values(rawData.anos)', '[]')

html = html.replace('Object.keys(rawData.classes)', '[]')
html = html.replace('Object.values(rawData.classes).map(v => v * 100)', '[]')

html = html.replace('Object.keys(rawData.assuntos)', '[]')
html = html.replace('Object.values(rawData.assuntos).map(v => v * 100)', '[]')

# 3. Call updateDashboard('Todas') at the end to populate
if "updateDashboard('Todas');" not in html[html.rfind('</script>'):]:
    html = html.replace('</script>\n</body>', "    // Initial load\n    updateDashboard('Todas');\n</script>\n</body>")

with open(r'c:\Users\adriano.castro\Desktop\Referências\Dashboards\taskade.com_share_apps_ujtqojrsimcct6io\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
