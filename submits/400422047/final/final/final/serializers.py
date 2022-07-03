from rest_framework import serializers


class YegInputSerializer(serializers.Serializer):
    text = serializers.CharField()
    num_1 = serializers.IntegerField()
    num_2 = serializers.IntegerField()