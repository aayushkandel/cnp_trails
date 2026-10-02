
# from django.db import models
# from django.utils.html import mark_safe
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.auth.hashers import make_password, check_password
# from shortuuid.django_fields import ShortUUIDField
# ACTIVITY_TYPES = (
#     ("","Choose activity to provide"),
#     ("Jeep Safari", "Jeep Safari"),
#     ("Elephant Safari", "Elephant Safari"),
#     ("Canoe Ride", "Canoe Ride"),
#     ("Jungle Walk", "Jungle Walk"),
#     ("Tharu Village Tour", "Tharu Village Tour"),
#     ("Elephant Breeding center", "Elephant Breeding center"),
#     ("Tower Night", "Tower Night"),
#     ("20000 Lake", "20000 Lake"),
#     ("Bird Watching", "Bird Watching"),
#     ("Biodiversity Museum", "Biodiversity Museum"),
#     ("Tharu Cultural Dance", "Tharu Cultural Dance"),
#     ("Tharu Cultural Museum", "Tharu Cultural Museum"),
#     ("Side Seen", "Side Seen"),
# )

# PARTNER_TYPES = (
#     ("","Choose your partner type"),
#     ("Register as Company", "Register as Company"),
#     ("Register as Individual", "Register as Individual"),
# )

# def partner_certificate_path(instance, filename):
#     return f"partners/{instance.ppid}/certificate_{filename}"

# class Partner(models.Model):
#     ppid = ShortUUIDField(length=7, max_length=20, primary_key=True, alphabet="abcdefghijklmnopqrstuvwxyz123")
#     operator_name = models.CharField(max_length=150)
#     company_name = models.CharField(max_length=200,null=True, blank=True)
#     email = models.EmailField(max_length=200)
#     partner_type = models.CharField(max_length=100, choices=PARTNER_TYPES)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES)
#     registration_certificate = models.FileField(upload_to=partner_certificate_path)
#     password = models.CharField(max_length=128)
#     is_verified = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-date_joined"]
#          # prevent duplicate activity for same company/email

#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)
#         self.save(update_fields=['password'])

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def __str__(self):
#         return f"{self.operator_name} ({self.company_name or 'Individual'})"

# class PartnerProfile(models.Model):
#     partner = models.OneToOneField('Partner', on_delete=models.CASCADE)
#     operator_name = models.CharField(max_length=150)
#     company_name = models.CharField(max_length=200,null=True, blank=True)
#     email = models.EmailField(max_length=200)
#     partner_type = models.CharField(max_length=100, choices=PARTNER_TYPES)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES)
#     registration_certificate = models.FileField(upload_to=partner_certificate_path)
#     is_verified = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return f"{self.operator_name} ({self.activity_type})"

# @receiver(post_save, sender=Partner)
# def create_partner_profile(sender, instance, created, **kwargs):
#     if created and instance.is_verified:
#         PartnerProfile.objects.create(partner=instance)

# @receiver(post_save, sender=Partner)
# def save_partner_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'partnerprofile'):
#         instance.partnerprofile.save()

# @receiver(post_delete, sender=PartnerProfile)
# def delete_partner_with_profile(sender, instance, **kwargs):
#     if instance.partner:
#         instance.partner.delete()

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, check_password
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone


# -------- Choices --------
ACTIVITY_TYPES = (
    ("", "Choose activity to provide"),
    ("Jeep Safari", "Jeep Safari"),
    ("Elephant Safari", "Elephant Safari"),
    ("Canoe Ride", "Canoe Ride"),
    ("Jungle Walk", "Jungle Walk"),
    ("Tharu Village Tour", "Tharu Village Tour"),
    ("Elephant Breeding Center", "Elephant Breeding Center"),
    ("Tower Night", "Tower Night"),
    ("20000 Lake", "20000 Lake"),
    ("Bird Watching", "Bird Watching"),
    ("Biodiversity Museum", "Biodiversity Museum"),
    ("Tharu Cultural Dance", "Tharu Cultural Dance"),
    ("Tharu Cultural Museum", "Tharu Cultural Museum"),
    ("Side Seen", "Side Seen"),
)

PARTNER_TYPES = (
    ("", "Choose your partner type"),
    ("Register as Company", "Register as Company"),
    ("Register as Individual", "Register as Individual"),
)

def partner_certificate_path(instance, filename):
    return f"partners/{instance.ppid}/certificate_{filename}"

# -------- Partner Model --------
class Partner(models.Model):
    ppid = ShortUUIDField(length=7, max_length=20, primary_key=True, alphabet="abcdefghijklmnopqrstuvwxyz123")
    operator_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200,default="abc@gmail.com")
    partner_type = models.CharField(max_length=100, choices=PARTNER_TYPES)
    phone = models.CharField(max_length=20, null=True, blank=True)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES)
    registration_certificate = models.FileField(upload_to=partner_certificate_path)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)

    
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_joined"]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.operator_name} ({self.company_name or 'Individual'})"

# -------- PartnerProfile Model --------
class PartnerProfile(models.Model):
    

    partner = models.OneToOneField(Partner, on_delete=models.CASCADE,to_field='ppid',db_column='partner_ppid')
    operator_name = models.CharField(max_length=150,default="none")
    company_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200,default="adc@gmail.com")
    partner_type = models.CharField(max_length=100, choices=PARTNER_TYPES, default="Register as Company")
    phone = models.CharField(max_length=20, null=True, blank=True)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES, default="Jeep Safari")
    registration_certificate = models.FileField(upload_to=partner_certificate_path,default="abc.jpg")
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.operator_name} ({self.activity_type})"

@receiver(post_save, sender=Partner)
def create_or_update_partner_profile(sender, instance, created, **kwargs):
    if instance.is_verified:
        PartnerProfile.objects.update_or_create(
            partner=instance,
            defaults={
                "operator_name": instance.operator_name,
                "company_name": instance.company_name,
                "email": instance.email,
                "partner_type": instance.partner_type,
                "phone": instance.phone,
                "activity_type": instance.activity_type,
                "registration_certificate": instance.registration_certificate,
            },
        )

        

@receiver(post_delete, sender=PartnerProfile)
def delete_partner_on_profile_delete(sender, instance, **kwargs):
    if instance.partner:
        instance.partner.delete()
