# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `virus_phage-lambda_sequence.fasta`
- **Tamanho Original:** 48.10 KB
- **Total de Bases:** 48,502

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 11.89 | 75.28 | 0.0125 | 0.0254 |
| **LZW (Real - JSON)** | 49.75 | -3.43 | 0.0093 | 0.0031 |
| **LZW (Teórico - Binário)** | 15.25 | 68.30 | 0.0093 | 0.0031 |

## Métricas Avançadas e Análise Teórica

### Análise do Algoritmo Huffman

- **Entropia de Shannon:** `1.9986` bits/símbolo
  - *Significado: Representa o **limite teórico** da compressão para este arquivo. É o número mínimo de bits, em média, necessários para representar cada caractere com base em suas frequências.*

- **Comprimento Médio do Código:** `2.0000` bits/símbolo
  - *Significado: Representa o **desempenho real** da nossa implementação. Um valor próximo da entropia indica uma compressão Huffman de altíssima eficiência, mostrando que o algoritmo se aproximou do ótimo teórico.*

### Análise do Algoritmo LZW

- **Tamanho Final do Dicionário:** `9,176` entradas
  - *Significado: Indica quantos padrões únicos e sequências repetitivas o algoritmo 'aprendeu'. Um número maior sugere que o arquivo possui uma estrutura com mais repetições que podem ser exploradas.*

- **Taxa de Redução de Símbolos:** `5.44`
  - *Significado: Mostra, em média, quantos caracteres do texto original foram representados por **um único código LZW**. Um valor maior é um forte indicador de alta eficiência de compressão.*


## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](virus_phage-lambda_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](virus_phage-lambda_sequence_comparativo_tempo.png)
