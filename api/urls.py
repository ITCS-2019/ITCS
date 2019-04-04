from django.urls import path

#from .views import ListTrainigDirectionsView
from . import views
urlpatterns = [
    path('trainigDirections/', views.ListTrainigDirectionsView.as_view(), name="trainigDirections-all"),
    path('issuedCerts/', views.issuedCerts, name="issuedCerts")
]
