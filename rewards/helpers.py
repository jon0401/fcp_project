from datetime import *
from django.utils import timezone

def calculate_expiry_datetime():
    return timezone.now() + timedelta(days=120)