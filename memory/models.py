from django.db import models

class Memory(models.Model):
    key=models.CharField(max_length=255,unique=True)
    value=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.key}:{self.value}'
    
class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    phone_number = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.name}"
            f" - "
            f"{self.phone_number}"
        )