# src/huffman.py

import heapq
from collections import Counter
import json
from typing import Tuple, Counter as CounterType
import math

class Node:
    """
    Representa um nó na árvore de Huffman.
    """
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other: 'Node') -> bool:
        return self.freq < other.freq


def calcular_frequencia(texto: str) -> CounterType:
    """
    Recebe um texto (string) e retorna um objeto Counter
    com a frequência de cada caractere.
    """
    return Counter(texto)


def criar_fila_de_prioridade(frequencias: CounterType) -> list:
    """
    Recebe um dicionário de frequências e cria uma fila de prioridade (min-heap)
    de nós.
    """
    fila = []
    for char, freq in frequencias.items():
        node = Node(char, freq)
        fila.append(node)
    
    heapq.heapify(fila)
    return fila


def construir_arvore_huffman(fila_prioridade: list) -> Node:
    """
    Recebe a fila de prioridade e constrói a árvore de Huffman.
    Retorna o nó raiz da árvore.
    """
    while len(fila_prioridade) > 1:
        no_esquerdo = heapq.heappop(fila_prioridade)
        no_direito = heapq.heappop(fila_prioridade)

        freq_soma = no_esquerdo.freq + no_direito.freq
        no_pai = Node(char=None, freq=freq_soma)
        no_pai.left = no_esquerdo
        no_pai.right = no_direito

        heapq.heappush(fila_prioridade, no_pai)

    return fila_prioridade[0]


def _percorrer_arvore_e_gerar_codigos(no_atual: Node, codigo_atual: str, codigos: dict):
    """
    Função auxiliar recursiva para percorrer a árvore e gerar os códigos.
    """
    if no_atual is None:
        return

    if no_atual.char is not None:
        codigos[no_atual.char] = codigo_atual or "0" # Garante código "0" se a árvore tiver um só nó
        return

    _percorrer_arvore_e_gerar_codigos(no_atual.left, codigo_atual + "0", codigos)
    _percorrer_arvore_e_gerar_codigos(no_atual.right, codigo_atual + "1", codigos)


def gerar_codigos_huffman(no_raiz: Node) -> dict:
    """
    Recebe o nó raiz da árvore de Huffman e retorna um dicionário
    mapeando cada caractere ao seu código binário.
    """
    codigos = {}
    _percorrer_arvore_e_gerar_codigos(no_raiz, "", codigos)
    return codigos


def _codificar_texto(texto: str, codigos: dict) -> str:
    """
    Função auxiliar para converter o texto em uma string de bits.
    Usa uma lista e o método .join() para eficiência.
    """
    # Cria uma lista com todos os códigos correspondentes a cada caractere
    lista_de_codigos = [codigos[char] for char in texto]
    
    # Junta todos os itens da lista em uma única string de forma eficiente
    return "".join(lista_de_codigos)


def _preencher_texto_codificado(texto_codificado: str) -> Tuple[str, int]:
    """
    Adiciona preenchimento ao final do texto codificado para que seu
    tamanho seja múltiplo de 8.
    """
    padding_amount = (8 - len(texto_codificado) % 8) % 8
    texto_preenchido = texto_codificado + ('0' * padding_amount)

    return texto_preenchido, padding_amount


def compress(texto: str, caminho_saida: str):
    """
    Função principal que comprime um texto e salva em um arquivo de saída.
    """
    if not texto:
        print("Aviso: Texto de entrada está vazio. Arquivo de saída não será criado.")
        return

    frequencias = calcular_frequencia(texto)
    # Caso especial: texto com apenas um tipo de caractere
    if len(frequencias) == 1:
        frequencias[next(iter(frequencias)) + '_dummy'] = 0

    fila_prioridade = criar_fila_de_prioridade(frequencias)
    no_raiz = construir_arvore_huffman(fila_prioridade)
    codigos_huffman = gerar_codigos_huffman(no_raiz)

    texto_codificado = _codificar_texto(texto, codigos_huffman)
    texto_preenchido, padding_amount = _preencher_texto_codificado(texto_codificado)

    with open(caminho_saida, 'wb') as f:
        f.write(bytes([padding_amount]))
        header = json.dumps(frequencias).encode('utf-8')
        f.write(len(header).to_bytes(2, 'big'))
        f.write(header)

        byte_array = bytearray(int(texto_preenchido[i:i+8], 2) for i in range(0, len(texto_preenchido), 8))
        f.write(bytes(byte_array))


def decompress(caminho_entrada: str, caminho_saida: str):
    """
    Descomprime um arquivo .huff e salva o texto original.
    """
    with open(caminho_entrada, 'rb') as f:
        # 1. Ler as informações do cabeçalho (rápido)
        padding_amount = int.from_bytes(f.read(1), 'big')
        header_size = int.from_bytes(f.read(2), 'big')
        header_json = f.read(header_size).decode('utf-8')
        frequencias = json.loads(header_json)
        
        # Remove o caractere dummy se existir
        frequencias = {k: v for k, v in frequencias.items() if not k.endswith('_dummy')}

        dados_comprimidos = f.read()

    # Caso especial: arquivo vazio após o cabeçalho
    if not dados_comprimidos:
        with open(caminho_saida, 'w') as f:
             if frequencias:
                char = next(iter(frequencias))
                f.write(char * frequencias[char])
        return

    # 2. Reconstruir a árvore de Huffman (rápido)
    fila_prioridade = criar_fila_de_prioridade(Counter(frequencias))
    no_raiz = construir_arvore_huffman(fila_prioridade)
    
    # --- Reconstrução da string de bits ---
    bits_lista = [f'{byte:08b}' for byte in dados_comprimidos]
    texto_codificado = "".join(bits_lista)
    
    # Remove os bits de preenchimento
    if padding_amount > 0:
        texto_codificado = texto_codificado[:-padding_amount]

    # --- Reconstrução do texto final ---
    chars_decodificados = []
    no_atual = no_raiz
    # Caso especial: se a árvore não tiver filhos (um só caractere)
    if not no_atual.left and not no_atual.right:
        # Se a árvore só tem um nó, o texto é apenas esse caractere repetido
        if no_atual.char:
             chars_decodificados.append(no_atual.char * frequencias[no_atual.char])
    else:
        for bit in texto_codificado:
            no_atual = no_atual.left if bit == '0' else no_atual.right

            if no_atual.char is not None:
                chars_decodificados.append(no_atual.char)
                no_atual = no_raiz
    
    texto_decodificado = "".join(chars_decodificados)

    # 4. Salvar o arquivo descomprimido
    with open(caminho_saida, 'w') as f:
        f.write(texto_decodificado)


def calcular_metricas_huffman(texto_original: str, frequencias: dict, codigos: dict) -> (float, float):
    """
    Calcula a Entropia de Shannon e o Comprimento Médio do Código Huffman.
    """
    total_caracteres = len(texto_original)
    entropia = 0.0
    comprimento_medio = 0.0

    for char, freq in frequencias.items():
        if freq > 0:
            probabilidade = freq / total_caracteres
            entropia -= probabilidade * math.log2(probabilidade)
            # Soma ponderada do comprimento de cada código
            comprimento_medio += probabilidade * len(codigos[char])
            
    return entropia, comprimento_medio