# autou-email-classifier
Aplicação web para classificar e-mails usando IA, desenvolvido para o case prático da AutoU
# Case Prático AutoU - Classificador de Emails

**Status do Projeto:** Concluído ✔️

## 📖 Descrição do Projeto

Esta é uma aplicação web desenvolvida como parte do processo seletivo da AutoU. O objetivo é classificar e-mails em categorias ("Produtivo" ou "Improdutivo") e sugerir uma resposta automática adequada, utilizando Inteligência Artificial e automação para otimizar o fluxo de trabalho de equipes que lidam com um grande volume de mensagens.

O projeto foi construído com foco na autonomia e na capacidade de resolver problemas complexos, aplicando tecnologia de forma simples e eficiente para melhorar a vida do usuário, conforme a introdução do desafio.

---

## ✨ Funcionalidades

* **Classificação Inteligente:** Utiliza um modelo de NLP da API da Hugging Face para analisar e categorizar o conteúdo dos e-mails.
* **Geração de Resposta com IA:** Emprega uma solução de automação com Selenium para controlar a interface do Google Gemini, garantindo respostas de alta qualidade e contextualmente adequadas.
* **Múltiplos Formatos de Entrada:** Permite a análise de e-mails colados diretamente na interface, ou através do upload de arquivos `.txt` e `.pdf`.
* **Interface Web Moderna:** Uma interface limpa, intuitiva e responsiva, construída com Flask e JavaScript, que oferece uma experiência de usuário fluida e sem recarregamento de página.
* **Recursos de Usabilidade:** Inclui feedback de carregamento ("Analisando..."), rolagem automática para os resultados e um botão para copiar a resposta sugerida com um clique.

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript (com Fetch API)
* **Inteligência Artificial:**
    * **Classificação:** Hugging Face Inference API (Modelo `facebook/bart-large-mnli`)
    * **Geração de Resposta:** Google Gemini (via automação)
* **Automação de Navegador:** Selenium
* **Utilitários:** python-dotenv, pypdf

---

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar a aplicação no seu ambiente local.

**1. Pré-requisitos:**
* Python 3.x instalado.
* Google Chrome instalado.

**2. Clone o Repositório:**
```bash
git clone [https://github.com/VithorMohr/autou-email-classifier.git]
cd nome-da-pasta-do-projeto


3. Instale as Dependências:
É altamente recomendado criar um ambiente virtual antes de instalar as dependências.

Bash

pip install -r requirements.txt
4. Baixe o ChromeDriver:

Verifique a versão do seu Google Chrome (Menu > Ajuda > Sobre o Google Chrome).

Acesse a página oficial de downloads: https://googlechromelabs.github.io/chrome-for-testing/

Baixe a versão do ChromeDriver que seja exatamente compatível com a do seu navegador (plataforma win64).

Descompacte o arquivo e coloque o chromedriver.exe na raiz da pasta do projeto (ao lado do app.py).

5. Configure as Variáveis de Ambiente:

Crie uma cópia do arquivo .env.example e renomeie-a para .env.

Abra o arquivo .env e insira sua chave da API da Hugging Face:

HUGGINGFACE_API_TOKEN="sua_chave_huggingface_aqui"
6. Execute a Aplicação:

Bash

python app.py
Acesse http://127.0.0.1:5000 no seu navegador.

📝 Decisões Técnicas e Justificativas
Geração de Resposta via Automação com Selenium
Durante o desenvolvimento, foram realizados testes com múltiplas APIs de IA generativa (Google Gemini, Groq, e modelos de geração da Hugging Face). No entanto, foram encontrados obstáculos técnicos intransponíveis relacionados a bloqueios de acesso por região ou por tipo de conta, que impediram a integração direta.

Para contornar este desafio e ainda assim entregar uma solução com geração de respostas de alta qualidade, foi implementada uma abordagem de automação de navegador com Selenium. O script controla a interface web pública do Google Gemini, o que demonstra uma capacidade avançada de resolução de problemas e garante o cumprimento do requisito de forma criativa e eficaz.

Execução Local vs. Deploy na Nuvem
Conforme a justificativa acima, a aplicação possui uma dependência de um ambiente com o Google Chrome e o ChromeDriver correspondente para funcionar. Plataformas de hospedagem gratuitas na nuvem (como Vercel, Render, etc.) não oferecem este tipo de ambiente.

Seguindo a orientação do próprio case prático, optei por não realizar o deploy, focando em uma solução local robusta e bem documentada. O funcionamento completo da aplicação é demonstrado no vídeo abaixo.

🎬 Vídeo Demonstrativo
[https://www.loom.com/share/48a8e814154544759b140435a7b8f083?sid=adb52a42-a5f2-4824-b9fd-bad1ccc577ff]

Ex usado para email improdutivo
bom dia, como o solicitado segue meu currículo em anexo att


Exemplos usados para email produtivo
Olá equipe, gostaria de verificar o andamento do protocolo #789-C. Poderiam me dar uma atualização?

Bom dia, equipe. Gostaria de solicitar uma atualização sobre o andamento do caso 89-B. Poderiam me dar um retorno? Atenciosamente, Vithor.
