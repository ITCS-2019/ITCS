from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework import generics

from mariner.models import Certificate, TrainigOrganisation, TrainigDirections, Sailor
from .serializers import TrainigDirectionsSerializer


class ListTrainigDirectionsView(generics.ListAPIView):
	queryset = TrainigDirections.objects.all()
	serializer_class = TrainigDirectionsSerializer

@login_required(login_url="login/")
def certificates(request):
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		certs = list(Certificate.objects.filter(trainigOrganisation=trainigOrganisation).values())
		data =  dict()
		data['certificates'] = certs
		return JsonResponse(data)
	elif request.user.groups.all()[0].name == 'Інспектор':
		certs = list(Certificate.objects.exclude(status=0).values())
		data =  dict()
		data['certificates'] = certs
		return JsonResponse(data)
	else:
		certs = list(Certificate.objects.all().values())
		data =  dict()
		data['certificates'] = certs
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
def exportXLS(request):
#print(request.GET.get('data'))
	print(request.GET.get('exportType'))
	print(request.GET.get('certIDs'))
	hasError = False
	errorMessage = "No Error"
	data = {
	'error' : hasError,
	'error_message' : errorMessage,
	}
	return JsonResponse(data)
	# trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=name)
	# rows = trainigOrganisation.get_certInReview().exclude(certf_number__isnull=True).values_list(
	# 	'certf_number', 'first_name_en', 'last_name_en', 'last_name_ukr', 'first_name_ukr', 'second_name_ukr',
	# 	'born', 'date_of_issue', 'valid_date')
	# #certsInReview = Certificate.objects.filter(status__startswith=1)
	# response = HttpResponse(content_type='application/ms-excel')
	# response['Content-Disposition'] = 'attachment; filename="certificates.xls"'
	# wb = xlwt.Workbook(encoding='utf-8')
	# ws = wb.add_sheet('Сертифікати')
	# # Sheet header, first row
	# row_num = 0
	# font_style = xlwt.XFStyle()
	# font_style.font.bold = True
	# columns = ['Номер документу', 'Name', 'SurName', 'Прізвище','Ім\'я', 'По батькові', 'Дата народження', 'Дата видачі', 'Дійсний до',]
	# for col_num in range(len(columns)):
	# 	ws.write(row_num, col_num, columns[col_num], font_style)
	# # Sheet body, remaining rows
	# font_style = xlwt.XFStyle()
	# #font_style.num_format_str = 'dd/mm/yyyy'
	# font_style.num_format_str = 'dd.mm.yyyy'
	# # rows = certsInReview.objects.all().values_list(
	# # 	'first_name_en', 'last_name_en', 'last_name_ukr', 'first_name_ukr', 'second_name_ukr',
	# # 	'born', 'date_of_issue', 'valid_date')
	# print(rows.count())
	# if rows.count() > 0:
	# 	for row in rows:
	# 		row_num += 1
	# 		for col_num in range(len(row)):
	# 			ws.write(row_num, col_num, row[col_num], font_style)
	# 	wb.save(response)
	# 	return response
	# else:
	# 	return HttpResponse(status=204)