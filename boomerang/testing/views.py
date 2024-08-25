from django.shortcuts import render, HttpResponse
from random import randint


MIN_NUMBER = 1
MAX_NUMBER = 2
DATA = None

class CreateRandomNumber():
    def __init__(self):
        self.five = self.random_number(1, 10)
        self.eight = self.random_number(1,10)
        self.eleven = self.random_number(1,10)
        self.seventeen = self.random_number(1,10)
        self.thirty_five = self.random_number(1,10)

    def random_number(self, min_number, max_number):
        return randint(min_number, max_number)
    
    def reset(self, min_number, max_number):
        self.five = self.random_number(min_number, max_number)
        self.eight = self.random_number(min_number, max_number)
        self.eleven = self.random_number(min_number, max_number)
        self.seventeen = self.random_number(min_number, max_number)
        self.thirty_five = self.random_number(min_number, max_number)

def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'testing/index.html', context)


def brackets(request, data=None):
    if data is None:
        data = [randint(MIN_NUMBER, MAX_NUMBER) for _ in range(5)]

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
    content = f'''
                    ({data[0]} * 5) +
                    ({data[1]} * 8) +
                    ({data[2]} * 11) +
                    ({data[3]} * 17) +
                    ({data[4]} * 35) ='''

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer is not None:
            try:
                user_answer = int(answer)
                if user_answer == correct_answer:
                    result_icon = '✅'
                    data = None
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'

    context = {
        'title': 'Скобки',
        'content': content,
        'result_icon': result_icon,
        'user_answer': user_answer,
    }
    return render(request, 'testing/brackets.html', context)

def bj(request):
    random_number = CreateRandomNumber
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
