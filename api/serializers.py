from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

from mariner.models import Certificate, TrainigOrganisation, RangeNumber, TrainigDirections, Sailor
from regulations.models import RegulationDoc
from accounts.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('organization_name',)

class UserSerializer(serializers.ModelSerializer):
	full_name = serializers.CharField(source='get_full_name')
	profile = ProfileSerializer(required=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'full_name', 'is_active', 'profile', )

	# def get_links(self, obj):
	# 	request = self.context['request']
	# 	return {
	# 		'self': reverse('user-detail', kwargs={'pk': obj.pk},
	# 			request=request),
	# 	}

	# def get_links(self, obj):
	# 	request = self.context['request']
	# 	username = obj.get_username()
	# 	return {
	# 		'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username},
	# 			request=request),
	# 	}

class MariloggerSerializer(serializers.Serializer):
	message = serializers.models.TextField()
	date = serializers.DateTimeField()
	action_username = serializers.CharField()

class SailorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sailor
		fields = (
			'id',
			'first_name_en',
			'last_name_en',
			'last_name_ukr',
			'first_name_ukr',
			'second_name_ukr',
			'born',
			'died',
			'inn',
			'sex',
			'passport_serie',
			'passport_number',
		)

class SailorCustomSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	first_name_en = serializers.CharField()
	last_name_ukr = serializers.CharField()
	last_name_ukr = serializers.CharField()
	first_name_ukr = serializers.CharField()
	second_name_ukr = serializers.CharField()
	born = serializers.DateField()
	died = serializers.DateField()
	inn = serializers.CharField()
	sex = serializers.IntegerField()
	passport_serie = serializers.CharField()
	passport_number = serializers.CharField()

class TrainigDirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrainigDirections
		fields = (
			'id',
			'price_id',
			'direction_title',
			'direction_title_eng',
			'level',
			'allow_functions',
			'price',
			'status',
			'infoText',
			'infoTextEng',
			'courseInfo',
			'courseInfoEng',
			'regulationInfo',
			'regulationInfoEng',
			'inspectionInfo',
			'inspectionInfoEng',
		)

class TrainigDirectionCustomSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	price_id = serializers.IntegerField()
	direction_title = serializers.CharField()
	direction_title_eng = serializers.CharField()
	level = serializers.CharField()
	allow_functions = serializers.CharField()
	price = serializers.IntegerField()
	status = serializers.IntegerField()
	infoText = serializers.models.TextField()
	infoTextEng = serializers.models.TextField()
	courseInfo = serializers.models.TextField()
	courseInfoEng = serializers.models.TextField()
	regulationInfo = serializers.models.TextField()
	regulationInfoEng = serializers.models.TextField()
	inspectionInfo = serializers.models.TextField()
	inspectionInfoEng = serializers.models.TextField()


class RangeNumberSerializer(serializers.ModelSerializer):
	class Meta:
		model = RangeNumber
		fields = (
			'id',
			'number',
			'organisation_id',
			'organisation_name',
			'direction_id',
			'direction_name',
		)
class RangeSerializer(serializers.ModelSerializer):
	startRange = serializers.IntegerField(max_value=None, min_value=None) 
	endRange = serializers.IntegerField(max_value=None, min_value=None)
	class Meta:
		model = RangeNumber
		fields = (
			'organisation_id',
			'direction_id',
			'startRange',
			'endRange',
		)

class TrainigOrganisationCustomSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	organisation_id = serializers.CharField()
	logo_pic = serializers.ImageField()
	certBg_pic = serializers.ImageField()
	organisation_name = serializers.CharField()
	organisation_name_eng = serializers.CharField()
	mail_adress_ukr = serializers.CharField()
	mail_adress_eng = serializers.CharField()
	phone1 = serializers.CharField()
	phone2 = serializers.CharField()
	orgnisation_email = serializers.CharField()
	site_link = serializers.CharField()
	contract_number = serializers.CharField()
	contract_number_date = serializers.DateField()
	checking_number = serializers.CharField()
	bank_name = serializers.CharField()
	mfo = serializers.CharField()
	okpo = serializers.CharField()
	inn = serializers.CharField()
	nds_number = serializers.CharField()
	head_full_name = serializers.CharField()
	head_position = serializers.CharField()
	accountant_full_name = serializers.CharField()
	activated = serializers.DateField()
	active_till = serializers.DateField()
	directions = TrainigDirectionSerializer(many=True)
	range_numbers = RangeNumberSerializer(many=True)

class TrainigOrganisationSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = TrainigOrganisation
		depth = 1
		fields = (
			'id',
			'organisation_id',
			'logo_pic',
			'certBg_pic',
			'organisation_name',
			'organisation_name_eng',
			'mail_adress_ukr',
			'mail_adress_eng',
			'phone1',
			'phone2',
			'orgnisation_email',
			'site_link',
			'contract_number',
			'contract_number_date',
			'checking_number',
			'bank_name',
			'mfo',
			'okpo',
			'inn',
			'nds_number',
			'head_full_name',
			'head_position',
			'accountant_full_name',
			'activated',
			'active_till',
			'directions',
			'range_numbers',
		)


class CertificateCustomSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	certf_number = serializers.CharField()
	form_number = serializers.CharField()
	#ntz_number = serializers.CharField()
	#first_name_en = serializers.CharField()
	#last_name_en = serializers.CharField()
	last_name_ukr = serializers.CharField()
	first_name_ukr = serializers.CharField()
	second_name_ukr = serializers.CharField()
	born = serializers.DateField()
	#inn = serializers.CharField()
	#sailor = SailorSerializer()
	#trainigOrganisation = TrainigOrganisationSerializer()
	organisation_name_cert = serializers.CharField()
	date_of_issue = serializers.DateField()
	valid_date = serializers.DateField()
	#valid_type = serializers.IntegerField()
	direction_level = serializers.CharField()
	direction_allow_functions = serializers.CharField()
	#training_direction = TrainigDirectionSerializer()
	direction_title_cert = serializers.CharField()
	status = serializers.IntegerField()

	
class CertificateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Certificate
		depth = 1
		fields = (
			'id', 
			'certf_number', 
			'form_number', 
			'ntz_number',
			'first_name_en',
			'last_name_en',
			'last_name_ukr',
			'first_name_ukr',
			'second_name_ukr',
			'born',
			'inn',
			'passport_serie',
			'passport_number',
			'sailor',
			'trainigOrganisation',
			'date_of_issue',
			'valid_date',
			'valid_type',
			'training_direction',
			'status', 
		)

	# def get_links(self, obj):
	# 	request = self.context['request']
	# 	return {
	# 		'self': reverse('certificate-detail', kwargs={'pk': obj.pk},
	# 			request=request),
	# 	}
class RegulationSerializer(serializers.ModelSerializer):
	class Meta:
		model = RegulationDoc
		fields = (
			'date_activation',
			'number',
			'title',
			'status',
			'text',
			'pdf_file',
			'user',
			'prev_version',
			'organisation',
			'regulation_organization_link',
		)
