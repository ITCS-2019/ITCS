from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse

from django.template.loader import render_to_string

from rest_framework import authentication, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import decorators


from .serializers import UserSerializer, TrainigDirectionSerializer, CertificateSerializer, SailorSerializer, TrainigOrganisationSerializer

from accounts.models import Profile
from mariner.models import Certificate, TrainigOrganisation, TrainigDirections, Sailor

# from django.core.files.storage import FileSystemStorage

from weasyprint import HTML

import xlwt

# import openpyxl

import datetime

"""
REST Requests
"""
# User = get_user_model()

class DefaultsMixin(object):
	"""
	Settings for view authentication, permissions, filtering and paginations.
	"""
	authentication_classes = (
		authentication.BasicAuthentication,
		authentication.TokenAuthentication,
	)
	permission_classes = (
		permissions.IsAuthenticated,
	)
	paginate_by = 25
	paginate_by_param = 'page_size'
	max_paginate_by = 100

class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
	lookup_field = User.USERNAME_FIELD
	lookup_url_kwarg = User.USERNAME_FIELD
	queryset = User.objects.order_by(User.USERNAME_FIELD)
	serializer_class = UserSerializer

class SailorViewSet(DefaultsMixin, viewsets.ModelViewSet):
	queryset = Sailor.objects.all()
	serializer_class = SailorSerializer

class TrainigDirectionViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""
    Returns a list of all training direction in DB.
    If user from training organisations return list of training directions of this organisation.
    """
	queryset = TrainigDirections.objects.all()
	serializer_class = TrainigDirectionSerializer

	def list(self, request):
		# request.user.auth_token.delete()
		directions = TrainigDirections()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			directions = trainigOrganisation.directions.all()
		else:
			directions = TrainigDirections.objects.all()
		serializer = TrainigDirectionSerializer(directions, many=True)
		return Response({"directions": serializer.data})

class TrainigOrganisationViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""
    Return a list of all training organisations.
    """
	queryset = TrainigOrganisation.objects.all()
	serializer_class = TrainigOrganisationSerializer

class CertificateViewSet(viewsets.ModelViewSet):
	"""
    Return a list of all certificates in DB.
    If user from training organisations return list of certificates of this organisation.
    If user from inspectors group return list of certificates exlude drafts status.
    """
	
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Certificate.objects.order_by('-id')
	serializer_class = CertificateSerializer

	# def get_permissions(self):
	# 	if self.action == 'list':
	# 		return [permissions.IsAuthenticated()]
	# 	else:
	# 		return [permissions.IsAuthenticated()]

	# @decorators.action(detail = 0, permission_classes=(permissions.IsAuthenticated, ))
	def list(self, request):
		certs = Certificate()
		certsDataArr = []
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			certs = Certificate.objects.filter(trainigOrganisation=trainigOrganisation).select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').order_by('-id')
		elif request.user.groups.all()[0].name == 'Інспектор':
			certs = Certificate.objects.exclude(status=0).select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').order_by('-id')
		else:
			certs = Certificate.objects.all().select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').order_by('-id')
		serializer = CertificateSerializer(certs, many=True)
		return Response({"certificates": serializer.data})

	def create(self, request, format=None):
		trainigOrganisation = TrainigOrganisation()
		if request.user.groups.all()[0].name == 'НТЗ':
			print('organisation_name = ', request.user.profile.organization_name)
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		else:
			print('Organisation ID = ' , request.data.get('trainigOrganisation'))
		print('Direction ID = ', request.data.get('training_direction'))
		return Response({"message": "Test POST data."}, status=200)

# class LogoutView(DefaultsMixin, APIView):
# 	#authentication_classes = (authentication.TokenAuthentication,)
# 	def get(self, request):
# 		print(request.user)
# 		#request.user.auth_token.delete()
# 		try:
# 			token = Token.objects.get(user=request.user)
# 			cache.delete(token.key)
# 			token.delete()
# 		except Token.DoesNotExist:
# 			pass
# 		return Response(status=200)

