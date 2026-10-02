from django.db import models
from partnerauths.models import Partner,PartnerProfile
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from partnerauths.models import ACTIVITY_TYPES
from django.utils.text import slugify
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

ACTIVITY_STATUS=(
    ("Drift" , "Drift"),
    ("Disabled" , "Disabled"),
    ("Rejected" , "Rejected"),
    ("In Review" , "In Review"),
    ("Live" , "Live"),
)


ICON_TYPE=(
    ("Bootstrap Icons" , "Bootstrap Icons"),
    ("Fontawesome Icons" , "Fontawesome Icons"),
    ("Box Icons" , "Box Icons"),
    ("Remi Icons" , "Remi Icons"),
    ("Flat Icons" , "Flat Icons"),
)
PAYMENT_STATUS=(
    ("paid" , "paid"),
    ("pending" , "pending"),
    ("processing" , "processing"),
    ("cancelled" , "cancelled"),
    ("initiated" , "initiated"),
    ("failed" , "failed"),
    ("refunding" , "refunding"),
    ("refunded" , "refunded"),
    ("unpaid" , "unpaid"),
    ("expired" , "expired"),
)

# Create your models here.
class Activity(models.Model):
    partner=models.ForeignKey(PartnerProfile, on_delete= models.CASCADE,null=True)              # it delete the listed activity if partner is deleted :-models.CASCADE
    name=models.CharField(max_length=100,null=True)
    description=CKEditor5Field(null=True,blank=True, config_name='extends')
    image=models.FileField(upload_to="activity_gallery")
    address=models.CharField(max_length=200)
    email = models.EmailField(max_length=200,default="adc@gmail.com")
    status=models.CharField(max_length=20, choices=ACTIVITY_STATUS,default="Live")
    tags=TaggableManager( blank=True)
    views=models.IntegerField(default=0)
    featured=models.BooleanField(default=False)
    aid=ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123" )
    slug=models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="partners" 
    
    def save(self,*args, **kwargs):
        if self.slug=="" or self.slug== None:
            uuid_key=shortuuid.uuid()
            uniqueid = uuid_key[ :4]
            self.slug= slugify(self.name) + '-' + str(uniqueid.lower())

        super(Activity,self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe("<img src='%s' width='50'  height='50'  style='object-fit: cover, boarder-radius= 6px;' />" %(self.image.url)) 
    
    def activity_gallery(self):
        return ActivityGallery.objects.filter(activity=self)
    
    def hotel_room_types(self):
        return RoomType.objects.filter(activity=self)
    
class ActivityGallery(models.Model):
    activity= models.ForeignKey(Activity,on_delete=models.CASCADE)
    image=models.FileField(upload_to="activity_gallery")
    agid=ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123" )

    def __str__(self):
        return str(self.activity.name)
    
    class Meta:
        verbose_name_plural="Activity Gallery"

class ActivityFeatures(models.Model):
    activity= models.ForeignKey(Activity, on_delete=models.CASCADE)
    icon_type=models.CharField(max_length=100, null=True, blank=True, choices=ICON_TYPE)
    icon = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural="Activity Features"

class HotelFaqs(models.Model):
    activity= models.ForeignKey(Activity, on_delete=models.CASCADE)
    question=models.CharField(max_length=1000)
    answer=models.CharField(max_length=1000,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural="Activity FAQs"

class RoomType(models.Model):
    activity= models.ForeignKey(Activity, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    price= models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds=models.PositiveIntegerField(default=0)
    room_capacity=models.PositiveIntegerField(default=0)
    rtid=ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123" )
    slug=models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.activity.name} - {self.price}"
    
    class Meta:
        verbose_name_plural="Activity Type" 

    def rooms_count(self):
        Room.objects.filter(room_type=self).count()

    def save(self,*args, **kwargs):
        if self.slug=="" or self.slug==None:
            uuid_key=shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug= slugify(self.name) + '-' + str(uniqueid.lower())

        super(RoomType,self).save(*args, **kwargs)

class Room(models.Model):
    activity= models.ForeignKey(Activity, on_delete=models.CASCADE)
    room_type= models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number=models.CharField(max_length=1000)
    is_available=models.BooleanField(default=True)
    rid=ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123" )
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type.type} - {self.activity.name} "
    
    class Meta:
        verbose_name_plural="Activity"

    def price(self):
        return self.room_type.price
    
    def number_of_beds(self):
        return self.room_type.number_of_beds

class Booking(models.Model):
    user=models.ForeignKey(Partner,on_delete= models.SET_NULL,null=True,blank=True)
    payment_status=models.CharField(max_length=100, choices=PAYMENT_STATUS)

    full_name=models.CharField(max_length=1000)
    email=models.EmailField(max_length=1000)
    phone=models.CharField(max_length=1000)

    activity= models.ForeignKey(Activity, on_delete= models.SET_NULL,null=True,blank=True)
    room_type= models.ForeignKey(RoomType, on_delete= models.SET_NULL,null=True,blank=True)
    room=models.ManyToManyField(Room)
    before_discount=models.DecimalField(max_digits=12,decimal_places=2, default=0.00)
    total=models.DecimalField(max_digits=12,decimal_places=2, default=0.00)
    saved=models.DecimalField(max_digits=12,decimal_places=2, default=0.00)

    check_in_date=models.DateField()
    check_out_date=models.DateField()

    total_days= models.PositiveIntegerField(default=0)
    num_adults=models.PositiveIntegerField(default=1)
    num_children=models.PositiveIntegerField(default=0)

    checked_in=models.BooleanField(default=False)
    checked_out=models.BooleanField(default=False)

    is_active=models.BooleanField(default=False)

    checked_in_tracker=models.BooleanField(default=False)
    checked_out_tracker=models.BooleanField(default=False)

    date=models.DateTimeField(auto_now_add=True)
    stripe_payment_intent=models.CharField(max_length=1000, null=True,blank=True)
    success_id=models.CharField(max_length=1000, null=True,blank=True)
    booking_id=ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123" )

    def __str__(self):
        return f"{self.booking_id} "
    
    def rooms(self):
        return self.room.all().count()
    
class ActivityLog(models.Model):
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE)
    guess_out= models.DateTimeField()
    guess_in=models.DateTimeField()
    description=models.TextField(null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} "
    
class StaffOnDuty(models.Model):
    booking=models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id=models.CharField(max_length=100, null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff_id} "





