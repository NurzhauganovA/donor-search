import json

from django.db.models import Count
from django.shortcuts import render

from authorization.models import User
from django.http import JsonResponse

from blood.models import DonationCenterRequests, BloodDonorCenter, DONOR_BLOOD_TYPES


def home(request):
    blood_donation_centers = BloodDonorCenter.objects.all()

    context = {
        'blood_donation_centers': blood_donation_centers
    }

    return render(request, 'dashboard/home.html', context)


def schedule_blood_donation(request, pk):
    blood_types = [
        {
            "key": blood_type[0],
            "value": blood_type[1]
        }
        for blood_type in DONOR_BLOOD_TYPES
    ]
    blood_donation_center = BloodDonorCenter.objects.get(pk=pk)
    all_blood_donation_centers = BloodDonorCenter.objects.all()

    context = {
        'blood_donation_center': blood_donation_center,
        'blood_types': blood_types,
        'all_blood_donation_centers': all_blood_donation_centers,
    }

    return render(request, 'dashboard/schedule_blood_donation.html', context)


def create_donation_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Получаем данные из запроса
        donation_type = data.get("donationType")
        planned_date = data.get("plannedDate")
        donation_category = data.get("donationGroup")
        city = data.get("city")
        blood_center_id = data.get("bloodCenter")

        if not all([donation_type, planned_date, donation_category, city, blood_center_id]):
            return JsonResponse({"success": False, "error": "All fields are required"}, status=400)

        DonationCenterRequests.objects.create(
            center=BloodDonorCenter.objects.get(pk=blood_center_id),
            donor_blood_type=donation_type,
            donor_type=donation_category,
            planned_date=planned_date,
            count=1
        )
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)