# src/main.py

import os
import time
import json 
import math

# Importa as funções de ambos os módulos, usando 'as' para evitar conflito de nomes
from huffman import compress as huffman_compress, decompress as huffman_decompress
from lzw import compress as lzw_compress, decompress as lzw_decompress

def parse_fasta(filepath: str) -> str:
    """
    Lê um arquivo no formato FASTA e retorna a sequência como uma string única.
    """
    sequence_parts = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence_parts.append(line.strip())
    return "".join(sequence_parts)

def main():
    """
    Função principal que orquestra todo o processo de análise e compressão.
    """
    print("--- INÍCIO DO PROCESSO DE ANÁLISE COMPARATIVA DE COMPRESSÃO ---")

    # --- CONFIGURAÇÃO ---
    arquivo_base = "virus_phage-lambda_sequence" # Altere para testar outros genomas
    
    caminho_entrada = f'data/{arquivo_base}.fasta'
    # Huffman paths
    caminho_comprimido_huffman = f'data/{arquivo_base}_huffman.huff'
    caminho_descomprimido_huffman = f'data/{arquivo_base}_huffman_decompressed.fasta'
    # LZW path (para o arquivo JSON real)
    caminho_comprimido_lzw = f'data/{arquivo_base}_lzw.lzw'

    resultados = {}

    # --- 1. ANÁLISE DO ARQUIVO ORIGINAL ---
    print("\n[ETAPA 1: Análise do Arquivo Original]")
    if not os.path.exists(caminho_entrada):
        print(f"ERRO: Arquivo de entrada não encontrado em '{caminho_entrada}'")
        return

    tamanho_original = os.path.getsize(caminho_entrada)
    print(f"Arquivo a ser processado: {caminho_entrada}")
    print(f"Tamanho Original: {tamanho_original / 1024:.2f} KB")
    
    texto_original = parse_fasta(caminho_entrada)
    print(f"Número de Bases (Caracteres): {len(texto_original):,}")

    # --- 2. PROCESSO DE COMPRESSÃO HUFFMAN ---
    # (Esta seção permanece inalterada)
    print("\n[ETAPA 2: Processamento com Huffman]")
    start_time = time.perf_counter()
    huffman_compress(texto_original, caminho_comprimido_huffman)
    end_time = time.perf_counter()
    tempo_compress_huffman = end_time - start_time
    
    tamanho_comprimido_huffman = os.path.getsize(caminho_comprimido_huffman)
    
    start_time = time.perf_counter()
    huffman_decompress(caminho_comprimido_huffman, caminho_descomprimido_huffman)
    end_time = time.perf_counter()
    tempo_decompress_huffman = end_time - start_time
    
    texto_descomprimido_huffman = parse_fasta(caminho_descomprimido_huffman)
    verificacao_huffman = "IDÊNTICOS" if texto_original == texto_descomprimido_huffman else "DIFERENTES"

    resultados['Huffman'] = {
        'Tamanho Comprimido (KB)': tamanho_comprimido_huffman / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_comprimido_huffman / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_huffman,
        'Tempo de Descompressão (s)': tempo_decompress_huffman,
        'Verificação de Integridade': verificacao_huffman
    }
    os.remove(caminho_descomprimido_huffman)

    # --- 3. PROCESSO DE COMPRESSÃO LZW ---
    print("\n[ETAPA 3: Processamento com LZW]")
    start_time = time.perf_counter()
    codigos_lzw = lzw_compress(texto_original)
    end_time = time.perf_counter()
    tempo_compress_lzw = end_time - start_time

    # --- INÍCIO DA MODIFICAÇÃO ---

    # Salva e mede o tamanho do arquivo REAL (JSON)
    with open(caminho_comprimido_lzw, 'w') as f:
        json.dump(codigos_lzw, f)
    tamanho_real_lzw_bytes = os.path.getsize(caminho_comprimido_lzw)

    # Calcula o tamanho TEÓRICO (binário)
    tamanho_teorico_lzw_bytes = 0
    if codigos_lzw:
        maior_codigo = max(codigos_lzw)
        bits_por_codigo = maior_codigo.bit_length()
        total_bits = len(codigos_lzw) * bits_por_codigo
        tamanho_teorico_lzw_bytes = math.ceil(total_bits / 8)

    # Descompressão e verificação (continua igual)
    start_time = time.perf_counter()
    texto_descomprimido_lzw = lzw_decompress(codigos_lzw)
    end_time = time.perf_counter()
    tempo_decompress_lzw = end_time - start_time
    verificacao_lzw = "IDÊNTICOS" if texto_original == texto_descomprimido_lzw else "DIFERENTES"

    # Adiciona os resultados REAIS do LZW
    resultados['LZW (Real - JSON)'] = {
        'Tamanho Comprimido (KB)': tamanho_real_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_real_lzw_bytes / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_lzw,
        'Tempo de Descompressão (s)': tempo_decompress_lzw,
        'Verificação de Integridade': verificacao_lzw
    }

    # Adiciona os resultados TEÓRICOS do LZW
    resultados['LZW (Teórico - Binário)'] = {
        'Tamanho Comprimido (KB)': tamanho_teorico_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_teorico_lzw_bytes / tamanho_original))
    }
    # --- FIM DA MODIFICAÇÃO ---

    # --- 4. EXIBIÇÃO DOS RESULTADOS COMPARATIVOS ---
    # (Esta seção permanece inalterada e irá imprimir os 3 resultados)
    print("\n\n" + "="*50)
    print("--- RESULTADO FINAL COMPARATIVO ---")
    print("="*50)
    print(f"Arquivo Analisado: {arquivo_base}.fasta")
    print(f"Tamanho Original: {tamanho_original / 1024:.2f} KB | Bases: {len(texto_original):,}")
    print("-"*50)

    for algoritmo, res in resultados.items():
        print(f"Algoritmo: {algoritmo}")
        for metrica, valor in res.items():
            if isinstance(valor, float):
                print(f"  -> {metrica}: {valor:.2f}")
            else:
                print(f"  -> {metrica}: {valor}")
        print("-"*25)
        
    print("--- FIM DO PROCESSO ---")

if __name__ == "__main__":
    main()