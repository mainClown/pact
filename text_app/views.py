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

def show_text_markup(request, text_id=4112):
    # Получаем текст по заданному ID или первый текст, если ID не указан
    if text_id is not None:
        text = get_object_or_404(Text, idtext=text_id)
    else:
        text = Text.objects.first()

    # Получаем токены для данного текста
    tokens = Token.objects.filter(idsentence__idtext=text.idtext).select_related('idsentence')

    # Параметры для выбора разметки
    selected_pos_markup = request.GET.get('pos_markup')
    selected_error_markup = request.GET.get('error_markup')

    # Все разметки частей речи
    pos_markups = {
        'tagtext': [],
        'tagtextrussian': [],
        'tagtextabbrev': [],
        'plain': []
    }

    # Все разметки ошибок
    error_markups = {
        'error': [],
        'error_russian': [],
        'error_abbrev': [],
        'plain': []
    }

    # Собираем все возможные разметки 
    for token in tokens:
        pos_tag = token.idpostag
        if pos_tag:
            pos_markups['tagtext'].append(pos_tag.tagtext)
            pos_markups['tagtextrussian'].append(pos_tag.tagtextrussian)
            pos_markups['tagtextabbrev'].append(pos_tag.tagtextabbrev)

        error_tag = error_tag_abbrev = error_color = error_level = error_correct = error_comment = None
        error_token = ErrorToken.objects.filter(idtoken=token.idtoken).first()
        if error_token:
            error = Error.objects.filter(iderror=error_token.iderror.iderror).first()
            if error:
                error_tag_obj = ErrorTag.objects.filter(iderrortag=error.iderrortag.iderrortag).first()
                if error_tag_obj:
                    error_markups['error'].append(error_tag_obj.tagtext)
                    error_markups['error_russian'].append(error_tag_obj.tagtextrussian)
                    error_markups['error_abbrev'].append(error_tag_obj.tagtextabbrev)

    sentence_data = []
    current_sentence = None
    current_tokens = []

    # Формируем данные для отображения
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
        pos_tag = token.idpostag
        if pos_tag:
            token_info['pos_tag'] = {
                'tagtext': pos_tag.tagtext,
                'tagtextrussian': pos_tag.tagtextrussian,
                'tagtextabbrev': pos_tag.tagtextabbrev,
            }

        # Разметка ошибок
        error_tag = error_tag_abbrev = error_color = error_level = error_correct = error_comment = None
        error_token = ErrorToken.objects.filter(idtoken=token.idtoken).first()
        if error_token:
            error = Error.objects.filter(iderror=error_token.iderror.iderror).first()
            if error:
                error_tag_obj = ErrorTag.objects.filter(iderrortag=error.iderrortag.iderrortag).first()
                if error_tag_obj:
                    token_info['error_tag'] = {
                        'error': error_tag_obj.tagtext,
                        'error_russian': error_tag_obj.tagtextrussian,
                        'error_abbrev': error_tag_obj.tagtextabbrev,
                    }
                    token_info['error_color'] = error_tag_obj.tagcolor
                    token_info['error_level'] = error.iderrorlevel.errorlevelname if error.iderrorlevel else 'Не указано'
                    token_info['error_correct'] = error.correct if error.correct else 'Не указано'
                    token_info['error_comment'] = error.comment if error.comment else 'Не указано'

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
        'pos_markups': pos_markups,  # Все возможные разметки частей речи
        'error_markups': error_markups,  # Все возможные разметки ошибок
    }

    return render(request, 'show_text_markup.html', context)

