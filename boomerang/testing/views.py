from decimal import Decimal as D
from django.shortcuts import render # , HttpResponse
from .models import (
    BracketsRandomNumber,
    NeighboursRandomNumber,
    BjRandomNumber,
    VoisinsDeZero,
    Tier,
    ZeroSpiel,
    Orphelins
)


# MIN_NUMBER = 1
# MAX_NUMBER = 2
# DATA = None
def calculate_the_answer(bet, series, max_bet_number=100):
    match series:
        case 'voisins':
            threshold = int(D(max_bet_number) * D(13.5))
            if bet > threshold:
                bet -= threshold
                return [threshold // 9 + bet // 7, bet % 7]
            else:
                return [bet // 9, bet % 9]
        case 'tier':
            return [bet // 6, bet % 6]
        case 'orphelins':
            threshold = max_bet_number * 5
            if bet > threshold:
                bet -= threshold
                return [threshold // 5 + bet // 4, bet % 4]
            else:
                return [bet // 5, bet % 5]
        case 'zero_spiel':
            threshold = max_bet_number * 4
            if bet  >threshold:
                bet -= threshold
                return [threshold // 4 + bet // 3, bet % 3]
            else:
                return [bet // 4, bet % 4]


def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'testing/index.html', context)


def brackets(request):
    numbers = BracketsRandomNumber.objects.all()

    if not numbers.exists():  # Если нет чисел, создаем их
        BracketsRandomNumber.generate_numbers(min_value=1, max_value=10)
        numbers = BracketsRandomNumber.objects.all()

    user_answer = None
    result_icon = None

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

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer is not None:
            try:
                user_answer = int(answer)
                if user_answer == correct_answer:
                    result_icon = '✅'
                    BracketsRandomNumber.generate_numbers()
                    numbers = BracketsRandomNumber.objects.all()
                    data = [num.number for num in numbers]
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'

    content = f'''
        ({data[0]} * 5) +
        ({data[1]} * 8) +
        ({data[2]} * 11) +
        ({data[3]} * 17) +
        ({data[4]} * 35) ='''

    context = {
        'title': 'Скобки',
        'content': content,
        'result_icon': result_icon,
        'user_answer': user_answer,
        'correct_answer': correct_answer,
    }
    return render(request, 'testing/brackets.html', context)

def bj(request):
    numbers = BjRandomNumber.objects.all()

    if not numbers.exists():  # Если нет чисел, создаем их
        BjRandomNumber.generate_numbers(min_value=1, max_value=100)
        numbers = BjRandomNumber.objects.all()

    user_answer = None
    result_icon = None

    # Преобразуем QuerySet в список чисел
    data = [num.number for num in numbers]
    correct_answer = D(data[0]) * D(1.5)

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer is not None:
            try:
                user_answer = D(answer)
                if user_answer == correct_answer:
                    result_icon = '✅'
                    BjRandomNumber.generate_numbers()
                    numbers = BjRandomNumber.objects.all()
                    data = [num.number for num in numbers]
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'


    context = {
        'title': 'Блек Джек',
        'content': f'{data[0]} * 1,5 = ',
        'result_icon': result_icon,
    }
    return render(request, 'testing/bj.html', context)

def neighbours(request):
    ROULETTE_WHEEL = (0,
                      32, 15, 19, 4,  21, 2,
                      25, 17, 34, 6,  27, 13,
                      36, 11, 30, 8,  23, 10,
                      5,  24, 16, 33, 1,  20,
                      14, 31, 9,  22, 18, 29,
                      7,  28, 12, 35, 3,  26)
    
    numbers = NeighboursRandomNumber.objects.all()

    if not numbers.exists():  # Если нет чисел, создаем их
        NeighboursRandomNumber.generate_numbers(min_value=0, max_value=36)
        numbers = NeighboursRandomNumber.objects.all()

    index_cell = [num.number for num in numbers][0]
    roulette_number = ROULETTE_WHEEL[index_cell]

    correct_answer = [        
        ROULETTE_WHEEL[index_cell-2],
        ROULETTE_WHEEL[index_cell-1],        
        ROULETTE_WHEEL[index_cell],
        ROULETTE_WHEEL[(index_cell+1) % 37],        
        ROULETTE_WHEEL[(index_cell+2) % 37]
    ]
    user_answer = None
    result_icon = None

    if request.method == 'POST':
        answer = [
            request.POST.get('far_left_answer'),
            request.POST.get('near_left_answer'),
            roulette_number,
            request.POST.get('near_right_answer'),
            request.POST.get('far_right_answer')
        ]

        if not None in answer:
            try:
                user_answer = [int(ans) for ans in answer]
                if user_answer == correct_answer:
                    result_icon = '✅'
                    NeighboursRandomNumber.generate_numbers(min_value=0, max_value=36)  # Удаляем старые числа и создаем новые

                    # Перезагружаем данные после генерации новых чисел
                    numbers = NeighboursRandomNumber.objects.all()
                    index_cell = [num.number for num in numbers][0]
                    roulette_number = ROULETTE_WHEEL[index_cell]
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'
    context = {
        'title': 'соседи',
        'content': roulette_number,
        'result_icon': result_icon,
    }
    return render(request, 'testing/neighbours.html', context)

def series(request):
    voisins_de_zero = VoisinsDeZero.objects.all()
    tier  = Tier.objects.all()
    orphelins = Orphelins.objects.all()
    zero_spiel = ZeroSpiel.objects.all()

    if not voisins_de_zero.exists():
        VoisinsDeZero.generate_numbers()
        Tier.generate_numbers()
        Orphelins.generate_numbers()
        ZeroSpiel.generate_numbers()
        voisins_de_zero = VoisinsDeZero.objects.all()
        tier  = Tier.objects.all()
        orphelins = Orphelins.objects.all()
        zero_spiel = ZeroSpiel.objects.all()

    voisins_de_zero_number = [num.number for num in voisins_de_zero][0]
    tier_number = [num.number for num in tier][0]
    orphelins_number = [num.number for num in orphelins][0]
    zero_spiel_number = [num.number for num in zero_spiel][0]

    voisins_correct_answer = calculate_the_answer(voisins_de_zero_number, 'voisins')
    tier_correct_answer = calculate_the_answer(tier_number, 'tier')
    orphelins_correct_answer = calculate_the_answer(orphelins_number, 'orphelins')
    zero_spiel_correct_answer = calculate_the_answer(zero_spiel_number, 'zero_spiel')

    user_voisins_answer = None
    result_icon = None

    if request.method == 'POST':
        voisins_answer = [
            int(request.POST.get('plays_by_voisins')),
            int(request.POST.get('change_voisins'))
        ]
        if voisins_answer is not None:
            user_voisins_answer = voisins_answer
            try:
                if user_voisins_answer == voisins_correct_answer:
                    result_icon = '✅'
                    VoisinsDeZero.generate_numbers()
                    voisins_de_zero = VoisinsDeZero.objects.all()
                    voisins_de_zero_number = [num.number for num in voisins_de_zero][0]
                else:
                    result_icon = '❌'
            except ValueError:
                result_icon = '❌'
            
    context = {
        'title': 'Серии',
        'voisins_content': f'voisins de zero {voisins_de_zero_number}',
        'result_icon': result_icon,
        'user_voisins_answer': user_voisins_answer,
        'correct_answer': voisins_correct_answer, 
        'tier': f'tier {tier_number}',
        'orphelins': f'orphelins {orphelins_number}',
        'zero_spiel': f'zero spiel {zero_spiel_number}',
        'voisins_correct_answer': voisins_correct_answer,
    }

    return render(request, 'testing/series.html', context)