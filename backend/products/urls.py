from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_list),
    path('saving/', views.saving_list),
]
