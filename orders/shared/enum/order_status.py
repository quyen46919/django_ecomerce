from enum import Enum, unique, Flag
from django.db import models  

class OrderStatusEnum(models.TextChoices):
  ORDERED = 'ordered',
  PENDING = 'pending',
  DELIVERY = 'delivery',
  SHIPPING = 'shipping',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
