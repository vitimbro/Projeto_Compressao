
import os
import time
import json 
import math
import matplotlib.pyplot as plt
import sys

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

    # Garante que a pasta 'graficos' exista
    output_dir = 'graficos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
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
    caminho_grafico_tamanho = os.path.join(output_dir, f'{arquivo_base}_comparativo_tamanho.png')
    plt.savefig(caminho_grafico_tamanho)
    print(f"Gráfico de tamanho salvo em: '{caminho_grafico_tamanho}'")
    plt.close() # Fecha a figura para liberar memória

    # --- Gráfico 2: Tempos de Execução ---

    # Filtra os dados para remover a entrada redundante do LZW Real
    algoritmos_tempo = [a for a in algoritmos if a != 'LZW (Real - JSON)']
    # Limpa os nomes para legendas mais bonitas no gráfico
    algoritmos_tempo_labels = [a.replace(' (Teórico - Binário)', '') for a in algoritmos_tempo]

    tempos_compressao = [resultados[a]['Tempo de Compressão (s)'] for a in algoritmos_tempo]
    tempos_descompressao = [resultados[a]['Tempo de Descompressão (s)'] for a in algoritmos_tempo]

    x = range(len(algoritmos_tempo))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 7))
    rects1 = ax.bar([i - width/2 for i in x], tempos_compressao, width, label='Compressão', color='#d62728')
    rects2 = ax.bar([i + width/2 for i in x], tempos_descompressao, width, label='Descompressão', color='#9467bd')

    ax.set_ylabel('Tempo (segundos)')
    ax.set_title(f'Comparativo de Tempos de Execução\nArquivo: {arquivo_base}.fasta')
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos_tempo_labels) # Usa os nomes limpos
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt='%.2fs')
    ax.bar_label(rects2, padding=3, fmt='%.2fs')

    fig.tight_layout()
    caminho_grafico_tempo = os.path.join(output_dir, f'{arquivo_base}_comparativo_tempo.png')
    plt.savefig(caminho_grafico_tempo)
    print(f"Gráfico de tempo salvo em: '{caminho_grafico_tempo}'")
    plt.close()


