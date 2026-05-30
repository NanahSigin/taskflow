import tkinter as tk
from tkinter import ttk, messagebox
from gerenciador import Gerenciador

gerenciador = Gerenciador()
tarefa_selecionada = None


# =====================
# CORES
# =====================

def cor_prioridade(prioridade):
    if prioridade == "Alta":
        return "#FDA4AF"
    elif prioridade == "Média":
        return "#DDD6FE"
    return "#F9A8D4"


# =====================
# KANBAN
# =====================

def atualizar_kanban():
    
    # limpa colunas
    for frame in [frame_afazer, frame_progresso, frame_concluido]:
        for widget in frame.winfo_children():
            widget.destroy()

    for tarefa in gerenciador.listar_tarefas():

        # define coluna
        if tarefa.status == "A Fazer":
            frame_destino = frame_afazer

        elif tarefa.status == "Em Progresso":
            frame_destino = frame_progresso

        else:
            frame_destino = frame_concluido

        # muda cor quando concluído
        cor_card = (
            "#86EFAC"
            if tarefa.status == "Concluído"
            else cor_prioridade(tarefa.prioridade)
        )

        card = tk.Frame(
            frame_destino,
            bg=cor_card,
            padx=10,
            pady=10,
            relief="raised",
            bd=2
        )

        card.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # título
        titulo = tk.Label(
            card,
            text=f"🐱 {tarefa.titulo}",
            bg=cor_card,
            fg="#4A044E",
            font=("Segoe UI", 10, "bold")
        )
        titulo.pack(anchor="w")

        # descrição
        descricao = tk.Label(
            card,
            text=tarefa.descricao,
            bg=cor_card,
            fg="#4A044E",
            justify="left",
            wraplength=220
        )
        descricao.pack(anchor="w")

        # prioridade
        prioridade = tk.Label(
            card,
            text=f"⭐ {tarefa.prioridade}",
            bg=cor_card,
            fg="#4A044E"
        )
        prioridade.pack(anchor="w")

        # detalhes ao clicar no card
        def selecionar(tarefa=tarefa):

            global tarefa_selecionada

            tarefa_selecionada = tarefa.id

            lbl_selecionada.config(
                text=f"😺 Selecionada: {tarefa.titulo}"
            )

            lbl_detalhes.config(
                text=(
                    f"👀 {tarefa.titulo}\n"
                    f"📝 {tarefa.descricao}\n"
                    f"👤 {tarefa.responsavel}\n"
                    f"⭐ {tarefa.prioridade}\n"
                    f"📌 {tarefa.status}"
                )
            )

        for widget in [card, titulo, descricao, prioridade]:
            widget.bind(
                "<Button-1>",
                lambda e, t=tarefa: selecionar(t)
            )

        # ==================
        # BOTÕES DO CARD
        # ==================

        frame_botoes = tk.Frame(
            card,
            bg=cor_card
        )
        frame_botoes.pack(
            fill="x",
            pady=(8, 0)
        )

        # avançar status
        def avancar(tarefa=tarefa):

            if tarefa.status == "A Fazer":
                tarefa.status = "Em Progresso"

            elif tarefa.status == "Em Progresso":
                tarefa.status = "Concluído"

            atualizar_kanban()

        tk.Button(
            frame_botoes,
            text="⏩",
            command=avancar,
            bg="#6366F1",
            fg="white",
            width=4
        ).pack(side="left", padx=2)

        # editar
        tk.Button(
            frame_botoes,
            text="✏",
            command=lambda t=tarefa: abrir_detalhes(t.id),
            bg="#A855F7",
            fg="white",
            width=4
        ).pack(side="left", padx=2)

        # excluir
        def excluir(tarefa=tarefa):

            resposta = messagebox.askyesno(
                "Excluir",
                f"Excluir '{tarefa.titulo}'?"
            )

            if resposta:
                gerenciador.excluir_tarefa(
                    tarefa.id
                )

                atualizar_kanban()

        tk.Button(
            frame_botoes,
            text="🗑",
            command=excluir,
            bg="#FB7185",
            fg="white",
            width=4
        ).pack(side="left", padx=2)

    janela.update_idletasks()

# =====================
# CADASTRAR
# =====================

def cadastrar_tarefa():

    titulo = entry_titulo.get().strip()
    descricao = entry_descricao.get().strip()
    prioridade = combo_prioridade.get()
    responsavel = entry_responsavel.get().strip()

    if not titulo:
        messagebox.showwarning(
            "Aviso",
            "Digite um título."
        )
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


# =====================
# AVANÇAR STATUS
# =====================

def avancar_status():

    global tarefa_selecionada

    if tarefa_selecionada is None:
        return

    tarefa = gerenciador.buscar_tarefa(
        tarefa_selecionada
    )

    if not tarefa:
        return

    if tarefa.status == "A Fazer":
        tarefa.status = "Em Progresso"

    elif tarefa.status == "Em Progresso":
        tarefa.status = "Concluído"

    atualizar_kanban()


# =====================
# JANELA EDITAR
# =====================

