from django.shortcuts import render
from activity.models import Activity, Booking,ActivityLog,StaffOnDuty,Room,RoomType
from partnerauths.models import Partner,PartnerProfile

def index(request):
    return render(request, "activity/activity.html")

def activity_detail(request, slug):
    activity=Activity.objects.get(status="Live", slug=slug)
    context={
        "activity":activity,
    }
    return render(request,"activity/activity_detail.html", context)


def jeep_safari(request):
    activities=Activity.objects.filter(  status="Live", partner__activity_type="Jeep Safari",partner__partner__is_verified=True) 
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/jeep-safari.html",context)

def elephant_safari(request):
    activities=Activity.objects.filter(  status="Live") and Partner.objects.filter(activity_type="Jeep Safari")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/elephant-safari.html",context)

def jungle_walk(request):
    activities=Activity.objects.filter(  status="Live") and Partner.objects.filter(activity_type="Jeep Safari")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/jungle-walk.html",context)

def side_seen(request):
    activities=Activity.objects.filter(  status="Live", partner__activity_type="Side Seen",partner__partner__is_verified=True) 
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/side-seen.html",context)

def bird_watching(request):
    activities=Activity.objects.filter(activity_type="Bird Watching")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/bird-watching.html",context)


def tower_night(request):
    activities=Activity.objects.filter(activity_type="Tower Night")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/tower-night.html",context)

def village_tour(request):
    activities=Activity.objects.filter(activity_type="Village Tour")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/village-tour.html",context)

def canoe(request):
    activities=Activity.objects.filter(activity_type="Canoe")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/canoe.html",context)

def ebc(request):
    activities=Activity.objects.filter(activity_type="Elephant Breeding Center")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/ebc.html")

def tharu_cultural_dance(request):
    activities=Activity.objects.filter(activity_type="Tharu Cultural Dance")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/tharu-cultural-dance.html",context)

def wildlife_museum(request):
    activities=Activity.objects.filter(activity_type="Wildlife Museum")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/wildlife-museum.html",context)

def tharu_cultural_museum(request):
    activities=Activity.objects.filter(activity_type="Thaur Cultural Museum")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/tharu-cultural-museum.html",context)

def lake(request):
    activities=Activity.objects.filter(activity_type="20000 Lake")
    context={
        "activity":activities
    }

    return render(request, "activity-homepage/20000-lake.html",context)

def activity_type_detail(request, slug, at_slug):
    activity=Activity.objects.get(status="Live", slug=slug)
    room_type=RoomType.objects.get(activity=activity,slug=at_slug)
    rooms=Room.objects.filter(room_type=room_type, is_available=True)

    context={
        "activity":activity,
        "room_type":room_type,
        "rooms":rooms,
    }

    return render(request, "activity/activity_type_detail",context)
