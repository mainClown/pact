from django.urls import path
from .views import view_academic_years

urlpatterns = [
    path('academic_years/', view_academic_years, name='view_academic_years'),
]
