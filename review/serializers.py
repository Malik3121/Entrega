
# reviews/serializers.py
from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # A serializer for the user model
    class Meta:
        model = get_user_model()
        fields = ("email", "name", "is_worker")

class ReviewSerializer(serializers.ModelSerializer):
    # A serializer for the review model
    customer = UserSerializer(read_only=True) # Show the customer details
    worker = UserSerializer(read_only=True) # Show the worker details

    class Meta:
        model = Review
        fields = ("id", "customer", "worker", "rating", "feedback", "created")