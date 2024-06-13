from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generic
from typing import List
import csv
import os
from typing import TypeVar, Generic, Optional, List, Tuple

T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self, value: T):
        self.value: T = value
        self.next: Optional[Node[T]] = None
        self.prev: Optional[Node[T]] = None

class ListaDuplamenteLigada(Generic[T]):
    def __init__(self):
        self.head: Optional[Node[T]] = None  # Cabeça da lista
        self.tail: Optional[Node[T]] = None  # Cauda da lista

    def append(self, value: T) -> None:
        """Adiciona um nó ao final da lista."""
        new_node = Node(value)
        if self.tail is None:  # Se a lista está vazia
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def prepend(self, value: T) -> None:
        """Adiciona um nó ao início da lista."""
        new_node = Node(value)
        if self.head is None:  # Se a lista está vazia
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def display(self) -> None:
        """Exibe todos os elementos da lista."""
        current = self.head
        while current:
            print(current.value, end=' <-> ' if current.next else '')
            current = current.next
        print()

    def remove(self, value: T) -> bool:
        """Remove um nó da lista pelo valor."""
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return True  # Nó encontrado e removido
            current = current.next
        return False  # Nó não encontrado

class NodeTree(Generic[T]):
    def __init__(self, item: T) -> None:
        self.key: T = item
        self.left: Optional[NodeTree[T]] = None
        self.right: Optional[NodeTree[T]] = None

class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self.root: Optional[NodeTree[T]] = None

    def insert(self, key: T) -> None:
        self.root = self._insert_rec(self.root, key)

    def _insert_rec(self, root: Optional[NodeTree[T]], key: T) -> NodeTree[T]:
        if root is None:
            return NodeTree(key)
        if key < root.key:
            root.left = self._insert_rec(root.left, key)
        elif key > root.key:
            root.right = self._insert_rec(root.right, key)
        return root

    def search(self, key: T) -> bool | T:
        return self._search_rec(self.root, key)

    def _search_rec(self, root: Optional[NodeTree[T]], key: T) -> bool:
        if root is None:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self._search_rec(root.left, key)
        else:
            return self._search_rec(root.right, key)

    
    def search_and_return(self, key: T) -> T:
        return self._search_and_return_rec(self.root, key)
    
    def _search_and_return_rec(self, root: Optional[NodeTree[T]], key: T) -> T:
        if root is None:
            return None
        if key == root.key:
            return root.key
        elif key < root.key:
            return self._search_and_return_rec(root.left, key)
        else:
            return self._search_and_return_rec(root.right, key)

    def inorder(self) -> None:
        self._inorder_rec(self.root)

    def _inorder_rec(self, root: Optional[NodeTree[T]]) -> None:
        if root:
            self._inorder_rec(root.left)
            print(root.key)
            self._inorder_rec(root.right)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

@dataclass
class Task:
    name: str
    priority: int
    completed: bool = field(default=False, compare=False)
    
    def __lt__(self, other: 'Task') -> bool:
        return self.priority < other.priority
    
    def __gt__(self, other: 'Task') -> bool:
        return self.priority > other.priority
    
    def __eq__(self, other: 'Task') -> bool:
        return self.priority == other.priority
    
    def __str__(self) -> str:
        return f'[{self.priority}] {"(X)" if self.completed else "( )"} {self.name}'

@dataclass
class DayTasks:
    date: str
    tasks: BinaryTree[Task]

class TaskManager:
    def __init__(self):
        self.tasks = ListaDuplamenteLigada[DayTasks]()

    def add_task(self, task: Task, date: str) -> BinaryTree[Task]:
        daytasks = self.get_daytasks(date)
        daytasks.tasks.insert(task)
        return daytasks.tasks

    def get_daytasks(self, date: str) -> DayTasks:
        current = self.tasks.head
        while current:
            if current.value.date == date:
                return current.value
            current = current.next
        daytasks = DayTasks(date=date, tasks=BinaryTree[Task]())
        self.tasks.append(daytasks)
        return daytasks
    
    def show_all_tasks(self) -> None:
        current = self.tasks.head
        while current:
            print(f"Data: {current.value.date}")
            current.value.tasks.inorder()
            current = current.next


