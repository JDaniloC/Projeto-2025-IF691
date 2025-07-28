# Análise de Conformidade contextualizada por LLM
Um projeto que demonstra o impacto da análise de conformidade de processos de negócio contextualizada por LLMs (Modelos de Linguagem de Grande Escala).

## 🛠️ Pré-requisitos
Antes de começar, garanta que você tenha os seguintes softwares instalados em seu sistema:
* [Python](https://www.python.org/downloads/) (versão 3.13 ou superior)
* [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de pacotes e dependências)

## 📦 Principais Dependências
* **pm4py**: Biblioteca central para mineração e análise de processos.
* **pandas**: Utilizada para a criação e manipulação dos DataFrames que servem como log de eventos.
* **zeep**: Dependência customizada para se obter a árvore de movimentos do CNJ, instalada a partir de um [repositório Git](https://github.com/JDaniloC/python-zeep.git).

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
Dentro da pasta `src`, você encontrará os notebooks Jupyter que contêm as análises e experimentos realizados, basta seguir a ordem dos arquivos para reproduzir os resultados.

## 📂 Estrutura do Projeto
```
/
├── pyproject.toml      # Arquivo de definição do projeto e dependências
├── poetry.lock         # Lock file para instalações reprodutíveis
├── README.md           # Este arquivo de instruções
└── src                 # Código-fonte do projeto
    ├── data            # Pasta de dados de entrada
    └── x_xxxxx.ipynb   # Notebooks de análise
```
