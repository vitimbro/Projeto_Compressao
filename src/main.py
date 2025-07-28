import time
import os  # Importa o módulo 'os' para interagir com o sistema

def parse_fasta(filepath: str) -> str:
    """
    Lê um arquivo no formato FASTA e retorna a sequência de DNA
    como uma string única, sem cabeçalhos ou quebras de linha.
    """
    sequence_parts = []
    # O 'try/except' foi movido para o bloco principal para evitar checagens duplicadas
    with open(filepath, 'r') as f:
        for line in f:
            # Ignora as linhas de cabeçalho que começam com '>'
            if not line.startswith('>'):
                # Remove espaços em branco e quebras de linha
                sequence_parts.append(line.strip())
    return "".join(sequence_parts)

# --- Exemplo de como usar ---
if __name__ == "__main__":
    print("Iniciando leitor de genoma...")

    # Caminho para o seu arquivo de dados (lembre-se de ajustar para testar outros arquivos)
    caminho_do_arquivo = 'data/humano_chromosome-22_sequence.fasta'
    
    print("-" * 40)

    # Verifica se o arquivo realmente existe no caminho especificado
    if os.path.exists(caminho_do_arquivo):
        
        # --- INÍCIO DAS NOVAS LINHAS ---

        # 1. Imprime o nome do arquivo que está sendo lido
        print(f"Analisando o arquivo: {caminho_do_arquivo}")

        # 2. Pega o tamanho do arquivo em bytes e converte para KB
        file_size_bytes = os.path.getsize(caminho_do_arquivo)
        file_size_kb = file_size_bytes / 1024
        print(f"Tamanho do arquivo: {file_size_kb:.2f} KB")

        # --- FIM DAS NOVAS LINHAS ---

        # Medindo o tempo de leitura
        start_time = time.perf_counter()
        
        sequencia_dna = parse_fasta(caminho_do_arquivo)
        
        end_time = time.perf_counter()
        
        print("\n--- Resultados da Leitura ---") # Adicionado para clareza
        print(f"Sequência lida com sucesso!")
        print(f"Número de bases: {len(sequencia_dna):,}")
        print(f"Tempo de leitura: {end_time - start_time:.4f} segundos")
        print(f"Primeiras 50 bases: {sequencia_dna[:50]}...")

    else:
        # Mensagem de erro caso o arquivo não seja encontrado
        print(f"ERRO: Arquivo não encontrado em '{caminho_do_arquivo}'")
    
    print("-" * 40)