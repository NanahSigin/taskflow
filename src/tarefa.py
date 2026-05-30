class Tarefa:
    def __init__(self, id, titulo, descricao, prioridade, responsavel="Não atribuído"):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.responsavel = responsavel
        self.status = "A Fazer"