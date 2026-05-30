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
    tarefa = gerenciador.buscar_tarefa(id_tarefa)

    lbl_selecionada.config(
        text=f"🐾 Tarefa selecionada: #{id_tarefa}"
    )

    if tarefa:
        lbl_detalhes.config(
            text=
            f"🐱 Título: {tarefa.titulo}\n"
            f"📝 Descrição: {tarefa.descricao}\n"
            f"👤 Responsável: {tarefa.responsavel}\n"
            f"⚡ Prioridade: {tarefa.prioridade}\n"
            f"📌 Status: {tarefa.status}"
        )


def atualizar_kanban():

    for frame in [frame_afazer, frame_progresso, frame_concluido]:
        for widget in frame.winfo_children():
            widget.destroy()

    for tarefa in gerenciador.listar_tarefas():

        card = tk.Frame(
            bg=cor_prioridade(tarefa.prioridade),
            padx=10,
            pady=10,
            cursor="hand2",
            relief="raised",
            bd=2
        )

        titulo = tk.Label(
            card,
            text=f"🐱 {tarefa.titulo}",
            bg=card["bg"],
            fg="#4A044E",
            font=("Segoe UI", 10, "bold")
        )
        titulo.pack(anchor="w")

        descricao = tk.Label(
            card,
            text=tarefa.descricao,
            bg=card["bg"],
            fg="#4A044E",
            wraplength=220,
            justify="left"
        )
        descricao.pack(anchor="w")

        prioridade = tk.Label(
            card,
            text=f"Prioridade: {tarefa.prioridade}",
            bg=card["bg"],
            fg="#4A044E"
        )
        prioridade.pack(anchor="w")

        # clique seguro
        def bind_click(tid):
            return lambda e: selecionar_tarefa(tid)

        card.bind("<Button-1>", bind_click(tarefa.id))
        titulo.bind("<Button-1>", bind_click(tarefa.id))
        descricao.bind("<Button-1>", bind_click(tarefa.id))
        prioridade.bind("<Button-1>", bind_click(tarefa.id))

        if tarefa.status == "A Fazer":
            card.pack(in_=frame_afazer, fill="x", pady=5, padx=5)

        elif tarefa.status == "Em Progresso":
            card.pack(in_=frame_progresso, fill="x", pady=5, padx=5)

        else:
            card.pack(in_=frame_concluido, fill="x", pady=5, padx=5)


def cadastrar_tarefa():

    titulo = entry_titulo.get()
    descricao = entry_descricao.get()
    prioridade = combo_prioridade.get()
    responsavel = entry_responsavel.get()

    if not titulo:
        messagebox.showwarning("Aviso", "Digite um título.")
        return

    gerenciador.criar_tarefa(
        titulo,
        descricao,
        prioridade,
        responsavel
    )

    entry_titulo.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_responsavel.delete(0, tk.END)

    atualizar_kanban()


def avancar_status():

    global tarefa_selecionada

    if not tarefa_selecionada:
        return

    tarefa = gerenciador.buscar_tarefa(tarefa_selecionada)

    if tarefa:
        if tarefa.status == "A Fazer":
            tarefa.status = "Em Progresso"
        elif tarefa.status == "Em Progresso":
            tarefa.status = "Concluído"

    atualizar_kanban()


def excluir_tarefa():

    global tarefa_selecionada

    if not tarefa_selecionada:
        return

    resposta = messagebox.askyesno(
        "Confirmar",
        "Deseja excluir esta tarefa?"
    )

    if resposta:
        gerenciador.excluir_tarefa(tarefa_selecionada)
        tarefa_selecionada = None

        lbl_selecionada.config(
            text="😺 Nenhuma tarefa selecionada"
        )

        lbl_detalhes.config(
            text="👀 Clique em uma tarefa para ver detalhes"
        )

        atualizar_kanban()


# =====================
# JANELA
# =====================

janela = tk.Tk()
janela.title("🐾 KittyFlow")
janela.geometry("1200x700")
janela.configure(bg="#FFF1F2")

