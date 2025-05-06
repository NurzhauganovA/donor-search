import json

from django.db.models import Count
from django.shortcuts import render

from authorization.models import User
from django.http import JsonResponse

from django.db.models import Value
from django.db.models.functions import Lower

from blood.models import DonationCenterRequests, BloodDonorCenter, DONOR_BLOOD_TYPES, BLOOD_GROUPS, Donor, DonorAdvice, UrgentDonorRequest, UrgentDonorRequestHistory, Donate


def home(request):
    blood_donation_centers = BloodDonorCenter.objects.all()
    donor_advices = DonorAdvice.objects.all()

    context = {
        'donor_advices': donor_advices,
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
    blood_groups = [
        {
            "key": blood_group[0],
            "value": blood_group[1]
        }
        for blood_group in BLOOD_GROUPS
    ]
    blood_donation_center = BloodDonorCenter.objects.get(pk=pk)
    all_blood_donation_centers = BloodDonorCenter.objects.all()

    context = {
        'blood_donation_center': blood_donation_center,
        'blood_types': blood_types,
        'blood_groups': blood_groups,
        'all_blood_donation_centers': all_blood_donation_centers,
    }

    return render(request, 'dashboard/schedule_blood_donation.html', context)


def how_become_donor(request):
    context = {}

    return render(request, 'dashboard/how_become_donor.html', context)


def where_donate_blood(request):
    unique_cities = BloodDonorCenter.objects.order_by(Lower('city')).values('city', 'country').distinct()
    count_bloodstations = BloodDonorCenter.objects.count()
    blood_donation_centers = BloodDonorCenter.objects.all()

    context = {
        "unique_cities": list(unique_cities),
        "count_bloodstations": count_bloodstations,
        "blood_donation_centers": blood_donation_centers
    }

    return render(request, 'dashboard/where_donate_blood.html', context)


def base_requirements(request):
    context = {}

    return render(request, 'dashboard/base_requirements.html', context)


def bloodstations_detail_city(request, city_name):
    blood_donation_centers = BloodDonorCenter.objects.filter(city=city_name)
    unique_cities = BloodDonorCenter.objects.order_by(Lower('city')).values('city', 'country').distinct()
    count_bloodstations = BloodDonorCenter.objects.filter(city=city_name).count()

    context = {
        "blood_donation_centers": blood_donation_centers,
        "count_bloodstations": count_bloodstations,
        "unique_cities": unique_cities
    }

    return render(request, 'dashboard/bloodstations_detail_city.html', context)


def urgently_need_donor(request):
    urgently_donor_needs = UrgentDonorRequest.objects.all()

    context = {
        "urgently_donor_needs": urgently_donor_needs
    }

    return render(request, 'dashboard/urgently_need_donor.html', context)


def search_urgently_need_donor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        blood_group = data.get("bloodGroup")
        city = data.get("city")
        blood_component = data.get("bloodComponent")

        if not all([blood_group, city, blood_component]):
            return JsonResponse({"success": False, "error": "All fields are required"}, status=400)

        donation_requests = DonationCenterRequests.objects.filter(
            blood_group=blood_group,
            city=city,
            blood_components=blood_component
        ).annotate(donation_count=Count('donation_center__donor')).order_by('-donation_count')

        result = [
            {
                "id": request.id,
                "blood_group": request.blood_group,
                "blood_component": request.blood_components,
                "donor_count": request.donor_count,
                "city": request.city,
                "donation_count": request.donation_count
            }
            for request in donation_requests
        ]

        return JsonResponse({"success": True, "data": result})
    else:
        return render(request, 'dashboard/search_urgently_donor.html')


def urgently_donor_detail(request, pk):
    urgently_donor_needs = UrgentDonorRequest.objects.all()
    donor_need = UrgentDonorRequest.objects.get(pk=pk)

    context = {
        "urgently_donor_needs": urgently_donor_needs,
        "donor_need": donor_need,
    }

    return render(request, 'dashboard/urgently_donor_detail.html', context)


def schedule_request_blood_donation(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)

        UrgentDonorRequestHistory.objects.create(
            urgent_donor_request=UrgentDonorRequest.objects.get(pk=pk),
            donor=request.user,
            donation_date=data.get('donationDate')
        )

        return JsonResponse({"success": True, "status": 200})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method", "status": 405}, status=405)


def create_urgently_donor_request(request):
    if request.method == 'POST':
        # form data
        data = request.POST

        blood_components = data.get('blood_components')
        blood_group = data.get('blood_group')
        donor_count = data.get('donor_count')
        city = data.get('city')
        center = data.get('center')
        deadline = data.get('deadline')
        last_name = data.get('last_name')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        birth_date = data.get('birth_date')
        reason = data.get('reason')
        photo = request.FILES.get('photo')

        UrgentDonorRequest.objects.create(
            blood_components=blood_components,
            blood_group=blood_group,
            donor_count=donor_count,
            city=city,
            center=BloodDonorCenter.objects.get(pk=int(center)),
            deadline=deadline,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=birth_date,
            reason=reason,
            photo=photo
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "This endpoint is not implemented yet"}, status=501)


def create_donation_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Получаем данные из запроса
        donation_type = data.get("donationType")
        planned_date = data.get("plannedDate")
        donation_blood_group = data.get("donationBloodGroup")
        donation_category = data.get("donationGroup")
        city = data.get("city")
        blood_center_id = data.get("bloodCenter")

        if not all([donation_type, planned_date, donation_category, city, blood_center_id]):
            return JsonResponse({"success": False, "error": "All fields are required"}, status=400)

        Donor.objects.create(
            author=request.user,
            donation_center=BloodDonorCenter.objects.get(pk=blood_center_id),
            blood_group=donation_blood_group,
            blood_type=donation_type,
            donation_type=donation_category,
            last_donation_date=planned_date,
        )
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


def get_unique_cities(request):
    cities = BloodDonorCenter.objects.values_list('city', flat=True).distinct()
    unique_cities = list(set(cities))
    return JsonResponse({"cities": unique_cities})


def get_blood_donation_centers_by_city(request):
    city = request.GET.get('city')
    blood_donation_centers = BloodDonorCenter.objects.filter(city=city).values('id', 'name')
    return JsonResponse({"centers": list(blood_donation_centers)})


def donate(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        Donate.objects.create(
            frequency=data.get('frequency'),
            amount=data.get('amount'),
            hideAmount=data.get('hideAmount'),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            hideFio=data.get('hideFio'),
            comment=data.get('comment')
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)