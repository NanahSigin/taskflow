import tkinter as tk
from tkinter import ttk, messagebox
from gerenciador import Gerenciador

gerenciador = Gerenciador()
tarefa_selecionada = None

# =====================
# FUNÇÕES
# =====================

def cor_prioridade(prioridade):
    if prioridade == "Alta":
        return "#FDA4AF"
    elif prioridade == "Média":
        return "#DDD6FE"
    return "#F9A8D4"


def selecionar_tarefa(id_tarefa):
    global tarefa_selecionada
    tarefa_selecionada = id_tarefa
    lbl_selecionada.config(text=f"🐾 Tarefa #{id_tarefa} selecionada")


def atualizar_kanban():
    for frame in [frame_afazer, frame_progresso, frame_concluido]:
        for w in frame.winfo_children():
            w.destroy()

    for tarefa in gerenciador.listar_tarefas():
        card = tk.Frame(
            bg=cor_prioridade(tarefa.prioridade),
            padx=10,
            pady=10,
            relief="raised",
            bd=2
        )

        tk.Label(card, text=tarefa.titulo, bg=card["bg"]).pack(anchor="w")
        tk.Label(card, text=tarefa.descricao, bg=card["bg"]).pack(anchor="w")
        tk.Label(card, text=tarefa.status, bg=card["bg"]).pack(anchor="w")

        for w in [card]:
            w.bind("<Button-1>", lambda e, id=tarefa.id: selecionar_tarefa(id))

        if tarefa.status == "A Fazer":
            card.pack(in_=frame_afazer, fill="x", pady=5)
        elif tarefa.status == "Em Progresso":
            card.pack(in_=frame_progresso, fill="x", pady=5)
        else:
            card.pack(in_=frame_concluido, fill="x", pady=5)


def cadastrar_tarefa():
    gerenciador.criar_tarefa(
        entry_titulo.get(),
        entry_descricao.get(),
        combo_prioridade.get()
    )

    entry_titulo.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

    atualizar_kanban()


def avancar_status():
    global tarefa_selecionada
    tarefa = gerenciador.buscar_tarefa(tarefa_selecionada)

    if tarefa:
        if tarefa.status == "A Fazer":
            tarefa.status = "Em Progresso"
        elif tarefa.status == "Em Progresso":
            tarefa.status = "Concluído"

    atualizar_kanban()


def excluir_tarefa():
    global tarefa_selecionada

    if tarefa_selecionada:
        gerenciador.excluir_tarefa(tarefa_selecionada)
        tarefa_selecionada = None
        atualizar_kanban()

# =====================
# UI
# =====================

janela = tk.Tk()
janela.title("KittyFlow")
janela.geometry("1100x700")
janela.configure(bg="#FFF1F2")

tk.Label(janela, text="🐾 KittyFlow", font=("Arial", 20), bg="#FFF1F2").pack()

# MENU
frame_menu = tk.Frame(janela, bg="#FFE4EC")
frame_menu.pack(fill="x")

tk.Button(frame_menu, text="Adicionar", command=cadastrar_tarefa).pack(side="left")
tk.Button(frame_menu, text="Avançar", command=avancar_status).pack(side="left")
tk.Button(frame_menu, text="Excluir", command=excluir_tarefa).pack(side="left")

# FORM
frame_form = tk.Frame(janela)
frame_form.pack()

entry_titulo = tk.Entry(frame_form)
entry_titulo.pack()

entry_descricao = tk.Entry(frame_form)
entry_descricao.pack()

combo_prioridade = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta"])
combo_prioridade.current(0)
combo_prioridade.pack()

# LABEL
lbl_selecionada = tk.Label(janela, text="Nenhuma tarefa selecionada")
lbl_selecionada.pack()

# KANBAN
frame_kanban = tk.Frame(janela)
frame_kanban.pack(fill="both", expand=True)

frame_afazer = tk.LabelFrame(frame_kanban, text="A Fazer")
frame_afazer.pack(side="left", expand=True, fill="both")

frame_progresso = tk.LabelFrame(frame_kanban, text="Em Progresso")
frame_progresso.pack(side="left", expand=True, fill="both")

frame_concluido = tk.LabelFrame(frame_kanban, text="Concluído")
frame_concluido.pack(side="left", expand=True, fill="both")

atualizar_kanban()

janela.mainloop()