from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse

from django.template.loader import render_to_string

from rest_framework import permissions, viewsets, mixins#, authentication 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import decorators


from .serializers import UserSerializer, TrainigDirectionSerializer,  RangeNumberSerializer, RangeSerializer, CertificateSerializer, CertificateCustomSerializer, SailorSerializer, TrainigOrganisationSerializer, RegulationSerializer

from accounts.models import Profile
from mariner.models import Certificate, TrainigOrganisation, RangeNumber, TrainigDirections, Sailor, CertificatePrintSettings
from regulations.models import RegulationDoc

# from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from weasyprint import HTML#, CSS

# Import QRCode from pyqrcode 
import pyqrcode 
from pyqrcode import QRCode
import png

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
	# authentication_classes = (
	# 	authentication.BasicAuthentication,
	# 	authentication.TokenAuthentication,
	# )
	# permission_classes = (
	# 	permissions.IsAuthenticated,
	# )
	paginate_by = 25
	paginate_by_param = 'page_size'
	max_paginate_by = 100


class CurrentUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
    Returns information about cerrent user.
    """
	queryset = Profile.objects.all()

	
	def list(self, request):
		current_user = User.objects.get(id = request.user.id)
		serializer = UserSerializer(current_user)
		return Response({"user": serializer.data})

	def get_permissions(self):
		if self.request.method == 'GET':
			return [permissions.IsAuthenticated()]
		else:
			return [permissions.IsAdminUser()]

class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):#ReadOnlyModelViewSet):
	"""
    Returns list of users.
    If user from training organisations return list of users of this organisation.
    """
	queryset = User.objects.all()
	serializer_class = UserSerializer

	#TODO: Show user by id only for admin?
	# def retrieve(self, request, pk):
	# 	print('--------------------')
	# 	print(pk)
	# 	current_user = User.objects.get(id = request.user.id)
	# 	serializer = UserSerializer(current_user)
	# 	#return Response({"User": "You can't get user by id"}, status=200)
	# 	return Response({"user": serializer.data})

	def list(self, request):
		users = User()
		users_count = int()
		if request.user.groups.all()[0].name == 'НТЗ':
			users = User.objects.get(id = request.user.id)#TODO: get users of organisation
			serializer = UserSerializer(users)
			return Response({"users": serializer.data})
		else:
			users = User.objects.all()
			serializer = UserSerializer(users, many=True)#TODO: check if len(users) count > 1
			return Response({"users": serializer.data})

	def get_permissions(self):
		if self.request.method == 'GET':
			return [permissions.IsAuthenticated()]
		else:
			return [permissions.IsAdminUser()]

class SailorViewSet(DefaultsMixin, viewsets.ModelViewSet):
	queryset = Sailor.objects.all()
	serializer_class = SailorSerializer

class RangeNumberViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""
    Returns list of all range numbers in DB.
    If user from training organisations return list of range numbers of this organisation.
    """
	queryset = RangeNumber.objects.all()
	serializer_class = RangeNumberSerializer

	def list(self, request):
		numbers = RangeNumber()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			numbers = RangeNumber.objects.filter(organisation_id=trainigOrganisation.id)
		else:
			numbers = RangeNumber.objects.all()
		serializer = RangeNumberSerializer(numbers, many=True)#TODO: check if len(directions) count > 1
		return Response({"range_numbers": serializer.data})

class RangeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
	queryset = RangeNumber.objects.all()
	serializer_class = RangeSerializer

	def create(self, request, format=None):
		print(request.data)
		orgId = request.data.get('organisation_id')
		directionID = request.data.get('direction_id')
		startFromNumber = request.data.get('startRange')
		endAtNumber = request.data.get('endRange')
		# print('Organisation ID: ', orgId)
		# print('Direction ID: ', directionID)
		# print('Start From Number: ', startFromNumber)
		# print('End At Number: ', endAtNumber)
		# if not (startFromNumber.isdigit()):
		# 	print('rangeStartNumber not digit')
		# 	form = RangeNumberForm(orgId)
		# 	organisation = TrainigOrganisation.objects.get(id=orgId)
		# 	return render(request, 'crm_rangeNumber.html', {'form': form, 'organisation': organisation, "error_message": "rangeStartNumber not digit"})
		# if not (endAtNumber.isdigit()):
		# 	print('rangeEndNumber not digit')
		# 	form = RangeNumberForm(orgId)
		# 	organisation = TrainigOrganisation.objects.get(id=orgId)
		# 	return render(request, 'crm_rangeNumber.html', {'form': form, 'organisation': organisation, "error_message": "rangeEndNumber not digit"})
		# if int(endAtNumber) < int(startFromNumber):
		# 	print('endAtNumber < startFromNumber')
		# 	form = RangeNumberForm(orgId)
		# 	organisation = TrainigOrganisation.objects.get(id=orgId)
		# 	return render(request, 'crm_rangeNumber.html', {'form': form, 'organisation': organisation, "error_message": "endAtNumber < startFromNumber"})
		#print('--------------------')
		organisation = TrainigOrganisation.objects.get(id=orgId)
		direction = organisation.directions.get(id=directionID)
		#print(organisation)
		#print(direction)
		#print('--------------------')
		for i in range(int(startFromNumber), int(endAtNumber)+1):
			print(i, ' - current number')
			rangeNum,created = RangeNumber.objects.get_or_create(number=i, organisation_id=orgId , organisation_name=organisation.organisation_name, direction_id=directionID, direction_name=direction.direction_title)
			if created:
				rangeNum.save()
				print('Created')
				organisation.range_numbers.add(rangeNum)
				print('Add to ranges')
			else:
				print('already created')
		return Response({"message": "Range created"}, status=200)

	def destroy(self, request, pk, format=None):
		print(request.data)

class TrainigDirectionViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""
    Returns a list of all training direction in DB.
    If user from training organisations return list of training directions of this organisation.
    """
	queryset = TrainigDirections.objects.all()
	serializer_class = TrainigDirectionSerializer

	def list(self, request):
		directions = TrainigDirections()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			directions = trainigOrganisation.directions.all()
		else:
			directions = TrainigDirections.objects.all()
		serializer = TrainigDirectionSerializer(directions, many=True)#TODO: check if len(directions) count > 1
		return Response({"directions": serializer.data})

	# def get_permissions(self):
	# 	if self.request.method == 'GET':
	# 		return [permissions.IsAuthenticated()]
	# 	else:
	# 		return [permissions.IsAdminUser()] #TODO: use custom permission class for Admin|Inspectors


class TrainigOrganisationViewSet(DefaultsMixin, viewsets.ModelViewSet):
	"""
    Return a list of all training organisations.
    If user from training organisations return organisation of user.
    """
	queryset = TrainigOrganisation.objects.all()
	serializer_class = TrainigOrganisationSerializer

	def list(self, request):
		organisations = TrainigOrganisation()
		if request.user.groups.all()[0].name == 'НТЗ':
			organisations = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			serializer = TrainigOrganisationSerializer(organisations)
			return Response({"organisations": serializer.data})
		else:
			organisations = TrainigOrganisation.objects.all()
			serializer = TrainigOrganisationSerializer(organisations, many=True)
			return Response({"organisations": serializer.data})

	def create(self, request, format=None):
		organisation = TrainigOrganisation()
		organisation.organisation_id = request.data.get('organisation_id')
		organisation.organisation_name = request.data.get('organisation_name')
		organisation.organisation_name_eng = request.data.get('organisation_name_eng')
		organisation.mail_adress_ukr = request.data.get('mail_adress_ukr')
		organisation.mail_adress_eng = request.data.get('mail_adress_eng')
		organisation.phone1 = request.data.get('phone1')
		organisation.phone2 = request.data.get('phone2')
		organisation.orgnisation_email = request.data.get('orgnisation_email')
		organisation.site_link = request.data.get('site_link')
		organisation.contract_number = request.data.get('contract_number')
		organisation.contract_number_date = request.data.get('contract_number_date')
		organisation.checking_number = request.data.get('checking_number')
		organisation.bank_name = request.data.get('bank_name')
		organisation.mfo = request.data.get('mfo')
		organisation.okpo = request.data.get('okpo')
		organisation.inn = request.data.get('inn')
		organisation.nds_number = request.data.get('nds_number')
		organisation.head_full_name = request.data.get('head_full_name')
		organisation.head_position = request.data.get('head_position')
		organisation.accountant_full_name = request.data.get('accountant_full_name')
		organisation.activated = request.data.get('activated')
		organisation.active_till = request.data.get('active_till')
		organisation.save()
		directions = self.request.data['directions']
		for direction in directions:
		 	# create instance of model from dict
		 	d = TrainigDirections(**direction)
		 	d.save()
		 	organisation.directions.add(d)
		organisation.save()
		return Response({"message": "Organisation created"}, status=200)
		#serializer.save(directions=self.request.data['directions'])

	def update(self, request, pk, format=None):
		organisation = TrainigOrganisation.objects.get(id=pk)

		organisation.organisation_id = request.data.get('organisation_id')
		organisation.organisation_name = request.data.get('organisation_name')
		organisation.organisation_name_eng = request.data.get('organisation_name_eng')
		organisation.mail_adress_ukr = request.data.get('mail_adress_ukr')
		organisation.mail_adress_eng = request.data.get('mail_adress_eng')
		organisation.phone1 = request.data.get('phone1')
		organisation.phone2 = request.data.get('phone2')
		organisation.orgnisation_email = request.data.get('orgnisation_email')
		organisation.site_link = request.data.get('site_link')
		organisation.contract_number = request.data.get('contract_number')
		organisation.contract_number_date = request.data.get('contract_number_date')
		organisation.checking_number = request.data.get('checking_number')
		organisation.bank_name = request.data.get('bank_name')
		organisation.mfo = request.data.get('mfo')
		organisation.okpo = request.data.get('okpo')
		organisation.inn = request.data.get('inn')
		organisation.nds_number = request.data.get('nds_number')
		organisation.head_full_name = request.data.get('head_full_name')
		organisation.head_position = request.data.get('head_position')
		organisation.accountant_full_name = request.data.get('accountant_full_name')
		organisation.activated = request.data.get('activated')
		organisation.active_till = request.data.get('active_till')
		organisation.save()

		organisation.directions.clear()
		directions = self.request.data['directions']
		for direction in directions:
		 	d = TrainigDirections(**direction)
		 	d.save()
		 	organisation.directions.add(d)
		organisation.save()

		return Response({"message": "Organisation updated"}, status=200)


	# def create(self, request, format=None):
	# 	if request.user.groups.all()[0].name == 'НТЗ':
	# 		return Response({"Message": "You can't create organisation"}, status=200)
	# 	else:
	# 		print('---------------')
	# 		print(request.data.get('directions'))

	# def get_permissions(self):
	# 	if self.request.method == 'GET':
	# 		return [permissions.IsAuthenticated()]
	# 	else:
	# 		return [permissions.IsAdminUser()] #TODO: use custom permission class for Admin|Inspectors
			
class RegulationViewSet(viewsets.ModelViewSet):
	"""
    Return a list of all regulation docs in DB.
    """
	queryset = RegulationDoc.objects.all()
	serializer_class = RegulationSerializer

class CertificateViewSet(viewsets.ModelViewSet):
	"""
    Return a list of all certificates in DB.
    If user from training organisations return list of certificates of this organisation.
    If user from inspectors group return list of certificates exlude drafts status.
    """
	
	#permission_classes = (permissions.IsAuthenticated,)
	queryset = Certificate.objects.order_by('-id')
	serializer_class = CertificateSerializer

	def list(self, request):
		certs = Certificate()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.prefetch_related('directions').prefetch_related('range_numbers').get(organisation_name=request.user.profile.organization_name)
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').filter(trainigOrganisation=trainigOrganisation).order_by('-id')
		elif request.user.groups.all()[0].name == 'Інспектор':
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').exclude(status=0).order_by('-id')
		else:
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').all().order_by('-id')
		serializer = CertificateSerializer(certs, many=True)
		return Response({"certificates": serializer.data})

	def update(self, request, pk, format=None):
		certificate = Certificate.objects.get(id=pk)

		certificate.certf_number = request.data.get('certf_number')
		certificate.form_number =request.data.get('form_number')
		certificate.ntz_number = request.data.get('ntz_number')

		certificate.first_name_en = request.data.get('first_name_en')
		certificate.last_name_en = request.data.get('last_name_en')
		certificate.last_name_ukr = request.data.get('last_name_ukr')
		certificate.first_name_ukr = request.data.get('first_name_ukr')
		certificate.second_name_ukr = request.data.get('second_name_ukr')
		certificate.born = request.data.get('born')
		certificate.inn = request.data.get('inn')

		sailorCount = Sailor.objects.filter(
			first_name_en = request.data.get('first_name_en'),
			last_name_en = request.data.get('last_name_en'),
			last_name_ukr = request.data.get('last_name_ukr'),
			first_name_ukr = request.data.get('first_name_ukr'),
			second_name_ukr = request.data.get('second_name_ukr'),
			born = request.data.get('born'),
		).count()

		print('SAILOR COUNT: ', sailorCount)
		if sailorCount > 1 : #if multiple objects
			sailor = Sailor.objects.filter(
				first_name_en = request.data.get('first_name_en'),
				last_name_en = request.data.get('last_name_en'),
				last_name_ukr = request.data.get('last_name_ukr'),
				first_name_ukr = request.data.get('first_name_ukr'),
				second_name_ukr = request.data.get('second_name_ukr'),
				born = request.data.get('born'),
			).first()
			certificate.sailor = sailor
		else:
			sailor, created = Sailor.objects.get_or_create(
				first_name_en = request.data.get('first_name_en'),
				last_name_en = request.data.get('last_name_en'),
				last_name_ukr = request.data.get('last_name_ukr'),
				first_name_ukr = request.data.get('first_name_ukr'),
				second_name_ukr = request.data.get('second_name_ukr'),
				born = request.data.get('born'),
			)
			if created:
				sailor.save()
			certificate.sailor = sailor

		trainigOrganisation = TrainigOrganisation()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			print("Update: set organisation NTZ")
		else:
			trainigOrganisation = TrainigOrganisation.objects.get(id=request.data.get('trainigOrganisation'))
			print("Update: set organisation ID")
		certificate.trainigOrganisation = trainigOrganisation
		certificate.organisation_name_cert = trainigOrganisation.organisation_name
		certificate.date_of_issue = request.data.get('date_of_issue')
		certificate.valid_date =  request.data.get('valid_date')
		certificate.valid_type = request.data.get('valid_type')
		derection = TrainigDirections.objects.get(id=request.data.get('training_direction'))
		certificate.training_direction = derection
		certificate.direction_title_cert = derection.direction_title
		certificate.direction_level = derection.level
		certificate.direction_allow_functions = derection.allow_functions
		certificate.status = request.data.get('status')

		printSettings, created = CertificatePrintSettings.objects.get_or_create(
			logo_pic = trainigOrganisation.logo_pic,
    		bg_pic = trainigOrganisation.certBg_pic,
    		#sailor_photo
    		organisationNameEng = trainigOrganisation.organisation_name_eng,
    		organisationAdress = trainigOrganisation.mail_adress_ukr,
    		organisationAdressEng = trainigOrganisation.mail_adress_eng,
    		organisationPhone1 = trainigOrganisation.phone1,
    		organisationPhone2 = trainigOrganisation.phone2,
    		organisationEmail = trainigOrganisation.orgnisation_email,
    		organisationSite = trainigOrganisation.site_link,
    		organisationNDSNumber = trainigOrganisation.nds_number,
    		directionTitleEng = derection.direction_title_eng,
    		directionInfoText = derection.infoText,
    		directionInfoTextEng = derection.infoTextEng,
    		directionCourseInfo = derection.courseInfo,
    		directionCourseInfoEng = derection.courseInfoEng,
    		directionRegulationInfo = derection.regulationInfo,
    		directionRegulationInfoEng = derection.regulationInfoEng,
    		directionInspectionInfo = derection.inspectionInfo,
    		directionInspectionInfoEng = derection.inspectionInfoEng,
		)
		if created:
			certificate.printInfo = printSettings

		certificate.save()

		return Response({"Certificate": "Updated"}, status=200)

	def create(self, request, format=None):
		certification = Certificate()
		if request.data.get('inn') is not None:
			dbSailor = Sailor.objects.filter(inn=request.data.get('inn')).first()
			if dbSailor is not None:
				if certification.inn != dbSailor.inn:#???
					sailor = Sailor()
					sailor.first_name_en = request.data.get('first_name_en')
					sailor.last_name_en = request.data.get('last_name_en')
					sailor.last_name_ukr = request.data.get('last_name_ukr')
					sailor.first_name_ukr = request.data.get('first_name_ukr')
					sailor.second_name_ukr = request.data.get('second_name_ukr')
					sailor.born = request.data.get('born')
					sailor.died = request.data.get('died')#?
					sailor.inn = request.data.get('inn')
					sailor.save()
				else:
					sailor = Sailor()
					sailor = dbSailor
					sailor.save()
			else:
				sailor = Sailor()
				sailor.first_name_en = request.data.get('first_name_en')
				sailor.last_name_en = request.data.get('last_name_en')
				sailor.last_name_ukr = request.data.get('last_name_ukr')
				sailor.first_name_ukr = request.data.get('first_name_ukr')
				sailor.second_name_ukr = request.data.get('second_name_ukr')
				sailor.born = request.data.get('born')
				sailor.inn = request.data.get('inn')
				sailor.save()
		else:
			sailor, created = Sailor.objects.get_or_create(
			first_name_en = request.data.get('first_name_en'),
			last_name_en = request.data.get('last_name_en'),
			last_name_ukr = request.data.get('last_name_ukr'),
			first_name_ukr = request.data.get('first_name_ukr'),
			second_name_ukr = request.data.get('second_name_ukr'),
			born = request.data.get('born'),
			)
			if created:
				sailor.save()
		#certification.sailor = sailor#???

		trainigOrganisation = TrainigOrganisation()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		else:
			trainigOrganisation = TrainigOrganisation.objects.get(id=request.data.get('trainigOrganisation'))
		#certification.trainigOrganisation = trainigOrganisation#???
		
		trainigDirection = TrainigDirections.objects.get(id=request.data.get('training_direction'))
		#certification.training_direction = trainigDirection???

		#get or create print settings
		
		certification, created = Certificate.objects.get_or_create(
			first_name_en = request.data.get('first_name_en'),
			last_name_en = request.data.get('last_name_en'),
			last_name_ukr = request.data.get('last_name_ukr'),
			first_name_ukr = request.data.get('first_name_ukr'),
			second_name_ukr = request.data.get('second_name_ukr'),
			born = request.data.get('born'),
			sailor = sailor,
			trainigOrganisation = trainigOrganisation,
			date_of_issue = request.data.get('date_of_issue'),
			valid_date = request.data.get('valid_date'),
			valid_type = request.data.get('valid_type'),
			training_direction = trainigDirection,
			status=request.data.get('status'),
			certf_number=request.data.get('certf_number'),
			form_number=request.data.get('form_number'),
			)
		if created:
			certification.inn = request.data.get('inn')
			certification.organisation_name_cert = trainigOrganisation.organisation_name
			certification.direction_title_cert = trainigDirection.direction_title
			certification.direction_level = trainigDirection.level
			certification.direction_allow_functions = trainigDirection.allow_functions

			printSettings, created = CertificatePrintSettings.objects.get_or_create(
				logo_pic = trainigOrganisation.logo_pic,
    			bg_pic = trainigOrganisation.certBg_pic,
    			#sailor_photo 
    			organisationNameEng = trainigOrganisation.organisation_name_eng,
    			organisationAdress = trainigOrganisation.mail_adress_ukr,
    			organisationAdressEng = trainigOrganisation.mail_adress_eng,
    			organisationPhone1 = trainigOrganisation.phone1,
    			organisationPhone2 = trainigOrganisation.phone2,
    			organisationEmail = trainigOrganisation.orgnisation_email,
    			organisationSite = trainigOrganisation.site_link,
    			organisationNDSNumber = trainigOrganisation.nds_number,
    			directionTitleEng = trainigDirection.direction_title_eng,
    			directionInfoText = trainigDirection.infoText,
    			directionInfoTextEng = trainigDirection.infoTextEng,
    			directionCourseInfo = trainigDirection.courseInfo,
    			directionCourseInfoEng = trainigDirection.courseInfoEng,
    			directionRegulationInfo = trainigDirection.regulationInfo,
    			directionRegulationInfoEng = trainigDirection.regulationInfoEng,
    			directionInspectionInfo = trainigDirection.inspectionInfo,
    			directionInspectionInfoEng = trainigDirection.inspectionInfoEng,
    			)
			if created:#check created dublication (created inside created)
				certification.printInfo = printSettings

			certification.save()
		
		return Response({"message": "Add Certificate"}, status=200)

class CertificatesOfOrganisation(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
    Return a list of organisation certificates.
    Use organisation id for retrieve certificates.
    If user from training organisations return list of certificates of this organisation.
    """
	#serializer = CertificateSerializer
	serializer = CertificateCustomSerializer

	def list(self, request):
		certs = Certificate()
		if request.user.groups.all()[0].name == 'НТЗ':
			#trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
			trainigOrganisation = TrainigOrganisation.objects.prefetch_related('directions').prefetch_related('range_numbers').get(organisation_name=request.user.profile.organization_name)
			#certs = Certificate.objects.filter(trainigOrganisation=trainigOrganisation).select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').order_by('-id')
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').filter(trainigOrganisation=trainigOrganisation).order_by('-id')
			#serializer = CertificateSerializer(certs, many=True)
			serializer = CertificateCustomSerializer(certs, many=True)
			return Response({"certificates": serializer.data})
		else:
			return Response({"Message": "Use organisation id for retrieve certificates"}, status=200)

	def retrieve(self, request, pk):
		if request.user.groups.all()[0].name != 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.get(id=pk)
			#certs = Certificate.objects.filter(trainigOrganisation=trainigOrganisation).select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').exclude(status=0).order_by('-id')
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').exclude(status=0).filter(trainigOrganisation=trainigOrganisation).order_by('-id')
			#serializer = CertificateSerializer(certs, many=True)
			serializer = CertificateCustomSerializer(certs, many=True)
			return Response({"certificates": serializer.data})
		else:
			return Response({"Message": "You can't get certificates of organisation"}, status=200) 

