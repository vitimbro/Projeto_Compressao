# Projeto_Compressao

Projeto em grupo da Disciplina de Algoritmos e Estrutura de Dados ll.

O objetivo do projeto é implementar e realizar uma análise comparativa de desempenho entre dois algoritmos de compressão clássicos: Huffman (compressão estatística) e Lempel-Ziv-Welch - LZW (compressão baseada em dicionário). O estudo de caso escolhido para a análise foi a compressão de dados genômicos, utilizando sequências de DNA em formato FASTA.

### Como Usar

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

1. Pré-requisitos
- Python 3.8 ou superior
- Git

1. Clonando o Repositório

``` bash
git clone [URL_DO_SEU_REPOSITORIO_NO_GITHUB]
cd [NOME_DA_PASTA_DO_PROJETO]
```

3. Configuração do Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

``` bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual

# No Windows: 
venv\Scripts\activate 
# No macOS/Linux: 
source venv/bin/activate
```

4. Instalação das Dependências

Crie um arquivo chamado `requirements.txt` na pasta raiz do projeto com o seguinte conteúdo:

```
matplotlib
```

Em seguida, instale as dependências com o pip:

``` bash
pip install -r requirements.txt
```

5. Preparando os Dados

Baixe os arquivos de genoma em formato .fasta que deseja analisar. Uma boa fonte é:

NCBI GenBank: https://www.ncbi.nlm.nih.gov/nuccore

Coloque os arquivos baixados dentro da pasta data/.

6. Executando a Análise

Abra o arquivo src/main.py em um editor de texto.

Localize a variável arquivo_base e altere seu valor para o nome do arquivo que você deseja analisar (sem a extensão .fasta).

``` python
# Em src/main.py
arquivo_base = "virus_phage-lambda_sequence" # Altere para "bacteria_e-coli_sequence" ou outro
```

Salve o arquivo.

No terminal (com o ambiente virtual ainda ativo), execute o script principal:

``` bash
python src/main.py
```
