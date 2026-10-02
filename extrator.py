import requests
from bs4 import BeautifulSoup

url = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

resposta = requests.get(url)

# Verifica se a pagina respondeu com sucesso (codigo HTTP 200)
if resposta.status_code == 200:
    print("Sucesso ao acessar a página")
    sopa = BeautifulSoup(resposta.text,"html.parser")
    print("Título da página:",sopa.title.text)
else:
    print(f"Erro ao acessar a página. Código:{resposta.status_code}")

# Procura todas as linhas de tabela na página
linhas = sopa.find_all("tr")
print(f"Total de linhas encontradas:{len(linhas)}")

# Mostra o texto da primeira linha para ver o que tem nela (normalmente é o cabeçalho)
if linhas:
    print("Cabeçalho:", linhas[0].text.strip().split())

clientes = []

# Pulamos a primeira linha (linhas [0]) porque ela é o cabeçalho da tabela
for linha in linhas [1:]:
    colunas = linha.find_all("td")

    # Se a linha tiver colunas de dados
    if colunas:
        # Pega o texto de cada coluna e limpa espaços extras com .strip()
        cliente = {
            "nome": colunas[0].text.strip(),
            "email": colunas[1].text.strip(),
            "saldo": colunas[2].text.strip(),
            "perfil": colunas[3].text.strip()
        }
        clientes.append(cliente)

print(f"Total de clientes extraídos:{len(clientes)}")
print("Exemplo do primeiro cliente extraído:")
print(clientes[0])

# Substitua pela Test URL que aparece no seu nó de Webhook do n8n
webhook_url = "http://localhost:5678/webhook-test/clientes-investimento"

# Comentar a variavel acima e descomentar a variavel abaixo
# webhook_url = "http://localhost:5678/webhook/clientes-investimento"

# Enviamos a lista via JSON
resposta_n8n = requests.post(webhook_url, json={"clientes": clientes})

print(f"Status do envio para o n8n: {resposta_n8n.status_code}")