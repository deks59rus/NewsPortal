from django import template
from .read_file import *
import string

register = template.Library()


CENSORED_WORDS = [ "сука", "СУКА", "Сука"]
#CENSORED_WORDS = read_txt_as_list("news\\templatetags\\censored_words.txt", Encoding.UTF8)
def symbol_changer(text):
    d = {'а': ['а', 'a', '@'],
         'б': ['б', '6', 'b'],
         'в': ['в', 'b', 'v'],
         'г': ['г', 'r', 'g'],
         'д': ['д', 'd'],
         'е': ['е', 'e'],
         'ё': ['ё', 'e'],
         'ж': ['ж', 'zh', '*'],
         'з': ['з', '3', 'z'],
         'и': ['и', 'u', 'i'],
         'й': ['й', 'u', 'i'],
         'к': ['к', 'k', 'i{', '|{'],
         'л': ['л', 'l', 'ji'],
         'м': ['м', 'm'],
         'н': ['н', 'h', 'n'],
         'о': ['о', 'o', '0'],
         'п': ['п', 'n', 'p'],
         'р': ['р', 'r', 'p'],
         'с': ['с', 'c', 's'],
         'т': ['т', 'm', 't'],
         'у': ['у', 'y', 'u'],
         'ф': ['ф', 'f'],
         'х': ['х', 'x', 'h', '}{'],
         'ц': ['ц', 'c', 'u,'],
         'ч': ['ч', 'ch'],
         'ш': ['ш', 'sh'],
         'щ': ['щ', 'sch'],
         'ь': ['ь', 'b'],
         'ы': ['ы', 'bi'],
         'ъ': ['ъ'],
         'э': ['э', 'e'],
         'ю': ['ю', 'io'],
         'я': ['я', 'ya']
         }

    for key, value in d.items():
       # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
       for letter in value:
          # Проходимся по каждой букве в нашей фразе.
          for phr in text:
             # Если буква совпадает с буквой в нашем списке.
             if letter == phr:
             # Заменяем эту букву на ключ словаря.
                text = text.replace(phr, key)
                #phrase = phrase.replace(key, "*")
    return text
@register.filter()
def censor(text):
    if (isinstance (text, str)) ==False:
        raise TypeError("Неправильный формат данных для фильтра!")

    phrase = text
    censored_phrase = phrase

    def distance(a, b):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n, m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)  # Keep current and previous row, not entire matrix
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    # Проходимся по всем словам.
    for word in CENSORED_WORDS:
        # Разбиваем слово на части, и проходимся по ним.
        for part in range(len(phrase)):
            # Вот сам наш фрагмент.
            fragment = censored_phrase[part: part + len(word)]
            # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
            # if distance(fragment, word) <= len(word) * 0.1:
            #     censored_phrase = censored_phrase.replace(fragment, "*" * len(fragment))
            if distance(fragment, word) <= len(word) * 0.1:
                censored_phrase = censored_phrase.replace(fragment, "*" * len(fragment))

            # Если они равны, выводим надпись о их нахождении.
            # print("Найдено", word, "\nПохоже на", fragment)
    return censored_phrase
