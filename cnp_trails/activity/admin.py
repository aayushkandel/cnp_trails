from django.contrib import admin
from activity.models import Activity,ActivityGallery

# Register your models here.

class ActivityGalleyInline(admin.TabularInline):
    model=ActivityGallery

class ActivityAdmin(admin.ModelAdmin):
    inlines=[ActivityGalleyInline]
    list_display= [ 'thumbnail','name', 'partner','status']
    prepopulated_fields={"slug":("name",    )}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show activities where the related partner is verified
        return qs.filter(partner__partner__is_verified=True)


admin.site.register(Activity,ActivityAdmin)

