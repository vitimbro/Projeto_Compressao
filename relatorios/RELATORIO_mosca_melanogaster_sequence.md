# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `mosca_melanogaster_sequence.fasta`
- **Tamanho Original:** 142236.61 KB
- **Total de Bases:** 143,726,002

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 50038.34 | 64.82 | 72.1991 | 108.8063 |
| **LZW (Teórico - Binário)** | 40058.96 | 71.84 | 120.9860 | 30.3906 |
| **LZW (Real - JSON)** | 116623.29 | 18.01 | --- | --- |

## Métricas Avançadas e Análise Teórica

### Análise do Algoritmo Huffman

- **Entropia de Shannon:** `2.7856` bits/símbolo
  - *Significado: Representa o **limite teórico** da compressão para este arquivo. É o número mínimo de bits, em média, necessários para representar cada caractere com base em suas frequências.*

- **Comprimento Médio do Código:** `2.8520` bits/símbolo
  - *Significado: Representa o **desempenho real** da nossa implementação. Um valor próximo da entropia indica uma compressão Huffman de altíssima eficiência, mostrando que o algoritmo se aproximou do ótimo teórico.*

### Análise do Algoritmo LZW

- **Tamanho Final do Dicionário:** `13,673,712` entradas
  - *Significado: Indica quantos padrões únicos e sequências repetitivas o algoritmo 'aprendeu'. Um número maior sugere que o arquivo possui uma estrutura com mais repetições que podem ser exploradas.*

- **Taxa de Redução de Símbolos:** `10.51`
  - *Significado: Mostra, em média, quantos caracteres do texto original foram representados por **um único código LZW**. Um valor maior é um forte indicador de alta eficiência de compressão.*


## Análise de Complexidade de Espaço (Uso de Memória)

A seguir, uma análise do uso de memória das principais estruturas de dados de cada algoritmo.

### Huffman

- **Overhead (Tamanho do Cabeçalho):** `0.13` KB
  - *Significado: Representa o custo de espaço fixo do Huffman. É o tamanho da tabela de frequências que precisa ser armazenada junto com os dados para permitir a descompressão. Este valor é geralmente muito pequeno e independe do tamanho do arquivo.*

### LZW

- **Estrutura Principal (Dicionário):** `13,673,712` entradas, ocupando uma memória estimada de **`1075086.20` KB**
  - *Significado: Representa o custo de espaço dinâmico do LZW. O dicionário cresce à medida que o algoritmo processa o arquivo, consumindo memória proporcional à quantidade e ao tamanho dos padrões encontrados.*


## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](../graficos/mosca_melanogaster_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](../graficos/mosca_melanogaster_sequence_comparativo_tempo.png)
