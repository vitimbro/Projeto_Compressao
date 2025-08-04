# src/gerar_grafico_geral.py

import os
import json
import matplotlib.pyplot as plt

# --- INÍCIO DA MODIFICAÇÃO ---

def formatar_bases(num_bases: int) -> str:
    """Formata o número de bases para uma leitura mais fácil (ex: 4.6M, 100.3M)."""
    if num_bases < 1_000_000:
        return f"{num_bases / 1_000:.1f}K bases"
    else:
        return f"{num_bases / 1_000_000:.1f}M bases"

# --- FIM DA MODIFICAÇÃO ---


def gerar_grafico_final():
    """
    Lê todos os arquivos de resultado JSON, agrega os dados e gera
    um gráfico comparativo da taxa de compressão entre os genomas.
    """
    resultados_dir = 'resultados'
    dados_agregados = []

    print(f"Lendo arquivos de resultado da pasta '{resultados_dir}'...")
    
    # 1. Carrega os dados de todos os arquivos JSON de resultado
    for filename in os.listdir(resultados_dir):
        if filename.startswith('resultados_') and filename.endswith('.json'):
            filepath = os.path.join(resultados_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                dados_agregados.append(dados)

    if not dados_agregados:
        print("Nenhum arquivo de resultado encontrado. Execute o main.py primeiro.")
        return

    # 2. Ordena os resultados pelo tamanho do arquivo original para um gráfico lógico
    dados_agregados.sort(key=lambda x: x['info_arquivo']['tamanho_original_kb'])

    # --- INÍCIO DA MODIFICAÇÃO ---

    # 3. Extrai os dados para o plot, criando rótulos mais informativos
    nomes_genomas_labels = []
    for d in dados_agregados:
        nome_limpo = d['info_arquivo']['nome_base'].replace('_sequence', '')
        num_bases = d['info_arquivo']['num_bases']
        # Cria um rótulo com duas linhas: nome e tamanho
        label_final = f"{nome_limpo}\n({formatar_bases(num_bases)})"
        nomes_genomas_labels.append(label_final)

    taxas_huffman = [d['Huffman']['Taxa de Compressão (%)'] for d in dados_agregados]
    taxas_lzw = [d['LZW (Teórico - Binário)']['Taxa de Compressão (%)'] for d in dados_agregados]

    # --- FIM DA MODIFICAÇÃO ---


    # 4. Cria o gráfico de barras agrupado
    x = range(len(nomes_genomas_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 8))
    rects1 = ax.bar([i - width/2 for i in x], taxas_huffman, width, label='Huffman', color='#1f77b4')
    rects2 = ax.bar([i + width/2 for i in x], taxas_lzw, width, label='LZW (Teórico)', color='#2ca02c')

    ax.set_ylabel('Taxa de Compressão (%)')
    ax.set_title('Taxa de Compressão (Huffman vs. LZW) por Tamanho do Genoma')
    ax.set_xticks(x)
    # Usa os novos rótulos com a informação de tamanho
    ax.set_xticklabels(nomes_genomas_labels, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Adiciona um limite superior ao eixo Y para dar espaço aos rótulos das barras
    ax.set_ylim(0, max(max(taxas_huffman), max(taxas_lzw)) * 1.15)

    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')

    fig.tight_layout()
    
    caminho_grafico_final = 'grafico_comparativo_geral.png'
    plt.savefig(caminho_grafico_final)
    print(f"\nGráfico comparativo final salvo em: '{caminho_grafico_final}'")
    plt.close()


if __name__ == '__main__':
    gerar_grafico_final()