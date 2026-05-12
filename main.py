import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime


class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("850x600")

        self.records = []

        # ===== Поля ввода =====
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Температура:").grid(row=1, column=0)
        self.temp_entry = tk.Entry(input_frame)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=2, column=1)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(
            input_frame,
            text="Осадки",
            variable=self.precip_var
        ).grid(row=3, column=1)

        tk.Button(
            input_frame,
            text="Добавить запись",
            command=self.add_record
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # ===== Фильтрация =====
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1)

        tk.Button(
            filter_frame,
            text="Применить",
            command=self.filter_by_date
        ).grid(row=0, column=2)

        tk.Label(filter_frame, text="Температура выше:").grid(row=1, column=0)
        self.filter_temp_entry = tk.Entry(filter_frame)
        self.filter_temp_entry.grid(row=1, column=1)

        tk.Button(
            filter_frame,
            text="Применить",
            command=self.filter_by_temperature
        ).grid(row=1, column=2)

        tk.Button(
            filter_frame,
            text="Показать все",
            command=self.show_all
        ).grid(row=2, column=0, columnspan=3, pady=5)

        # ===== Таблица =====
        self.tree = ttk.Treeview(
            root,
            columns=("Дата", "Температура", "Описание", "Осадки"),
            show="headings"
        )

        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура", text="Температура")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== Кнопки JSON =====
        json_frame = tk.Frame(root)
        json_frame.pack(pady=10)

        tk.Button(
            json_frame,
            text="Сохранить JSON",
            command=self.save_json
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            json_frame,
            text="Загрузить JSON",
            command=self.load_json
        ).grid(row=0, column=1, padx=10)

    # ===== Проверка даты =====
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ===== Добавление записи =====
    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = "Да" if self.precip_var.get() else "Нет"

        # Проверка даты
        if not self.validate_date(date):
            messagebox.showerror(
                "Ошибка",
                "Дата должна быть в формате YYYY-MM-DD"
            )
            return

        # Проверка температуры
        try:
            temp = float(temp)
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Температура должна быть числом"
            )
            return

        # Проверка описания
        if desc.strip() == "":
            messagebox.showerror(
                "Ошибка",
                "Описание не должно быть пустым"
            )
            return

        record = {
            "date": date,
            "temperature": temp,
            "description": desc,
            "precipitation": precip
        }

        self.records.append(record)

        self.tree.insert(
            "",
            tk.END,
            values=(date, temp, desc, precip)
        )

        self.clear_inputs()

    # ===== Очистка полей =====
    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    # ===== Обновление таблицы =====
    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    record["date"],
                    record["temperature"],
                    record["description"],
                    record["precipitation"]
                )
            )

    # ===== Фильтр по дате =====
    def filter_by_date(self):
        date = self.filter_date_entry.get()

        filtered = [
            r for r in self.records
            if r["date"] == date
        ]

        self.update_table(filtered)

    # ===== Фильтр по температуре =====
    def filter_by_temperature(self):
        try:
            min_temp = float(self.filter_temp_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Введите число"
            )
            return

        filtered = [
            r for r in self.records
            if r["temperature"] > min_temp
        ]

        self.update_table(filtered)

    # ===== Показать все =====
    def show_all(self):
        self.update_table(self.records)
    

    # ===== Сохранение JSON =====
    def save_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.records,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            messagebox.showinfo(
                "Успех",
                "Данные сохранены"
            )

    # ===== Загрузка JSON =====
    def load_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.records = json.load(file)

            self.update_table(self.records)

            messagebox.showinfo(
                "Успех",
                "Данные загружены"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()