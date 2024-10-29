import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import csv

EVENTS_FILE = "pythonlab6/events.csv"

def read_events():
    events = []
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    name, date_str = row
                    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                    events.append((name, date_obj))
    except FileNotFoundError:
        pass
    return events

def add_event_to_file(name, date_str):
    with open(EVENTS_FILE, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, date_str])

def main_window():
    window = tk.Tk()
    window.title("Календарь событий")

    title = tk.Label(window, text="Календарь событий", font=("Arial", 16))
    title.pack()

    add_button = tk.Button(window, text="Добавить событие", command=add_event_window)
    add_button.pack(pady=10)

    view_button = tk.Button(window, text="Просмотр событий", command=view_events_window)
    view_button.pack(pady=10)

    window.mainloop()

def add_event_window():
    def add_event():
        name = event_name_entry.get().strip()
        date_str = event_date_entry.get().strip()

        try:
            datetime.datetime.strptime(date_str, "%d/%m/%Y")
            add_event_to_file(name, date_str)
            messagebox.showinfo("Успех", "Событие добавлено")
            add_event_win.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте дд/мм/гггг")

    add_event_win = tk.Toplevel()
    add_event_win.title("Добавить событие")

    tk.Label(add_event_win, text="Название события:").pack(pady=5)
    event_name_entry = tk.Entry(add_event_win)
    event_name_entry.pack(pady=5)

    tk.Label(add_event_win, text="Дата события (дд/мм/гггг):").pack(pady=5)
    event_date_entry = tk.Entry(add_event_win)
    event_date_entry.pack(pady=5)

    add_button = tk.Button(add_event_win, text="Добавить", command=add_event)
    add_button.pack(pady=10)

def view_events_window():
    def show_events():
        year = int(year_entry.get().strip())
        month = month_combo.get().strip()

        events = read_events()
        filtered_events = [event for event in events if event[1].year == year and event[1].strftime("%B") == month]
        today = datetime.datetime.today()

        for widget in events_frame.winfo_children():
            widget.destroy()

        if not filtered_events:
            tk.Label(events_frame, text="Событий не найдено").pack()
        else:
            for name, date_obj in filtered_events:
                day_of_week = date_obj.strftime("%A")
                days_diff = (date_obj - today).days
                if days_diff > 0:
                    status = f"Осталось {days_diff} дней"
                elif days_diff < 0:
                    status = f"Прошло {-days_diff} дней"
                else:
                    status = "Сегодня"

                event_info = f"{name} - {date_obj.strftime('%d/%m/%Y')} ({day_of_week}), {status}"
                tk.Label(events_frame, text=event_info).pack()

    view_events_win = tk.Toplevel()
    view_events_win.title("Просмотр событий")

    # Верхняя часть - вывод текущей даты
    today = datetime.datetime.today()
    current_date_label = tk.Label(view_events_win, text=f"Сегодня: {today.strftime('%d/%m/%Y, %A')}", font=("Arial", 12))
    current_date_label.pack(pady=10)

    # Левая часть - ввод года и выбор месяца
    input_frame = tk.Frame(view_events_win)
    input_frame.pack(side=tk.LEFT, padx=10)

    tk.Label(input_frame, text="Введите год:").pack(pady=5)
    year_entry = tk.Entry(input_frame)
    year_entry.pack(pady=5)

    tk.Label(input_frame, text="Выберите месяц:").pack(pady=5)
    month_combo = ttk.Combobox(input_frame, values=[datetime.date(1900, i, 1).strftime('%B') for i in range(1, 13)])
    month_combo.pack(pady=5)

    # Правая часть - вывод событий
    events_frame = tk.Frame(view_events_win)
    events_frame.pack(side=tk.RIGHT, padx=10)

    # Нижняя часть - кнопки
    buttons_frame = tk.Frame(view_events_win)
    buttons_frame.pack(side=tk.BOTTOM, pady=10)

    show_button = tk.Button(buttons_frame, text="Просмотр", command=show_events)
    show_button.pack(side=tk.LEFT, padx=5)

    back_button = tk.Button(buttons_frame, text="Назад", command=view_events_win.destroy)
    back_button.pack(side=tk.RIGHT, padx=5)

if __name__ == "__main__":
    main_window()