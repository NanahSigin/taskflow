class Tarefa:
    def __init__(self, id, titulo, descricao, prioridade):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = "A Fazer"

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.status})"