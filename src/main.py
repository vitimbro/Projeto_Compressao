
import os
import time
import json 
import math
import matplotlib.pyplot as plt

# Importa as funções de ambos os módulos, usando 'as' para evitar conflito de nomes
import huffman 
import lzw     

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


def gerar_graficos_comparativos(resultados: dict, arquivo_base: str):
    """
    Gera e salva gráficos comparativos com base no dicionário de resultados.
    """
    print("\n[ETAPA 5: Gerando Gráficos Comparativos]")
    
    algoritmos = list(resultados.keys())
    
    # --- Gráfico 1: Tamanho Comprimido ---
    tamanhos = [res['Tamanho Comprimido (KB)'] for res in resultados.values()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algoritmos, tamanhos, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    plt.title(f'Comparativo de Tamanho Comprimido\nArquivo: {arquivo_base}.fasta')
    plt.ylabel('Tamanho Comprimido (KB)')
    plt.xticks(rotation=8) # Rotaciona os nomes para não sobrepor
    
    # Adiciona os valores no topo das barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f} KB', va='bottom', ha='center')

    # Salva a figura em um arquivo PNG
    caminho_grafico_tamanho = f'{arquivo_base}_comparativo_tamanho.png'
    plt.savefig(caminho_grafico_tamanho)
    print(f"Gráfico de tamanho salvo em: '{caminho_grafico_tamanho}'")
    plt.close() # Fecha a figura para liberar memória

    # --- Gráfico 2: Tempos de Execução ---
    tempos_compressao = [res['Tempo de Compressão (s)'] for res in resultados.values()]
    tempos_descompressao = [res['Tempo de Descompressão (s)'] for res in resultados.values()]

    x = range(len(algoritmos)) # Posições no eixo X
    width = 0.35 # Largura das barras

    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar([i - width/2 for i in x], tempos_compressao, width, label='Compressão', color='#d62728')
    rects2 = ax.bar([i + width/2 for i in x], tempos_descompressao, width, label='Descompressão', color='#9467bd')

    ax.set_ylabel('Tempo (segundos)')
    ax.set_title(f'Comparativo de Tempos de Execução\nArquivo: {arquivo_base}.fasta')
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos, rotation=8)
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt='%.2fs')
    ax.bar_label(rects2, padding=3, fmt='%.2fs')

    fig.tight_layout()
    caminho_grafico_tempo = f'{arquivo_base}_comparativo_tempo.png'
    plt.savefig(caminho_grafico_tempo)
    print(f"Gráfico de tempo salvo em: '{caminho_grafico_tempo}'")
    plt.close()


def gerar_relatorio_markdown(resultados: dict, arquivo_base: str, tamanho_original_kb: float, num_bases: int):
    """
    Gera um arquivo de relatório em formato Markdown com a tabela de resultados e os gráficos.
    """
    print("\n[ETAPA 6: Gerando Relatório em Markdown]")
    
    # Define os nomes dos arquivos de imagem que foram gerados
    path_grafico_tamanho = f'{arquivo_base}_comparativo_tamanho.png'
    path_grafico_tempo = f'{arquivo_base}_comparativo_tempo.png'
    path_relatorio = f'RELATORIO_{arquivo_base}.md'

    with open(path_relatorio, 'w', encoding='utf-8') as f:
        # Título e informações do arquivo original
        f.write(f"# Relatório de Análise Comparativa de Compressão\n\n")
        f.write(f"## Arquivo Analisado\n")
        f.write(f"- **Nome:** `{arquivo_base}.fasta`\n")
        f.write(f"- **Tamanho Original:** {tamanho_original_kb:.2f} KB\n")
        f.write(f"- **Total de Bases:** {num_bases:,}\n\n")
        
        # Tabela de Resultados
        f.write("## Tabela de Resultados\n\n")
        # Cabeçalho da tabela
        f.write("| Algoritmo | Tamanho Comprimido (KB) | Taxa de Compressão (%) | Tempo Compressão (s) | Tempo Descompressão (s) |\n")
        f.write("|---|---|---|---|---|\n")
        
        # Linhas da tabela
        for algoritmo, res in resultados.items():
            # Ignora as métricas extras para a tabela principal
            tamanho = res['Tamanho Comprimido (KB)']
            taxa = res['Taxa de Compressão (%)']
            t_comp = res['Tempo de Compressão (s)']
            t_decomp = res['Tempo de Descompressão (s)']
            f.write(f"| **{algoritmo}** | {tamanho:.2f} | {taxa:.2f} | {t_comp:.4f} | {t_decomp:.4f} |\n")
        
        # Gráficos
        f.write("\n## Gráficos Comparativos\n\n")
        f.write("### Comparativo de Tamanho Final\n")
        f.write(f"![Comparativo de Tamanho]({path_grafico_tamanho})\n\n")
        
        f.write("### Comparativo de Tempos de Execução\n")
        f.write(f"![Comparativo de Tempo]({path_grafico_tempo})\n")

    print(f"Relatório salvo em: '{path_relatorio}'")



