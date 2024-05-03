import csv
import datetime
from customtkinter import *
from PIL import Image
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import *


def select_file():
    nome_arquivo = filedialog.askopenfilename()
    entry.insert(0, nome_arquivo)


def click_handler():
    retornar_valores_pdf(entry.get())
    escrever_valores_app()


def escrever_valores_app():
    with open('csv_file_new.csv') as csvfile:
        for linha in csvfile.readlines():
            textbox.insert("0.0", linha)


def retornar_valores_pdf(path_arquivo: str):
    paginas = extract_pages(path_arquivo)
    lista_data, lista_descricao, lista_valor = extrair_paginas(paginas)

    with open('csv_file.csv', 'w') as f:
        for idx, item in enumerate(lista_data):
            if item:
                texto = f"{lista_data[idx]}\t{lista_descricao[idx]}\t{lista_valor[idx]}\r"

                # Salva se não for a linha de histórico do pagto da última fatura
                if "Pagamento De Fatura" not in texto:
                    f.write(texto)

    with open('csv_file.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        spamreader = sorted(spamreader, key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)

        writer = csv.writer(open("csv_file_new.csv", 'w', newline=''), delimiter='\t', quoting=csv.QUOTE_NONE, doublequote=False, escapechar="\\")
        for row in spamreader:
            writer.writerow(row)


def extrair_paginas(paginas):
    lista_datas, lista_descricoes, lista_valores = [], [], []

    # Percorre cada pagina
    for idx, page in enumerate(paginas):
        lista_datas_aux, lista_descricoes_aux, lista_valores_aux = extrai_campos_pagina(page)

        lista_datas += lista_datas_aux
        lista_descricoes += lista_descricoes_aux
        lista_valores += lista_valores_aux

    return lista_datas, lista_descricoes, lista_valores


def extrai_campos_pagina(pagina):
    # Inicia as listas vazias
    lista_datas, lista_descricoes, lista_valores = [], [], []

    # Percorre campos de cada página
    for item in pagina:
        if isinstance(item, pdfminer.layout.LTTextContainer):
            if "Data\n" in item.get_text():
                # Obtem Indice para considerar o texto somente após a palavra
                index = item.get_text().find("Data") + len("Data\n")

                lista_datas = criar_lista_data_produto(item.get_text()[index:], lista_datas)
            elif "Descrição\n" in item.get_text():
                # Obtem Indice para considerar o texto somente após a palavra
                index = item.get_text().find("Descrição") + len("Descrição\n")

                lista_descricoes = criar_lista_descricao_produto(item.get_text()[index:], lista_descricoes)
            elif "Valor (R$)" in item.get_text():
                # Obtem Indice para considerar o texto somente após a palavra
                index = item.get_text().find("Valor (R$)") + len("Valor (R$)\n")

                lista_valores = criar_lista_valor_produto(item.get_text()[index:], lista_valores)
    return lista_datas, lista_descricoes, lista_valores


def criar_lista_data_produto(datas, lista_data_atual):
    #print(datas)
    datas_novo = datas.split("\n")
    for item in datas_novo:
        #print(item)
        if item != "Data" and item != "":
            lista_data_atual.append(item)
    return lista_data_atual


def criar_lista_descricao_produto(descricoes, lista_descricao_atual):
    # print(descricoes)
    descricoes_novo = descricoes.split("\n")
    for item in descricoes_novo:
        # print(item)
        if item != "Descrição" and item != "":
            lista_descricao_atual.append(item)
    return lista_descricao_atual


def criar_lista_valor_produto(valores, lista_valor_atual):
    #print(valores)
    valores_novo = valores.split("\n")
    for item in valores_novo:
        #print(item)
        if item != "Valor (R$)" and item != "":
            lista_valor_atual.append(item)
    return lista_valor_atual


app = CTk()
app.geometry("500x400")
app.title("Santander PDF Extractor")

set_appearance_mode("dark")


# Label
label = CTkLabel(master=app, text="Obter gastos Santander - PDF", font=("Arial", 20), text_color="#FFCC70")
label.pack(anchor="n", expand=True, pady=10)

# Entry
entry = CTkEntry(master=app, placeholder_text="Path do arquivo...", text_color="#FFCC70")
entry.pack(anchor="s", expand=True, pady=10)

# Button Select File
img_file = Image.open("static/file.png")
btn_file = CTkButton(master=app, text="Procurar arquivo", corner_radius=32, fg_color="#4158D0", 
                hover_color="#C850C0", border_color="#FFCC70",
                image=CTkImage(dark_image=img_file, light_image=img_file),
                command=select_file)
btn_file.pack(anchor="n", expand=True)

# Button
img_process = Image.open("static/processing.png")
btn = CTkButton(master=app, text="Extrair valores", corner_radius=32, fg_color="#4158D0", 
                hover_color="#C850C0", border_color="#FFCC70",
                image=CTkImage(dark_image=img_process, light_image=img_process),
                command=click_handler)
btn.pack(anchor="n", expand=True)

# TextBox
textbox = CTkTextbox(master=app, scrollbar_button_color="#FFCC70", corner_radius=16,
                     border_color="#FFCC70", border_width=2, width=400)
textbox.pack(anchor="s", expand=True, pady=10)


app.mainloop()
