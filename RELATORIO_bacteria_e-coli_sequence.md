# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `bacteria_e-coli_sequence.fasta`
- **Tamanho Original:** 4597.69 KB
- **Total de Bases:** 4,641,652

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 1133.27 | 75.35 | 0.8363 | 0.9472 |
| **LZW (Real - JSON)** | 3941.95 | 14.26 | 1.0600 | 0.4779 |
| **LZW (Teórico - Binário)** | 1329.53 | 71.08 | 1.0600 | 0.4779 |

## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](bacteria_e-coli_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](bacteria_e-coli_sequence_comparativo_tempo.png)
