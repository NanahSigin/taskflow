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
        return "#FECDD3"   # Rosa/Vermelho pastel moderno
    elif prioridade == "Média":
        return "#E9D5FF"   # Roxo pastel moderno
    return "#FCE7F3"       # Rosa pastel (Baixa)


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
            "#BBF7D0"   # Verde pastel moderno para concluído
            if tarefa.status == "Concluído"
            else cor_prioridade(tarefa.prioridade)
        )

        # Card Clean (Flat Design) com borda suave
        card = tk.Frame(
            frame_destino,
            bg=cor_card,
            padx=12,
            pady=12,
            highlightbackground="#FDA4AF",
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=10,
            pady=6
        )

        # título
        titulo = tk.Label(
            card,
            text=f"🐱 {tarefa.titulo}",
            bg=cor_card,
            fg="#4C0519",
            font=("Segoe UI", 11, "bold")
        )
        titulo.pack(anchor="w")

        # descrição
        descricao = tk.Label(
            card,
            text=tarefa.descricao,
            bg=cor_card,
            fg="#475569",   # Cinza escuro elegante para melhor leitura
            font=("Segoe UI", 9),
            justify="left",
            wraplength=240
        )
        descricao.pack(anchor="w", pady=(2, 2))

        # prioridade
        prioridade = tk.Label(
            card,
            text=f"⭐ {tarefa.prioridade}",
            bg=cor_card,
            fg="#4C0519",
            font=("Segoe UI", 9, "italic")
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
            widget.config(cursor="hand2") # Cursor de mãozinha ao passar no card

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

        # Só mostra o botão avançar se não estiver concluído
        if tarefa.status != "Concluído":
            tk.Button(
                frame_botoes,
                text="⏩ Avançar",
                command=avancar,
                bg="#6366F1",
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                cursor="hand2",
                padx=5
            ).pack(side="left", padx=2)

        # editar
        tk.Button(
            frame_botoes,
            text="✏️",
            command=lambda t=tarefa: abrir_detalhes(t.id),
            bg="#A855F7",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            width=3
        ).pack(side="left", padx=2)

        # excluir
        def excluir(tarefa=tarefa):
            global tarefa_selecionada

            resposta = messagebox.askyesno(
                "Excluir",
                f"Excluir '{tarefa.titulo}'?"
            )

            if resposta:
                gerenciador.excluir_tarefa(
                    tarefa.id
                )

                # ✨ Limpa o painel do topo se a tarefa deletada estava selecionada
                if tarefa_selecionada == tarefa.id:
                    tarefa_selecionada = None
                    lbl_selecionada.config(text="😺 Nenhuma tarefa selecionada")
                    lbl_detalhes.config(text="👀 Clique em uma tarefa para ver detalhes")

                atualizar_kanban()

        tk.Button(
            frame_botoes,
            text="🗑️",
            command=excluir,
            bg="#F43F5E",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            width=3
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
    janela_det.geometry("380x440")
    janela_det.configure(bg="#FFF1F2")
    janela_det.grab_set()

    # Container interno para espaçamento confortável
    container = tk.Frame(janela_det, bg="#FFF1F2", padx=20, pady=10)
    container.pack(fill="both", expand=True)

    lbl_style = {"bg": "#FFF1F2", "fg": "#4C0519", "font": ("Segoe UI", 10, "bold"), "anchor": "w"}
    entry_style = {"font": ("Segoe UI", 10), "relief": "solid", "bd": 1}

    tk.Label(container, text="Título", **lbl_style).pack(fill="x", pady=(10, 2))
    entry_titulo_editar = tk.Entry(container, **entry_style)
    entry_titulo_editar.insert(0, tarefa.titulo)
    entry_titulo_editar.pack(fill="x", pady=5)

    tk.Label(container, text="Descrição", **lbl_style).pack(fill="x", pady=(10, 2))
    entry_desc_editar = tk.Entry(container, **entry_style)
    entry_desc_editar.insert(0, tarefa.descricao)
    entry_desc_editar.pack(fill="x", pady=5)

    tk.Label(container, text="Responsável", **lbl_style).pack(fill="x", pady=(10, 2))
    entry_resp_editar = tk.Entry(container, **entry_style)
    entry_resp_editar.insert(0, tarefa.responsavel)
    entry_resp_editar.pack(fill="x", pady=5)

    tk.Label(container, text="Prioridade", **lbl_style).pack(fill="x", pady=(10, 2))
    combo_editar = ttk.Combobox(container, values=["Baixa", "Média", "Alta"], font=("Segoe UI", 10), state="readonly")
    combo_editar.set(tarefa.prioridade)
    combo_editar.pack(fill="x", pady=5)

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
        container,
        text="✏️ Salvar",
        command=salvar,
        bg="#A855F7",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        pady=6,
        cursor="hand2"
    ).pack(fill="x", pady=(20, 5))

    tk.Button(
        container,
        text="🗑️ Excluir",
        command=excluir,
        bg="#FB7185",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        pady=6,
        cursor="hand2"
    ).pack(fill="x")


# =====================
# JANELA PRINCIPAL
# =====================

janela = tk.Tk()
janela.title("🐾 KittyFlow")
janela.geometry("1100x750")
janela.configure(bg="#FFF1F2")

# Estilo para renderizar a Combobox de forma mais moderna
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="white", background="#FBCFE8")

