from rest_framework import serializers
from mariner.models import Certificate, TrainigOrganisation, TrainigDirections, Sailor

class TrainigDirectionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = TrainigDirections
		fields = ("price_id", "direction_title", "level", "allow_functions", "price")
