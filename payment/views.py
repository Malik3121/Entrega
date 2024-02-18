# views.py
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import stripe
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            price = request.data.get('price')
            token = request.data.get('token')

            stripe.PaymentIntent.create(
                price=price,
                currency='usd',
                payment_method=token,
                confirmation_method='manual',
                confirm=True,
            )

            payment = Payment.objects.create(user=user, price=price)
            serializer = PaymentSerializer(payment)

            return Response(serializer.data, status=200)
        except Exception:
            return Response(status=400)
