
# from django.contrib import admin
# from .models import Partner, PartnerProfile
# from django.utils.html import format_html

# # ---------------- Partner Admin ----------------
# class PartnerAdmin(admin.ModelAdmin):
#     list_display = [
#         "operator_name", "company_name", "email", "phone",
#         "activity_type", "is_verified", "date_joined", "registration_certificate_preview"
#     ]
#     list_filter = ["activity_type", "is_verified"]
#     search_fields = ["operator_name", "company_name", "email"]
#     list_editable = ["is_verified",]

#     def registration_certificate_preview(self, obj):
#      if obj.registration_certificate:
#         return format_html(
#             '<a href="{}" target="_blank"><img src="{}" style="width:100px; height:auto; border-radius:5px;" /></a>',
#             obj.registration_certificate.url,
#             obj.registration_certificate.url
#         )
#      return "No Certificate"
#     registration_certificate_preview.short_description = "Certificate Preview"
#     registration_certificate_preview.admin_order_field = "registration_certificate"

# # ---------------- PartnerProfile Admin ----------------
# class PartnerProfileAdmin(admin.ModelAdmin):
#     list_display = ["partner", "partner_email", "partner_activity_type", "partner_phone", "certificate_preview"]
#     search_fields = ["partner__operator_name", "partner__email", "partner__phone"]

#     def has_add_permission(self, request):
#         return False
    
#     def has_delete_permission(self, request, obj=None):
#         return True

#     def partner_email(self, obj):
#         return obj.partner.email
#     partner_email.admin_order_field = 'partner__email'
#     partner_email.short_description = 'Email'

#     def partner_activity_type(self, obj):
#         return obj.partner.activity_type
#     partner_activity_type.admin_order_field = 'partner__activity_type'
#     partner_activity_type.short_description = 'Activity Type'

#     def partner_phone(self, obj):
#         return obj.partner.phone
#     partner_phone.admin_order_field = 'partner__phone'
#     partner_phone.short_description = 'Phone'

#     def certificate_preview(self, obj):
#      if obj.partner.registration_certificate:
#         return format_html(
#             '<a href="{}" target="_blank">'
#             '<img src="{}" style="width:100px; height:auto; border-radius:5px;" />'
#             '</a>',
#             obj.partner.registration_certificate.url,
#             obj.partner.registration_certificate.url
#         )
#      return "No Certificate"

#     certificate_preview.short_description = "Registration Certificate"

#     fields = ("partner", "certificate_preview")
#     readonly_fields = ("certificate_preview",)

#     # Optional: show all partners, not only verified
#     def get_queryset(self, request):
#         return super().get_queryset(request)  # remove filtering if you want all partners

# # ---------------- Register ----------------
# admin.site.register(Partner, PartnerAdmin)
# admin.site.register(PartnerProfile, PartnerProfileAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Partner, PartnerProfile
from django.urls import reverse

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["operator_name", "company_name", "email", "phone", "activity_type","partner_type", "is_verified", "date_joined","registration_certificate_preview","edit_link", "delete_link"]
    list_editable = ["is_verified"]
    list_filter = ["activity_type", "is_verified"]
    search_fields = ["operator_name", "company_name", "email"]

    def edit_link(self, obj):
        url = reverse('admin:partnerauths_partner_change', args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = 'Edit'

    def delete_link(self, obj):
        url = reverse('admin:partnerauths_partner_delete', args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = 'Delete'
    
    def registration_certificate_preview(self, obj):
     if obj.registration_certificate:
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" style="width:50px; height:auto; border-radius:5px;" /></a>',
            obj.registration_certificate.url,
            obj.registration_certificate.url
        )
     return "No Certificate"
    registration_certificate_preview.short_description = "Certificate Preview"
    registration_certificate_preview.admin_order_field = "registration_certificate"


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ["operator_name", "company_name", "email", "activity_type"]
    search_fields = ["operator_name", "email"]
    readonly_fields = ["partner"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(partner__is_verified=True)