tk.Label(
    janela,
    text="🐾 KITTYFLOW",
    bg="#FFF1F2",
    fg="#DB2777",
    font=("Segoe UI", 26, "bold")
).pack(pady=(15, 5))

# FORM (Reorganizado em Grid alinhado e compacto)
frame_form = tk.Frame(
    janela,
    bg="#FBCFE8",
    padx=20,
    pady=15,
    highlightbackground="#F472B6",
    highlightthickness=1
)
frame_form.pack(
    fill="x",
    padx=30,
    pady=10
)

form_lbl_style = {"bg": "#FBCFE8", "fg": "#4C0519", "font": ("Segoe UI", 10, "bold")}
form_entry_style = {"font": ("Segoe UI", 10), "relief": "solid", "bd": 1}

tk.Label(frame_form, text="Título:", **form_lbl_style).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_titulo = tk.Entry(frame_form, width=25, **form_entry_style)
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Descrição:", **form_lbl_style).grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_descricao = tk.Entry(frame_form, width=35, **form_entry_style)
entry_descricao.grid(row=0, column=3, padx=10, pady=5)

tk.Label(frame_form, text="Prioridade:", **form_lbl_style).grid(row=1, column=0, sticky="w", padx=5, pady=5)
combo_prioridade = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta"], width=22, font=("Segoe UI", 10), state="readonly")
combo_prioridade.current(0)
combo_prioridade.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Responsável:", **form_lbl_style).grid(row=1, column=2, sticky="w", padx=5, pady=5)
entry_responsavel = tk.Entry(frame_form, width=35, **form_entry_style)
entry_responsavel.grid(row=1, column=3, padx=10, pady=5)

tk.Button(
    frame_form,
    text="🐱 Nova Tarefa",
    command=cadastrar_tarefa,
    bg="#EC4899",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).grid(
    row=0,
    column=4,
    rowspan=2,
    padx=20,
    pady=5,
    ipady=5
)

# STATUS & DETALHES (Painel Unificado)
frame_detalhes = tk.Frame(
    janela,
    bg="#FFE4EC",
    padx=20,
    pady=12,
    highlightbackground="#FBCFE8",
    highlightthickness=1
)
frame_detalhes.pack(
    fill="x",
    padx=30,
    pady=10
)

lbl_selecionada = tk.Label(
    frame_detalhes,
    text="😺 Nenhuma tarefa selecionada",
    bg="#FFE4EC",
    fg="#831843",
    font=("Segoe UI", 11, "bold"),
    anchor="w"
)
lbl_selecionada.pack(fill="x")

lbl_detalhes = tk.Label(
    frame_detalhes,
    text="👀 Clique em uma tarefa para ver detalhes",
    bg="#FFE4EC",
    fg="#831843",
    font=("Segoe UI", 10),
    justify="left",
    anchor="w"
)
lbl_detalhes.pack(
    fill="x",
    pady=(4, 0)
)

# KANBAN (Customizado com cabeçalhos limpos sem usar LabelFrame nativo)
frame_kanban = tk.Frame(
    janela,
    bg="#FFF1F2"
)
frame_kanban.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=5
)

def criar_coluna(titulo_texto):
    col_container = tk.Frame(frame_kanban, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1)
    col_container.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    
    lbl_header = tk.Label(col_container, text=titulo_texto, bg="#E2E8F0", fg="#4C0519", font=("Segoe UI", 12, "bold"), pady=8)
    lbl_header.pack(fill="x", side="top")
    
    content_frame = tk.Frame(col_container, bg="#F8FAFC")
    content_frame.pack(fill="both", expand=True, pady=5)
    return content_frame

frame_afazer = criar_coluna("😴 Soneca (A Fazer)")
frame_progresso = criar_coluna("🐈 Caçando (Em Progresso)")
frame_concluido = criar_coluna("🐾 Concluído")

# START
atualizar_kanban()
janela.mainloop()