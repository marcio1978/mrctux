import os
import re
from collections import defaultdict
from datetime import datetime

log_path = '/var/log/squid/access.log'
saida_dir = '/var/www/html/wordpress/relatorio'
os.makedirs(saida_dir, exist_ok=True)

# Estrutura: acessos[dia][tipo][ip] = lista de acessos
acessos = defaultdict(lambda: {'liberado': defaultdict(list), 'bloqueado': defaultdict(list)})
banda_por_ip = defaultdict(lambda: defaultdict(int))  # banda_por_ip[dia][ip]

regex = re.compile(r'(\d+\.\d+)\s+\d+\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)')

with open(log_path, 'r') as arquivo:
    for linha in arquivo:
        match = regex.search(linha)
        if match:
            timestamp, ip, status, tamanho, metodo, url = match.groups()
            dt = datetime.fromtimestamp(float(timestamp))
            data = dt.strftime('%Y-%m-%d')
            horario = dt.strftime('%H:%M:%S')
            tamanho = int(tamanho)

            tipo = 'bloqueado' if 'DENIED' in status else 'liberado'
            acessos[data][tipo][ip].append((horario, status, metodo, url, tamanho))
            if tipo == 'liberado':
                banda_por_ip[data][ip] += tamanho

# Gerar HTML por dia
for data, tipos in acessos.items():
    with open(f'{saida_dir}/{data}.html', 'w') as f:
        f.write(f'''<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório de Acessos - {data}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .botoes button {{ padding: 10px; margin-right: 10px; }}
        .secao {{ display: none; }}
    </style>
    <script>
        function mostrar(tipo) {{
            document.getElementById('liberado').style.display = 'none';
            document.getElementById('bloqueado').style.display = 'none';
            document.getElementById(tipo).style.display = 'block';
        }}
    </script>
</head>
<body>
    <h1>Relatório de Acessos do Squid - {data}</h1>
    <div class="botoes">
        <button onclick="mostrar('liberado')">Acessos Liberados</button>
        <button onclick="mostrar('bloqueado')">Acessos Bloqueados</button>
    </div>
''')

        # Seção liberado
        f.write('<div id="liberado" class="secao">')
        f.write('<h2>Acessos Liberados</h2>')
        for ip, entradas in tipos['liberado'].items():
            total_kb = banda_por_ip[data][ip] / 1024
            f.write(f'<h3>IP: {ip} - Banda: {total_kb:.2f} KB</h3><ul>')
            for horario, status, metodo, url, tamanho in entradas:
                f.write(f'<li>[{horario}] - {status} - {metodo} - {tamanho} bytes - <a href="{url}" target="_blank">{url}</a></li>')
            f.write('</ul><hr>')
        f.write('</div>')

        # Seção bloqueado
        f.write('<div id="bloqueado" class="secao">')
        f.write('<h2>Acessos Bloqueados</h2>')
        for ip, entradas in tipos['bloqueado'].items():
            f.write(f'<h3>IP: {ip}</h3><ul>')
            for horario, status, metodo, url, tamanho in entradas:
                f.write(f'<li>[{horario}] - {status} - {metodo} - <a href="{url}" target="_blank">{url}</a></li>')
            f.write('</ul><hr>')
        f.write('</div>')

        f.write('<script>mostrar("liberado");</script>')
        f.write('</body></html>')

# Gerar índice
with open(f'{saida_dir}/index.html', 'w') as f:
    f.write('<html><head><meta charset="UTF-8"><title>Índice</title></head><body>')
    f.write('<h1>Relatórios Diários</h1><ul>')
    for data in sorted(acessos.keys()):
        f.write(f'<li><a href="{data}.html">{data}</a></li>')
    f.write('</ul></body></html>')

print(f'✅ Relatórios diários gerados com sucesso no diretório: {saida_dir}')