def main():
    """
    Função principal que orquestra todo o processo de análise e compressão.
    """
    print("--- INÍCIO DO PROCESSO DE ANÁLISE COMPARATIVA DE COMPRESSÃO ---")

    # --- CONFIGURAÇÃO ---
    arquivo_base = "plant_thaliana_sequence" # Altere para testar outros genomas
    
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
    huffman.compress(texto_original, caminho_comprimido_huffman)
    end_time = time.perf_counter()
    tempo_compress_huffman = end_time - start_time
    
    tamanho_comprimido_huffman = os.path.getsize(caminho_comprimido_huffman)
    
    start_time = time.perf_counter()
    huffman.decompress(caminho_comprimido_huffman, caminho_descomprimido_huffman)
    end_time = time.perf_counter()
    tempo_decompress_huffman = end_time - start_time
    
    texto_descomprimido_huffman = parse_fasta(caminho_descomprimido_huffman)
    verificacao_huffman = "IDÊNTICOS" if texto_original == texto_descomprimido_huffman else "DIFERENTES"

    # Para calcular as métricas, precisamos dos códigos e frequências
    frequencias_huff = huffman.calcular_frequencia(texto_original)
    fila_huff = huffman.criar_fila_de_prioridade(frequencias_huff)
    arvore_huff = huffman.construir_arvore_huffman(fila_huff)
    codigos_huffman = huffman.gerar_codigos_huffman(arvore_huff)
    entropia, comp_medio = huffman.calcular_metricas_huffman(texto_original, frequencias_huff, codigos_huffman)

    resultados['Huffman'] = {
        'Tamanho Comprimido (KB)': tamanho_comprimido_huffman / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_comprimido_huffman / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_huffman,
        'Tempo de Descompressão (s)': tempo_decompress_huffman,
        'Verificação de Integridade': verificacao_huffman,
        'Entropia de Shannon (bits/símbolo)': entropia,
        'Comprimento Médio do Código (bits/símbolo)': comp_medio
    }
    os.remove(caminho_descomprimido_huffman)

    # --- 3. PROCESSO DE COMPRESSÃO LZW ---
    print("\n[ETAPA 3: Processamento com LZW]")
    start_time = time.perf_counter()
    codigos_lzw, tamanho_final_dicionario = lzw.compress(texto_original)
    end_time = time.perf_counter()
    tempo_compress_lzw = end_time - start_time

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
    texto_descomprimido_lzw = lzw.decompress(codigos_lzw)
    end_time = time.perf_counter()
    tempo_decompress_lzw = end_time - start_time
    verificacao_lzw = "IDÊNTICOS" if texto_original == texto_descomprimido_lzw else "DIFERENTES"

    taxa_reducao_simbolos = len(texto_original) / len(codigos_lzw) if codigos_lzw else 0

    # Adiciona os resultados REAIS do LZW
    resultados['LZW (Real - JSON)'] = {
        'Tamanho Comprimido (KB)': tamanho_real_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_real_lzw_bytes / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_lzw,
        'Tempo de Descompressão (s)': tempo_decompress_lzw,
        'Verificação de Integridade': verificacao_lzw,
        'Tamanho Final do Dicionário': tamanho_final_dicionario,
        'Taxa de Redução de Símbolos': taxa_reducao_simbolos
    }

    # Adiciona os resultados TEÓRICOS do LZW
    resultados['LZW (Teórico - Binário)'] = {
        'Tamanho Comprimido (KB)': tamanho_teorico_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_teorico_lzw_bytes / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_lzw,     
        'Tempo de Descompressão (s)': tempo_decompress_lzw,  
        'Verificação de Integridade': verificacao_lzw,
        'Tamanho Final do Dicionário': tamanho_final_dicionario,
        'Taxa de Redução de Símbolos': taxa_reducao_simbolos     
    }

    # --- 4. EXIBIÇÃO DOS RESULTADOS COMPARATIVOS ---
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


    # --- 5. CHAMADA PARA GERAR GRÁFICOS ---
    gerar_graficos_comparativos(resultados, arquivo_base)

    # --- 6. CHAMADA PARA GERAR RELATÓRIO MD ---
    tamanho_original_kb = tamanho_original / 1024
    num_bases = len(texto_original)
    gerar_relatorio_markdown(resultados, arquivo_base, tamanho_original_kb, num_bases)
        
    print("--- FIM DO PROCESSO ---")

if __name__ == "__main__":
    main()