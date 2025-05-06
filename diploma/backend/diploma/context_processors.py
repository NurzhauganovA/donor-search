def active_page(request):
    path = request.path_info
    parts = path.strip('/').split('/')

    if len(parts) > 1 and parts[0] in ["en", "ru", "kk"]:
        active_url = '/'.join(parts[1:])
    else:
        active_url = path

    print("Active URL:", active_url)

    return {
        "active_page": active_url,
        "find_donor": active_url.startswith('urgently-need-donor/search'),
        "is_urgently_need_donor_detail": active_url.startswith('urgently-need-donor/'),
        "is_schedule_blood_donation": active_url.startswith('schedule-blood-donation/'),
        "bloodstations_city": active_url.startswith('bloodstations/'),
        "LANGUAGE_CODE": request.LANGUAGE_CODE,
    }
