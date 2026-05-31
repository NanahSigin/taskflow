#  KittyFlow – Sistema de Gerenciamento de Tarefas

## Sobre o Projeto

O **KittyFlow** é um sistema de gerenciamento de tarefas desenvolvido como atividade prática da disciplina de **Engenharia de Software**.

O objetivo do projeto é auxiliar na organização e acompanhamento de tarefas por meio de uma interface visual inspirada em um quadro **Kanban**, permitindo o gerenciamento do fluxo de trabalho de forma simples e intuitiva.

O sistema foi desenvolvido utilizando **Python**, com interface gráfica feita em **Tkinter**, além de práticas de versionamento, testes automatizados e integração contínua.

---

## Objetivo do Projeto

Desenvolver um sistema funcional para gerenciamento de tarefas baseado em metodologias ágeis, permitindo:

* Criar tarefas;
* Visualizar tarefas organizadas em um quadro Kanban;
* Editar informações das tarefas;
* Excluir tarefas;
* Controlar prioridade;
* Acompanhar o status das atividades.

---

## Escopo Inicial

O escopo inicial do projeto consistia na criação de um sistema simples para gerenciamento de tarefas, contendo funcionalidades básicas de CRUD (**Create, Read, Update e Delete**).

As tarefas deveriam possuir:

* título;
* descrição;
* prioridade;
* status da tarefa.

O foco principal era desenvolver uma aplicação funcional utilizando conceitos de Engenharia de Software e organização ágil.

---

## Funcionalidades

O sistema permite:

Cadastro de tarefas
Visualização de tarefas em estilo Kanban
Alteração de status das tarefas
Edição de tarefas
Exclusão de tarefas
Definição de prioridade
Associação de responsável à tarefa
Interface gráfica amigável com Tkinter

---

## Tecnologias Utilizadas

* **Python**
* **Tkinter**
* **Pytest**
* **Git**
* **GitHub**
* **GitHub Actions**
* **GitHub Projects (Kanban)**
* **Pinterest**

---

## Estrutura do Projeto

```txt
taskflow/
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── src/
│   ├── main.py
│   ├── gerenciador.py
│   ├── tarefa.py
│   └── tests/
│       ├── test_gerenciador.py
│       └── test_tarefa.py
│
├── README.md
```

---

## Metodologia Ágil Utilizada

Foi utilizada a metodologia **Kanban** para organização das atividades do projeto.

As tarefas foram organizadas no **GitHub Projects**, utilizando colunas como:

* **To Do (A Fazer)**
* **In Progress (Em Progresso)**
* **Done (Concluído)**

Essa organização permitiu acompanhar o andamento do desenvolvimento e controlar as atividades realizadas ao longo do projeto.

---

## Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entre na pasta do projeto

```bash
cd taskflow
```

### 3. Execute o sistema

```bash
python src/main.py
```

---

## Testes Automatizados

O projeto utiliza **Pytest** para realização de testes automatizados.

Para executar os testes:

```bash
python -m pytest
```

Atualmente o projeto possui testes unitários para validação das funcionalidades do sistema.

---

## Integração Contínua (CI)

Foi configurado um pipeline utilizando **GitHub Actions** para execução automática dos testes.

A cada atualização no repositório (**push**), os testes são executados automaticamente para garantir o correto funcionamento do sistema.

---

## Mudança de Escopo

Durante o desenvolvimento do projeto, foi simulada uma alteração de escopo.

Inicialmente, o sistema realizava apenas o cadastro e gerenciamento básico das tarefas.

Posteriormente, foi adicionada a funcionalidade de **responsável da tarefa**, permitindo associar uma pessoa responsável a cada atividade cadastrada.

Essa mudança exigiu:

* atualização do código;
* atualização dos testes automatizados;
* reorganização das tarefas no quadro Kanban;
* atualização da documentação do projeto.

---

## Autora

Ana Paula Machado Silva - Engenharia da Computação
