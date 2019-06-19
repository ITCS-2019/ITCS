from django.urls import path

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'directions', views.TrainigDirectionViewSet)
router.register(r'certificates', views.CertificateViewSet)

urlpatterns = [
    path('dashInfo/', views.dashInfo, name="api-dashInfo"),
    path('directionsInfo/', views.trainingDirectionsInfo, name="api-directionsInfo"),
    #path('trainigDirections/', views.ListTrainigDirectionsView.as_view(), name="trainigDirections-all"),
    #path('certificates/', views.CertificateViewSet.as_view(), name="certificates-all"),
    path('allCerts/', views.certificates, name="api-allCerts"),
    path('trainingOrganisationsInfo/', views.trainingOrganisationsInfo, name="api-trainingOrganisationsInfo"),
    path('issuedCerts/', views.issuedCerts, name="api-issuedCerts"),
    path('changeCertNumber/', views.changeCertNumber, name="api-changeCertNumber"),
    path('giveCertNumber/', views.giveCertNumber, name="api-giveCertNumber"),
    path('changeTrainigDirectionStatus/', views.changeTrainigDirectionStatus, name="api-changeTrainigDirectionStatus"),
    path('changeToReviewStatus/', views.changeToReviewStatus, name="api-changeToReviewStatus"),
    path('removeDraftCerts/', views.removeDraftCerts, name="api-removeDraftCerts"),
    path('exportXLS/', views.exportXLS, name='api-exportXLS'),
    path('exportToPrint/', views.exportToPrint, name='api-exportToPrint'),
    # path('uploadXLS/', views.uploadXLS, name='api-uploadXLS'),
]
