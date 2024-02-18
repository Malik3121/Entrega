# reviews/models.py
from django.db import models
from django.conf import settings

class Review(models.Model):
    # A review model that stores the rating and feedback of a customer for a worker
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews_received", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # A rating from 1 to 10
    feedback = models.TextField(blank=True, null=True) # An optional feedback text
    created = models.DateTimeField(auto_now_add=True) # The date and time of the review creation

    class Meta:
        ordering = ("-created",) # Order by the most recent reviews

    def __str__(self):
        return f"{self.customer} rated {self.worker} {self.rating}/10"




