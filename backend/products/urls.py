from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_list),
    path('saving/', views.saving_list),

     #F03-03 (Vue가 호출할 API)
    path('api/deposits/<int:pk>/', views.DepositDetailAPIView.as_view()),
    path('api/deposits/<int:pk>/subscribe/', views.DepositSubscribeAPIView.as_view()),

    path('api/savings/<int:pk>/', views.SavingDetailAPIView.as_view()),
    path('api/savings/<int:pk>/subscribe/', views.SavingSubscribeAPIView.as_view()),
]
