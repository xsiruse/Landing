from collections import Counter, defaultdict

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    from_ref = request.GET.get('from-landing')
    if from_ref != 'test':
        counter_show['other'] += 1
    else:
        counter_show['test'] += 1
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    # return render_to_response('landing.html')
    count = defaultdict(int)
    ab_test = request.GET.get('ab-test-arg')
    print(ab_test)
    if ab_test != 'test':
        counter_click['click_or'] += 1

        return render_to_response('landing.html')
    else:
        counter_click['click_te'] += 1

        return render_to_response('landing_alternate.html')
    print(count)
    return render_to_response('landing.html'), count




def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:

    if counter_click['click_te'] > 0 and counter_click['click_or'] > 0:
        test_conv = counter_show['test'] / counter_click['click_te']
        other_conv = counter_show['other'] / counter_click['click_or']
        return render_to_response('stats.html', context={
                                'test_conversion': test_conv,
                                'original_conversion': other_conv,
                                })
    else:
        return render_to_response('stats.html', context={
            'test_conversion': 'not enough data',
            'original_conversion': 'not enough data',
        })