tk.Label(
    janela,
    text="🐾 KITTYFLOW",
    bg="#FFF1F2",
    fg="#DB2777",
    font=("Segoe UI", 24, "bold")
).pack(pady=(15, 5))

tk.Label(
    janela,
    text="Organize suas tarefas com ajuda dos gatinhos 😺",
    bg="#FFF1F2",
    fg="#9D174D",
    font=("Segoe UI", 10)
).pack()

# =====================
# FORM
# =====================

frame_form = tk.Frame(
    janela,
    bg="#FBCFE8",
    padx=20,
    pady=20
)
frame_form.pack(fill="x", padx=20, pady=20)

tk.Label(frame_form, text="Título", bg="#FBCFE8", fg="#831843").grid(row=0, column=0)
entry_titulo = tk.Entry(frame_form, width=35)
entry_titulo.grid(row=0, column=1, padx=10)

tk.Label(frame_form, text="Descrição", bg="#FBCFE8", fg="#831843").grid(row=1, column=0)
entry_descricao = tk.Entry(frame_form, width=35)
entry_descricao.grid(row=1, column=1, padx=10)

tk.Label(frame_form, text="Prioridade", bg="#FBCFE8", fg="#831843").grid(row=2, column=0)
combo_prioridade = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta"])
combo_prioridade.current(0)
combo_prioridade.grid(row=2, column=1, padx=10)

tk.Label(frame_form, text="Responsável", bg="#FBCFE8", fg="#831843").grid(row=3, column=0)
entry_responsavel = tk.Entry(frame_form, width=35)
entry_responsavel.grid(row=3, column=1, padx=10)

tk.Button(
    frame_form,
    text="🐱 Nova Tarefa",
    command=cadastrar_tarefa,
    bg="#EC4899",
    fg="white"
).grid(row=4, column=0, columnspan=2, pady=10)

# =====================
# STATUS
# =====================

lbl_selecionada = tk.Label(
    janela,
    text="😺 Nenhuma tarefa selecionada",
    bg="#FFF1F2",
    fg="#831843"
)
lbl_selecionada.pack()

# =====================
# DETALHES
# =====================

frame_detalhes = tk.Frame(janela, bg="#FFE4EC", padx=10, pady=10)
frame_detalhes.pack(fill="x", padx=20, pady=10)

lbl_detalhes = tk.Label(
    frame_detalhes,
    text="👀 Clique em uma tarefa para ver detalhes",
    bg="#FFE4EC",
    fg="#831843",
    justify="left"
)
lbl_detalhes.pack()

# =====================
# KANBAN
# =====================

frame_kanban = tk.Frame(janela, bg="#FFF1F2")
frame_kanban.pack(fill="both", expand=True, padx=20, pady=10)

frame_afazer = tk.LabelFrame(frame_kanban, text="😴 Soneca", bg="#FCE7F3")
frame_afazer.pack(side="left", fill="both", expand=True, padx=5)

frame_progresso = tk.LabelFrame(frame_kanban, text="🐈 Caçando", bg="#FCE7F3")
frame_progresso.pack(side="left", fill="both", expand=True, padx=5)

frame_concluido = tk.LabelFrame(frame_kanban, text="🐾 Missão Cumprida", bg="#FCE7F3")
frame_concluido.pack(side="left", fill="both", expand=True, padx=5)

# =====================
# BOTÕES
# =====================

frame_botoes = tk.Frame(janela, bg="#FFF1F2")
frame_botoes.pack(pady=10)

tk.Button(
    frame_botoes,
    text="🐾 Avançar",
    command=avancar_status,
    bg="#A855F7",
    fg="white"
).pack(side="left", padx=10)

tk.Button(
    frame_botoes,
    text="😾 Excluir",
    command=excluir_tarefa,
    bg="#FB7185",
    fg="white"
).pack(side="left", padx=10)

# =====================
# START
# =====================

atualizar_kanban()
janela.mainloop()