from rest_framework import serializers
from webapp.models import CustomUser


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
