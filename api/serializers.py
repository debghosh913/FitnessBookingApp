from rest_framework import serializers
from .models import FitnessClass, Slot, Booking, Client
from django.db import transaction
from django.utils.timezone import now
from django.db.models import Q



class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'date', 'start_time', 'end_time', 'available_slots']


class FitnessClassSerializer(serializers.ModelSerializer):
    slots = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'class_type', 'instructor', 'slots']

    def get_slots(self, obj):
        current = now()
        today = current.date()
        current_time = current.time()
        upcoming_slots = obj.slots.filter(
            Q(date__gt=today) |
            Q(date=today, start_time__gte=current_time)
        ).order_by('date', 'start_time')

        return SlotSerializer(upcoming_slots, many=True).data


class BookingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(write_only=True)
    client_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'slot', 'client_name', 'client_email', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def create(self, validated_data):
        client_name = validated_data.pop('client_name')
        client_email = validated_data.pop('client_email')
        slot = validated_data['slot']

        # Create or get client
        client, _ = Client.objects.get_or_create(email=client_email, defaults={'name': client_name})

        # Prevent duplicate booking
        if Booking.objects.filter(client=client, slot=slot).exists():
            raise serializers.ValidationError("You already booked this slot.")

        with transaction.atomic():
            # Lock slot row to prevent race condition
            slot = Slot.objects.select_for_update().get(pk=slot.pk)

            # Recheck availability after locking
            if slot.available_slots <= 0:
                return Booking.objects.create(client=client, slot=slot, status='failed')

            # Create confirmed booking
            return Booking.objects.create(client=client, slot=slot, status='confirmed')
