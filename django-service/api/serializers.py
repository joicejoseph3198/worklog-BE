from rest_framework import serializers
from .models import Task, Notes


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user_id', 'title', 'description', 'tag', 'date']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'tag': {'required': False, 'allow_blank': True},
        }

class TaskResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'tag', 'date', 'ticked']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'tag': {'required': False, 'allow_blank': True},
        }

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user_id','title', 'description', 'tag', 'date', 'ticked']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'tag': {'required': False, 'allow_blank': True},
        }

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'user_id', 'date', 'body']
        extra_kwargs = {
            'body': {'required': False, 'allow_blank': True},
        }