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

        tk.Label(card, text=f"🐱 {tarefa.titulo}",
                 bg=card["bg"], fg="#4A044E",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        tk.Label(card, text=tarefa.descricao,
                 bg=card["bg"], fg="#4A044E",
                 wraplength=220, justify="left").pack(anchor="w")

        tk.Label(card, text=f"Prioridade: {tarefa.prioridade}",
                 bg=card["bg"], fg="#4A044E").pack(anchor="w")

        def bind_click(id_tarefa):
            return lambda e: abrir_detalhes(id_tarefa)

        card.bind("<Button-1>", bind_click(tarefa.id))

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

    if not tarefa_selecionada:
        return

    tarefa = gerenciador.buscar_tarefa(tarefa_selecionada)

    if tarefa:
        if tarefa.status == "A Fazer":
            tarefa.status = "Em Progresso"
        elif tarefa.status == "Em Progresso":
            tarefa.status = "Concluído"

    atualizar_kanban()


# =====================
# JANELA DE DETALHES
# =====================

def abrir_detalhes(id_tarefa):

    global tarefa_selecionada
    tarefa_selecionada = id_tarefa

    tarefa = gerenciador.buscar_tarefa(id_tarefa)
    if not tarefa:
        return

    janela_det = tk.Toplevel(janela)
    janela_det.title(f"🐱 Tarefa #{tarefa.id}")
    janela_det.geometry("420x450")
    janela_det.configure(bg="#FFE4EC")

    tk.Label(janela_det, text="Título", bg="#FFE4EC").pack()
    entry_titulo = tk.Entry(janela_det)
    entry_titulo.insert(0, tarefa.titulo)
    entry_titulo.pack()

    tk.Label(janela_det, text="Descrição", bg="#FFE4EC").pack()
    entry_descricao = tk.Entry(janela_det)
    entry_descricao.insert(0, tarefa.descricao)
    entry_descricao.pack()

    tk.Label(janela_det, text="Responsável", bg="#FFE4EC").pack()
    entry_resp = tk.Entry(janela_det)
    entry_resp.insert(0, tarefa.responsavel)
    entry_resp.pack()

    tk.Label(janela_det, text="Prioridade", bg="#FFE4EC").pack()
    combo = ttk.Combobox(janela_det, values=["Baixa", "Média", "Alta"])
    combo.set(tarefa.prioridade)
    combo.pack()

    def salvar():
        tarefa.titulo = entry_titulo.get()
        tarefa.descricao = entry_descricao.get()
        tarefa.responsavel = entry_resp.get()
        tarefa.prioridade = combo.get()

        atualizar_kanban()
        janela_det.destroy()

    tk.Button(
        janela_det,
        text="✏ Salvar",
        bg="#A855F7",
        fg="white",
        command=salvar
    ).pack(pady=10)


# =====================
# EXCLUIR (FORA DO CARD)
# =====================

def excluir_tarefa():
    
    global tarefa_selecionada

    if not tarefa_selecionada:
        messagebox.showwarning(
            "Aviso",
            "Selecione uma tarefa"
        )
        return

    tarefa = gerenciador.buscar_tarefa(
        tarefa_selecionada
    )

    if not tarefa:
        return

    resposta = messagebox.askyesno(
        "Confirmar",
        f"Excluir tarefa '{tarefa.titulo}'?"
    )

    if resposta:

        # remove do gerenciador
        gerenciador.excluir_tarefa(tarefa.id)

        # limpa seleção
        tarefa_selecionada = None

        lbl_selecionada.config(
            text="😺 Nenhuma tarefa selecionada"
        )

        lbl_detalhes.config(
            text="👀 Clique em uma tarefa para ver detalhes"
        )

        # força atualização visual
        janela.update_idletasks()
        atualizar_kanban()

# =====================
# JANELA PRINCIPAL
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
).pack(pady=10)

# FORM

frame_form = tk.Frame(janela, bg="#FBCFE8", padx=20, pady=20)
frame_form.pack(fill="x", padx=20, pady=20)

tk.Label(frame_form, text="Título", bg="#FBCFE8").grid(row=0, column=0)
entry_titulo = tk.Entry(frame_form, width=30)
entry_titulo.grid(row=0, column=1)

tk.Label(frame_form, text="Descrição", bg="#FBCFE8").grid(row=1, column=0)
entry_descricao = tk.Entry(frame_form, width=30)
entry_descricao.grid(row=1, column=1)

tk.Label(frame_form, text="Prioridade", bg="#FBCFE8").grid(row=2, column=0)
combo_prioridade = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta"])
combo_prioridade.current(0)
combo_prioridade.grid(row=2, column=1)

tk.Label(frame_form, text="Responsável", bg="#FBCFE8").grid(row=3, column=0)
entry_responsavel = tk.Entry(frame_form, width=30)
entry_responsavel.grid(row=3, column=1)

tk.Button(
    frame_form,
    text="🐱 Nova Tarefa",
    command=cadastrar_tarefa,
    bg="#EC4899",
    fg="white"
).grid(row=4, column=0, columnspan=2)

# STATUS

lbl_selecionada = tk.Label(
    janela,
    text="😺 Nenhuma tarefa selecionada",
    bg="#FFF1F2",
    fg="#831843"
)
lbl_selecionada.pack()

lbl_detalhes = tk.Label(
    janela,
    text="👀 Clique em uma tarefa para ver detalhes",
    bg="#FFE4EC",
    fg="#831843",
    justify="left"
)
lbl_detalhes.pack(fill="x", padx=20, pady=10)

# KANBAN

frame_kanban = tk.Frame(janela, bg="#FFF1F2")
frame_kanban.pack(fill="both", expand=True)

frame_afazer = tk.LabelFrame(frame_kanban, text="😴 Soneca")
frame_afazer.pack(side="left", fill="both", expand=True)

frame_progresso = tk.LabelFrame(frame_kanban, text="🐈 Caçando")
frame_progresso.pack(side="left", fill="both", expand=True)

frame_concluido = tk.LabelFrame(frame_kanban, text="🐾 Concluído")
frame_concluido.pack(side="left", fill="both", expand=True)

# BOTÕES (FORA DOS CARDS)

frame_botoes = tk.Frame(janela, bg="#FFF1F2")
frame_botoes.pack(pady=10)

tk.Button(
    frame_botoes,
    text="⏩ Avançar",
    command=avancar_status,
    bg="#6366F1",
    fg="white"
).pack(side="left", padx=10)

tk.Button(
    frame_botoes,
    text="🗑 Excluir",
    command=excluir_tarefa,
    bg="#FB7185",
    fg="white"
).pack(side="left", padx=10)

# START

atualizar_kanban()
janela.mainloop()