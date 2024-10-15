import json
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from datetime import datetime

# Klass som representerar en uppgift
class Task:
    def __init__(self, title, due_date, project):
        self.title = title
        self.due_date = due_date  # Förväntad i formatet 'ÅÅÅÅ-MM-DD'
        self.project = project if project else "Inget projekt"  # Default project name if empty
        self.done = False  # Status för att markera om uppgiften är klar

    # Metod för att markera uppgiften som klar
    def mark_done(self):
        self.done = True

    # Metod för att konvertera uppgiften till en ordbok
    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "project": self.project,
            "done": self.done
        }

    # Statisk metod för att skapa en uppgift från en ordbok
    @staticmethod
    def from_dict(data):
        task = Task(data['title'], data['due_date'], data['project'])
        task.done = data['done']
        return task

# Klass som hanterar uppgifter
class TaskManager:
    def __init__(self):
        self.tasks = []  # Lista för att lagra uppgifter
        self.load_tasks()  # Ladda uppgifter från fil

    # Metod för att lägga till en ny uppgift
    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()  # Spara ändringar efter att ha lagt till en ny uppgift

    # Metod för att ta bort en uppgift baserat på index
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()  # Spara ändringar efter att ha tagit bort en uppgift

    # Metod för att redigera en uppgift
    def edit_task(self, index, new_title, new_due_date, new_project):
        if 0 <= index < len(self.tasks):
            self.tasks[index].title = new_title
            self.tasks[index].due_date = new_due_date
            self.tasks[index].project = new_project if new_project else "Inget projekt"
            self.save_tasks()  # Spara ändringar efter att ha redigerat en uppgift

    # Metod för att markera en uppgift som klar
    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
            self.save_tasks()  # Spara ändringar efter att ha markerat en uppgift som klar

    # Metod för att spara uppgifter till en JSON-fil
    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    # Metod för att ladda uppgifter från en JSON-fil
    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                task_data = json.load(file)
                self.tasks = [Task.from_dict(data) for data in task_data]
        except FileNotFoundError:
            self.tasks = []  # Ingen fil hittades, skapa en tom lista

# Klass som representerar GUI för att hantera uppgifter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Att-Göra-Lista-Special")
        self.task_manager = TaskManager()

        # Skapa en textruta för att visa uppgifter
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(pady=10)

        # Skapa knappar för olika funktioner
        self.add_button = tk.Button(root, text="Lägg till uppgift", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Redigera uppgift", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.mark_done_button = tk.Button(root, text="Markera som klar", command=self.mark_done)
        self.mark_done_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Ta bort uppgift", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.help_button = tk.Button(root, text="?", command=self.show_help)
        self.help_button.pack(pady=5)

        self.load_tasks()

    # Metod för att ladda uppgifter och visa dem i textrutan med nummer
    def load_tasks(self):
        self.text_area.delete(1.0, tk.END)  # Rensa textrutan
        for index, task in enumerate(self.task_manager.tasks, start=1):
            status = "✔" if task.done else "✘"
            self.text_area.insert(tk.END, f"{index}. [{status}] {task.title} (Förfallodatum: {task.due_date}, Projekt: {task.project})\n")

    # Metod för att validera att förfallodatum är i korrekt format (ÅÅÅÅ-MM-DD)
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # Metod för att lägga till en uppgift
    def add_task(self):
        title = simpledialog.askstring("Uppgiftstitel", "Ange uppgiftens titel:")
        due_date = simpledialog.askstring("Förfallodatum", "Ange förfallodatum (ÅÅÅÅ-MM-DD):")
        if due_date and not self.validate_date(due_date):
            messagebox.showerror("Fel", "Ogiltigt datumformat. Ange datum i formatet ÅÅÅÅ-MM-DD.")
            return
        project = simpledialog.askstring("Projektnamn", "Ange projektnamn:")
        if title:
            self.task_manager.add_task(Task(title, due_date if due_date else "Inget datum", project))
            self.load_tasks()  # Ladda uppgifter efter att ha lagt till

    # Metod för att redigera en uppgift
    def edit_task(self):
        index = simpledialog.askinteger("Redigera uppgift", "Ange uppgiftsnummer för att redigera:") - 1
        if 0 <= index < len(self.task_manager.tasks):
            title = simpledialog.askstring("Ny uppgiftstitel", "Ange ny titel:")
            due_date = simpledialog.askstring("Nytt förfallodatum", "Ange nytt förfallodatum (ÅÅÅÅ-MM-DD):")
            if due_date and not self.validate_date(due_date):
                messagebox.showerror("Fel", "Ogiltigt datumformat. Ange datum i formatet ÅÅÅÅ-MM-DD.")
                return
            project = simpledialog.askstring("Nytt projektnamn", "Ange nytt projektnamn:")
            if title:
                self.task_manager.edit_task(index, title, due_date if due_date else "Inget datum", project)
                self.load_tasks()  # Ladda uppgifter efter att ha redigerat
        else:
            messagebox.showerror("Fel", "Ogiltigt uppgiftsnummer.")

    # Metod för att markera en uppgift som klar
    def mark_done(self):
        index = simpledialog.askinteger("Markera som klar", "Ange uppgiftsnummer att markera som klar:") - 1
        if 0 <= index < len(self.task_manager.tasks):
            self.task_manager.mark_task_done(index)
            self.load_tasks()  # Ladda uppgifter efter att ha markerat som klar
        else:
            messagebox.showerror("Fel", "Ogiltigt uppgiftsnummer.")

    # Metod för att ta bort en uppgift
    def remove_task(self):
        index = simpledialog.askinteger("Ta bort uppgift", "Ange uppgiftsnummer för att ta bort:") - 1
        if 0 <= index < len(self.task_manager.tasks):
            self.task_manager.remove_task(index)
            self.load_tasks()  # Ladda uppgifter efter att ha tagit bort
        else:
            messagebox.showerror("Fel", "Ogiltigt uppgiftsnummer.")

    # Metod för att visa hjälpinformation
    def show_help(self):
        help_text = (
            "Instruktioner för Att-Göra-Lista-Special:\n\n"
            "1. Lägg till uppgift: Klicka på 'Lägg till uppgift' och fyll i informationen.\n"
            "2. Redigera uppgift: Välj ett uppgiftsnummer och klicka på 'Redigera uppgift' för att ändra det.\n"
            "3. Markera som klar: Välj ett uppgiftsnummer och klicka på 'Markera som klar' för att markera det som klart.\n"
            "4. Ta bort uppgift: Välj ett uppgiftsnummer och klicka på 'Ta bort uppgift' för att ta bort det.\n"
            "5. Använd '?' för att visa denna hjälp.\n"
            "6. Förfallodatum bör vara i formatet 'ÅÅÅÅ-MM-DD'.\n\n"
            "Använd programmet för att hantera dina uppgifter!"
        )
        messagebox.showinfo("Hjälp", help_text)

# Huvudprogrammet
if __name__ == "__main__":
    root = tk.Tk()  # Skapa huvudfönstret
    app = App(root)  # Skapa en instans av App
    root.mainloop()  # Starta GUI-händelseloopen
