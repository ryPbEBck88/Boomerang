from django.shortcuts import render, HttpResponse
from random import randint
from .models import RandomNumber


MIN_NUMBER = 1
MAX_NUMBER = 2
DATA = [randint(MIN_NUMBER, MAX_NUMBER) for _ in range(5)]

def random_number(min_number, max_number):
    return randint(min_number, max_number)

def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'testing/index.html', context)


def brackets(request):
    numbers = RandomNumber.objects.all()

    if not numbers.exists():  # Если нет чисел, создаем их
        RandomNumber.generate_numbers()

    # Преобразуем QuerySet в список чисел
    data = [num.number for num in numbers]

    # Вычисление правильного ответа
    correct_answer = (
        (data[0] * 5) +
        (data[1] * 8) +
        (data[2] * 11) +
        (data[3] * 17) +
        (data[4] * 35)
    )

    user_answer = None
    result_icon = None

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer is not None:
            try:
                user_answer = int(answer)
                if user_answer == correct_answer:
                    result_icon = '✅'
                    RandomNumber.generate_numbers()  # Удаляем старые числа и создаем новые

                    # Перезагружаем данные после генерации новых чисел
                    numbers = RandomNumber.objects.all()
                    data = [num.number for num in numbers]
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'

    context = {
        'title': 'Скобки',
        'content': f'''
                    ({data[0]} * 5) +
                    ({data[1]} * 8) +
                    ({data[2]} * 11) +
                    ({data[3]} * 17) +
                    ({data[4]} * 35) =''',
        'data': data,
        'result_icon': result_icon,
        'user_answer': user_answer,
    }
    return render(request, 'testing/brackets.html', context)

def bj(request):
    data = [random_number(MIN_NUMBER, MAX_NUMBER)]
    context = {
        'title': 'Блек Джек',
        'content': f'{data[0]} * 1,5 = '
    }
    return render(request, 'testing/bj.html', context)

def neighbours(request):
    context = {
        'title': 'соседи',
    }