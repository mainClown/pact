from django.shortcuts import render, get_object_or_404
from db_editor.models import Text, Token, PosTag, Error, ErrorToken, ErrorTag

def show_text(request, text_id=4112):
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)
    else:
        text = Text.objects.first()
    
    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
    # Параметры для выбора разметки
    selected_markup = request.GET.get('markup', 'tagtext')
    
    # Собираем данные для отображения
    token_data = []
    for token in tokens:
        if selected_markup == 'plain':
            pos = None  # Не показываем часть речи в режиме 'plain'
            tagcolor = None
        else:
            pos_tag = token.idpostag
            pos = None
            tagcolor = None
            if pos_tag:
                if selected_markup == 'tagtextrussian':
                    pos = pos_tag.tagtextrussian
                elif selected_markup == 'tagtextabbrev':
                    pos = pos_tag.tagtextabbrev
                else:
                    pos = pos_tag.tagtext
                tagcolor = pos_tag.tagcolor  # Получаем цвет части речи

        token_data.append({
            'token': token.tokentext,
            'pos': pos,
            'tagcolor': tagcolor,  # Передаем цвет
        })
    
    context = {
        'text': text,
        'token_data': token_data,
        'selected_markup': selected_markup,
    }

    return render(request, 'show_text.html', context)

def show_error_markup(request, text_id=4112):
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)
    else:
        text = Text.objects.first()
    
    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
    # Параметры для выбора разметки
    selected_markup = request.GET.get('markup', 'tagtext')
    
    # Собираем данные для отображения
    token_data = []
    for token in tokens:
        error_tag = None
        error_color = None
        
        # Проверяем, есть ли ошибка для данного токена
        error_token = ErrorToken.objects.filter(idtoken=token.idtoken).first()
        if error_token:
            error = Error.objects.filter(iderror=error_token.iderror.iderror).first()
            if error:
                error_tag_obj = ErrorTag.objects.filter(iderrortag=error.iderrortag.iderrortag).first()
                if error_tag_obj:
                    if selected_markup == 'tagtextrussian':
                        error_tag = error_tag_obj.tagtextrussian
                    elif selected_markup == 'tagtextabbrev':
                        error_tag = error_tag_obj.tagtextabbrev
                    else:
                        error_tag = error_tag_obj.tagtext
                    error_color = error_tag_obj.tagcolor

        token_data.append({
            'token': token.tokentext,
            'error_tag': error_tag,
            'error_color': error_color,
        })
        
        # print(f"Token: {token.tokentext}, Error Tag: {error_tag}, Error Color: {error_color}")
    
    context = {
        'text': text,
        'token_data': token_data,
        'selected_markup': selected_markup,
    }

    return render(request, 'show_error_markup.html', context)

# def show_text(request, text_id=None):
#     # Получаем текст по заданному ID или первый текст, если ID не указан
#     if text_id is not None:
#         text = get_object_or_404(Text, idtext=text_id)  # Если текст с таким ID не найден, вернёт 404
#     else:
#         text = Text.objects.first()  # Используем первый текст по умолчанию
    
#     # Получаем токены для данного текста
#     tokens = Token.objects.filter(idsentence__idtext=text.idtext)
    
#     # Получаем все части речи
#     pos_tags = PosTag.objects.all()
    
#     # Параметры для выбора разметки (по умолчанию 'tagtext', можно выбирать 'tagtextrussian', 'tagtextabbrev' или 'plain')
#     selected_markup = request.GET.get('markup', 'tagtext')
    
#     # Собираем токены и их данные в список для отображения
#     token_data = []
#     for token in tokens:
#         if selected_markup == 'plain':
#             pos = None  # Не показываем часть речи в режиме 'plain'
#         elif selected_markup == 'tagtextrussian':
#             pos = token.idpostag.tagtextrussian if token.idpostag else None
#         elif selected_markup == 'tagtextabbrev':
#             pos = token.idpostag.tagtextabbrev if token.idpostag else None
#         else:
#             pos = token.idpostag.tagtext if token.idpostag else None

#         token_info = {
#             'token': token.tokentext,
#             'pos': pos,
#         }
#         token_data.append(token_info)
    
#     context = {
#         'text': text,
#         'token_data': token_data,
#         'pos_tags': pos_tags,
#         'selected_markup': selected_markup,
#     }

#     return render(request, 'show_text.html', context)