"""
AJAX Requests
"""
@login_required(login_url="login/")
def dashInfo(request):
	profile, created = Profile.objects.get_or_create(user=request.user)
	dashDataArr = []
	if request.user.groups.all()[0].name == 'НТЗ':
		if request.user.profile.organization_name == '':
			return redirect('update_profile')
		else:
			sailorsCount = Sailor.objects.all().count()
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			trainigDirectionsCount = trainigOrganisation.directions.count()
			certCount = trainigOrganisation.trained.filter(status__startswith=2).count()
			certsInDraftCount = trainigOrganisation.trained.filter(status__startswith=0).count()
			certsInReviewCount = trainigOrganisation.get_certInReview().count()
			dashData = {
			'sailorsCount': sailorsCount,
			'certCount': certCount,
			'trainigDirectionsCount': trainigDirectionsCount,
			'certsInDraftCount': certsInDraftCount,
			'certsInReviewCount': certsInReviewCount,
			}
			dashDataArr.append(dashData)
			dashInfoDict = {'dashInfo': dashDataArr,}
			return JsonResponse(dashInfoDict)
	else:
		sailorsCount = Sailor.objects.all().count()
		certCount = Certificate.objects.filter(status__startswith=2).count()
		certsInReviewCount = Certificate.objects.filter(status__startswith=1).count()
		trainigDirectionsCount = TrainigDirections.objects.all().count()
		trainigOrganisations = list(TrainigOrganisation.objects.all().values())
		dashData = {
			'sailorsCount': sailorsCount,
			'certCount': certCount,
			'trainigDirectionsCount': trainigDirectionsCount,
			'certsInReviewCount': certsInReviewCount,
			'trainigOrganisations': trainigOrganisations,
		}
		dashDataArr.append(dashData)
		dashInfoDict = {'dashInfo': dashDataArr,}
		# dashInfoDict = {'dashInfo': dashData,}#'trainigOrganisations': trainigOrganisations,}
		return JsonResponse(dashInfoDict)


@login_required(login_url="login/")
def trainingOrganisationsInfo(request):
	trainigOrganisations = TrainigOrganisation.objects.all()
	organisationDataArr = []
	organisationDirections = []
	
	for organisation in trainigOrganisations:
		reviewCertIDs = []
		for reviewCert in organisation.get_certInReview():
			reviewCertIDs.append(reviewCert.training_direction.id)
		issuedCertIDs = []
		for issuedCert in organisation.get_issuedCerts():
			issuedCertIDs.append(issuedCert.training_direction.id)
		directionsDataArr = []
		for direction in organisation.directions.all():
			reviewCertCount = reviewCertIDs.count(direction.id)
			issuedCertCount = issuedCertIDs.count(direction.id)
			certsLeftCount = direction.range_numbers.count()
			directionData = {
			'direction_id': direction.id,
			'dirction_name': direction.direction_title,
			'direction_reviewCertCount': reviewCertCount,
			'direction_issuedCertCount': issuedCertCount,
			'direction_reviewAndIssuedCertsCount': reviewCertCount + issuedCertCount,
			'direction_certsLeftCount': certsLeftCount,
			'direction_allCertsCount': reviewCertCount + issuedCertCount + certsLeftCount,
			}
			directionsDataArr.append(directionData)
		organisationData = {
		'organisation_id': organisation.id,
		'organisation_name': organisation.organisation_name,
		'organisation_activated': organisation.activated,
		'organisation_active_till': organisation.active_till,
		'organisation_allCertsInReviewCount': organisation.get_certInReview().count(),
		'organisation_reviewCertIDs': reviewCertIDs,
		'organisation_allIssuedCertsCount': organisation.get_issuedCerts().count(),
		'organisation_issuedCertIDs': issuedCertIDs,
		'organisation_directions': directionsDataArr,
		}
		organisationDataArr.append(organisationData)
		
	organisationsDict = {'organisations': organisationDataArr,}
	return JsonResponse(organisationsDict)

