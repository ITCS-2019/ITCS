from django.urls import path

#from .views import ListTrainigDirectionsView
from . import views
urlpatterns = [
    path('trainigDirections/', views.ListTrainigDirectionsView.as_view(), name="trainigDirections-all"),
    path('allCerts/', views.certificates, name="api-allCerts"),
    path('issuedCerts/', views.issuedCerts, name="api-issuedCerts"),
    path('changeCertNumber/', views.changeCertNumber, name="api-changeCertNumber"),
    path('exportXLS/', views.exportXLS, name='api-exportXLS'),
]