def save_daytasks_to_csv(daytasks_list: ListaDuplamenteLigada[DayTasks], filename: str) -> None:
    """Salva uma Lista duplamente encadeada de DayTasks em um arquivo CSV."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['dia', 'name', 'priority', 'completed'])
        
        current = daytasks_list.head
        while current:
            daytasks = current.value
            tasks = []

            def collect_tasks(node: Optional[NodeTree[Task]]) -> None:
                if node is not None:
                    collect_tasks(node.left)
                    tasks.append(node.key)
                    collect_tasks(node.right)

            collect_tasks(daytasks.tasks.root)
            
            for task in tasks:
                writer.writerow([daytasks.date, task.name, task.priority, task.completed])
            
            current = current.next

def load_daytasks_from_csv(filename: str) -> ListaDuplamenteLigada[DayTasks]:
    """Lê um arquivo CSV e recria uma Lista duplamente encadeada de DayTasks."""
    lista_daytasks = ListaDuplamenteLigada[DayTasks]()
    daytasks_dict = {}

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['dia']
            task = Task(name=row['name'], priority=int(row['priority']), completed=row['completed'].lower() == 'true')

            if date not in daytasks_dict:
                daytasks_dict[date] = BinaryTree[Task]()
            daytasks_dict[date].insert(task)

    for date, tasks_tree in daytasks_dict.items():
        daytasks = DayTasks(date=date, tasks=tasks_tree)
        lista_daytasks.append(daytasks)

    return lista_daytasks

def menu_add_task(task_manager: TaskManager) -> Task:
    name = input("Digite o nome da tarefa\n>> ")
    date = input("Digite a data da tarefa (dd/mm/aaaa):\n>> ")
    priority = int(input("Digite a prioridade da tarefa:\n>> "))
    task_manager.add_task(Task(name=name, priority=priority), date)
    input("\n\nPressione Enter para continuar...")

def menu_show_all_tasks(task_manager: TaskManager) -> None:
    limpar_tela()
    print("Tarefas:")
    task_manager.show_all_tasks()
    input("\n\nPressione Enter para continuar...")

def menu_save_tasks(task_manager: TaskManager) -> None:
    save_daytasks_to_csv(task_manager.tasks, 'tasks.csv')
    print("Tarefas salvas com sucesso!")

def menu_mark_task_as_completed(task_manager: TaskManager) -> None:
    print("Qual tarefa deseja marcar como concluída?")
    date = input("Digite a data da tarefa (dd/mm/aaaa):\n>> ")
    daytasks = task_manager.get_daytasks(date)
    daytasks.tasks.inorder()
    task_priority = int(input("Digite a prioridade da tarefa:\n>> "))
    task = daytasks.tasks.search_and_return(Task(name='', priority=task_priority))
    if task:
        task.completed = True
        print("Tarefa marcada como concluída!")
    else:
        print("Tarefa não encontrada.")

def main() -> None:
    task_manager = TaskManager()
    try:
        tasks = load_daytasks_from_csv('tasks.csv')
        task_manager.tasks = tasks
    except csv.Error:
        print("Erro ao carregar tarefas do arquivo CSV. Possivelmente o arquivo está corrompido.")
    except FileNotFoundError:
        pass
    opt_map = {
        '1': lambda: menu_add_task(task_manager),
        '2': lambda: menu_show_all_tasks(task_manager),
        '3': lambda: menu_save_tasks(task_manager),
        '4': lambda: menu_mark_task_as_completed(task_manager),
        '0': lambda: exit(0)
    }

    while True:
        opt = -1
        print("\n\nBem-vindo ao sistema de tarefas!")
        print("1 - Adicionar tarefa")
        print("2 - Exibir tarefas")
        print("3 - Salvar tarefas")
        print("4 - Marcar tarefa como concluída")
        print("0 - Sair")

        while opt not in opt_map:
            opt = input("Digite a opção desejada:\n>> ")
            if(opt not in opt_map):
                print("Opção inválida!")
        
        opt_map[opt]()
        limpar_tela()

if __name__ == '__main__':
    main()