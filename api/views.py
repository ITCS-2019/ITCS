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