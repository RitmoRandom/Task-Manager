import json
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style
import os
from utils import validate_date

class TaskManager:
    def __init__(self):
        self.tasks_file = 'tasks.json'
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        description = input("Descripción de la tarea: ")
        priority = input("Prioridad (baja, media, alta): ").lower()
        due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")

        if not validate_date(due_date):
            print(Fore.RED + "Fecha inválida. Intenta de nuevo." + Style.RESET_ALL)
            return
        
        task = {
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(Fore.GREEN + "Tarea agregada exitosamente." + Style.RESET_ALL)

    def view_tasks(self, show_completed=True):
        tasks_to_show = [task for task in self.tasks if not task['completed'] or show_completed]
        if not tasks_to_show:
            print("No hay tareas para mostrar.")
            return

        table = []
        for idx, task in enumerate(tasks_to_show):
            status = "Completada" if task['completed'] else "Pendiente"
            table.append([idx + 1, task['description'], task['priority'], task['due_date'], status])

            # Alerta si la tarea está próxima a vencer
            days_left = (datetime.strptime(task['due_date'], "%Y-%m-%d") - datetime.now()).days
            if days_left <= 2 and not task['completed']:
                print(Fore.YELLOW + f"¡Alerta! La tarea '{task['description']}' está próxima a vencer." + Style.RESET_ALL)

        print(tabulate(table, headers=["#", "Descripción", "Prioridad", "Fecha de Vencimiento", "Estado"]))

    def complete_task(self):
        self.view_tasks(show_completed=False)
        try:
            task_index = int(input("Selecciona el número de la tarea a completar: ")) - 1
            if self.tasks[task_index]['completed']:
                print("La tarea ya está completada.")
            else:
                self.tasks[task_index]['completed'] = True
                self.save_tasks()
                print(Fore.GREEN + "Tarea marcada como completada." + Style.RESET_ALL)
        except (ValueError, IndexError):
            print(Fore.RED + "Número inválido, intenta de nuevo." + Style.RESET_ALL)

    def delete_task(self):
        self.view_tasks(show_completed=True)
        try:
            task_index = int(input("Selecciona el número de la tarea a eliminar: ")) - 1
            del self.tasks[task_index]
            self.save_tasks()
            print(Fore.GREEN + "Tarea eliminada." + Style.RESET_ALL)
        except (ValueError, IndexError):
            print(Fore.RED + "Número inválido, intenta de nuevo." + Style.RESET_ALL)