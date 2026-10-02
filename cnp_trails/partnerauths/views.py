from django.shortcuts import render, redirect
from .forms import PartnerRegisterForm, PartnerLoginForm
from .models import Partner,PartnerProfile
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from activity.models import ActivityGallery

@csrf_protect
def partner_register(request):
    if request.method == "POST":
        form = PartnerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.set_password(form.cleaned_data["password1"])
            partner.save()
            messages.success(request,"Registration Successful! please wait for admin approvel")
            return redirect("partnerauths:partner-login")
     

    else:
        form = PartnerRegisterForm()
    return render(request, "partnerauths/partner-sign-up.html", {"form": form})


@csrf_protect
def partner_login(request):
    if request.method == "POST":
        form = PartnerLoginForm(request.POST)
        if form.is_valid():
            partner = Partner.objects.filter(
                email=form.cleaned_data["email"],
                activity_type=form.cleaned_data["activity_type"],
                partner_type=form.cleaned_data["partner_type"],
        
            ).first()

            if partner and partner.check_password(form.cleaned_data["password"]):
                # Password correct, login success
                request.session["partner_id"] = partner.ppid
                activity = partner.activity_type

                # Redirect based on activity
                activity_redirects = {
                    "Jeep Safari": "partnerauths:jeep-safari-dashboard",
                    "Elephant Safari": "partnerauths:elephant-safari-dashboard",
                    "Bird Watching": "partnerauths:bird-watching-dashboard",
                    "Canoe Ride": "partnerauths:canoe-ride-dashboard",
                    "Elephant Breeding Center": "partnerauths:elaphant-breeding-center-dashboard",
                    "Tower Night": "partnerauths:tower-night-dashboard",
                    "20000 Lake": "partnerauths:20000-lake-dashboard",
                    "Biodiversity Museum": "partnerauths:biodiversity-museum-dashboard",
                    "Tharu Cultural Dance": "partnerauths:tharu-cultural-dance-dashboard",
                    "Tharu Cultural Museum": "partnerauths:tharu-cultural-museum-dashboard",
                    "Side Seen": "partnerauths:side-seen-dashboard",
                    "Tharu Village Tour": "partnerauths:tharu-village-tour-dashboard",
                    "Jungle Walk": "partnerauths:jungle-walk-dashboard",
                }

                return redirect(activity_redirects.get(activity, "partnerauths:partner-login"))

            else:
                messages.error(request, "Invalid login credentials.")
                return redirect("partnerauths:partner-login")
    else:
        form = PartnerLoginForm()

    return render(request, "partnerauths/partner-sign-in.html", {"form": form})

@csrf_protect
def jeep_safari_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Jeep Safari")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/jeep-safari-dashboard.html", context)
    
@csrf_protect
def elephant_safari_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Elephant Safari")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/elephant-safari-dashboard.html",context)

@csrf_protect
def tharu_village_tour_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Tharu Village Tour")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/tharu-village-tour-dashboard.html",context)

@csrf_protect
def jungle_walk_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Jungle Walk")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/jungle-walk-dashboard.html",context)

@csrf_protect
def side_seen_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Side Seen")
    

   

    context = {
        "partner": partner,
        "partners": partners,
        
    }
    return render(request, "partnerauths/side-seen-dashboard.html",context)

@csrf_protect
def tower_night_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Tower Night")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/tower-night-dashboard.html",context)

@csrf_protect
def bird_watching_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Bird Watching")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/bird-watching-dashboard.html",context)

@csrf_protect
def lake_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="20000 Lake")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/20000-lake-dashboard.html",context)

@csrf_protect
def biodiversity_museum_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Biodiversity Museum")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/biodiversity-museum-dashboard.html",context)

@csrf_protect
def tharu_cultural_dance_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Tharu Cultural Dance")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/tharu-cultural-dance-dashboard.html",context)

@csrf_protect
def tharu_cultural_museum_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Tharu Cultual Museum")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/tharu-cultural-museum-dashboard.html",context)

@csrf_protect
def canoe_ride_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Canoe Ride")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/canoe-ride-dashboard.html",context)

@csrf_protect
def elaphant_breeding_center_dashboard(request):
    partner_id = request.session.get("partner_id")
    if not partner_id:
        return redirect("partnerauths:partner-login")

    partner = Partner.objects.get(ppid=partner_id)  # get logged-in partner
    # Example: fetch all partners or related data
    partners = Partner.objects.filter(activity_type="Elephant Breeding Center")

    context = {
        "partner": partner,
        "partners": partners,  # list of jeep safari partners
    }
    return render(request, "partnerauths/elaphant-breeding-center-dashboard.html",context)





def partner_logout(request):
    if 'partner_id' in request.session:
        del request.session['partner_id']
    messages.success(request, "You have been logged out.")
    return redirect("partnerauths:partner-login")


def partnerprofile_list(request):
    # Only show profiles where the related partner is verified
    profiles = PartnerProfile.objects.filter(partner__is_verified=True)
    return render(request, "partnerauths/partnerprofile_list.html", {"profiles": profiles})