from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

# GET /api/classes/
class FitnessClassListView(generics.ListAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

# POST /api/book/
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

# GET /api/bookings/?email=
@api_view(['GET'])
def client_bookings(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)

    bookings = Booking.objects.filter(client__email=email).select_related('slot', 'slot__fitness_class')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

