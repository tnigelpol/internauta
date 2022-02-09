from rest_framework import serializers
from .models import Text, Dictionary

class TextSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Text
        fields = ['title', 'subtitle', 'author', 'text', 'id', 'username']

    def get_username(self, obj):
        return obj.user.username

class DictionarySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Dictionary
        fields = ['word', 'synonym', 'translation']

    def get_username(self, obj):
        return obj.user.username


    

