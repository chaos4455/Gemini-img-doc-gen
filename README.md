# 🐍 Gemini Python Snippet Doc/Image Generator (PT-BR) 🇧🇷

**Repository:** [https://github.com/chaos4455/Gemini-img-doc-gen](https://github.com/chaos4455/Gemini-img-doc-gen)
**Live Demo (Hugging Face Space):** [https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1](https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1)

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![AI Model](https://img.shields.io/badge/AI-Google%20Gemini-blueviolet.svg)](https://ai.google.dev/)
[![Pillow](https://img.shields.io/badge/Imaging-Pillow-blueviolet.svg)](https://python-pillow.org/)

---

Olá! Sou [Elias Andrade](https://www.linkedin.com/in/itilmgf/), um desenvolvedor que adora criar ferramentas para otimizar o fluxo de trabalho. Este projeto, `gemini-img-doc-gen`, é uma aplicação Streamlit que utiliza o poder do **Google Gemini** para **gerar automaticamente documentação em português** para trechos de código Python e, em seguida, renderiza essa documentação como **imagens PNG temáticas de alta qualidade**.

O objetivo é facilitar a criação de visuais atraentes e informativos sobre funções ou métodos específicos de um código, ideal para portfólios, apresentações, ou simplesmente para documentar partes importantes de um projeto de forma visualmente agradável.

✨ **Experimente a versão online no Hugging Face Spaces!** ✨
[https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1](https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1)

---

## 🖼️ Interface e Exemplo de Saída

A aplicação oferece uma interface simples via Streamlit para carregar seu código, configurar opções e visualizar os resultados:

*(Screenshot da interface Streamlit aqui - Substitua ou adicione se tiver uma atualizada)*
<img width="1920" alt="chrome_dgTevGfeyR" src="https://github.com/user-attachments/assets/92de5818-9b06-42b3-8e62-1ae2a5bc21aa" />

Exemplos de imagens PNG geradas com diferentes temas:

*(Adicione aqui as imagens PNG de exemplo que você já incluiu no README anterior, pois elas pertencem a ESTE projeto)*
![GitHub Dark Theme Example](https://github.com/user-attachments/assets/de902fd1-731b-466c-80bb-eb024200d5a3)
![Synthwave Theme Example](https://github.com/user-attachments/assets/789a0979-27be-43a4-8757-5392d6445cb8)
![Dracula Theme Example](https://github.com/user-attachments/assets/039fc0dd-a83b-4da9-9f6d-1319c2045d99)
![Forest Whisper Theme Example](https://github.com/user-attachments/assets/7428ec11-8a3c-49ca-a13d-fef66b3a69b5)

---

## ✨ Funcionalidades Principais

*   **🤖 Geração de Documentação com IA:** Utiliza modelos Google Gemini (Flash/Pro) para analisar código Python e identificar trechos essenciais.
*   **🇧🇷 Foco em Português (Brasil):** Gera títulos concisos e descrições **detalhadas** em PT-BR, explicando propósito, funcionamento, parâmetros e retorno.
*   **🎨 Temas Visuais:** Inclui múltiplos temas pré-definidos (Synthwave, Dracula, GitHub Dark, Forest Whisper) para estilizar as imagens geradas. Facilmente extensível com novos temas.
*   **🖼️ Geração de Imagem PNG:** Cria arquivos PNG para cada snippet documentado usando a biblioteca Pillow.
*   **🖍️ Syntax Highlighting na Imagem:** Aplica coloração de sintaxe básica ao código Python dentro da imagem, de acordo com o tema selecionado.
*   **✨ Alta Qualidade Visual:**
    *   **Supersampling:** Renderiza a imagem em tamanho maior (ex: 2x) e depois redimensiona (com filtro Lanczos) para obter anti-aliasing superior e texto mais nítido.
    *   **Fontes Customizadas:** Suporte para carregar fontes TrueType (.ttf) customizadas (requer instalação no ambiente de execução), permitindo melhor controle tipográfico e suporte a caracteres especiais/emojis (com fontes como Noto).
*   **⚙️ Configuração Flexível:** Permite ajustar parâmetros da IA (modelo, temperatura, top_p, top_k, max_tokens) e selecionar o tema visual via interface Streamlit.
*   **⬆️ Upload Fácil:** Interface Streamlit para fazer upload de arquivos `.py`.
*   **💬 Instruções Adicionais:** Campo para fornecer instruções extras para guiar a análise da IA.
*   **💾 Download Individual:** Botões para baixar cada imagem PNG gerada.

---

## 💡 Como Funciona?

1.  **Upload e Configuração:** O usuário carrega um arquivo `.py`, seleciona um tema visual, configura os parâmetros da IA e opcionalmente fornece instruções adicionais.
2.  **Envio para IA (Gemini):** O código Python e as instruções são enviados para o modelo Gemini selecionado, utilizando um prompt específico que instrui a IA a identificar snippets chave e gerar título/descrição em PT-BR no formato YAML.
3.  **Parsing da Resposta:** A resposta da IA (texto contendo blocos de código Python e YAML) é processada para extrair os pares de `código`, `título` e `descrição`.
4.  **Geração da Imagem (Pillow):** Para cada par válido:
    *   As fontes TTF definidas no tema são carregadas (com fallback).
    *   Uma imagem é criada em memória com dimensões *escaladas* (ex: 2x).
    *   Um fundo gradiente (definido no tema) é desenhado.
    *   O título, o bloco de código (com syntax highlighting básico aplicado token a token) e a descrição são desenhados na imagem usando as fontes e cores do tema, nas posições calculadas.
    *   A imagem escalada é redimensionada para o tamanho final usando um filtro de alta qualidade (Lanczos) para anti-aliasing (supersampling).
    *   A imagem final é salva como PNG em bytes.
5.  **Exibição e Download:** As imagens PNG geradas são exibidas na interface Streamlit, com botões de download individuais e expanders para ver o código/descrição originais.

---

## 🛠️ Tecnologias Utilizadas

*   [Python 3.8+](https://www.python.org/)
*   [Streamlit](https://streamlit.io/) - Framework da Interface Web
*   [Google Generative AI SDK (`google-generativeai`)](https://ai.google.dev/docs/python_sdk) - Interação com a API Gemini
*   [Pillow (PIL Fork)](https://python-pillow.org/) - Geração e manipulação de imagens
*   [PyYAML](https://pyyaml.org/) - Parsing da resposta YAML da IA
*   [python-dotenv](https://github.com/theskumar/python-dotenv) (Opcional) - Carregar variáveis de ambiente localmente

---

## 🚀 Como Usar

### 1. Online (Recomendado e Mais Fácil)

*   Acesse o **Hugging Face Space**: [https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1](https://huggingface.co/spaces/chaos4455/Gemini-2.0-PYTHON-snippet-doc-gen-img-v1)
*   **Importante:** Você precisará configurar sua chave da API Google Gemini nos **Secrets** do Space (nome da chave: `GOOGLE_API_KEY`). Veja a seção abaixo sobre como obter a chave.
*   Siga as instruções na interface: faça upload do seu arquivo `.py`, ajuste as configurações e clique em gerar!

### 2. Localmente

1.  **Pré-requisitos:**
    *   Python 3.8 ou superior instalado.
    *   Git instalado.
    *   **Fontes TTF Instaladas:** Este é o passo mais crítico para execução local! A aplicação espera encontrar fontes específicas (como Fira Code, JetBrains Mono, Inter, Noto Sans, etc.) nos caminhos definidos no dicionário `FONT_PATHS` dentro do script Python (ex: `/usr/share/fonts/...`).
        *   **Linux (Debian/Ubuntu):** Você pode instalar fontes usando `apt-get install fonts-firacode fonts-jetbrains-mono fonts-inter fonts-lato fonts-noto-color-emoji ...` (verifique nomes exatos dos pacotes). Se usar o `packages.txt` deste repo em um ambiente como Docker ou HF Spaces, ele já tenta instalar algumas.
        *   **Windows/macOS:** Você precisará baixar e instalar as fontes TTF manualmente no seu sistema e **provavelmente precisará editar os caminhos no dicionário `FONT_PATHS` no script Python** para apontar para os locais corretos onde as fontes foram instaladas no seu OS. Se as fontes não forem encontradas, a aplicação tentará usar fallbacks ou a fonte default do Pillow (com qualidade inferior e sem suporte a acentos/emojis).
2.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/chaos4455/Gemini-img-doc-gen.git
    cd Gemini-img-doc-gen
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Certifique-se de que o arquivo `requirements.txt` contenha: `streamlit`, `google-generativeai`, `Pillow`, `PyYAML`, `python-dotenv`)*
4.  **Configure a API Key:**
    *   **Recomendado:** Crie um arquivo chamado `.env` na pasta do projeto e adicione a linha:
        ```
        GOOGLE_API_KEY='SUA_CHAVE_API_AQUI'
        ```
    *   Ou configure a variável de ambiente `GOOGLE_API_KEY` diretamente no seu sistema (veja seção sobre API Key abaixo).
5.  **Execute a Aplicação:**
    ```bash
    streamlit run seu_script_principal.py
    ```
    *(Substitua `seu_script_principal.py` pelo nome real do arquivo Python principal)*
6.  **Dica para Windows:** Para facilitar a execução local no Windows, você pode usar o [Streamlit Script Launcher](https://github.com/chaos4455/Streamlit-script-launcher) que criei. Após configurar as dependências e a API Key, basta arrastar o arquivo `.py` da aplicação para o launcher.

---

## ⚙️ Configuração e Customização

*   **Temas Visuais:** Edite o dicionário `THEMES` no script para modificar cores, fontes e tamanhos dos temas existentes ou adicionar novos.
*   **Fontes:** O dicionário `FONT_PATHS` define os caminhos esperados para as fontes. Adapte-os se necessário para seu ambiente local ou instale as fontes nos locais padrão do Linux. A qualidade da imagem depende fortemente de fontes TTF corretas estarem acessíveis.
*   **Parâmetros da IA:** Ajuste `temperature`, `top_p`, `top_k`, `max_tokens` na interface Streamlit para controlar a criatividade e o tamanho da resposta da IA.
*   **Prompt da IA:** Modifique a função `create_documentation_prompt_for_parsing` para alterar como a IA é instruída a analisar o código e gerar a documentação.
*   **Supersampling:** O `scale_factor` na função `create_code_image_pillow_themed_custom_font` controla a qualidade (atualmente fixo em `2`). Aumentar para `3` pode melhorar ainda mais a qualidade (ao custo de performance).

---

## 🔑 Sobre a Chave da API do Google Gemini (Importante!)

*(Esta seção pode ser reutilizada do README anterior, pois as instruções são as mesmas)*

ℹ️ Para usar esta aplicação (tanto online no Space quanto localmente), você **precisa** de uma chave de API do Google Gemini.

1.  **Obtenha sua Chave de API:**
    *   Acesse o [**Google AI Studio**](https://aistudio.google.com/).
    *   Faça login com sua conta Google.
    *   Clique em "**Get API key**" (Obter chave de API).
    *   Crie um novo projeto ou selecione um existente.
    *   Sua chave de API será gerada. **Copie e guarde-a em um local seguro**.

2.  **Configure a Chave:**
    *   **No Hugging Face Space:** Vá em "Settings" -> "Secrets" e adicione um novo segredo chamado `GOOGLE_API_KEY` com o valor da sua chave.
    *   **Localmente (Recomendado):** Crie um arquivo `.env` na raiz do projeto com `GOOGLE_API_KEY='SUA_CHAVE_AQUI'`.
    *   **Localmente (Alternativa):** Defina a variável de ambiente `GOOGLE_API_KEY` no seu sistema operacional.
        *   Linux/macOS: `export GOOGLE_API_KEY='SUA_CHAVE_AQUI'`
        *   Windows (CMD): `set GOOGLE_API_KEY=SUA_CHAVE_AQUI`
        *   Windows (PowerShell): `$env:GOOGLE_API_KEY = 'SUA_CHAVE_AQUI'`
        *   Windows (Permanente): Use as configurações de variáveis de ambiente do sistema.

---

## 👤 Autor

*   **Elias Andrade**
    *   Desenvolvedor | Entusiasta de Automação, IA e Ferramentas Dev ✨
    *   📍 Maringá, Paraná, Brasil
    *   🔗 [LinkedIn: itilmgf](https://www.linkedin.com/in/itilmgf/)
    *   🐙 [GitHub: chaos4455](https://github.com/chaos4455)
    *   📱 WhatsApp: +55 11 9 1335 3137 (Contato profissional/colaboração)

---

## ©️ Licença

Este projeto está licenciado sob a Licença MIT. Consulte [MIT License](https://opensource.org/licenses/MIT) para mais detalhes.