@login_required(login_url="login/")
def trainingDirectionsInfo(request):
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		reviewCertIDs = []
		for reviewCert in trainigOrganisation.get_certInReview():
			reviewCertIDs.append(reviewCert.training_direction.id)
		issuedCertIDs = []
		for issuedCert in trainigOrganisation.get_issuedCerts():
			issuedCertIDs.append(issuedCert.training_direction.id)
		directionsDataArr = []
		for direction in trainigOrganisation.directions.all():
			reviewCertCount = reviewCertIDs.count(direction.id)
			issuedCertCount = issuedCertIDs.count(direction.id)
			certsLeftCount = direction.range_numbers.count()
			directionData = {
			'direction_id': direction.id,
			'dirction_name': direction.direction_title,
			'price_id':direction.price_id,
			'level':direction.level,
			'allow_functions':direction.allow_functions,
			'status':direction.status,
			'direction_reviewCertCount': reviewCertCount,
			'direction_issuedCertCount': issuedCertCount,
			'direction_reviewAndIssuedCertsCount': reviewCertCount + issuedCertCount,
			}
			directionsDataArr.append(directionData)
		data = {'trainigDirections': directionsDataArr,}
		return JsonResponse(data)
	else:
		trainigDirections = list(TrainigDirections.objects.all().values())
		data = dict()
		data['trainigDirections'] = trainigDirections
		return JsonResponse(data)

@login_required(login_url="login/")
def issuedCerts(request):
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		certifications = list(Certificate.objects.filter(trainigOrganisation=trainigOrganisation).filter(status=2).values())
		data =  dict()
		data['certificates'] = certifications
		return JsonResponse(data)
	else:
		certs = list(Certificate.objects.filter(status=2).values())
		data =  dict()
		data['certificates'] = certs
		return JsonResponse(data)

@login_required(login_url="login/")
def changeTrainigDirectionStatus(request):
	trainingDirID = request.GET.get('certID')
	dirStatus = request.GET.get('dirStatus')
	#print(trainingDirID)
	#rint(dirStatus)
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		#print(trainigOrganisation.directions.get(id=trainingDirID))
		direction = trainigOrganisation.directions.get(id=trainingDirID)
		#print('Direction Status:')
		#print(direction.status)
		data = {
			'error' : False,
			'error_message' : "Test MODE",
		}
		return JsonResponse(data)
	else:
		data = {
			'error' : True,
			'error_message' : "Test MODE",
		}
		return JsonResponse(data)

def changeCertNumber(request):
	certID = request.GET.get('certID')
	certNumber = request.GET.get('certNumber')
	hasError = False
	errorMessage = "No Error"
	if certNumber != None:
		if certNumber != "":
			certificate = Certificate.objects.get(id=certID)
			certificate.certf_number = certNumber
			certificate.save()
		else:
			hasError = True
			errorMessage = "Number is Empty"
	else:
			hasError = True
			errorMessage = "Number is None"
	data = {
		'error' : hasError,
		'error_message' : errorMessage,
	}
	return JsonResponse(data)

@login_required(login_url="login/")
def giveCertNumber(request):
	certIDsList = request.GET.get('certIDs').split(',')
	hasError = False
	errorMessage = "No Error"
	if certIDsList != '':
		# certsInChange = Certificate.objects.filter(pk__in=certIDsList)
		# for cert in certsInChange:
		# 	if cert.certf_number is None or cert.certf_number is '':
		# 		cert.certf_number = ""
		# 		cert.save()
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)
	else:
		hasError = True
		errorMessage = "Empty certIDs"
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)

@login_required(login_url="login/")
def changeToReviewStatus(request):
	certIDsList = request.GET.get('certIDs').split(',')
	hasError = False
	errorMessage = "No Error"
	if certIDsList != '':
		certsInChange = Certificate.objects.filter(pk__in=certIDsList)
		for cert in certsInChange:
			if cert.status == 0:
				cert.status = 1
				cert.save()
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)
	else:
		hasError = True
		errorMessage = "Empty certIDs"
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)

