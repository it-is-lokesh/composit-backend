from rest_framework import serializers
from userdashboard.models import userDashboard


class userDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = userDashboard
        fields = '__all__'