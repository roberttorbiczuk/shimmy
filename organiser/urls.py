from django.urls import path

from .views import index, AddProfileView

urlpatterns = [
    path('', index, name='index'),
    path('add_user/', AddProfileView.as_view()),
]