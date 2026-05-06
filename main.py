import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        
        # Файл для сохранения истории
        self.history_file = "tasks_history.json"
        
        # Предопределённые задачи
        self.default_tasks = [
            {"name": "Прочитать статью", "type": "учеба"},
            {"name": "Сделать зарядку", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Выучить 10 новых слов", "type": "учеба"},
            {"name": "Пробежка 2 км", "type": "спорт"},
            {"name": "Позвонить клиенту", "type": "работа"},
            {"name": "Решить 5 задач", "type": "учеба"},
            {"name": "Отжимания 30 раз", "type": "спорт"},
            {"name": "Проверить почту", "type": "работа"},
            {"name": "Прочитать главу книги", "type": "учеба"},
            {"name": "Приседания 50 раз", "type": "спорт"},
            {"name": "Сделать презентацию", "type": "работа"}
        ]
        
        # Загрузка истории
        self.history = self.load_history()
        
        # Переменные
        self.filter_type = tk.StringVar(value="все")
        
        self.create_widgets()
        self.update_history_display()
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохранение истории в JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def create_widgets(self):
        # Рамка для генерации
        gen_frame = ttk.LabelFrame(self.root, text="Генератор задач", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)
        
        self.generate_btn = ttk.Button(gen_frame, text="🎲 Сгенерировать задачу", 
                                        command=self.generate_task)
        self.generate_btn.pack(pady=10)
        
        self.current_task_var = tk.StringVar(value="Нажмите кнопку")
        self.current_label = tk.Label(gen_frame, textvariable=self.current_task_var, 
                                       font=("Arial", 12, "bold"), fg="blue", wraplength=550)
        self.current_label.pack(pady=10)
        
        # Рамка для добавления задач
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(add_frame, text="Название задачи:").pack(anchor="w")
        self.new_task_entry = ttk.Entry(add_frame, width=50)
        self.new_task_entry.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="Тип задачи:").pack(anchor="w")
        self.type_combo = ttk.Combobox(add_frame, values=["учеба", "спорт", "работа"], 
                                        state="readonly")
        self.type_combo.set("учеба")
        self.type_combo.pack(fill="x", pady=5)
        
        ttk.Button(add_frame, text="➕ Добавить задачу", command=self.add_task).pack(pady=5)
        
        # Рамка для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация по типу", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        filter_buttons = ttk.Frame(filter_frame)
        filter_buttons.pack()
        
        ttk.Radiobutton(filter_buttons, text="📋 Все", variable=self.filter_type, 
                        value="все", command=self.filter_history).pack(side="left", padx=10)
        ttk.Radiobutton(filter_buttons, text="📚 Учеба", variable=self.filter_type, 
                        value="учеба", command=self.filter_history).pack(side="left", padx=10)
        ttk.Radiobutton(filter_buttons, text="🏃 Спорт", variable=self.filter_type, 
                        value="спорт", command=self.filter_history).pack(side="left", padx=10)
        ttk.Radiobutton(filter_buttons, text="💼 Работа", variable=self.filter_type, 
                        value="работа", command=self.filter_history).pack(side="left", padx=10)
        
        # Рамка для истории
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, 
                                          font=("Courier", 10), height=12)
        self.history_listbox.pack(fill="both", expand=True, padx=5)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопки управления
        btn_frame = ttk.Frame(history_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="📋 Копировать задачу", 
                  command=self.copy_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Очистить историю", 
                  command=self.clear_history).pack(side="left", padx=5)
    
    def generate_task(self):
        """Генерация случайной задачи"""
        all_tasks = self.default_tasks.copy()
        
        # Добавляем пользовательские задачи из истории
        existing_names = {(t["name"], t["type"]) for t in all_tasks}
        for item in self.history:
            key = (item["name"], item["type"])
            if key not in existing_names:
                all_tasks.append({"name": item["name"], "type": item["type"]})
                existing_names.add(key)
        
        if not all_tasks:
            messagebox.showwarning("Ошибка", "Нет доступных задач!")
            return
        
        selected = random.choice(all_tasks)
        
        # Отображаем
        type_emoji = {"учеба": "📚", "спорт": "🏃", "работа": "💼"}
        emoji = type_emoji.get(selected["type"], "📌")
        self.current_task_var.set(f"{emoji} {selected['name']} (Тип: {selected['type']})")
        
        # Сохраняем в историю
        self.add_to_history(selected["name"], selected["type"])
    
    def add_to_history(self, task_name, task_type):
        """Добавление в историю"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.insert(0, {
            "name": task_name,
            "type": task_type,
            "time": timestamp
        })
        
        # Оставляем последние 100 записей
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        self.save_history()
        self.filter_history()
    
    def add_task(self):
        """Добавление новой задачи (с валидацией)"""
        task_name = self.new_task_entry.get().strip()
        task_type = self.type_combo.get()
        
        # ВАЛИДАЦИЯ: проверяем на пустую строку
        if not task_name:
            messagebox.showwarning("Ошибка", "Название задачи не может быть пустым!")
            return
        
        # Проверяем, нет ли уже такой задачи в default_tasks
        for task in self.default_tasks:
            if task["name"].lower() == task_name.lower() and task["type"] == task_type:
                messagebox.showwarning("Ошибка", "Такая задача уже существует!")
                return
        
        # Добавляем
        self.default_tasks.append({"name": task_name, "type": task_type})
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{task_name}' добавлена!")
    
    def filter_history(self):
        """Фильтрация истории по типу"""
        self.history_listbox.delete(0, tk.END)
        
        filter_value = self.filter_type.get()
        
        for item in self.history:
            if filter_value == "все" or item["type"] == filter_value:
                type_emoji = {"учеба": "📚", "спорт": "🏃", "работа": "💼"}
                emoji = type_emoji.get(item["type"], "📌")
                display = f"{item['time']} {emoji} [{item['type']}] {item['name']}"
                self.history_listbox.insert(tk.END, display)
    
    def update_history_display(self):
        """Обновление списка истории"""
        self.filter_history()
    
    def copy_selected(self):
        """Копирование выбранной задачи"""
        selection = self.history_listbox.curselection()
        if selection:
            text = self.history_listbox.get(selection[0])
            # Извлекаем название задачи
            parts = text.split("] ", 1)
            if len(parts) > 1:
                task_name = parts[1]
            else:
                task_name = text
            self.root.clipboard_clear()
            self.root.clipboard_append(task_name)
            messagebox.showinfo("Успех", "Задача скопирована!")
        else:
            messagebox.showwarning("Ошибка", "Выберите задачу из истории")
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.save_history()
            self.filter_history()
            messagebox.showinfo("Успех", "История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
