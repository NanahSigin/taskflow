import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Classe Tarefa (Backend Simulado) ---
class Tarefa:
    def __init__(self, id, titulo, descricao, prioridade, status="A Fazer"):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = status
        self.anexos = []

class Gerenciador:
    def __init__(self):
        self._tarefas = [Tarefa(101, "Exemplo", "Descrição da tarefa", "Alta", "A Fazer")]
    def listar_tarefas(self): return self._tarefas
    def criar_tarefa(self, t, d, p): 
        nova = Tarefa(random.randint(100, 999), t, d, p)
        self._tarefas.append(nova)
    def buscar_tarefa(self, id): return next((t for t in self._tarefas if t.id == id), None)
    def excluir_tarefa(self, id): self._tarefas = [t for t in self._tarefas if t.id != id]

gerenciador = Gerenciador()
tarefa_selecionada = None

# --- Funções de Lógica ---
def atualizar_kanban():
    for f in [frame_afazer, frame_progresso, frame_concluido]:
        for widget in f.winfo_children(): widget.destroy()

    for t in gerenciador.listar_tarefas():
        card = tk.Frame(bg="#FFFFFF", bd=1, relief="raised", padx=10, pady=10)
        tk.Label(card, text=f"🐾 #{t.id} {t.titulo}", bg="#FFFFFF", font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(card, text=t.descricao, bg="#FFFFFF", wraplength=180, justify="left").pack(anchor="w")
        
        card.bind("<Button-1>", lambda e, i=t.id: exibir_detalhes(i))
        
        target = {"A Fazer": frame_afazer, "Em Progresso": frame_progresso, "Concluído": frame_concluido}[t.status]
        card.pack(in_=target, fill="x", padx=5, pady=5)

def exibir_detalhes(id_t):
    global tarefa_selecionada
    tarefa_selecionada = id_t
    t = gerenciador.buscar_tarefa(id_t)
    lbl_detalhe_titulo.config(text=f"Editando: {t.titulo}")
    txt_descricao.delete("1.0", tk.END)
    txt_descricao.insert("1.0", t.descricao)

def avancar():
    if not tarefa_selecionada: return
    t = gerenciador.buscar_tarefa(tarefa_selecionada)
    mapa = {"A Fazer": "Em Progresso", "Em Progresso": "Concluído", "Concluído": "A Fazer"}
    t.status = mapa[t.status]
    atualizar_kanban()

# --- Interface Gráfica ---
root = tk.Tk()
root.title("🐾 KittyFlow Pro")
root.geometry("1200x700")
root.configure(bg="#FFF1F2")

# Header
tk.Label(root, text="🐾 KITTYFLOW", bg="#FFF1F2", fg="#DB2777", font=("Segoe UI", 24, "bold")).pack(pady=10)

# Estrutura Principal
main = tk.Frame(root, bg="#FFF1F2")
main.pack(fill="both", expand=True, padx=20)

# Kanban Area
kanban = tk.Frame(main, bg="#FFF1F2")
kanban.pack(side="left", fill="both", expand=True)

frame_afazer = tk.LabelFrame(kanban, text="😴 Soneca", bg="#FCE7F3", width=250)
frame_progresso = tk.LabelFrame(kanban, text="🐈 Caçando", bg="#FCE7F3", width=250)
frame_concluido = tk.LabelFrame(kanban, text="🐾 Missão Cumprida", bg="#FCE7F3", width=250)
for f in [frame_afazer, frame_progresso, frame_concluido]: f.pack(side="left", fill="both", expand=True, padx=5)

# Sidebar (Detalhes e Cadastro)
sidebar = tk.Frame(main, bg="#FBCFE8", width=300, padx=20, pady=20)
sidebar.pack(side="right", fill="y")

lbl_detalhe_titulo = tk.Label(sidebar, text="Detalhes da Tarefa", bg="#FBCFE8", font=("Arial", 12, "bold"))
lbl_detalhe_titulo.pack(pady=10)
txt_descricao = tk.Text(sidebar, height=8, width=30)
txt_descricao.pack()

# Área de Imagem (Simulação de Trello)
area_img = tk.Label(sidebar, text="[ Arraste imagem aqui ]", bg="#E5E7EB", width=30, height=8)
area_img.pack(pady=10)

tk.Button(sidebar, text="🐾 Avançar Status", command=avancar, bg="#A855F7", fg="white").pack(fill="x", pady=5)
tk.Button(sidebar, text="😾 Excluir", command=lambda: [gerenciador.excluir_tarefa(tarefa_selecionada), atualizar_kanban()], bg="#FB7185", fg="white").pack(fill="x")

atualizar_kanban()
root.mainloop()