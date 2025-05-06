from django.db import models

from authorization.models import User

BLOOD_GROUPS = (
    ('0plus', '0(I) Rh+'),
    ('0minus', '0(I) Rh-'),
    ('Aplus', 'A(II) Rh+'),
    ('Aminus', 'A(II) Rh-'),
    ('Bplus', 'B(III) Rh+'),
    ('Bminus', 'B(III) Rh-'),
    ('ABplus', 'AB(IV) Rh+'),
    ('ABminus', 'AB(IV) Rh-'),
)

DONOR_BLOOD_TYPES = (
    ('WB', 'Whole Blood'),
    ('PS', 'Plasma'),
    ('PL', 'Platelets'),
    ('ER', 'Erythrocytes'),
    ('GR', 'Granulocytes'),
)

DONOR_STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive'),
    ('B', 'Banned'),
)

DONOR_TYPE = (
    ('Free', 'Free'),
    ('Paid', 'Paid'),
)


class BloodDonorCenter(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='centers/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Blood Donor Center'
        verbose_name_plural = 'Blood Donor Centers'
        db_table = 'blood_donor_centers'


class Donor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor', blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS)
    blood_type = models.CharField(max_length=2, choices=DONOR_BLOOD_TYPES)
    status = models.CharField(max_length=1, choices=DONOR_STATUS, default='A')
    last_donation_date = models.DateField(blank=True, null=True)
    donation_center = models.ForeignKey(BloodDonorCenter, on_delete=models.CASCADE, related_name='donor_center')
    donation_type = models.CharField(max_length=4, choices=DONOR_TYPE)

    def __str__(self):
        return f"{self.blood_group}"

    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
        db_table = 'donors'


class Recipient(models.Model):
    recipient_full_name = models.CharField(max_length=200)
    recipient_phone_number = models.CharField(max_length=25)
    recipient_address = models.CharField(max_length=200)
    recipient_reference = models.FileField(upload_to='recipient/references/', blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS)
    blood_type = models.CharField(max_length=2, choices=DONOR_BLOOD_TYPES)
    is_urgent = models.BooleanField(default=False)
    description = models.TextField()
    photo = models.ImageField(upload_to='recipient/photos', blank=True, null=True)
    donation_center = models.ForeignKey(BloodDonorCenter, on_delete=models.CASCADE, related_name='recipient_center')

    def __str__(self):
        return self.recipient_full_name

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'
        db_table = 'recipients'


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_donor')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='donation_recipient')
    donation_date = models.DateTimeField(auto_now_add=True)
    donation_type = models.CharField(max_length=4, choices=DONOR_TYPE)

    def __str__(self):
        return f'{self.donor.author.full_name} - {self.recipient.recipient_full_name}'

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        db_table = 'donations'


class DonationCenterRequests(models.Model):
    center = models.ForeignKey(BloodDonorCenter, on_delete=models.CASCADE, related_name='center_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    donor_blood_type = models.CharField(max_length=2, choices=DONOR_BLOOD_TYPES)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS, blank=True, null=True)
    donor_type = models.CharField(max_length=4, choices=DONOR_TYPE)
    count = models.IntegerField(blank=True, null=True)
    any_blood_group = models.BooleanField(default=False)
    planned_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.center.name} - {self.blood_group}'

    class Meta:
        verbose_name = 'Donation Center Request'
        verbose_name_plural = 'Donation Center Requests'
        db_table = 'donation_center_requests'

    def get_is_required(self):
        count_donations = Donor.objects.filter(donation_center=self.center, blood_group=self.blood_group).count()

        if count_donations < self.count:
            return "required"
        return "enough"


class DonorAdvice(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_advice')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Donor Advice'
        verbose_name_plural = 'Donor Advices'
        db_table = 'donor_advices'

    def get_count_donor_donations(self):
        return Donor.objects.filter(author=self.author).count()


class UrgentDonorRequest(models.Model):
    BLOOD_COMPONENTS = (
        ('WB', 'Whole blood'),
        ('PS', 'Plasma'),
        ('PL', 'Platelets'),
        ('ER', 'Erythrocytes'),
        ('GR', 'Granulocytes'),
    )

    blood_components = models.CharField(max_length=2, choices=BLOOD_COMPONENTS)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS)
    donor_count = models.PositiveIntegerField(default=1)

    city = models.CharField(max_length=100)
    center = models.ForeignKey(BloodDonorCenter, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateField()

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    reason = models.TextField()
    photo = models.ImageField(upload_to='urgent_requests/photos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} — {self.blood_components}, {self.donor_count} доноров"

    class Meta:
        verbose_name = 'Urgent Donor Request'
        verbose_name_plural = 'Urgent Donor Requests'
        db_table = 'urgent_donor_requests'

    def get_donor_count(self):
        return UrgentDonorRequestHistory.objects.filter(urgent_donor_request=self).count()


class UrgentDonorRequestHistory(models.Model):
    urgent_donor_request = models.ForeignKey(UrgentDonorRequest, on_delete=models.CASCADE, related_name='urgent_donor_request')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_user')
    donation_date = models.DateField()

    def __str__(self):
        return f"{self.urgent_donor_request} - {self.donor}"

    class Meta:
        verbose_name = 'Urgent Donor Request History'
        verbose_name_plural = 'Urgent Donor Request Histories'
        db_table = 'urgent_donor_request_histories'


class Donate(models.Model):
    frequency = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    hideAmount = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    hideFio = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.frequency}"

    class Meta:
        verbose_name = 'Donate'
        verbose_name_plural = 'Donates'
        db_table = 'donates'