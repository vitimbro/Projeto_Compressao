# src/main.py

import os
import time
# Importa as funções do módulo huffman
from huffman import compress as huffman_compress
from huffman import decompress as huffman_decompress

def parse_fasta(filepath: str) -> str:
    """
    Lê um arquivo no formato FASTA e retorna a sequência de DNA
    como uma string única, sem cabeçalhos ou quebras de linha.
    """
    sequence_parts = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence_parts.append(line.strip())
    return "".join(sequence_parts)

def main():
    """
    Função principal que orquestra o processo de análise e compressão.
    """
    print("--- INÍCIO DO PROCESSO DE ANÁLISE DE COMPRESSÃO ---")

    # --- CONFIGURAÇÃO DOS ARQUIVOS ---
    # Altere esta variável para testar outros genomas
    arquivo_base = "humano_chromosome-22_sequence"
    
    caminho_entrada = f'data/{arquivo_base}.fasta'
    caminho_comprimido_huffman = f'data/{arquivo_base}_huffman.huff'
    caminho_descomprimido_huffman = f'data/{arquivo_base}_huffman_decompressed.fasta'

    # --- 1. ANÁLISE DO ARQUIVO DE ENTRADA ---
    print("\n[ETAPA 1: Análise do Arquivo Original]")
    if not os.path.exists(caminho_entrada):
        print(f"ERRO: Arquivo de entrada não encontrado em '{caminho_entrada}'")
        return

    tamanho_original = os.path.getsize(caminho_entrada)
    print(f"Arquivo a ser processado: {caminho_entrada}")
    print(f"Tamanho Original: {tamanho_original / 1024:.2f} KB")
    
    texto_original = parse_fasta(caminho_entrada)
    if not texto_original:
        print("Arquivo FASTA vazio ou inválido.")
        return

    print(f"Número de Bases (Caracteres): {len(texto_original):,}")

    # --- 2. PROCESSO DE COMPRESSÃO HUFFMAN ---
    print("\n[ETAPA 2: Compressão com Huffman]")
    start_time = time.perf_counter()
    huffman_compress(texto_original, caminho_comprimido_huffman)
    end_time = time.perf_counter()
    
    tamanho_comprimido_huffman = os.path.getsize(caminho_comprimido_huffman)
    taxa_huffman = 100 * (1 - (tamanho_comprimido_huffman / tamanho_original))
    
    print(f"Arquivo comprimido salvo em: {caminho_comprimido_huffman}")
    print(f"Tamanho Comprimido (Huffman): {tamanho_comprimido_huffman / 1024:.2f} KB")
    print(f"Taxa de Compressão (Huffman): {taxa_huffman:.2f}%")
    print(f"Tempo de Compressão (Huffman): {end_time - start_time:.4f} segundos")

    # --- 3. PROCESSO DE DESCOMPRESSÃO E VERIFICAÇÃO HUFFMAN ---
    print("\n[ETAPA 3: Descompressão e Verificação com Huffman]")
    start_time = time.perf_counter()
    huffman_decompress(caminho_comprimido_huffman, caminho_descomprimido_huffman)
    end_time = time.perf_counter()
    
    print(f"Arquivo descomprimido salvo em: {caminho_descomprimido_huffman}")
    print(f"Tempo de Descompressão (Huffman): {end_time - start_time:.4f} segundos")

    # Verificação da integridade
    texto_descomprimido = parse_fasta(caminho_descomprimido_huffman)
    if texto_original == texto_descomprimido:
        print("VERIFICAÇÃO BEM-SUCEDIDA: O arquivo original e o descomprimido são idênticos.")
    else:
        print("ERRO NA VERIFICAÇÃO: Os arquivos são diferentes.")
    
    print("\n--- FIM DO PROCESSO ---")


if __name__ == "__main__":
    main()