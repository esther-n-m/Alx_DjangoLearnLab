from django.urls import path
from . import views

urlpatterns = [
    path('form-example/', views.example_form_view, name='form_example'),
]
