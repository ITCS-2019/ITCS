from rest_framework import serializers
from mariner.models import Certificate, TrainigOrganisation, TrainigDirections, Sailor

class TrainigDirectionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrainigDirections
		fields = ("price_id", "direction_title", "level", "allow_functions", "price")

class CertificatesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Certificate
		depth = 1
		fields = ("certf_number", "form_number", "ntz_number", "sailor", "trainigOrganisation", "training_direction")