from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

# Função para encontrar o CPF baseado no telefone
def encontrar_cpf_por_telefone(telefone):
    try:
        with open('dados.txt', 'r') as file:
            for line in file:
                cpf, telefone_atual = line.strip().split(',')
                if telefone == telefone_atual:
                    return cpf
    except FileNotFoundError:
        return None

# Função para consultar a API com o CPF
def consultar_api_cpf(cpf):
    url = f'https://sitedoaplicativo.xyz:8443/?port=3000&id=consulta&key=COD-IJKHSADU&tp=cpf&cpf={cpf}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            if 'DadosBasicos' in dados:
                return dados['DadosBasicos']
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Erro ao consultar API: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        telefone = request.form['telefone']
        cpf = encontrar_cpf_por_telefone(telefone)
        if cpf:
            dados_api = consultar_api_cpf(cpf)
            if dados_api:
                return render_template('index.html', cpf=cpf, telefone=telefone, dados=dados_api)
            else:
                return render_template('index.html', cpf=cpf, telefone=telefone, erro="Não foi possível consultar os dados na API.")
        else:
            return render_template('index.html', erro="Telefone não encontrado.")
    return render_template('index.html')

# No Railway, ele usa o WSGI, então não chamamos app.run()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