@login_required(login_url="login/")
def removeDraftCerts(request):
	certIDsList = request.GET.get('certIDs').split(',')
	hasError = False
	errorMessage = "No Error"
	if certIDsList != '':
		certsInChange = Certificate.objects.filter(pk__in=certIDsList)
		for cert in certsInChange:
			if cert.status == 0:
				cert.delete()
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)
	else:
		hasError = True
		errorMessage = "Empty certIDs"
		data = {
			'error' : hasError,
			'error_message' : errorMessage,
		}
		return JsonResponse(data)

@login_required(login_url="login/")
def exportXLS(request):
	print(request.GET.get('exportType'))
	certIDsList = request.GET.get('certIDs').split(',')
	# certsQuerySet = Certificate.objects.filter(pk__in=certIDsList)
	if request.GET.get('exportType') == 'Register':
		rows = Certificate.objects.filter(pk__in=certIDsList).values_list(
		'certf_number', 'first_name_en', 'last_name_en', 'last_name_ukr', 'first_name_ukr', 'second_name_ukr',
		'born', 'date_of_issue', 'valid_date')
		fileNameXLS = 'attachment; filename=\"itcs-' + datetime.datetime.today().strftime('%Y%m%d-%H%M') + '.xls\"'
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = fileNameXLS #'attachment; filename="certificates.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Сертифікати')
		
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		columns = ['Номер документу', 'Name', 'SurName', 'Прізвище','Ім\'я', 'По батькові', 'Дата народження', 'Дата видачі', 'Дійсний до',]
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)
		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()
		font_style.num_format_str = 'dd.mm.yyyy'
		
		if rows.count() > 0:
			for row in rows:
				row_num += 1
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response
		else:
			return HttpResponse(status=204)
	elif request.GET.get('exportType') == 'GiveCerts':
		#need filter(status__startswith=1) check???
		certsInReview = Certificate.objects.filter(pk__in=certIDsList).exclude(certf_number__isnull=True)
		if certsInReview.count() > 0:
			now = datetime.datetime.now()
			for certificate in certsInReview:
				if certificate.certf_number != None:
					if certificate.certf_number != '':
						print('////////////////////')
						#TODO: create hash sum
						ntzNumberStr = "{}/{}{}{}{}".format(
							certificate.certf_number, 
							certificate.trainigOrganisation.organisation_id, 
							now.month,
							now.year,
							certificate.training_direction.id)
						print(ntzNumberStr)
						certificate.ntz_number = ntzNumberStr
						certificate.status = 2
						certificate.save()
					else:
						print('Cert number is Empty')
				else:
					print('Cert number is None')
			return redirect('crm_home')
		else:
			#ErrorMessage: "Zero Certs"
			print('Zero Certs')
			return HttpResponse(status=204)
	else:
		#ErrorMessage: "Incorrect Export Type"
		print('Incorrect Export Type')
		return HttpResponse(status=204)

@login_required(login_url="login/")
def exportToPrint(request):
	print(request.GET.get('exportType'))
	certIDsList = request.GET.get('certIDs').split(',')
	fileNameXLS = 'attachment; filename=\"itcs-' + datetime.datetime.today().strftime('%Y%m%d-%H%M') + '.xls\"'
	fileNamePDF = 'inline; filename=itcs-' + datetime.datetime.today().strftime('%Y%m%d-%H%M') + '.pdf'
	if request.GET.get('exportType') == 'XLSExp':
		rows = Certificate.objects.filter(pk__in=certIDsList).values_list(
		'certf_number', 'first_name_en', 'last_name_en', 'last_name_ukr', 'first_name_ukr', 'second_name_ukr',
		'born', 'date_of_issue', 'valid_date')
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = fileNameXLS #'attachment; filename="certificates.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Сертифікати')
		
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		columns = ['Номер документу', 'Name', 'SurName', 'Прізвище','Ім\'я', 'По батькові', 'Дата народження', 'Дата видачі', 'Дійсний до',]
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)
		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()
		font_style.num_format_str = 'dd.mm.yyyy'
		
		if rows.count() > 0:
			for row in rows:
				row_num += 1
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response
		else:
			return HttpResponse(status=204)
	elif request.GET.get('exportType') == 'PdfExp':
		certifications = Certificate.objects.filter(pk__in=certIDsList)
		fileTitleStr = ''
		if request.user.groups.all()[0].name == 'НТЗ':
			fileTitleStr = request.user.profile.organization_name
		fileTitleStr = fileTitleStr + ' ' + datetime.datetime.today().strftime('%Y%m%d-%H%M')
		html_string = render_to_string('printTable.html', {'certifications': certifications, 'fileTitle': fileTitleStr})
		html = HTML(string=html_string).write_pdf()
		response = HttpResponse(html, content_type='application/pdf')
		response['Content-Disposition'] = fileNamePDF #"inline; filename=certificates.pdf"
		return response
	elif request.GET.get('exportType') == 'PrintExp':
		return HttpResponse(status=204)
	else:
		print('Incorrect Export Type')
		return HttpResponse(status=204)


