from django.db import models
from django.contrib.auth.models import User

class Advisory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    issued_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-issued_date']

class AgroAdvisory(models.Model):
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE, related_name='agro_advisories')
    crop = models.CharField(max_length=100)
    pest = models.CharField(max_length=100, blank=True)
    advice = models.TextField()

    def __str__(self):
        return f"{self.crop} - {self.advice[:50]}"