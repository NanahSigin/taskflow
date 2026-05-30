import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys
import os


# ==========================
# ABRIR APP PRINCIPAL
# ==========================
def abrir_app():
    janela.destroy()

    caminho_main = os.path.join(
        os.path.dirname(__file__),
        "main.py"
    )

    subprocess.Popen(
        [sys.executable, caminho_main]
    )


# ==========================
# JANELA
# ==========================
janela = tk.Tk()
janela.title("🐾 KittyFlow")
janela.geometry("1200x700")
janela.resizable(False, False)

BASE_DIR = os.path.dirname(__file__)

# ==========================
# BACKGROUND
# ==========================
caminho_bg = os.path.join(BASE_DIR, "cats_bg.png.jpg")

imagem_bg = Image.open(caminho_bg)
imagem_bg = imagem_bg.resize((1200, 700))

bg_photo = ImageTk.PhotoImage(imagem_bg)

label_bg = tk.Label(janela, image=bg_photo)
label_bg.place(x=0, y=0, relwidth=1, relheight=1)


# ==========================
# HEADER SUPERIOR
# ==========================
header = tk.Frame(
    janela,
    bg="#EAF7F6",
    height=90,
    highlightthickness=1,
    highlightbackground="#D9EAEA"
)
header.pack(fill="x", padx=12, pady=12)

tk.Label(
    header,
    text="🐾 KITTYFLOW",
    font=("Segoe UI", 30, "bold"),
    fg="#D65A8A",
    bg="#EAF7F6"
).pack(pady=(10, 0))

tk.Label(
    header,
    text="Kanban-style task management app ✨",
    font=("Segoe UI", 12),
    bg="#EAF7F6",
    fg="#555"
).pack()


# ==========================
# CARD CENTRAL
# ==========================
card = tk.Frame(
    janela,
    bg="#F7B9C9",
    padx=50,
    pady=40,
    highlightbackground="#D78DA1",
    highlightthickness=2
)

card.place(relx=0.5, rely=0.52, anchor="center")


# Emoji gato
tk.Label(
    card,
    text="🐱",
    bg="#F7B9C9",
    font=("Segoe UI Emoji", 50)
).pack(pady=(0, 10))


# Título
tk.Label(
    card,
    text="Bem-vindo ao KittyFlow",
    bg="#F7B9C9",
    fg="#4C0519",
    font=("Segoe UI", 24, "bold")
).pack()


# Subtexto
tk.Label(
    card,
    text="Seu gerenciador de tarefas fofinho 😺",
    bg="#F7B9C9",
    fg="#6B213C",
    font=("Segoe UI", 13)
).pack(pady=(8, 30))


# Botão Entrar
btn = tk.Button(
    card,
    text="🚀 Entrar",
    command=abrir_app,
    bg="#EC4899",
    fg="white",
    font=("Segoe UI", 16, "bold"),
    relief="flat",
    padx=35,
    pady=12,
    cursor="hand2",
    activebackground="#DB2777",
    activeforeground="white"
)

btn.pack()


# Rodapé fofo
tk.Label(
    janela,
    text="made with 🐾 + ☕",
    bg="#F8E9EE",
    fg="#8B5C6E",
    font=("Segoe UI", 10)
).place(relx=0.5, rely=0.96, anchor="center")


janela.mainloop()