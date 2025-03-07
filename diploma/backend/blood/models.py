from django.db import models

from authorization.models import User

BLOOD_GROUPS = (
    ('0+', '0+'),
    ('0-', '0-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    blood_type = models.CharField(max_length=2, choices=DONOR_BLOOD_TYPES)
    status = models.CharField(max_length=1, choices=DONOR_STATUS, default='A')
    last_donation_date = models.DateField(blank=True, null=True)
    donation_center = models.ForeignKey(BloodDonorCenter, on_delete=models.CASCADE, related_name='donor_center')
    donation_type = models.CharField(max_length=4, choices=DONOR_TYPE)

    def __str__(self):
        return f"{self.author.full_name} - {self.blood_group}"

    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
        db_table = 'donors'


class Recipient(models.Model):
    recipient_full_name = models.CharField(max_length=200)
    recipient_phone_number = models.CharField(max_length=25)
    recipient_address = models.CharField(max_length=200)
    recipient_reference = models.FileField(upload_to='recipient/references/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
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
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True, null=True)
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
