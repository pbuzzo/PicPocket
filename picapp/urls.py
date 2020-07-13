from django.urls import path
from picapp import views

urlpatterns = [
    path('', views.ScanImage.as_view()),
]
