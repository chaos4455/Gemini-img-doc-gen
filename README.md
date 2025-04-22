# 🖼️ Gemini Image Collage Generator (gemini-img-doc-gen)

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()
[![Framework](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![Pillow](https://img.shields.io/badge/Imaging-Pillow-blueviolet.svg)](https://python-pillow.org/)

Olá! Eu sou [Elias Andrade](https://www.linkedin.com/in/itilmgf/), um desenvolvedor com mais de 15 anos de experiência, e este é um dos meus projetos pessoais: o `gemini-img-doc-gen`. Como entusiasta da criação das minhas próprias ferramentas para otimizar fluxos de trabalho, desenvolvi esta aplicação para simplificar e agilizar a criação de colagens de imagens, incorporando funcionalidades inteligentes para lidar com duplicatas e performance.

Atualmente, o foco principal desta ferramenta é a **geração eficiente de colagens de imagens** com recursos avançados. A parte "Gemini" no nome reflete uma aspiração futura ou integração potencial com modelos de IA generativa para documentação ou outras tarefas (veja a seção sobre a API Key do Gemini).


---

## ✨ Funcionalidades Principais

Este projeto oferece uma interface gráfica intuitiva (construída com PyQt5) para criar colagens a partir de imagens arrastadas para a aplicação:

*   **🖼️ Interface Drag & Drop:** Simplesmente arraste e solte seus arquivos de imagem na janela.
*   **⚙️ Redimensionamento Automático:** As imagens são redimensionadas para `50%` (configurável no código via `RESIZE_FACTOR`) de seu tamanho original antes de serem adicionadas à colagem, usando um filtro de alta qualidade (Lanczos).
*   **🧠 Remoção Inteligente de Duplicatas:**
    *   Calcula o hash (SHA256) do conteúdo de cada imagem.
    *   Verifica também nomes de arquivos idênticos.
    *   **Mantém apenas a versão mais antiga** (baseado no timestamp de criação do arquivo - `ctime`) em caso de conteúdo ou nome duplicado. Isso evita colagens repetitivas e preserva a imagem "original" caso haja cópias.
*   **🚀 Processamento Paralelo:** Utiliza `ThreadPoolExecutor` para carregar, calcular hash e redimensionar imagens em paralelo, aproveitando múltiplos núcleos de CPU para acelerar o processo, especialmente com muitas imagens.
*   **📊 Feedback Visual:** Uma barra de progresso informa o status do processamento (carregamento, filtragem, montagem, salvamento) e o tempo decorrido.
*   **💾 Salvamento Automático:** A colagem final é salva automaticamente como um arquivo PNG no diretório `C:\colagens_filtradas` (configurável no código via `save_path`) com um nome único baseado em timestamp e hash.
*   **✅ Tratamento de Erros:** Exibe mensagens de erro claras na interface caso ocorram problemas (ex: arquivo não encontrado, erro ao processar imagem, erro ao criar diretório).
*   **🚫 Cancelamento:** Permite cancelar o processo em andamento ao tentar fechar a janela.

---

## 💡 Por Que Criei Este Projeto?

Como desenvolvedor há mais de 15 anos, sempre acreditei no poder de criar minhas próprias ferramentas. Muitas vezes, as soluções existentes não se encaixam perfeitamente nas minhas necessidades ou fluxos de trabalho específicos. Este projeto nasceu da necessidade de agrupar visualmente conjuntos de imagens de forma rápida, mas com o controle adicional de evitar duplicatas baseadas não só no nome, mas no conteúdo real e na data, algo que ferramentas comuns nem sempre oferecem de forma tão direta.

Além disso, é uma ótima oportunidade para praticar e demonstrar o uso de tecnologias como:

*   **🐍 Python:** Linguagem versátil e poderosa.
*   **🖼️ Pillow:** Biblioteca essencial para manipulação de imagens em Python.
*   **💻 PyQt5:** Um framework robusto para criação de interfaces gráficas desktop.
*   **⚡ `concurrent.futures`:** Para explorar o paralelismo e otimizar a performance.
*   **🔒 `hashlib`:** Para a verificação de integridade e identificação única de conteúdo.


![b8cc8b0c81bb3ea67ea1ac6622c7f3adcbb3994707e52011239c5028](https://github.com/user-attachments/assets/de902fd1-731b-466c-80bb-eb024200d5a3)

![07359e92e67a23f3d770e35a5f19849a407ad8b7923e93e7f08e0047](https://github.com/user-attachments/assets/789a0979-27be-43a4-8757-5392d6445cb8)

![ed76eeda6661b1fa8634fabef9399c0e05b29b320ee1569c99790b44](https://github.com/user-attachments/assets/039fc0dd-a83b-4da9-9f6d-1319c2045d99)

![199bcd9151955d9ec1d0a556babfc8ad72356e1580f5e44deec5f9f2](https://github.com/user-attachments/assets/7428ec11-8a3c-49ca-a13d-fef66b3a69b5)



---

## 🛠️ Tecnologias Utilizadas

*   [Python 3.8+](https://www.python.org/)
*   [PyQt5](https://riverbankcomputing.com/software/pyqt/)
*   [Pillow (PIL Fork)](https://python-pillow.org/)
*   `concurrent.futures` (Módulo nativo do Python)
*   `hashlib` (Módulo nativo do Python)
*   `dataclasses` (Módulo nativo do Python)

---

## 🚀 Como Usar

1.  **Pré-requisitos:**
    *   Certifique-se de ter o Python 3.8 ou superior instalado.
    *   Você precisará instalar as bibliotecas necessárias.

2.  **Instalação das Dependências:**
    Abra seu terminal ou prompt de comando e execute:
    ```bash
    pip install Pillow PyQt5
    ```
    *(Se você criar um arquivo `requirements.txt`, pode usar `pip install -r requirements.txt`)*

3.  **Executando a Aplicação:**
    *   Salve o código fornecido como um arquivo Python (por exemplo, `collage_generator.py`).
    *   Navegue até o diretório onde salvou o arquivo via terminal.
    *   Execute o script:
        ```bash
        python collage_generator.py
        ```

4.  **Criando a Colagem:**
    *   A janela da aplicação será aberta.
    *   Arraste os arquivos de imagem (PNG, JPG, WEBP, BMP, GIF, TIFF) que deseja incluir na colagem para dentro da área indicada ("Arraste imagens aqui...").
    *   O processo iniciará automaticamente. A barra de progresso mostrará as etapas: processamento inicial, filtragem de duplicatas, montagem da colagem e salvamento.
    *   Após a conclusão, uma mensagem de sucesso será exibida, indicando o caminho onde a colagem foi salva (por padrão: `C:\colagens_filtradas\colagem_filtrada_*.png`).

---

## ⚙️ Configuração (Opcional)

Você pode ajustar alguns parâmetros diretamente no código-fonte:

*   `RESIZE_FACTOR`: Controla a porcentagem de redimensionamento das imagens (padrão: `0.50` para 50%). Mude este valor decimal para ajustar o tamanho das imagens na colagem.
*   `save_path`: Define o diretório onde as colagens serão salvas (padrão: `r'C:\colagens_filtradas'`). Altere esta string para o caminho desejado.
*   `RESAMPLING_FILTER`: Define o algoritmo de redimensionamento (padrão: `Image.Resampling.LANCZOS`). Você pode experimentar outros filtros da biblioteca Pillow se necessário.

---

## 🧠 Lógica de Detecção de Duplicatas

A remoção de duplicatas é um recurso chave e funciona da seguinte maneira:

1.  **Processamento Inicial:** Todas as imagens arrastadas são carregadas, têm seu hash de conteúdo (SHA256) calculado *antes* de qualquer modificação (como redimensionamento ou conversão de modo de cor), e seu timestamp de criação (`ctime`) é registrado.
2.  **Identificação dos Melhores Candidatos:**
    *   Um dicionário rastreia o **hash de conteúdo** e armazena o timestamp de criação e o índice da imagem *mais antiga* encontrada com aquele hash.
    *   Outro dicionário faz o mesmo, mas usando o **nome do arquivo (basename)** como chave.
3.  **Seleção Final:** O conjunto final de imagens a serem incluídas na colagem é formado pelas imagens que foram consideradas as "mais antigas" tanto na verificação por hash quanto na verificação por nome de arquivo. Isso garante que, se houver múltiplas cópias exatas ou arquivos com o mesmo nome, apenas a versão criada primeiro será usada.
4.  **Resultado:** A colagem é montada usando apenas as imagens únicas selecionadas, preservando a ordem original o máximo possível.

---

## 🔑 Sobre a Chave da API do Google Gemini (Importante!)

ℹ️ **Nota:** O código fornecido neste repositório, em seu estado atual, **não utiliza a API do Google Gemini**. Ele foca exclusivamente na criação de colagens de imagens com as funcionalidades descritas acima.

No entanto, como o nome do projeto (`gemini-img-doc-gen`) sugere uma intenção de integração futura ou o uso em um contexto mais amplo envolvendo o Gemini, e conforme solicitado, aqui estão as instruções sobre como obter e configurar uma chave de API do Google Gemini:

1.  **Obtenha sua Chave de API:**
    *   Acesse o [**Google AI Studio**](https://aistudio.google.com/).
    *   Faça login com sua conta Google.
    *   Clique em "**Get API key**" (Obter chave de API) no menu lateral ou em um dos botões/links disponíveis na interface.
    *   Crie um novo projeto ou selecione um existente, se solicitado.
    *   Sua chave de API será gerada. **Copie e guarde-a em um local seguro**, pois ela não será exibida novamente.

2.  **Configure a Chave como Variável de Ambiente (Recomendado):**
    A maneira mais segura e recomendada de usar chaves de API é através de variáveis de ambiente. O código que eventualmente usar a API provavelmente procurará por uma variável chamada `GOOGLE_API_KEY`.

    *   **Linux/macOS:**
        ```bash
        export GOOGLE_API_KEY='SUA_CHAVE_API_AQUI'
        ```
        *(Adicione esta linha ao seu `~/.bashrc`, `~/.zshrc` ou perfil similar para torná-la permanente).*

    *   **Windows (Prompt de Comando):**
        ```cmd
        set GOOGLE_API_KEY=SUA_CHAVE_API_AQUI
        ```
        *(Isso define a variável apenas para a sessão atual do prompt).*

    *   **Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_API_KEY = 'SUA_CHAVE_API_AQUI'
        ```
        *(Também para a sessão atual).*

    *   **Windows (Permanente):**
        *   Pesquise por "Variáveis de ambiente" no menu Iniciar e selecione "Editar as variáveis de ambiente do sistema".
        *   Clique em "Variáveis de Ambiente...".
        *   Em "Variáveis de usuário" ou "Variáveis do sistema", clique em "Novo...".
        *   Nome da variável: `GOOGLE_API_KEY`
        *   Valor da variável: `SUA_CHAVE_API_AQUI`
        *   Clique em OK em todas as janelas. Talvez seja necessário reiniciar o terminal ou o IDE para que a alteração tenha efeito.

3.  **Alternativa (Não Recomendado): Refatorar o Código:**
    Se preferir não usar variáveis de ambiente, você precisaria modificar o código (futuro) que usa a API para aceitar a chave diretamente como uma string. **Isso não é recomendado por razões de segurança**, pois a chave ficaria exposta no código-fonte.

---

## 👤 Autor

*   **Elias Andrade**
    *   Desenvolvedor de Software (15+ anos de experiência)
    *   📍 Maringá, Paraná, Brasil
    *   🔗 [LinkedIn: itilmgf](https://www.linkedin.com/in/itilmgf/)
    *   🐙 [GitHub: chaos4455](https://github.com/chaos4455)
    *   📱 WhatsApp: +55 11 9 1335 3137

---

## ©️ Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes (se houver um) ou consulte [MIT License](https://opensource.org/licenses/MIT).
