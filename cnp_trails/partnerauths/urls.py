
from django.urls import path
from . import views

app_name = "partnerauths"

urlpatterns = [
    path("register/", views.partner_register, name="partner-register"),
    path("login/", views.partner_login, name="partner-login"),
    path("jeep-sarafi-dashboard/", views.jeep_safari_dashboard, name="jeep-safari-dashboard"),
    path("elephant-safari-dashboard/", views.elephant_safari_dashboard, name="elephant-safari-dashboard"),
    path("tharu-village-tour-dashboard/", views.tharu_village_tour_dashboard, name="tharu-village-tour-dashboard"),
    path("jungle-walk-dashboard/", views.jungle_walk_dashboard, name="jungle-walk-dashboard"),
    path("side-seen-dashboard/", views.side_seen_dashboard, name="side-seen-dashboard"),
    path("canoe-ride-dashboard/", views.canoe_ride_dashboard, name="canoe-ride-dashboard"),
    path("tower-night-dashboard/", views.tower_night_dashboard, name="tower-night-dashboard"),
    path("bird-watching-dashboard/", views.bird_watching_dashboard, name="bird-watching-dashboard"),
    path("20000-lake-dashboard/", views.lake_dashboard, name="20000-lake-dashboard"),
    path("biodiversity-museum-dashboard/", views.biodiversity_museum_dashboard, name="biodiversity-museum-dashboard"),
    path("tharu-cultural-dance-dashboard/", views.tharu_cultural_dance_dashboard, name="tharu-cultural-dance-dashboard"),
    path("tharu-cultural-museum-dashboard/", views.tharu_cultural_museum_dashboard, name="tharu-cultural-museum-dashboard"),
    path("elaphant-breeding-center-dashboard/", views.elaphant_breeding_center_dashboard, name="elaphant-breeding-center-dashboard"),
    
    path("logout/", views.partner_logout, name="partner-logout"),
]
