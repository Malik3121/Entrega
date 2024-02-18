# reviews/views.py
from rest_framework import generics, permissions, viewsets
from .models import Review
from .serializers import ReviewSerializer
from django.contrib.auth import get_user_model

class ReviewViewSet(viewsets.ModelViewSet):
    # A viewset for the review model
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Set the customer to the current user
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        # Filter the reviews by the worker or the customer
        queryset = super().get_queryset()
        worker = self.request.query_params.get("worker")
        customer = self.request.query_params.get("customer")
        if worker:
            queryset = queryset.filter(worker__email=worker)
        if customer:
            queryset = queryset.filter(customer__email=customer)
        return queryset