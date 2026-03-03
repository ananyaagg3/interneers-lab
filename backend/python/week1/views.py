from django.http import JsonResponse
from .weather_service import get_weather

def weather_view(request):
    city = request.GET.get("city")

    if not city:
        return JsonResponse({"error": "City parameter is required"}, status=400)

    data = get_weather(city)
    return JsonResponse(data)