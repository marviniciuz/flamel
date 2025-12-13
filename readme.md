# 🧪 Flamel: Sistema de Transmutação Digital de Documentos

O **Flamel** é um sistema web desenvolvido para "transmutar" (converter e melhorar) documentos PDF antigos, digitalizados ou com pouca legibilidade em formatos modernos, acessíveis e pesquisáveis.

## 🚀 Funcionalidades Principais

O sistema oferece três tipos de processamento ("transmutações") para documentos PDF:

### 1. Melhorar Legibilidade (PDF Otimizado)

-   **O que faz:** Recebe um PDF digitalizado (imagem), limpa o ruído visual, aumenta o contraste e gera um novo PDF onde o texto pode ser selecionado e pesquisado (Ctrl+F).
    
-   **Técnica:** Converte o PDF em imagens, aplica filtros de binarização (preto e branco puro) para remover sombras e sujidade, e remonta o PDF inserindo uma camada de texto invisível sobre a imagem limpa.
    

### 2. Extração de Texto (OCR)

-   **O que faz:** Lê o conteúdo visual de um PDF e extrai apenas o texto bruto.
    
-   **Técnica:** Utiliza OCR (_Optical Character Recognition_) para identificar caracteres nas imagens do PDF e salva o resultado num arquivo `.txt`.
    

### 3. PDF para Áudio (Acessibilidade/TTS)

-   **O que faz:** Converte o conteúdo escrito do documento num arquivo de áudio falado (Audiolivro).
    
-   **Técnica:** Extrai o texto via OCR e utiliza síntese de voz (TTS - _Text-to-Speech_) com sotaque brasileiro para gerar um arquivo `.mp3`.
    

## 🛠️ Arquitetura e Tecnologias

O projeto utiliza uma arquitetura moderna e assíncrona para garantir desempenho, mesmo ao processar arquivos pesados.

### Backend (O Cérebro)

-   **Linguagem:** Python 3.12+
    
-   **Framework Web:** **Django 5.x** (Gere rotas, base de dados e lógica).
    
-   **API:** **Django Rest Framework (DRF)** (Recebe os uploads e valida dados).
    
-   **Processamento Assíncrono:**
    
    -   **Celery:** Gestor de filas de tarefas. Executa o OCR e o tratamento de imagem em segundo plano para não bloquear o site.
        
    -   **Redis:** _Broker_ (Carteiro) que transporta as mensagens entre o Django e o Celery.
        

### Frontend (A Interface)

-   **Visual:** **Materialize CSS** (Framework responsivo com design moderno e limpo).
    
-   **Interatividade:** **HTMX**.
    
    -   Substitui a complexidade de frameworks como React/Angular.
        
    -   Permite atualizações dinâmicas da tela (tipo SPA), como barra de progresso e troca de telas, usando apenas atributos HTML.
        
-   **Templates:** Django Templates (HTML renderizado no servidor).
    

## 📚 Bibliotecas e Motores de Processamento

Estas são as ferramentas que fazem a "mágia" acontecer no código Python:

**Biblioteca Python**

**Função no Sistema**

**`opencv-python`**

**Visão Computacional.** Usada para limpar a imagem, aplicar escala de cinzentos e binarização (thresholding).

**`pytesseract`**

**OCR.** A ponte entre o Python e o motor Tesseract. Lê o texto da imagem.

**`pdf2image`**

Converte as páginas do PDF em imagens (JPG/PNG) para serem processadas.

**`PyMuPDF` (`fitz`)**

Manipulação avançada de PDF. Usado para criar o novo PDF otimizado e inserir a camada de texto invisível.

**`gTTS`**

**Google Text-to-Speech.** Converte o texto extraído em áudio MP3 (usando a API do Google Tradutor).

**`Pillow` (PIL)**

Manipulação básica de imagens.

### Softwares de Sistema (Dependências Externas)

Além do Python, o servidor precisa destes softwares instalados no Sistema Operativo (Linux/Windows):

1.  **Tesseract OCR Engine:** O motor que realmente lê o texto.
    
2.  **Poppler Utils:** Necessário para o `pdf2image` funcionar.
    
3.  **Redis Server:** O servidor de base de dados em memória para a fila de tarefas.
    

## 🔄 Fluxo de Dados (Como funciona)

1.  **Upload:** O utilizador envia o PDF via Frontend (HTMX).
    
2.  **Receção:** O Django recebe o arquivo e cria um registo na base de dados com estado `PENDENTE`.
    
3.  **Fila:** O Django envia o ID do documento para o **Redis**.
    
4.  **Processamento (Worker):** O **Celery** pega a tarefa do Redis e começa a trabalhar (OCR, OpenCV, TTS).
    
    -   _Enquanto isso, o utilizador vê uma tela de "A processar..." que se atualiza sozinha a cada 3 segundos via HTMX._
        
5.  **Conclusão:** O Celery salva o arquivo final (`.pdf`, `.txt` ou `.mp3`) e muda o estado para `SUCESSO`.
    
6.  **Entrega:** O HTMX deteta o sucesso e mostra o botão de **Download**.
    

## 🧪 Resumo da "Fórmula Flamel"

> **PDF Sujo** + **OpenCV** (Limpeza) + **Tesseract** (Leitura) + **Python** (Lógica) = **Documento Transmutado (Acessível)**