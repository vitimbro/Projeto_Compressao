# Projeto_Compressao

Projeto em grupo da Disciplina de Algoritmos e Estrutura de Dados ll.

O objetivo do projeto é implementar e realizar uma análise comparativa de desempenho entre dois algoritmos de compressão clássicos: Huffman (compressão estatística) e Lempel-Ziv-Welch - LZW (compressão baseada em dicionário). O estudo de caso escolhido para a análise foi a compressão de dados genômicos, utilizando sequências de DNA em formato FASTA.

### Tecnologias Utilizadas

Linguagem: Python 3.10+

Bibliotecas Externas:
- matplotlib: para a geração dos gráficos comparativos.

### Como Usar (via GitHub Codespaces)

Este projeto é otimizado para ser executado diretamente no seu navegador usando o GitHub Codespaces, sem a necessidade de nenhuma instalação local.

0. Preparando os Dados

Baixe os arquivos de genoma em formato .fasta que deseja analisar. Uma boa fonte é:

NCBI GenBank: https://www.ncbi.nlm.nih.gov/nuccore

Coloque os arquivos baixados dentro da pasta data/.

1. Iniciando o Ambiente
   
- Na página principal deste repositório no GitHub, clique no botão verde "< > Code".
- Mude para a aba "Codespaces".
- Clique em "Create codespace on main". Aguarde um ou dois minutos enquanto o GitHub prepara seu ambiente de desenvolvimento na nuvem.

2. Configurando e Executando o Projeto
   
Uma vez que o ambiente carregar, siga os passos no terminal integrado que aparecerá na parte inferior da tela:

- Crie e Ative o Ambiente Virtual:

``` bash
python -m venv venv
source venv/bin/activate
```

- Instale as Dependências:

``` bash
pip install -r requirements.txt
```

- Execute a Análise:

``` bash
python src/main.py
```

O programa irá listar os arquivos .fasta disponíveis na pasta data/ e pedirá para você escolher um para analisar.


3. Visualizando os Resultados
   
Relatório no Terminal: A tabela comparativa final será exibida diretamente no terminal.

Arquivos Gerados: Após a execução, os gráficos (.png) e o relatório (.md) aparecerão nas pastas graficos/ e relatorios/, respectivamente, no explorador de arquivos à esquerda.

Visualizando o Relatório Formatado:

Clique no arquivo de relatório gerado (ex: relatorios/RELATORIO_bacteria_e-coli_sequence.md).

Para visualizar o arquivo de forma formatada e bonita (com tabelas e imagens), use o atalho Ctrl + Shift + V.