def gerar_relatorio_markdown(resultados: dict, arquivo_base: str, tamanho_original_kb: float, num_bases: int):
    """
    Gera um arquivo de relatório em formato Markdown com a tabela de resultados e os gráficos.
    """
    print("\n[ETAPA 6: Gerando Relatório em Markdown]")

    # Garante que a pasta 'relatorios' exista
    output_dir_report = 'relatorios'
    if not os.path.exists(output_dir_report):
        os.makedirs(output_dir_report)
    
    # Define os nomes dos arquivos de imagem que foram gerados
    path_grafico_tamanho = f'../graficos/{arquivo_base}_comparativo_tamanho.png'
    path_grafico_tempo = f'../graficos/{arquivo_base}_comparativo_tempo.png'
    path_relatorio = os.path.join(output_dir_report, f'RELATORIO_{arquivo_base}.md')

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
            tamanho = res.get('Tamanho Comprimido (KB)', 0)
            taxa = res.get('Taxa de Compressão (%)', 0)
            # Usa .get() para fornecer um valor padrão caso a chave não exista
            t_comp = res.get('Tempo de Compressão (s)', '---')
            t_decomp = res.get('Tempo de Descompressão (s)', '---')

            # Formata os valores numéricos ou mantém o texto '---'
            t_comp_str = f"{t_comp:.4f}" if isinstance(t_comp, float) else t_comp
            t_decomp_str = f"{t_decomp:.4f}" if isinstance(t_decomp, float) else t_decomp
            
            f.write(f"| **{algoritmo}** | {tamanho:.2f} | {taxa:.2f} | {t_comp_str} | {t_decomp_str} |\n")
        

        f.write("\n## Métricas Avançadas e Análise Teórica\n\n")

        # --- Análise Huffman ---
        huffman_res = resultados.get('Huffman', {})
        if 'Entropia de Shannon (bits/símbolo)' in huffman_res:
            f.write("### Análise do Algoritmo Huffman\n\n")
            entropia = huffman_res['Entropia de Shannon (bits/símbolo)']
            comp_medio = huffman_res['Comprimento Médio do Código (bits/símbolo)']
            
            f.write(f"- **Entropia de Shannon:** `{entropia:.4f}` bits/símbolo\n")
            f.write("  - *Significado: Representa o **limite teórico** da compressão para este arquivo. É o número mínimo de bits, em média, necessários para representar cada caractere com base em suas frequências.*\n\n")
            
            f.write(f"- **Comprimento Médio do Código:** `{comp_medio:.4f}` bits/símbolo\n")
            f.write("  - *Significado: Representa o **desempenho real** da nossa implementação. Um valor próximo da entropia indica uma compressão Huffman de altíssima eficiência, mostrando que o algoritmo se aproximou do ótimo teórico.*\n\n")

        # --- Análise LZW ---
        lzw_res = resultados.get('LZW (Teórico - Binário)', {})
        if 'Tamanho Final do Dicionário' in lzw_res:
            f.write("### Análise do Algoritmo LZW\n\n")
            dict_size = lzw_res['Tamanho Final do Dicionário']
            reduction_rate = lzw_res['Taxa de Redução de Símbolos']

            f.write(f"- **Tamanho Final do Dicionário:** `{dict_size:,}` entradas\n")
            f.write("  - *Significado: Indica quantos padrões únicos e sequências repetitivas o algoritmo 'aprendeu'. Um número maior sugere que o arquivo possui uma estrutura com mais repetições que podem ser exploradas.*\n\n")

            f.write(f"- **Taxa de Redução de Símbolos:** `{reduction_rate:.2f}`\n")
            f.write("  - *Significado: Mostra, em média, quantos caracteres do texto original foram representados por **um único código LZW**. Um valor maior é um forte indicador de alta eficiência de compressão.*\n\n")

        # Nova seção para análise de espaço
        f.write("\n## Análise de Complexidade de Espaço (Uso de Memória)\n\n")
        f.write("A seguir, uma análise do uso de memória das principais estruturas de dados de cada algoritmo.\n\n")

        # Análise de Espaço Huffman
        huffman_res = resultados.get('Huffman', {})
        if 'Overhead de Espaço (Cabeçalho KB)' in huffman_res:
            f.write("### Huffman\n\n")
            overhead_huffman = huffman_res['Overhead de Espaço (Cabeçalho KB)']
            f.write(f"- **Overhead (Tamanho do Cabeçalho):** `{overhead_huffman:.2f}` KB\n")
            f.write("  - *Significado: Representa o custo de espaço fixo do Huffman. É o tamanho da tabela de frequências que precisa ser armazenada junto com os dados para permitir a descompressão. Este valor é geralmente muito pequeno e independe do tamanho do arquivo.*\n\n")

        # Análise de Espaço LZW
        lzw_res = resultados.get('LZW (Teórico - Binário)', {})
        if 'Tamanho Final do Dicionário' in lzw_res:
            f.write("### LZW\n\n")
            dict_size_entries = lzw_res['Tamanho Final do Dicionário']
            dict_size_kb = lzw_res['Uso de Memória (Dicionário KB)'] # Pega a nova métrica

            f.write(f"- **Estrutura Principal (Dicionário):** `{dict_size_entries:,}` entradas, ocupando uma memória estimada de **`{dict_size_kb:.2f}` KB**\n")
            f.write("  - *Significado: Representa o custo de espaço dinâmico do LZW. O dicionário cresce à medida que o algoritmo processa o arquivo, consumindo memória proporcional à quantidade e ao tamanho dos padrões encontrados.*\n\n")


        # Gráficos
        f.write("\n## Gráficos Comparativos\n\n")
        f.write("### Comparativo de Tamanho Final\n")
        f.write(f"![Comparativo de Tamanho]({path_grafico_tamanho})\n\n")
        
        f.write("### Comparativo de Tempos de Execução\n")
        f.write(f"![Comparativo de Tempo]({path_grafico_tempo})\n")

    print(f"Relatório salvo em: '{path_relatorio}'")


# --- Adicione esta nova função ao seu main.py ---
def estimar_tamanho_dicionario_lzw(dicionario: dict) -> float:
    """
    Estima o tamanho em memória de um dicionário LZW em KB.
    Soma o tamanho de todas as chaves (strings) e valores (ints).
    """
    tamanho_bytes = 0
    for chave, valor in dicionario.items():
        tamanho_bytes += sys.getsizeof(chave)
        tamanho_bytes += sys.getsizeof(valor)
    
    return tamanho_bytes / 1024