class CertificatesOfTable(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer = CertificateCustomSerializer

	def list(self, request):
		certs = Certificate()
		if request.user.groups.all()[0].name == 'НТЗ':
			trainigOrganisation = TrainigOrganisation.objects.prefetch_related('directions').prefetch_related('range_numbers').get(organisation_name=request.user.profile.organization_name)
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').filter(trainigOrganisation=trainigOrganisation).order_by('-id')
		elif request.user.groups.all()[0].name == 'Інспектор':
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').exclude(status=0).order_by('-id')
		else:
			certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').all().order_by('-id')
		serializer = CertificateCustomSerializer(certs, many=True)
		return Response({"certificates": serializer.data})
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
def dashInfoStat(request):
	profile, created = Profile.objects.get_or_create(user=request.user)
	dashDataArr = []
	if request.user.groups.all()[0].name == 'НТЗ':
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
		#trainigOrganisations = list(TrainigOrganisation.objects.all().values())
		trainigOrganisations = TrainigOrganisation.objects.all().prefetch_related('directions').prefetch_related('range_numbers')
		organisationDataArr = []
	
		for organisation in trainigOrganisations:
			organisationData = {
				'id': organisation.id,
				'organisation_id': organisation.organisation_id,
				'organisation_name': organisation.organisation_name,
				'organisation_activated': organisation.activated,
				'organisation_active_till': organisation.active_till,
				'organisation_allCertsInReviewCount': organisation.get_certInReview().count(),
			}
			organisationDataArr.append(organisationData)
		
		dashData = {
			'sailorsCount': sailorsCount,
			'certCount': certCount,
			'trainigDirectionsCount': trainigDirectionsCount,
			'certsInReviewCount': certsInReviewCount,
			'trainigOrganisations': organisationDataArr,
		}
		dashDataArr.append(dashData)
		dashInfoDict = {'dashInfo': dashDataArr,}
		# dashInfoDict = {'dashInfo': dashData,}#'trainigOrganisations': trainigOrganisations,}
		return JsonResponse(dashInfoDict)

@login_required(login_url="login/")
def trainingOrganisationsInfo(request):
	trainigOrganisations = TrainigOrganisation.objects.all().prefetch_related('directions').prefetch_related('range_numbers')
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
			certsLeftCount = 0 #direction.range_numbers.count()
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
		'id': organisation.id,
		'organisation_id': organisation.organisation_id,
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
			certsLeftCount = 0#direction.range_numbers.count()
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
def organisationDirectionsStat(request):
	orgID = request.GET.get('orgID')
	trainigOrganisation = TrainigOrganisation.objects.get(id=orgID)
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
		certsLeftCount = 0 #direction.range_numbers.count()
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
	data = {'organisation_directions': directionsDataArr,}
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
	hasError = False
	errorMessage = "No Error"
	if request.user.groups.all()[0].name == 'НТЗ':
		trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=request.user.profile.organization_name)
		#print(trainigOrganisation.directions.get(id=trainingDirID))
		direction = trainigOrganisation.directions.get(id=trainingDirID)
		#print('Direction Status:')
		direction.status = dirStatus
		direction.save()
	else:
		hasError = False
		errorMessage = "Not Training Organisation"
	data = {
		'error' : hasError,
		'error_message' : errorMessage,
	}
	return JsonResponse(data)

