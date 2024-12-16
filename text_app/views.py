from django.shortcuts import render, get_object_or_404
from db_editor.models import Text, Token, PosTag, Error, ErrorToken, ErrorTag

def show_text(request, text_id=None):
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

# 4112
def show_error_markup(request, text_id=4112): 
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)
    else:
        text = Text.objects.first()

    tokens = Token.objects.filter(idsentence__idtext=text.idtext)

    selected_markup = request.GET.get('markup', 'tagtext')
    
    # Собираем данные для отображения
    token_data = []
    for token in tokens:
        error_tag = None
        error_tag_abbrev = None 
        error_color = None
        error_level = None
        error_correct = None
        error_comment = None
        
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
                    error_tag_abbrev = error_tag_obj.tagtextabbrev  
                    error_level = error.iderrorlevel.errorlevelname if error.iderrorlevel else 'Не указано'
                    error_correct = error.correct if error.correct else 'Не указано'
                    error_comment = error.comment if error.comment else 'Не указано'

        token_data.append({
            'token': token.tokentext,
            'error_tag': error_tag,
            'error_tag_abbrev': error_tag_abbrev, 
            'error_color': error_color,
            'error_level': error_level,
            'error_correct': error_correct,
            'error_comment': error_comment,
        })
    
    context = {
        'text': text,
        'token_data': token_data,
        'selected_markup': selected_markup,
    }

    return render(request, 'show_error_markup.html', context)
<<<<<<< Updated upstream
=======

def show_text_markup(request, text_id=4112):
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)
    else:
        text = Text.objects.first()

    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext).select_related('idsentence')

    # Параметры для выбора разметки
    selected_pos_markup = request.GET.get('pos_markup', 'plain')
    selected_error_markup = request.GET.get('error_markup', 'plain')

    # Собираем данные для отображения
    sentence_data = []
    current_sentence = None
    current_tokens = []

    for token in tokens:
        # Проверяем, началась ли новая группа (предложение)
        if current_sentence != token.idsentence.idsentence:
            # Если предложение не пустое, сохраняем данные для текущего предложения
            if current_sentence is not None:
                sentence_data.append({
                    'sentence': current_sentence,
                    'tokens': current_tokens
                })
            # Обновляем текущие данные для нового предложения
            current_sentence = token.idsentence.idsentence
            current_tokens = []

        token_info = {'token': token.tokentext}

        # Разметка частей речи
        if selected_pos_markup != 'plain':
            pos_tag = token.idpostag
            if pos_tag:
                if selected_pos_markup == 'tagtextrussian':
                    token_info['pos'] = pos_tag.tagtextrussian
                elif selected_pos_markup == 'tagtextabbrev':
                    token_info['pos'] = pos_tag.tagtextabbrev
                else:
                    token_info['pos'] = pos_tag.tagtext
                token_info['tagcolor'] = pos_tag.tagcolor
            else:
                token_info['pos'] = None
                token_info['tagcolor'] = None
        else:
            token_info['pos'] = None
            token_info['tagcolor'] = None

        # Разметка ошибок
        if selected_error_markup != 'plain':
            error_tag = error_tag_abbrev = error_color = error_level = error_correct = error_comment = None
            error_token = ErrorToken.objects.filter(idtoken=token.idtoken).first()
            if error_token:
                error = Error.objects.filter(iderror=error_token.iderror.iderror).first()
                if error:
                    error_tag_obj = ErrorTag.objects.filter(iderrortag=error.iderrortag.iderrortag).first()
                    if error_tag_obj:
                        if selected_error_markup == 'error_russian':
                            error_tag = error_tag_obj.tagtextrussian
                        elif selected_error_markup == 'error_abbrev':
                            error_tag = error_tag_obj.tagtextabbrev
                        else:
                            error_tag = error_tag_obj.tagtext
                        error_tag_abbrev = error_tag_obj.tagtextabbrev
                        error_color = error_tag_obj.tagcolor
                        error_level = error.iderrorlevel.errorlevelname if error.iderrorlevel else 'Не указано'
                        error_correct = error.correct if error.correct else 'Не указано'
                        error_comment = error.comment if error.comment else 'Не указано'

            token_info.update({
                'error_tag': error_tag,
                'error_tag_abbrev': error_tag_abbrev,
                'error_color': error_color,
                'error_level': error_level,
                'error_correct': error_correct,
                'error_comment': error_comment,
            })
        else:
            token_info['error_tag'] = None
            token_info['error_tag_abbrev'] = None
            token_info['error_color'] = None
            token_info['error_level'] = None
            token_info['error_correct'] = None
            token_info['error_comment'] = None

        # Добавляем токен в текущие данные предложения
        current_tokens.append(token_info)

    # Не забываем добавить последнее предложение
    if current_tokens:
        sentence_data.append({
            'sentence': current_sentence,
            'tokens': current_tokens
        })

    context = {
        'text': text,
        'sentence_data': sentence_data,
        'selected_pos_markup': selected_pos_markup,
        'selected_error_markup': selected_error_markup,
    }

    return render(request, 'show_text_markup.html', context)
>>>>>>> Stashed changes
