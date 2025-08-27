import customtkinter as ctk
from PIL import Image
import os

app = ctk.CTk()
app.geometry("350x450")

# Verificar quais ícones existem
pasta_icones = os.path.join(os.path.dirname(__file__), "assets", "fonts", "feather")
icones_disponiveis = []
print(pasta_icones)

# if os.path.exists(pasta_icones):
#     print("✅ Pasta de ícones encontrada!")
    
#     # Procurar arquivos SVG
#     for arquivo in os.listdir(pasta_icones):
#         if arquivo.endswith('.svg'):
#             icones_disponiveis.append(arquivo)

# Ícones que queremos usar
icones_desejados = [
    "user.svg", "save.svg", "edit.svg", "trash-2.svg",
    "search.svg", "settings.svg"
]

# Carregar ícone
caminho = os.path.join(pasta_icones, "user.svg")
img = Image.open(caminho)
icone_img = ctk.CTkImage(light_image=img, dark_image=img, size=(25, 25))

# Nome do botão (remover .svg)
# nome = arquivo.replace('.svg', '').capitalize()

btn = ctk.CTkButton(
    app,
    image=icone_img,
    compound="left",
    height=40
)
btn.pack(pady=8)

app.mainloop()
