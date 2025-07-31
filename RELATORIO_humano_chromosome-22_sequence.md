# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `humano_chromosome-22_sequence.fasta`
- **Tamanho Original:** 50336.44 KB
- **Total de Bases:** 50,818,468

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 15772.12 | 68.67 | 11.2468 | 15.7926 |
| **LZW (Real - JSON)** | 29263.49 | 41.86 | 23.3278 | 4.1289 |
| **LZW (Teórico - Binário)** | 9722.73 | 80.68 | 23.3278 | 4.1289 |

## Métricas Avançadas e Análise Teórica

### Análise do Algoritmo Huffman

- **Entropia de Shannon:** `2.3162` bits/símbolo
  - *Significado: Representa o **limite teórico** da compressão para este arquivo. É o número mínimo de bits, em média, necessários para representar cada caractere com base em suas frequências.*

- **Comprimento Médio do Código:** `2.5425` bits/símbolo
  - *Significado: Representa o **desempenho real** da nossa implementação. Um valor próximo da entropia indica uma compressão Huffman de altíssima eficiência, mostrando que o algoritmo se aproximou do ótimo teórico.*

### Análise do Algoritmo LZW

- **Tamanho Final do Dicionário:** `3,620,645` entradas
  - *Significado: Indica quantos padrões únicos e sequências repetitivas o algoritmo 'aprendeu'. Um número maior sugere que o arquivo possui uma estrutura com mais repetições que podem ser exploradas.*

- **Taxa de Redução de Símbolos:** `14.04`
  - *Significado: Mostra, em média, quantos caracteres do texto original foram representados por **um único código LZW**. Um valor maior é um forte indicador de alta eficiência de compressão.*


## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](humano_chromosome-22_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](humano_chromosome-22_sequence_comparativo_tempo.png)
