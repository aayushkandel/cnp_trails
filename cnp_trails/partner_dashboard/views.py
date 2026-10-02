from django.shortcuts import render, get_object_or_404, redirect
from partnerauths.models import PartnerProfile,Partner
from activity.models import Activity
from .forms import PartnerActivityUpdateForm,PartnerActivityGalleryForm
from activity.models import ActivityGallery
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from activity.models import RoomType

def update_partner_activity(request, ppid):
    partner_profile = get_object_or_404(PartnerProfile, partner__ppid=ppid)
    activity = Activity.objects.filter(partner=partner_profile).first()

    if request.method == "POST":
        form = PartnerActivityUpdateForm(
            request.POST,
            request.FILES,
            instance=partner_profile,
            activity_instance=activity
        )

        if form.is_valid():
            # Save PartnerProfile
            partner_profile = form.save(commit=False)
            partner_profile.save()

            # Update or create Activity
            if activity:
                activity_instance = activity
            else:
                activity_instance = Activity(partner=partner_profile)

            # Assign values from form.cleaned_data
            activity_instance.email = form.cleaned_data["email"]
            activity_instance.name = form.cleaned_data["name"]
            activity_instance.address = form.cleaned_data["address"]
            activity_instance.status = form.cleaned_data["status"]

            # Update image only if uploaded
            if form.cleaned_data.get("image"):
                activity_instance.image = form.cleaned_data["image"]

            activity_instance.save()

            return redirect(
                'partner_dashboard:update_partner_activity',
                ppid=partner_profile.partner.ppid
            )

    else:
        form = PartnerActivityUpdateForm(
            instance=partner_profile,
            activity_instance=activity
        )

    return render(request, "partner_dashboard/update_partner_activity.html", {
        "form": form,
        "ppid": ppid
    })

# Activity Gallary views 

def partner_activity_gallery(request,partner_id=None):
    if partner_id:
        partner = get_object_or_404(PartnerProfile, partner_id=partner_id)
    else:
        partner_id = request.session.get("partner_id")
        if not partner_id:
            return redirect("partnerauths:partner-login")
        partner = get_object_or_404(PartnerProfile, partner_id=partner_id)

    # Get activities of this partner
    activities = Activity.objects.filter(partner=partner)
    gallery = ActivityGallery.objects.filter(activity__in=activities)


    if request.method == 'POST':
        form = PartnerActivityGalleryForm(request.POST, request.FILES)
        activity_id = request.POST.get('activity_id')
        activity = get_object_or_404(Activity, pk=activity_id, partner=partner)

        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.activity = activity
            new_image.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('partner_dashboard:partner_activity_gallery')
    else:
        form = PartnerActivityGalleryForm()

    context = {
        "partner": partner,
        "activities": activities,
        "gallery": gallery,
        "form": form,
    }
    return render(request, "partner_dashboard/partner_activity_gallery.html", context)


def delete_gallery_image(request, image_id):
    # Get logged-in partner
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = get_object_or_404(PartnerProfile, partner_id=partner_id)
    
    # Look up by agid (ShortUUIDField), not numeric pk
    image = get_object_or_404(ActivityGallery, agid=image_id, activity__partner=partner)
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect('partner_dashboard:partner_activity_gallery')
