from django.db import models
from datetime import date, time


class FitnessClass(models.Model):
    """
    Represents a type of fitness class, like Yoga or Zumba.
    """
    class_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    instructor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_type} by {self.instructor}"


class Slot(models.Model):
    """
    Represents a scheduled time for a fitness class.
    Each slot is linked to a FitnessClass and can have multiple bookings.
    """
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default=time(7, 0))  # 07:00 AM
    end_time = models.TimeField(default=time(8, 0))    # 08:00 AM

    def __str__(self):
        return f"{self.fitness_class.class_type} on {self.date} at {self.start_time}"

    @property
    def available_slots(self):
        """
        Calculates remaining available slots based on class capacity and confirmed bookings.
        """
        confirmed_bookings = self.bookings.filter(status='confirmed').count()
        return self.fitness_class.capacity - confirmed_bookings


class Client(models.Model):
    """
    Represents a client who can book classes.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    """
    Represents a client's booking for a slot.
    """
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'slot')  # A client can only book the same slot once

    def __str__(self):
        return f"{self.client.name} booked {self.slot} [{self.status}]"
