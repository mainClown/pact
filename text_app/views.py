from django.shortcuts import render
from db_editor.models import Text, Token, PosTag

def show_text(request):
    # Получаем первый текст из базы данных
    text = Text.objects.first()
    
    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
    # Получаем все части речи
    pos_tags = PosTag.objects.all()
    
    # Параметры для выбора разметки (по умолчанию 'tagtext', можно выбирать 'tagtextrussian' или 'tagtextabbrev')
    selected_markup = request.GET.get('markup', 'tagtext')
    
    # Собираем токены и их данные в список для отображения
    token_data = []
    for token in tokens:
        if selected_markup == 'tagtextrussian':
            pos = token.idpostag.tagtextrussian if token.idpostag else None
        elif selected_markup == 'tagtextabbrev':
            pos = token.idpostag.tagtextabbrev if token.idpostag else None
        else:
            pos = token.idpostag.tagtext if token.idpostag else None

        token_info = {
            'token': token.tokentext,
            'pos': pos,
        }
        token_data.append(token_info)
    
    context = {
        'text': text,
        'token_data': token_data,
        'pos_tags': pos_tags,
        'selected_markup': selected_markup,
    }

    return render(request, 'show_text.html', context)