@login_required(login_url="login/")
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
def setRangeNumbers(request):
	certIDsList = request.GET.get('certIDs').split(',')
	hasError = False
	errorMessage = "No Error"
	if certIDsList != '':
		certsInChange = Certificate.objects.filter(pk__in=certIDsList)
		for cert in certsInChange:
			print('----------------------')
			print('Cert ID: ', cert.id)
			print('Cert organisation ID: ', cert.trainigOrganisation.id)
			print('Cert direction ID: ', cert.training_direction.id)
			rangeNumber = RangeNumber.objects.filter(organisation_id =  cert.trainigOrganisation.id, direction_id = cert.training_direction.id).first()
			if rangeNumber:
				if cert.certf_number == '' or cert.certf_number == None:
					print('Range number: ', rangeNumber.number)
					cert.certf_number = rangeNumber.number
					cert.save()
					org = TrainigOrganisation.objects.get(id = cert.trainigOrganisation.id)
					org.range_numbers.remove(rangeNumber)
					rangeNumber.delete()
				else:
					print('Cert already has number')
			else:
				print('Organisation range is empty for this direction')
			
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
			return HttpResponse(status=204)
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


def printCertificate(request, certID):
	cert = Certificate.objects.get(id=certID)
	organisationLogoURLStr = cert.trainigOrganisation.logo_pic
	organisationBgImgURLStr = cert.trainigOrganisation.certBg_pic
	organisationNameStr = cert.trainigOrganisation.organisation_name
	organisationNameEngStr = cert.trainigOrganisation.organisation_name_eng
	organisationAdressStr = cert.trainigOrganisation.mail_adress_ukr
	organisationAdressEngStr = cert.trainigOrganisation.mail_adress_eng
	organisationPhone1Field = ''
	if cert.trainigOrganisation.phone1:
		organisationPhone1Field = cert.trainigOrganisation.phone1.split(';')
	organisationPhone2Str = cert.trainigOrganisation.phone2
	organisationEmailStr = cert.trainigOrganisation.orgnisation_email
	organisationSiteStr = cert.trainigOrganisation.site_link
	organisationNumberStr = cert.trainigOrganisation.nds_number
	organisationContractNumberStr = cert.trainigOrganisation.contract_number
	organisationContractNumberDateStr = cert.trainigOrganisation.contract_number_date
	sailorPhotoURLStr = cert.sailor.photo
	sailorNameStr = cert.last_name_ukr + ' ' + cert.first_name_ukr + ' ' + cert.second_name_ukr
	sailorNameEngStr = cert.first_name_en + ' ' + cert.last_name_en
	sailorBirthdayStr = cert.born
	directionTitleStr = cert.training_direction.direction_title
	directionTitleEngStr = cert.training_direction.direction_title_eng
	directionInfoTextStr = cert.training_direction.infoText
	directionInfoTextEngStr = cert.training_direction.infoTextEng
	directionCourseInfoStr = cert.training_direction.courseInfo
	directionCourseInfoEngStr = cert.training_direction.courseInfoEng
	directionRegulationInfoStr = cert.training_direction.regulationInfo
	directionRegulationInfoEngStr = cert.training_direction.regulationInfoEng
	directionInspectionInfoField = ''
	if cert.training_direction.inspectionInfo:
		directionInspectionInfoField = cert.training_direction.inspectionInfo.split('<br>')
	directionInspectionInfoEngField = ''
	if cert.training_direction.inspectionInfoEng:
		directionInspectionInfoEngField = cert.training_direction.inspectionInfoEng.split('<br>')
	dateIssueStr = cert.date_of_issue
	validDateStr = cert.valid_date

	# String which represent the QR code 
	s = "http://127.0.0.1:8000/mariner/api/printCertificate/" + certID + '/'
	# Generate QR code 
	url = pyqrcode.create(s)
 
	# Create and save the png file naming "myqr.png"
	#url.png('swallow.png', scale=5)
	qrfilename = 'media/qrcodes/qrCertID' + certID + '.png'
	url.png(qrfilename, scale=7)

	context = {'organisationLogoURL': organisationLogoURLStr,
		'organisationBgImgURL': organisationBgImgURLStr,
		'organisationName': organisationNameStr,
		'organisationNameEng': organisationNameEngStr,
		'organisationAdress': organisationAdressStr,
		'organisationAdressEng': organisationAdressEngStr,
		'organisationPhone1': organisationPhone1Field,
		'organisationPhone2': organisationPhone2Str,
		'organisationEmail': organisationEmailStr,
		'organisationSite': organisationSiteStr,
		'organisationNumber': organisationNumberStr,
		'organisationContractNumber': organisationContractNumberStr,
		'organisationContractNumberDate': organisationContractNumberDateStr,
		'sailorPhotoURL':sailorPhotoURLStr,
		'sailorName': sailorNameStr,
		'sailorNameEng': sailorNameEngStr,
		'sailorBirthday': sailorBirthdayStr,
		'directionTitle': directionTitleStr,
		'directionTitleEng': directionTitleEngStr,
		'directionInfoText': directionInfoTextStr,
		'directionInfoTextEng': directionInfoTextEngStr,
		'directionCourseInfo': directionCourseInfoStr,
		'directionCourseInfoEng': directionCourseInfoEngStr,
		'directionRegulationInfo': directionRegulationInfoStr,
		'directionRegulationInfoEng': directionRegulationInfoEngStr,
		'directionInspectionInfo': directionInspectionInfoField,
		'directionInspectionInfoEng': directionInspectionInfoEngField,
		'dateIssue': dateIssueStr,
		'validDate': validDateStr,
		'qrImg': qrfilename}

	return render(request, "certificate_general.html", context)

