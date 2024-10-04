import tkinter as tk
import random

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тест по математике")
        
        self.questions = self.generate_questions()
        self.entries = []  # Список для полей ввода
        self.labels = []   # Список для с вопросами
        
        self.create_widgets()
    
    def generate_questions(self):
        questions = []
        for _ in range(5):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(['+', '*'])
            question = f"{num1} {operation} {num2}"
            answer = eval(question)  # Вычисляем правильный ответ
            questions.append((question, answer))
        return questions
    
    def create_widgets(self):
        for i, (question, _) in enumerate(self.questions):
            label = tk.Label(self.root, text=f"{question} = ")
            label.grid(row=i, column=0, padx=10, pady=5)
            self.labels.append(label)
            
            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)
        
        check_btn = tk.Button(self.root, text="Проверка", command=self.check_answers)
        check_btn.grid(row=5, column=0, columnspan=2, pady=10)
    
    def check_answers(self):
        correct_count = 0
        for i, (_, correct_answer) in enumerate(self.questions):
            user_answer = self.entries[i].get()
            
            if user_answer.isdigit() and int(user_answer) == correct_answer:
                self.entries[i].config(bg="green")  # Если правильно, выделяем зеленым
                correct_count += 1
            else:
                self.entries[i].config(bg="red")  # Если неправильно, выделяем красным
        
        result_label = tk.Label(self.root, text=f"Правильных ответов: {correct_count}/5")
        result_label.grid(row=6, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()