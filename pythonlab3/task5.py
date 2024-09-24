rus_file = 'pythonlab3\\russian_words.txt'
eng_file = 'pythonlab3\\english_words.txt'


with open(rus_file, 'r', encoding='utf-8') as rf, open(eng_file, 'r', encoding='utf-8') as ef:
    russian_words = rf.readlines()
    english_words = ef.readlines()


if len(russian_words) != len(english_words):
    raise ValueError("Количество строк в обоих файлах должно совпадать.")


word_pairs = list(zip(map(str.strip, russian_words), map(str.strip, english_words)))


correct_answers = 0
total_questions = len(word_pairs)

def conduct_test():
    global correct_answers
    for russian_word, english_word in word_pairs:
        print(f"Переведите на английский: {russian_word}")
        user_translation = input("Ваш перевод: ").strip().lower()

        if user_translation == english_word.lower():
            print("Верно!")
            correct_answers += 1
        else:
            print(f"Неверно. Правильный ответ: {english_word}")


conduct_test()

score = correct_answers / total_questions * 100

# Оценивание
if score >= 90:
    grade = "Отлично"
elif score >= 75:
    grade = "Хорошо"
elif score >= 50:
    grade = "Удовлетворительно"
else:
    grade = "Неудовлетворительно"

print(f"\nТест завершен. Вы ответили правильно на {correct_answers} из {total_questions} вопросов.")
print(f"Оценка: {grade} ({score:.2f}%)")