def abrir_detalhes(id_tarefa):

    tarefa = gerenciador.buscar_tarefa(id_tarefa)

    if not tarefa:
        return

    janela_det = tk.Toplevel(janela)
    janela_det.title("Editar tarefa")
    janela_det.geometry("400x420")
    janela_det.configure(bg="#FFE4EC")

    tk.Label(
        janela_det,
        text="Título",
        bg="#FFE4EC"
    ).pack(pady=(10, 0))

    entry_titulo_editar = tk.Entry(
        janela_det,
        width=35
    )
    entry_titulo_editar.insert(
        0,
        tarefa.titulo
    )
    entry_titulo_editar.pack()

    tk.Label(
        janela_det,
        text="Descrição",
        bg="#FFE4EC"
    ).pack()

    entry_desc_editar = tk.Entry(
        janela_det,
        width=35
    )
    entry_desc_editar.insert(
        0,
        tarefa.descricao
    )
    entry_desc_editar.pack()

    tk.Label(
        janela_det,
        text="Responsável",
        bg="#FFE4EC"
    ).pack()

    entry_resp_editar = tk.Entry(
        janela_det,
        width=35
    )
    entry_resp_editar.insert(
        0,
        tarefa.responsavel
    )
    entry_resp_editar.pack()

    tk.Label(
        janela_det,
        text="Prioridade",
        bg="#FFE4EC"
    ).pack()

    combo_editar = ttk.Combobox(
        janela_det,
        values=["Baixa", "Média", "Alta"]
    )
    combo_editar.set(
        tarefa.prioridade
    )
    combo_editar.pack()

    def salvar():

        tarefa.titulo = (
            entry_titulo_editar.get()
        )

        tarefa.descricao = (
            entry_desc_editar.get()
        )

        tarefa.responsavel = (
            entry_resp_editar.get()
        )

        tarefa.prioridade = (
            combo_editar.get()
        )

        atualizar_kanban()
        janela_det.destroy()

    def excluir():

        resposta = messagebox.askyesno(
            "Excluir",
            f"Excluir '{tarefa.titulo}'?"
        )

        if not resposta:
            return

        gerenciador.excluir_tarefa(
            tarefa.id
        )

        global tarefa_selecionada
        tarefa_selecionada = None

        lbl_selecionada.config(
            text="😺 Nenhuma tarefa selecionada"
        )

        lbl_detalhes.config(
            text="👀 Clique em uma tarefa para ver detalhes"
        )

        janela_det.destroy()

        atualizar_kanban()

    tk.Button(
        janela_det,
        text="✏ Salvar",
        command=salvar,
        bg="#A855F7",
        fg="white"
    ).pack(pady=10)

    tk.Button(
        janela_det,
        text="🗑 Excluir",
        command=excluir,
        bg="#FB7185",
        fg="white"
    ).pack()


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

frame_form = tk.Frame(
    janela,
    bg="#FBCFE8",
    padx=20,
    pady=20
)
frame_form.pack(
    fill="x",
    padx=20,
    pady=20
)

tk.Label(
    frame_form,
    text="Título",
    bg="#FBCFE8"
).grid(row=0, column=0)

entry_titulo = tk.Entry(
    frame_form,
    width=30
)
entry_titulo.grid(row=0, column=1)

tk.Label(
    frame_form,
    text="Descrição",
    bg="#FBCFE8"
).grid(row=1, column=0)

entry_descricao = tk.Entry(
    frame_form,
    width=30
)
entry_descricao.grid(row=1, column=1)

tk.Label(
    frame_form,
    text="Prioridade",
    bg="#FBCFE8"
).grid(row=2, column=0)

combo_prioridade = ttk.Combobox(
    frame_form,
    values=["Baixa", "Média", "Alta"]
)
combo_prioridade.current(0)
combo_prioridade.grid(row=2, column=1)

tk.Label(
    frame_form,
    text="Responsável",
    bg="#FBCFE8"
).grid(row=3, column=0)

entry_responsavel = tk.Entry(
    frame_form,
    width=30
)
entry_responsavel.grid(row=3, column=1)

tk.Button(
    frame_form,
    text="🐱 Nova Tarefa",
    command=cadastrar_tarefa,
    bg="#EC4899",
    fg="white"
).grid(
    row=4,
    column=0,
    columnspan=2
)

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
lbl_detalhes.pack(
    fill="x",
    padx=20,
    pady=10
)

# KANBAN

frame_kanban = tk.Frame(
    janela,
    bg="#FFF1F2"
)
frame_kanban.pack(
    fill="both",
    expand=True
)

frame_afazer = tk.LabelFrame(
    frame_kanban,
    text="😴 Soneca"
)
frame_afazer.pack(
    side="left",
    fill="both",
    expand=True
)

frame_progresso = tk.LabelFrame(
    frame_kanban,
    text="🐈 Caçando"
)
frame_progresso.pack(
    side="left",
    fill="both",
    expand=True
)

frame_concluido = tk.LabelFrame(
    frame_kanban,
    text="🐾 Concluído"
)
frame_concluido.pack(
    side="left",
    fill="both",
    expand=True
)

# BOTÃO STATUS

tk.Button(
    janela,
    text="⏩ Avançar",
    command=avancar_status,
    bg="#6366F1",
    fg="white"
).pack(pady=10)

# START

atualizar_kanban()
janela.mainloop()