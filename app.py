import os
import pypdf
import requests
import time
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------------------------------------
# CONFIGURAÇÃO INICIAL E VARIÁVEIS DE AMBIENTE
# --------------------------------------------------------------------------

# Carrega as variáveis de ambiente do arquivo .env para manter as chaves seguras
load_dotenv()

# Configuração da API da Hugging Face para o serviço de classificação
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL_CLASSIFICACAO = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
hf_headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Inicialização da aplicação Flask
app = Flask(__name__)


# --------------------------------------------------------------------------
# FUNÇÕES DE INTELIGÊNCIA ARTIFICIAL
# --------------------------------------------------------------------------

def classificar_com_huggingface(texto_email):
    """
    Classifica um e-mail em 'Produtivo' ou 'Improdutivo' usando um modelo 
    de Zero-Shot Classification da Hugging Face.
    """
    
    # O prompt foi aprimorado com exemplos para dar mais contexto ao modelo,
    # aumentando a precisão em textos curtos ou ambíguos.
    prompt_melhorado = f"""
    A tarefa é classificar um e-mail em uma de duas categorias.
    'Produtivo': um e-mail que exige uma ação, resposta ou se refere a um trabalho em andamento (ex: 'gostaria de saber o status do meu pedido').
    'Improdutivo': um e-mail social, que não exige ação (ex: 'obrigado pela ajuda', 'feliz final de semana').

    Baseado nas definições acima, classifique o seguinte e-mail:
    E-mail: '{texto_email}'
    """

    payload = {
        "inputs": prompt_melhorado,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]},
    }
    
    # Realiza a chamada à API com tratamento de erro para o caso do modelo estar carregando (código 503)
    response = requests.post(API_URL_CLASSIFICACAO, headers=hf_headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        if response.status_code == 503:
            time.sleep(10)
            response = requests.post(API_URL_CLASSIFICACAO, headers=hf_headers, json=payload)
            if response.status_code == 200:
                return response.json()
        raise Exception(f"Erro na API Hugging Face: {response.status_code} - {response.text}")
    

def gerar_resposta_com_gemini_selenium(texto_email, categoria):
    """
    Gera uma resposta de e-mail utilizando automação de navegador com Selenium.

    Esta abordagem foi escolhida para contornar bloqueios de API encontrados em
    múltiplos serviços de IA generativa, garantindo uma resposta de alta qualidade
    através da automação da interface pública do Google Gemini.
    """
    
    # Configurações do Chrome para rodar em segundo plano e de forma estável
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Garante que a janela do navegador não apareça para o usuário
    options.add_argument('--log-level=3') 
    options.add_argument('--disable-gpu') 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    # Inicializa o serviço do ChromeDriver, que deve estar na mesma pasta do script
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Iniciando Selenium para acessar Gemini...")
        driver.get("https://gemini.google.com/app")
        
        # Define um tempo de espera máximo de 60 segundos para os elementos aparecerem
        wait = WebDriverWait(driver, 60)
        
        # Aguarda até que a caixa de texto esteja visível e clicável
        prompt_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.ql-editor[contenteditable="true"]')))
        
        prompt = ""
        if categoria == "Produtivo":
            prompt = f'Aja como um assistente de atendimento da empresa AutoU. Um cliente enviou o seguinte e-mail produtivo: "{texto_email}". Sua tarefa é escrever uma resposta curta e profissional em português, confirmando o recebimento e informando que a equipe analisará a solicitação. Responda apenas com o texto do e-mail sugerido, sem introduções ou despedidas adicionais.'
        else: # Improdutivo
            prompt = f'Aja como um assistente de atendimento da empresa AutoU. Um cliente enviou o seguinte e-mail social: "{texto_email}". Sua tarefa é escrever uma resposta curta e amigável em português, agradecendo a mensagem. Responda apenas com o texto do e-mail sugerido, sem introduções ou despedidas adicionais.'
        
        print("Enviando prompt para o Gemini...")
        from selenium.webdriver.common.keys import Keys

        # A automação digita o prompt e simula o aperto da tecla Enter para enviar
        prompt_box.send_keys(prompt + Keys.ENTER)
        
        # Aguarda a aparição do container da resposta para garantir que a IA terminou de gerar
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.model-response-text .markdown')))
        time.sleep(3) # Pausa extra para garantir que todo o texto foi renderizado

        print("Resposta recebida. Extraindo texto...")
        # Localiza todos os blocos de resposta e pega o último (o mais recente)
        response_elements = driver.find_elements(By.CSS_SELECTOR, ".model-response-text .markdown")
        resposta_gerada = response_elements[-1].text

        return resposta_gerada
    finally:
        # Garante que o navegador seja fechado ao final do processo, mesmo se ocorrer um erro
        driver.quit()

def analisar_com_ia(texto_email):
    """Função principal que orquestra a classificação e a geração."""
    try:
        # ETAPA 1: Classificação do e-mail usando a API da Hugging Face
        print(f"Enviando para classificação (Hugging Face): '{texto_email[:50]}...'")
        resultado_classificacao = classificar_com_huggingface(texto_email)
        categoria = resultado_classificacao['labels'][0]
        print(f"Categoria recebida: {categoria}")

        # ETAPA 2: Geração da resposta usando automação do Gemini via Selenium
        print(f"Enviando para geração (Gemini via Selenium)...")
        resposta_sugerida = gerar_resposta_com_gemini_selenium(texto_email, categoria)
        print("Resposta gerada com sucesso!")
        
        return {"categoria": categoria, "resposta_sugerida": resposta_sugerida}
    except Exception as e:
        print(f"ERRO no processo de análise: {e}")
        return {"categoria": "Erro", "resposta_sugerida": f"Não foi possível analisar o e-mail. Detalhes: {e}"}

# --------------------------------------------------------------------------
# ROTAS DA APLICAÇÃO FLASK
# --------------------------------------------------------------------------

@app.route('/')
def home():
    """Renderiza a página inicial da aplicação."""
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar_email():
    """Recebe os dados do formulário, processa e retorna a análise da IA."""
    texto_email = ""
    # Lógica para extrair o texto do formulário, seja da área de texto ou de um arquivo
    if 'email_text' in request.form and request.form['email_text'].strip():
        texto_email = request.form['email_text']
    elif 'email_file' in request.files:
        arquivo = request.files.get('email_file')
        if arquivo and arquivo.filename:
            if arquivo.filename.endswith('.txt'):
                texto_email = arquivo.read().decode('utf-8', errors='ignore')
            elif arquivo.filename.endswith('.pdf'):
                try:
                    reader = pypdf.PdfReader(arquivo.stream)
                    texto_completo = [page.extract_text() for page in reader.pages]
                    texto_email = "\n".join(texto_completo)
                except Exception as e:
                    return jsonify({"error": f"Não foi possível ler o arquivo PDF: {e}"}), 400

    if not texto_email.strip():
        return jsonify({"error": "Nenhum texto de e-mail fornecido."}), 400

    # Chama a função principal de análise e retorna o resultado em formato JSON
    resultado_ia = analisar_com_ia(texto_email)
    return jsonify(resultado_ia)

# Ponto de entrada para executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)