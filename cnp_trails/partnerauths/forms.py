from django import forms
from django.core.exceptions import ValidationError
from .models import Partner, PARTNER_TYPES, ACTIVITY_TYPES, PartnerProfile
from django.core.validators import validate_email
import re
from activity.models import ActivityGallery

class PartnerRegisterForm(forms.ModelForm):
    partner_type = forms.ChoiceField(choices=PARTNER_TYPES,widget=forms.Select(attrs={'class':"partner_type"}), required=True,error_messages={'required': "Please select a partner type"})
    company_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':" Company Name",'class':"company_name"}), required=False,error_messages={'required': "Company name cannot be empty."})
    operator_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':" Operater Name",'class':"operator_name"}),required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':" Email",'class':"email"}),required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':" Phone Number",'class':"phone"}),required=False)
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES,widget=forms.Select(attrs={'class':"activity_type"}),required=True,error_messages={'required': "Please select a activity type"})
    registration_certificate = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':"registration_certificate"}),required=True,error_messages={'required': "Please upload your registration certificate"})
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':"password1"}),required=False)
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm_password ",'class':"password2"}),required=False)
    class Meta:
        model = Partner
        fields = ["partner_type", "operator_name", "company_name", "email", "phone", "activity_type", "registration_certificate"]

    

    def clean_email(self):
        
        email = self.cleaned_data.get("email")

    # Check if empty
        if not email:
            raise forms.ValidationError("Email cannot be empty.")

    # Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

    # Check uniqueness

        return email


    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

    # Check if empty
        if not phone:
            raise forms.ValidationError("Phone number cannot be empty.")

    # Allow only digits and must be 10 digits long
        if not re.fullmatch(r"\d{10}", phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number (digits only).")

    # Check uniqueness

        return phone
    
    def clean_password1(self):
       
        password1 = self.cleaned_data.get("password1")
        

    # Check if passwords are empty
        if not password1:
            raise forms.ValidationError(" password fields are required.")

    # Check if passwords match
        

    # Check password strength
        errors = []

        if len(password1) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", password1):
            errors.append("a uppercase letter")
        if not re.search(r"[0-9]", password1):
            errors.append("a number")
        if not re.search(r"[@$!%*?&]", password1):
            errors.append("a special character (@, $, !, %, *, ?, &)")
    
        if errors:
            raise forms.ValidationError("Password must contain " + ", ".join(errors) + ".")
     

        return password1

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        partner_type = self.cleaned_data.get("partner_type")
        if partner_type == "Register as Company" and not company_name:
            raise ValidationError("Company name is required..")
        return company_name or ""
    
    def clean_operator_name(self):
        operator_name= self.cleaned_data.get("operator_name")

        if not operator_name:
            raise ValidationError("Operator name is required.")
        return operator_name
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        
        company_name = cleaned_data.get("company_name")
        activity_type = cleaned_data.get("activity_type")
        partner_type= cleaned_data.get("partner_type")

        

        # Duplicate check rules
        if PartnerProfile.objects.filter(email=email, activity_type=activity_type).exists():
            raise ValidationError(f"Partner with this {email}  is already register to {activity_type}.")
        if partner_type=="Register as Company":
                PartnerProfile.objects.filter(company_name=company_name, activity_type=activity_type).exists()
                raise ValidationError(f" {company_name} is already registered for {activity_type}.")
        

        return cleaned_data

    def save(self, commit=True):
        partner = super().save(commit=False)
        partner.set_password(self.cleaned_data["password1"])
        if commit:
            partner.save()
        return partner


class PartnerLoginForm(forms.Form):
    partner_type = forms.ChoiceField(choices=PARTNER_TYPES,widget=forms.Select(attrs={'class':"partner_type"}), required=True,error_messages={'required': "Please choose your partner type"})
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES,widget=forms.Select(attrs={'class':"activity_type"}),required=True,error_messages={'required': "Please please choose your activity type"})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':" Email",'class':"email"}),required=False)
    
    password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':"password1"}),required=True,error_messages={'required': "Password cannot be empty."})

    class Meta:
        model = Partner
        fields = ["partner_type", "email","password" ]

    def clean_email(self):
        
        email = self.cleaned_data.get("email")

    # Check if empty
        if not email:
            raise forms.ValidationError("Email cannot be empty.")

    # Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

    # Check uniqueness

        return email

    

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        partner_type = cleaned_data.get("partner_type")
        activity_type = cleaned_data.get("activity_type")

        if email and password and activity_type and partner_type:
            try:
                partner = Partner.objects.get(email=email, partner_type=partner_type, activity_type=activity_type)
                if not partner.check_password(password):
                    raise ValidationError("Invalid password.")
                if not partner.is_verified:
                    raise ValidationError("Your account is not approved by the admin yet.")
            except Partner.DoesNotExist:
                raise ValidationError("No partner found")
        return cleaned_data

    # ACTIVITY GALLERY

