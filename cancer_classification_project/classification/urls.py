from django.urls import path
from . import views

print("Loading classification/urls.py...")  # Debugging output

urlpatterns = [
    path('', views.predict_cancer_type, name='predict_cancer_type'),
]
