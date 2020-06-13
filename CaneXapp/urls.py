from django.urls import path
from .views import mainfunc, uploadfunc, deletefunc

urlpatterns = [
    path('', mainfunc, name='main'),
    path('upload/', uploadfunc, name='upload'),
    path('delete/', deletefunc, name='delete'),
]