"""
OLD Requests For Clear
"""
@login_required(login_url="login/")
def certificates(request):
	certs = Certificate()
	certsDataArr = []
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		certs = Certificate.objects.filter(trainigOrganisation=trainigOrganisation)
	elif request.user.groups.all()[0].name == 'Інспектор':
		certs = Certificate.objects.exclude(status=0)
	else:
		certs = Certificate.objects.all().select_related('sailor').select_related('trainigOrganisation').select_related('training_direction')
		
	for cert in certs:
		organisationID = ''
		organisationName = ''
		directionID = ''
		directionName = ''
		if cert.trainigOrganisation is not None:
			organisationID = cert.trainigOrganisation.id
			organisationName = cert.trainigOrganisation.organisation_name
		if cert.training_direction is not None:
			directionID = cert.training_direction.id
			directionName = cert.training_direction.direction_title
		certData = {
			'cert_id': cert.id,
			'certf_number': cert.certf_number,
			'form_number': cert.form_number,
			'ntz_number': cert.ntz_number,
			'first_name_en': cert.first_name_en,
			'last_name_en': cert.last_name_en,
			'last_name_ukr': cert.last_name_ukr,
			'first_name_ukr': cert.first_name_ukr,
			'second_name_ukr': cert.second_name_ukr,
			'born': cert.born.strftime("%m.%d.%Y"),
			'inn': cert.inn,
			'sailor_id': cert.sailor.id,
			'trainigOrganisation_id': organisationID,
			'trainigOrganisation_name': organisationName,
			'date_of_issue': cert.date_of_issue,
			'valid_date': cert.valid_date,
			'valid_type': cert.valid_type,
			'direction_level': cert.direction_level,
			'direction_allow_functions': cert.direction_allow_functions,
			'training_direction_id': directionID,
			'training_direction_title': directionName,
			'status': cert.status,
		}
		certsDataArr.append(certData)
	certificatesDict = {'certificates':certsDataArr,}
	return JsonResponse(certificatesDict)
# @login_required(login_url="login/")
# def uploadXLS(request):
# 	if "GET" == request.method:
# 		print('GET request')
# 		return render(request, "crm_xlsImport.html", {})
# 	else:
# 		print('load file')
# 		print(request.POST.get('my_options'))
# 		excel_file = request.FILES["excel_file"]
# 		# TODO: validations check extension or file size
# 		wb = openpyxl.load_workbook(excel_file, read_only=False, keep_vba=False, data_only=False, keep_links=True)
# 		# getting a particular sheet by name out of many sheets
# 		worksheet = wb[0]
# 		print(worksheet)
# 		excel_data = list()
# 		# iterating over the rows and
# 		# getting value from each cell in row
# 		for row in worksheet.iter_rows():
# 			row_data = list()
# 			for cell in row:
# 				row_data.append(str(cell.value))
# 			excel_data.append(row_data)
# 		print(excel_data)
# 		return render(request, 'crm_xlsImport.html', {"excel_data":excel_data})
# 		#return HttpResponse(status=204)