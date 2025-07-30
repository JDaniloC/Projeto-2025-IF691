# Análise de Conformidade por meio de uma interface de LLM
Um projeto que demonstra o impacto das LLMs (Modelos de Linguagem de Grande Escala) como interface para realizar análise de conformidade de processos de negócio.

## 🎯 Funcionalidades Principais
* **Análise de Conformidade com xSemAD**: Implementação de análise semântica de conformidade utilizando o framework xSemAD, que detecta anomalias de forma explicável.
* **Sistema de Q&A com LLM**: Interface de perguntas e respostas sobre processos de negócio usando modelos de linguagem
* **Agente Inteligente**: Agente baseado em LLM capaz de analisar e interpretar logs de processos
* **Análise de Restrições**: Suporte a múltiplos tipos de restrições como Precedence, Response, Succession, etc.

## 🛠️ Pré-requisitos
Antes de começar, garanta que você tenha os seguintes softwares instalados em seu sistema:
* [Python](https://www.python.org/downloads/) (versão 3.10 ou superior)
* [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de pacotes e dependências)

## 📦 Principais Dependências
* **pm4py**: Biblioteca central para mineração e análise de processos.
* **pandas**: Utilizada para a criação e manipulação dos DataFrames que servem como log de eventos.
* **transformers**: Biblioteca da Hugging Face para trabalhar com modelos de transformers.
* **langchain**: Framework para desenvolvimento de aplicações com LLMs.
* **torch**: Framework de deep learning do PyTorch.
* **nltk**: Biblioteca para processamento de linguagem natural.
* **python-dotenv**: Para gerenciamento de variáveis de ambiente.

## ⚙️ Instalação
Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente.

1.  **Clone o repositório:**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

2. **Crie um ambiente virtual:**
É recomendado criar um ambiente virtual para isolar as dependências do projeto. Você pode fazer isso com o Poetry ou manualmente com o venv do Python:
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate  # No Windows
```

3. **Instale as dependências:**
Para fazer isso, é possível utilizar o gerenciador de pacotes Poetry ou o pip. Abaixo estão as instruções para ambos os métodos.

3.1.  **Instale as dependências com Poetry:**
O comando a seguir irá ler o arquivo `pyproject.toml`, criar um ambiente virtual isolado para o projeto e instalar todas as dependências necessárias a partir do arquivo `poetry.lock` para garantir uma instalação 100% reprodutível.
```bash
poetry install
```

3.2.  **Instale as dependências com pip:**
Se preferir usar o pip, você pode instalar as dependências diretamente por meio do arquivo `pyproject.toml`.
```bash
pip install .
```

## 🚀 Como Executar o Projeto
O projeto contém notebooks Jupyter organizados em sequência numerada que demonstram as análises e experimentos realizados:

### Notebooks Principais (pasta `src/`)
1. **`1_xSemAD.ipynb`**: Análise inicial com o framework xSemAD
2. **`2_llm_qa.ipynb`**: Sistema de perguntas e respostas com LLM
3. **`3_llm_agent.ipynb`**: Implementação de agente baseado em LLM

### Configuração de Ambiente
1. Configure as variáveis de ambiente copiando o arquivo `.env.example` para `.env` na pasta `src/`:
```bash
cp src/.env.example src/.env
```
2. Edite o arquivo `.env` com suas credenciais de API (Google Gemini, etc.)

Siga a ordem numérica dos notebooks para reproduzir os resultados da pesquisa.

## 📂 Estrutura do Projeto
```
/
├── pyproject.toml           # Arquivo de definição do projeto e dependências
├── poetry.lock              # Lock file para instalações reprodutíveis
├── requirements.txt         # Dependências para instalação com pip
├── README.md                # Este arquivo de instruções
├── LICENSE                  # Licença do projeto
└── src/                     # Código-fonte principal do projeto
    ├── .env.example         # Exemplo de configuração de variáveis de ambiente
    ├── 1_xSemAD.ipynb       # Análise com framework xSemAD
    ├── 2_llm_qa.ipynb       # Sistema de Q&A com LLM
    ├── 3_llm_agent.ipynb    # Agente baseado em LLM
    ├── x_sem_ad.py          # Módulo principal do xSemAD
    ├── stateful_python_tool.py # Ferramenta Python com estado
    ├── data/                # Dados de entrada e modelos
    │   ├── InternationalDeclarations.xes # Log de eventos principal
    │   ├── context.txt      # Contexto para LLM
    │   ├── qa_prompt.txt    # Template de prompt para Q&A
    │   ├── agent_prompt.txt # Template de prompt para agente
    │   └── model/           # Modelos treinados
    ├── evaluation/          # Módulos de avaliação
    │   └── utils.py         # Utilitários para avaliação
    └── labelparser/         # Módulos para parsing de labels
        └── label_utils.py   # Utilitários para processamento de labels
```
