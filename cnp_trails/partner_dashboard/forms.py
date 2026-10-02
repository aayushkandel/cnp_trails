from django import forms
from partnerauths.models import Partner,PartnerProfile
from django.forms import inlineformset_factory
from activity.models import Activity,ACTIVITY_STATUS,ActivityGallery


class PartnerActivityUpdateForm(forms.ModelForm):
    # Activity fields
    address = forms.CharField(label="Address", max_length=200)
    image = forms.FileField(label="Activity Image", required=False)
    status = forms.ChoiceField(choices=ACTIVITY_STATUS)
    name=forms.CharField(label="name", max_length=100)
    email = forms.EmailField()

    class Meta:
        model = PartnerProfile
        fields = [
            "partner_type",
            "phone",
            "activity_type",
        ]
    
    def __init__(self, *args, **kwargs):
        # Optional existing activity passed in
        self._activity_instance = kwargs.pop('activity_instance', None)
        super().__init__(*args, **kwargs)

        # Make these fields readonly
        self.fields["partner_type"].disabled = True
        self.fields["activity_type"].disabled = True

        # Prefill from activity if given
        if self._activity_instance:
            self.initial.update({
                "email": self._activity_instance.email,
                "name": self._activity_instance.name,
                "address": self._activity_instance.address,
                "status": self._activity_instance.status,
                "image": self._activity_instance.image,
            })

    # Validation for unique email & phone
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Activity.objects.filter(email=email)
         # Exclude current activity
        if self._activity_instance:
            qs = qs.exclude(pk=self._activity_instance.pk)

        if qs.exists():
            raise forms.ValidationError("This email is already used by another activity.")
        return email
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and PartnerProfile.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already used by another partner.")
        return phone

#Gallary form

class PartnerActivityGalleryForm(forms.ModelForm):
    image = forms.FileField(label="Upload Image", required=True)

    class Meta:
        model = ActivityGallery
        fields = ['image']