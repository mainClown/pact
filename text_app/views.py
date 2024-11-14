from django.shortcuts import render, get_object_or_404
from db_editor.models import Text, Token, PosTag

def show_text(request, text_id=None):
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)  # Если текст с таким ID не найден, вернёт 404
    else:
        text = Text.objects.first()  # Используем первый текст по умолчанию
    
    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
    # Получаем все части речи
    pos_tags = PosTag.objects.all()
    
    # Параметры для выбора разметки (по умолчанию 'tagtext', можно выбирать 'tagtextrussian', 'tagtextabbrev' или 'plain')
    selected_markup = request.GET.get('markup', 'tagtext')
    
    # Собираем токены и их данные в список для отображения
    token_data = []
    for token in tokens:
        if selected_markup == 'plain':
            pos = None  # Не показываем часть речи в режиме 'plain'
        elif selected_markup == 'tagtextrussian':
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
