from django.urls import path
from . import views

urlpatterns = [
    # Добавляем маршрут для отображения текста
    path('show_text/', views.show_text, name='show_text'),
]