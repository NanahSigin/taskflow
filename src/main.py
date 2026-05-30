import tkinter as tk
from tkinter import ttk, messagebox
from gerenciador import Gerenciador

gerenciador = Gerenciador()

tarefa_selecionada = None


def cor_prioridade(prioridade):

    if prioridade == "Alta":
        return "#DC2626"

    elif prioridade == "Média":
        return "#EAB308"

    return "#16A34A"


def selecionar_tarefa(id_tarefa):

    global tarefa_selecionada

    tarefa_selecionada = id_tarefa

    lbl_selecionada.config(
        text=f"Tarefa selecionada: #{id_tarefa}"
    )


def atualizar_kanban():

    for frame in [
        frame_afazer,
        frame_progresso,
        frame_concluido
    ]:

        for widget in frame.winfo_children():
            widget.destroy()

    for tarefa in gerenciador.listar_tarefas():

        card = tk.Frame(
            bg=cor_prioridade(
                tarefa.prioridade
            ),
            padx=10,
            pady=10,
            cursor="hand2"
        )

        titulo = tk.Label(
            card,
            text=tarefa.titulo,
            bg=card["bg"],
            fg="white",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        titulo.pack(anchor="w")

        descricao = tk.Label(
            card,
            text=tarefa.descricao,
            bg=card["bg"],
            fg="white",
            wraplength=220,
            justify="left"
        )

        descricao.pack(anchor="w")

        prioridade = tk.Label(
            card,
            text=f"Prioridade: {tarefa.prioridade}",
            bg=card["bg"],
            fg="white"
        )

        prioridade.pack(anchor="w")

        for widget in [
            card,
            titulo,
            descricao,
            prioridade
        ]:

            widget.bind(
                "<Button-1>",
                lambda e,
                id=tarefa.id:
                selecionar_tarefa(id)
            )

        if tarefa.status == "A Fazer":

            card.pack(
                fill="x",
                pady=5
            )

            card.pack(
                in_=frame_afazer
            )

        elif tarefa.status == "Em Progresso":

            card.pack(
                fill="x",
                pady=5
            )

            card.pack(
                in_=frame_progresso
            )

        else:

            card.pack(
                fill="x",
                pady=5
            )

            card.pack(
                in_=frame_concluido
            )


def cadastrar_tarefa():

    titulo = entry_titulo.get()
    descricao = entry_descricao.get()
    prioridade = combo_prioridade.get()

    if not titulo:

        messagebox.showwarning(
            "Aviso",
            "Digite um título."
        )

        return

    gerenciador.criar_tarefa(
        titulo,
        descricao,
        prioridade
    )

    entry_titulo.delete(
        0,
        tk.END
    )

    entry_descricao.delete(
        0,
        tk.END
    )

    atualizar_kanban()


def avancar_status():

    global tarefa_selecionada

    if not tarefa_selecionada:
        return

    tarefa = gerenciador.buscar_tarefa(
        tarefa_selecionada
    )

    if tarefa:

        if tarefa.status == "A Fazer":

            tarefa.status = "Em Progresso"

        elif tarefa.status == "Em Progresso":

            tarefa.status = "Concluído"

        else:

            tarefa.status = "A Fazer"

    atualizar_kanban()


def excluir_tarefa():

    global tarefa_selecionada

    if not tarefa_selecionada:
        return

    gerenciador.excluir_tarefa(
        tarefa_selecionada
    )

    tarefa_selecionada = None

    lbl_selecionada.config(
        text="Nenhuma tarefa selecionada"
    )

    atualizar_kanban()


# JANELA

janela = tk.Tk()
janela.title("TaskFlow Kanban")
janela.geometry("1200x700")
janela.configure(bg="#0F172A")

titulo = tk.Label(
    janela,
    text="🚀 TASKFLOW",
    bg="#0F172A",
    fg="white",
    font=(
        "Segoe UI",
        24,
        "bold"
    )
)

titulo.pack(
    pady=(15, 5)
)

subtitulo = tk.Label(
    janela,
    text="Gerenciador Ágil de Tarefas",
    bg="#0F172A",
    fg="#94A3B8"
)

subtitulo.pack()

frame_form = tk.Frame(
    janela,
    bg="#1E293B",
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
    bg="#1E293B",
    fg="white"
).grid(
    row=0,
    column=0
)

entry_titulo = tk.Entry(
    frame_form,
    width=35
)

entry_titulo.grid(
    row=0,
    column=1,
    padx=10
)

tk.Label(
    frame_form,
    text="Descrição",
    bg="#1E293B",
    fg="white"
).grid(
    row=1,
    column=0
)

entry_descricao = tk.Entry(
    frame_form,
    width=35
)

entry_descricao.grid(
    row=1,
    column=1,
    padx=10
)

tk.Label(
    frame_form,
    text="Prioridade",
    bg="#1E293B",
    fg="white"
).grid(
    row=2,
    column=0
)

combo_prioridade = ttk.Combobox(
    frame_form,
    values=[
        "Baixa",
        "Média",
        "Alta"
    ]
)

combo_prioridade.current(0)

combo_prioridade.grid(
    row=2,
    column=1,
    padx=10
)

btn_cadastrar = tk.Button(
    frame_form,
    text="➕ Nova Tarefa",
    command=cadastrar_tarefa,
    bg="#2563EB",
    fg="white"
)

btn_cadastrar.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)

lbl_selecionada = tk.Label(
    janela,
    text="Nenhuma tarefa selecionada",
    bg="#0F172A",
    fg="white"
)

lbl_selecionada.pack()

frame_kanban = tk.Frame(
    janela,
    bg="#0F172A"
)

frame_kanban.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

frame_afazer = tk.LabelFrame(
    frame_kanban,
    text="📋 A Fazer",
    bg="#1E293B",
    fg="white"
)

frame_afazer.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

frame_progresso = tk.LabelFrame(
    frame_kanban,
    text="⚙️ Em Progresso",
    bg="#1E293B",
    fg="white"
)

frame_progresso.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

frame_concluido = tk.LabelFrame(
    frame_kanban,
    text="✅ Concluído",
    bg="#1E293B",
    fg="white"
)

frame_concluido.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

frame_botoes = tk.Frame(
    janela,
    bg="#0F172A"
)

frame_botoes.pack(
    pady=10
)

tk.Button(
    frame_botoes,
    text="🔄 Avançar Status",
    command=avancar_status,
    bg="#22C55E",
    fg="white"
).pack(
    side="left",
    padx=10
)

tk.Button(
    frame_botoes,
    text="🗑 Excluir",
    command=excluir_tarefa,
    bg="#DC2626",
    fg="white"
).pack(
    side="left",
    padx=10
)

janela.mainloop()