@login_required(login_url="login/")
def updateCertForTable(request):
	certs = Certificate.objects.select_related('sailor').select_related('trainigOrganisation').select_related('training_direction').all().order_by('-id')
	#certs = Certificate.objects.all()

	for cert in certs:
		cert.direction_title_cert = cert.training_direction.direction_title
		cert.organisation_name_cert = cert.trainigOrganisation.organisation_name
		cert.save()
	return HttpResponse(status=204)

@login_required(login_url="login/")
def uploadSailorPhoto(request):
	sailor = Sailor()
	sailorCount = Sailor.objects.filter(
			first_name_en = request.POST.get('first_name_en'),
			last_name_en = request.POST.get('last_name_en'),
			last_name_ukr = request.POST.get('last_name_ukr'),
			first_name_ukr = request.POST.get('first_name_ukr'),
			second_name_ukr = request.POST.get('second_name_ukr'),
			born = request.POST.get('born'),
		).count()

	if sailorCount > 1 : #if multiple objects
		sailor = Sailor.objects.filter(
			first_name_en = request.POST.get('first_name_en'),
			last_name_en = request.POST.get('last_name_en'),
			last_name_ukr = request.POST.get('last_name_ukr'),
			first_name_ukr = request.POST.get('first_name_ukr'),
			second_name_ukr = request.POST.get('second_name_ukr'),
			born = request.POST.get('born'),
		).first()
	else:
		sailor = Sailor.objects.get(
			first_name_en = request.POST.get('first_name_en'),
			last_name_en = request.POST.get('last_name_en'),
			last_name_ukr = request.POST.get('last_name_ukr'),
			first_name_ukr = request.POST.get('first_name_ukr'),
			second_name_ukr = request.POST.get('second_name_ukr'),
			born = request.POST.get('born'),
		)

	if request.POST.get('sailorPhoto') is not '':
		photoFile = request.FILES['sailorPhoto']
		photoFileName = request.POST.get('first_name_en') + request.POST.get('last_name_en') + request.POST.get('born') + '.png'
		sailor.photo.save(photoFileName, photoFile, save=True)
		sailor.save()

	return HttpResponse(status=200)

def uploadOrganisationLogo(request):
	organisationID = request.POST.get('orgID')
	organisation = TrainigOrganisation.objects.get(id=organisationID)

	if request.POST.get('logo_pic') is not '':
		logo_file = request.FILES['logo_pic']
		file_name = organisationID + '-logo.png'
		organisation.logo_pic.save(file_name, logo_file, save=True)
		organisation.save()

	if request.POST.get('certBg_pic') is not '':
		print('SAVE BG:')
		bg_file = request.FILES['certBg_pic']
		bgfile_name = organisationID + '-bglogo.png'
		organisation.certBg_pic.save(bgfile_name, bg_file, save=True)
		organisation.save()
	
	return HttpResponse(status=200)

def uploadRegulationPDF(request):
	regDocNumber = request.POST.get('docNumber')
	regDoc = RegulationDoc.objects.get(number=regDocNumber)

	if request.POST.get('docPDF') is not '':
		regFile = request.FILES['docPDF']
		regFileName = regDocID + '.pdf'
		regDoc.pdf_file.save(regFileName, regFile, save=True)
		regDoc.save()

	return HttpResponse(status=200)
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