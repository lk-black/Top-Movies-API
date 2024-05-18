"""
Serializers para movie API views. 
"""
from rest_framework import serializers


class MoviesSerializer(serializers.Serializer):
    """Serializa os resultados do movies API."""
    
    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.URLField()
    poster = serializers.CharField()
    