# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `virus_corona_sequence.fasta`
- **Tamanho Original:** 30.14 KB
- **Total de Bases:** 29,903

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 7.35 | 75.62 | 0.0119 | 0.0249 |
| **LZW (Real - JSON)** | 31.33 | -3.95 | 0.0067 | 0.0032 |
| **LZW (Teórico - Binário)** | 9.08 | 69.86 | 0.0067 | 0.0032 |

## Métricas Avançadas e Análise Teórica

### Análise do Algoritmo Huffman

- **Entropia de Shannon:** `1.9570` bits/símbolo
  - *Significado: Representa o **limite teórico** da compressão para este arquivo. É o número mínimo de bits, em média, necessários para representar cada caractere com base em suas frequências.*

- **Comprimento Médio do Código:** `2.0000` bits/símbolo
  - *Significado: Representa o **desempenho real** da nossa implementação. Um valor próximo da entropia indica uma compressão Huffman de altíssima eficiência, mostrando que o algoritmo se aproximou do ótimo teórico.*

### Análise do Algoritmo LZW

- **Tamanho Final do Dicionário:** `5,979` entradas
  - *Significado: Indica quantos padrões únicos e sequências repetitivas o algoritmo 'aprendeu'. Um número maior sugere que o arquivo possui uma estrutura com mais repetições que podem ser exploradas.*

- **Taxa de Redução de Símbolos:** `5.22`
  - *Significado: Mostra, em média, quantos caracteres do texto original foram representados por **um único código LZW**. Um valor maior é um forte indicador de alta eficiência de compressão.*


## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](../graficos/virus_corona_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](../graficos/virus_corona_sequence_comparativo_tempo.png)
