from task_manager import TaskManager

def main():
    manager = TaskManager()
    while True:
        print("\n1. Agregar tarea\n2. Ver todas las tareas\n3. Ver tareas pendientes\n4. Marcar tarea como completada\n5. Eliminar tarea\n6. Salir")
        option = input("Selecciona una opción: ")

        if option == '1':
            manager.add_task()
        elif option == '2':
            manager.view_tasks(show_completed=True)
        elif option == '3':
            manager.view_tasks(show_completed=False)
        elif option == '4':
            manager.complete_task()
        elif option == '5':
            manager.delete_task()
        elif option == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()