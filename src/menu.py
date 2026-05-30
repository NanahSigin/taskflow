import tkinter as tk
import subprocess
import sys
import os


def abrir_app():

    janela.destroy()

    caminho_main = os.path.join(
        os.path.dirname(__file__),
        "main.py"
    )

    subprocess.Popen(
        [sys.executable, caminho_main]
    )


janela = tk.Tk()
janela.title("🐾 KittyFlow")
janela.geometry("1200x700")
janela.configure(bg="#EC4899")


tk.Label(
    janela,
    text="🐾 KITTYFLOW",
    bg="#EC4899",
    fg="white",
    font=("Segoe UI", 30, "bold")
).pack(pady=60)

tk.Label(
    janela,
    text="Seu gerenciador de tarefas 😺",
    bg="#EC4899",
    fg="#FBCFE8",
    font=("Segoe UI", 14)
).pack()

tk.Button(
    janela,
    text="🚀 Entrar",
    command=abrir_app,
    bg="#DB2777",
    fg="white",
    font=("Segoe UI", 16, "bold"),
    padx=30,
    pady=10,
    relief="flat",
    cursor="hand2"
).pack(pady=50)

janela.mainloop()