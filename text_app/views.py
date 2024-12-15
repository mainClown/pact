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