def main():
    """
    Função principal que orquestra todo o processo de análise e compressão.
    """
    print("--- INÍCIO DO PROCESSO DE ANÁLISE COMPARATIVA DE COMPRESSÃO ---")

    # --- SELEÇÃO DE ARQUIVO INTERATIVA ---
    
    print("\n[ETAPA 0: Seleção de Arquivo]")
    
    # 1. Encontra todos os arquivos .fasta na pasta data/
    data_path = 'data'
    try:
        fasta_files = [f for f in os.listdir(data_path) if f.endswith(('.fasta', '.fa', '.fna'))]
    except FileNotFoundError:
        print(f"ERRO: A pasta '{data_path}' não foi encontrada. Crie-a e adicione seus arquivos .fasta.")
        return

    if not fasta_files:
        print(f"ERRO: Nenhum arquivo .fasta encontrado na pasta '{data_path}'.")
        return

    # 2. Mostra os arquivos para o usuário
    print("Por favor, escolha o arquivo de genoma para analisar:")
    for i, filename in enumerate(fasta_files):
        print(f"  [{i + 1}] {filename}")

    # 3. Pede ao usuário para escolher um número
    escolha = -1
    while True:
        try:
            entrada = input(f"Digite o número do arquivo (1-{len(fasta_files)}): ")
            escolha = int(entrada) - 1
            if 0 <= escolha < len(fasta_files):
                break
            else:
                print("Escolha inválida. Por favor, digite um número da lista.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    # 4. Define o arquivo_base com base na escolha do usuário
    arquivo_fasta_selecionado = fasta_files[escolha]
    arquivo_base = os.path.splitext(arquivo_fasta_selecionado)[0]
    
    # --- FIM DA SELEÇÃO ---


    # --- CONFIGURAÇÃO ---
    
    caminho_entrada = os.path.join('data', arquivo_fasta_selecionado) # Usa o nome completo
    caminho_comprimido_huffman = os.path.join('data', f'{arquivo_base}_huffman.huff') # Usa o nome base
    caminho_descomprimido_huffman = os.path.join('data', f'{arquivo_base}_huffman_decompressed.fasta') # Usa o nome base
    caminho_comprimido_lzw = os.path.join('data', f'{arquivo_base}_lzw.lzw') # Usa o nome base

    resultados = {}

    # --- 1. ANÁLISE DO ARQUIVO ORIGINAL ---
    print("\n[ETAPA 1: Análise do Arquivo Original]")

    tamanho_original = os.path.getsize(caminho_entrada)
    print(f"Arquivo a ser processado: {caminho_entrada}")
    print(f"Tamanho Original: {tamanho_original / 1024:.2f} KB")
    
    texto_original = parse_fasta(caminho_entrada)
    print(f"Número de Bases (Caracteres): {len(texto_original):,}")

    # --- 2. PROCESSO DE COMPRESSÃO HUFFMAN ---
    # (Esta seção permanece inalterada)
    print("\n[ETAPA 2: Processamento com Huffman]")
    start_time = time.perf_counter()
    tamanho_header_huffman = huffman.compress(texto_original, caminho_comprimido_huffman)
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
        'Comprimento Médio do Código (bits/símbolo)': comp_medio,
        'Overhead de Espaço (Cabeçalho KB)': tamanho_header_huffman / 1024
    }
    os.remove(caminho_descomprimido_huffman)

    # --- 3. PROCESSO DE COMPRESSÃO LZW ---
    print("\n[ETAPA 3: Processamento com LZW]")
    start_time = time.perf_counter()
    codigos_lzw, tamanho_final_dicionario, dicionario_final_lzw = lzw.compress(texto_original)
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

    memoria_dicionario_lzw_kb = estimar_tamanho_dicionario_lzw(dicionario_final_lzw)


    # Adiciona os resultados TEÓRICOS do LZW
    resultados['LZW (Teórico - Binário)'] = {
        'Tamanho Comprimido (KB)': tamanho_teorico_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_teorico_lzw_bytes / tamanho_original)),
        'Tempo de Compressão (s)': tempo_compress_lzw,
        'Tempo de Descompressão (s)': tempo_decompress_lzw,
        'Verificação de Integridade': verificacao_lzw,
        'Tamanho Final do Dicionário': tamanho_final_dicionario,
        'Taxa de Redução de Símbolos': taxa_reducao_simbolos,
        'Uso de Memória (Dicionário KB)': memoria_dicionario_lzw_kb
    }
    
    # Adiciona os resultados REAIS do LZW (apenas com as métricas de tamanho)
    resultados['LZW (Real - JSON)'] = {
        'Tamanho Comprimido (KB)': tamanho_real_lzw_bytes / 1024,
        'Taxa de Compressão (%)': 100 * (1 - (tamanho_real_lzw_bytes / tamanho_original))
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


    # --- 7. SALVAR RESULTADOS EM ARQUIVO JSON ---
    # Garante que a pasta 'resultados' exista
    output_dir_results = 'resultados'
    if not os.path.exists(output_dir_results):
        os.makedirs(output_dir_results)

    # Salva o dicionário completo de resultados em um arquivo JSON
    path_resultado_json = os.path.join(output_dir_results, f'resultados_{arquivo_base}.json')
    with open(path_resultado_json, 'w', encoding='utf-8') as f:
        # Adiciona informações do arquivo original ao dicionário para uso posterior
        resultados['info_arquivo'] = {
            'nome_base': arquivo_base,
            'tamanho_original_kb': tamanho_original / 1024,
            'num_bases': len(texto_original)
        }
        json.dump(resultados, f, indent=4)
    
    print(f"\n[ETAPA 7: Resultados Salvos]")
    print(f"Dicionário de resultados salvo em: '{path_resultado_json}'")
    
        
    print("--- FIM DO PROCESSO ---")

if __name__ == "__main__":
    main()