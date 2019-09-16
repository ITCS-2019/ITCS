from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.get_api_root_view().cls.__name__ = "ITCS"
router.get_api_root_view().cls.__doc__ = "root api router"
router.register(r'user', views.CurrentUserViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'sailors', views.SailorViewSet)
router.register(r'directions', views.TrainigDirectionViewSet)
router.register(r'organisations', views.TrainigOrganisationViewSet)
router.register(r'rangeNumbers', views.RangeNumberViewSet)
router.register(r'ranger', views.RangeViewSet, base_name='ranger')
router.register(r'organisationCerts', views.CertificatesOfOrganisation, base_name='organisationCerts')
router.register(r'certificates', views.CertificateViewSet)
router.register(r'tableCertificates', views.CertificatesOfTable, base_name='tableCertificates')
router.register(r'regulations', views.RegulationViewSet)
router.register(r'marilogger', views.MariloggerViewSet, base_name='marilogger')

urlpatterns = [
    path('dashInfo/', views.dashInfo, name="api-dashInfo"),
    path('dashInfoStat/', views.dashInfoStat, name="api-dashInfoStat"),
    path('directionsInfo/', views.trainingDirectionsInfo, name="api-directionsInfo"),
    #path('trainigDirections/', views.ListTrainigDirectionsView.as_view(), name="trainigDirections-all"),
    #path('certificates/', views.CertificateViewSet.as_view(), name="certificates-all"),
    path('allCerts/', views.certificates, name="api-allCerts"),
    path('trainingOrganisationsInfo/', views.trainingOrganisationsInfo, name="api-trainingOrganisationsInfo"),
    path('organisationDirectionsStat/', views.organisationDirectionsStat, name="api-organisationDirectionsStat"),
    path('issuedCerts/', views.issuedCerts, name="api-issuedCerts"),
    path('changeCertNumber/', views.changeCertNumber, name="api-changeCertNumber"),
    path('giveCertNumber/', views.giveCertNumber, name="api-giveCertNumber"),
    path('changeTrainigDirectionStatus/', views.changeTrainigDirectionStatus, name="api-changeTrainigDirectionStatus"),
    path('changeToReviewStatus/', views.changeToReviewStatus, name="api-changeToReviewStatus"),
    path('removeDraftCerts/', views.removeDraftCerts, name="api-removeDraftCerts"),
    path('setRangeNumbers/', views.setRangeNumbers, name="api-setRangeNumbers"),
    path('exportXLS/', views.exportXLS, name='api-exportXLS'),
    path('exportToPrint/', views.exportToPrint, name='api-exportToPrint'),
    path('printCertificate/<certID>/', views.printCertificate, name='api-printCertificate'),
    path('updateCertForTable/', views.updateCertForTable, name='api-updateCertForTable'),
    path('uploadSailorPhoto/', views.uploadSailorPhoto, name='api-uploadSailorPhoto'),
    path('uploadOrganisationLogo/', views.uploadOrganisationLogo, name='api-uploadOrganisationLogo'),
    path('uploadRegulationPDF/', views.uploadRegulationPDF, name='api-uploadRegulationPDF'),
    # path('uploadXLS/', views.uploadXLS, name='api-uploadXLS'),
    # path('logout/', views.LogoutView.as_view(), name="api-logout"),
]