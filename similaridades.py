import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import PyPDF2
import nltk
import re
from collections import Counter

# Baixar recursos do nltk
nltk.download('punkt')
nltk.download('punkt_tab')


# Função para abrir e ler o conteúdo de arquivos .pdf
def ler_pdf(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        texto = []
        for pagina in range(len(reader.pages)):
            pagina_texto = reader.pages[pagina].extract_text()
            texto.append(pagina_texto)
    return '\n'.join(texto)


# Função para calcular a similaridade das palavras inseridas no texto
def calcular_similaridade(texto, palavras_busca):
    # Tokenização do texto
    palavras_texto = nltk.word_tokenize(texto.lower())  # Tokeniza e coloca tudo em minúsculo
    total_palavras = len(palavras_texto)

    # Contar a ocorrência de cada palavra no texto
    contagem_palavras = Counter(palavras_texto)

    resultados = {}

    for palavra in palavras_busca:
        palavra = palavra.lower()  # Convertendo a palavra de busca para minúsculo

        # Usando expressão regular para buscar palavras que contenham a palavra digitada
        # re.IGNORECASE torna a busca insensível ao caso (maiusculas/minusculas)
        palavras_encontradas = [p for p in palavras_texto if
                                re.search(rf'\b{re.escape(palavra)}\w*\b', p, re.IGNORECASE)]

        # Calculando a porcentagem de similaridade
        ocorrencias = len(palavras_encontradas)
        porcentagem = (ocorrencias / total_palavras) * 100 if total_palavras > 0 else 0
        resultados[palavra] = {
            'porcentagem': porcentagem,
            'encontradas': palavras_encontradas
        }

    return resultados, total_palavras


# Função principal
def main():
    # Janela principal do Tkinter
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Seleção do arquivo .pdf
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("Arquivos .pdf", "*.pdf")]
    )

    if not caminho_arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado!")
        return

    # Ler o conteúdo do arquivo selecionado
    if caminho_arquivo.endswith('.pdf'):
        texto = ler_pdf(caminho_arquivo)
    else:
        messagebox.showerror("Erro", "Formato de arquivo não suportado!")
        return

    # Solicitar ao usuário as palavras a serem buscadas
    palavras_busca = simpledialog.askstring(
        "Palavras para buscar",
        "Insira as palavras para busca (separadas por vírgulas):"
    )

    if not palavras_busca:
        messagebox.showerror("Erro", "Nenhuma palavra inserida para busca!")
        return

    palavras_busca = [p.strip() for p in palavras_busca.split(',')]

    # Calcular a similaridade das palavras no texto
    resultados, total_palavras = calcular_similaridade(texto, palavras_busca)

    if not resultados:
        messagebox.showinfo("Resultado", "Nenhuma palavra foi encontrada no arquivo.")
        return

    # Exibir os resultados
    resultado_str = f"Total de palavras no arquivo: {total_palavras}\n\n"
    resultado_str += "Palavra - Similaridade (%) - Palavras Encontradas\n"

    for palavra, info in resultados.items():
        palavra_str = f"{palavra} - {info['porcentagem']:.2f}%"
        if info['encontradas']:
            palavra_str += f" - {', '.join(set(info['encontradas']))}"
        else:
            palavra_str += " - Nenhuma palavra encontrada"

        resultado_str += palavra_str + "\n"

    messagebox.showinfo("Resultados de Similaridade", resultado_str)


if __name__ == "__main__":
    main()
