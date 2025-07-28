# src/lzw.py

from typing import List, Dict

def compress(texto: str) -> List[int]:
    """
    Comprime um texto usando o algoritmo LZW.
    """
    if not texto:
        return []
        
    tamanho_dicionario = 256 # Inicia com o alfabeto ASCII básico
    dicionario: Dict[str, int] = {chr(i): i for i in range(tamanho_dicionario)}

    sequencia_atual = ""
    resultado_comprimido = []

    for caractere in texto:
        nova_sequencia = sequencia_atual + caractere
        if nova_sequencia in dicionario:
            sequencia_atual = nova_sequencia
        else:
            resultado_comprimido.append(dicionario[sequencia_atual])
            dicionario[nova_sequencia] = tamanho_dicionario
            tamanho_dicionario += 1
            sequencia_atual = caractere

    if sequencia_atual:
        resultado_comprimido.append(dicionario[sequencia_atual])
        
    return resultado_comprimido

def decompress(lista_codigos: List[int]) -> str:
    """
    Descomprime uma lista de códigos LZW para o texto original.
    """
    if not lista_codigos:
        return ""

    tamanho_dicionario = 256
    dicionario: Dict[int, str] = {i: chr(i) for i in range(tamanho_dicionario)}

    codigo_anterior = lista_codigos[0]
    sequencia_anterior = dicionario[codigo_anterior]
    partes_decodificadas = [sequencia_anterior]

    for codigo_atual in lista_codigos[1:]:
        sequencia_atual = ""
        if codigo_atual in dicionario:
            sequencia_atual = dicionario[codigo_atual]
        elif codigo_atual == tamanho_dicionario:
            sequencia_atual = sequencia_anterior + sequencia_anterior[0]
        else:
            raise ValueError(f"Código inválido: {codigo_atual}")

        partes_decodificadas.append(sequencia_atual)

        nova_entrada_dicionario = sequencia_anterior + sequencia_atual[0]
        dicionario[tamanho_dicionario] = nova_entrada_dicionario
        tamanho_dicionario += 1

        sequencia_anterior = sequencia_atual
        
    return "".join(partes_decodificadas)