from django.contrib import admin
from .models import *


admin.site.register(BloodDonorCenter)
admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Donation)
admin.site.register(DonationCenterRequests)
admin.site.register(DonorAdvice)
admin.site.register(UrgentDonorRequest)
admin.site.register(UrgentDonorRequestHistory)
admin.site.register(Donate)