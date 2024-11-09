from django.shortcuts import render
from db_editor.models import Text, Token, PosTag

def show_text(request):
    # Получаем первый текст из базы данных
    text = Text.objects.first()
    
    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
    # Получаем все части речи
    pos_tags = PosTag.objects.all()
    
    # Параметры для выбора разметки
    selected_markup = request.GET.get('markup', 'all')  # по умолчанию 'all', можно фильтровать по 'pos'
    
    # Фильтрация токенов по выбранной разметке
    if selected_markup == 'pos':
        tokens = tokens.filter(idpostag__isnull=False)
    
    # Собираем токены и их данные в список для отображения
    token_data = []
    for token in tokens:
        token_info = {
            'token': token.tokentext,
            'pos': token.idpostag.tagtext if token.idpostag else None,
        }
        token_data.append(token_info)
    
    context = {
        'text': text,
        'token_data': token_data,
        'pos_tags': pos_tags,
        'selected_markup': selected_markup,
    }

    return render(request, 'show_text.html', context)
