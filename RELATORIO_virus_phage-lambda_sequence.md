# Relatório de Análise Comparativa de Compressão

## Arquivo Analisado
- **Nome:** `virus_phage-lambda_sequence.fasta`
- **Tamanho Original:** 48.10 KB
- **Total de Bases:** 48,502

## Tabela de Resultados

| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |
|---|---|---|---|---|
| **Huffman** | 11.89 | 75.28 | 0.0082 | 0.0186 |
| **LZW (Real - JSON)** | 49.75 | -3.43 | 0.0101 | 0.0028 |
| **LZW (Teórico - Binário)** | 15.25 | 68.30 | 0.0101 | 0.0028 |

## Gráficos Comparativos

### Comparativo de Tamanho Final
![Comparativo de Tamanho](virus_phage-lambda_sequence_comparativo_tamanho.png)

### Comparativo de Tempos de Execução
![Comparativo de Tempo](virus_phage-lambda_sequence_comparativo_tempo.png)
