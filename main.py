import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3


class Task:
    def __init__(self, subject: str, description: str, due_date: datetime, importance: int):
        self.subject = subject
        self.description = description
        self.due_date = due_date
        self.importance = importance


class Schedule:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.schedule = Schedule()

        self.title('Умный планер')
        self.geometry('500x500')

        self.create_widgets()

        self.create_database()
        self.load_tasks_from_db()



    def create_database(self):
        self.connection= sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, subject TEXT, description TEXT, due_date DATETIME, importance INTEGER)''')
        self.connection.commit()


    def create_widgets(self):
        self.subject_label = tk.Label(self, text="Название предмета")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self)
        self.subject_entry.pack()

        self.description_label = tk.Label(self, text="Описание задания")
        self.description_label.pack()
        self.description_entry = tk.Entry(self)
        self.description_entry.pack()

        self.due_date_label = tk.Label(self, text="Дата выполнения (ГГГГ-ММ-ДД):")
        self.due_date_label.pack()
        self.due_date_entry = tk.Entry(self)
        self.due_date_entry.pack()

        self.importance_label = tk.Label(self, text="Важность 1-3")
        self.importance_label.pack()
        self.importance_entry = tk.Entry(self)
        self.importance_entry.pack()

        self.add_task_button = tk.Button(self, text="Добавить задание", command=self.add_task)
        self.add_task_button.pack()

        self.show_tasks_button = tk.Button(self, text="Показать задания", command=self.show_tasks)
        self.show_tasks_button.pack()

        self.tasks_text = tk.Text(self, state='disabled', height=10)
        self.tasks_text.pack()

    def add_task(self):
        subject = self.subject_entry.get()
        description = self.description_entry.get()
        due_date_str = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            if due_date < datetime.now() or due_date > datetime.now() + timedelta(days=30):
                raise ValueError("Дата должна быть в пределах 1 месяца от сегодняшней даты")

            importance = int(self.importance_entry.get())
            if importance not in [1, 2, 3]:
                raise ValueError("Пожалуйста, введите значение от 1 до 3 (1 - низкая, 2 - средняя, 3 - высокая)")

            task = Task(subject, description, due_date, importance)
            self.schedule.add_task(task)
            self.save_task_to_db(task)

            messagebox.showinfo("Задание добавлено")
            self.clear_entries()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def get_sorted_tasks(self):
        return sorted(self.schedule.tasks, key=lambda x: (-x.importance, x.due_date))

    def save_task_to_db(self, task: Task):
        self.cursor.execute('''INSERT INTO tasks (subject, description, due_date, importance) VALUES (?,?,?,?)''', (task.subject, task.description, task.due_date, task.importance))
        self.connection.commit()

    def load_tasks_from_db(self):
        self.cursor.execute('''SELECT subject, description, due_date, importance FROM tasks''')
        rows = self.cursor.fetchall()
        for row in rows:
            subject = row[0]
            description = row[1]
            due_date = row[2]
            importance = row[3]
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            task = Task(subject, description, due_date, importance)
            self.schedule.tasks.append(task)

    def show_tasks(self):
        self.tasks_text.config(state='normal')
        self.tasks_text.delete(1.0, tk.END)

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        self.tasks_text.insert(tk.END, "Все задания на завтра:\n")
        tasks_for_tomorrow = [task for task in self.get_sorted_tasks() if task.due_date.date() == tomorrow]
        if tasks_for_tomorrow:
            for task in tasks_for_tomorrow:
                self.tasks_text.insert(tk.END,
                                       f"{task.subject}: {task.description}, Дата выполнения: {task.due_date.strftime('%Y-%m-%d')}, Важность: {task.importance}\n")
        else:
            self.tasks_text.insert(tk.END, "Заданий нет\n")

        self.tasks_text.insert(tk.END, "\nВсе задания:\n")
        all_tasks = self.get_sorted_tasks()
        if all_tasks:
            for task in all_tasks:
                self.tasks_text.insert(tk.END,
                                       f"{task.subject}: {task.description}, Дата выполнения: {task.due_date.strftime('%Y-%m-%d')}, Важность: {task.importance}\n")
        else:
            self.tasks_text.insert(tk.END, "Заданий нет\n")

        self.tasks_text.config(state='disabled')

    def clear_entries(self):
        self.subject_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.importance_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def on_closing(self):
        self.connection.close()
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()