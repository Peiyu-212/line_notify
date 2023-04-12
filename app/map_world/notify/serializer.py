from rest_framework import serializers

class SelectNationSerializer(serializers.Serializer):

    nation = serializers.CharField()
    