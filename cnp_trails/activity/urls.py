from django.urls import path
from activity import views

app_name="activity"

urlpatterns=[
    path("", views.index, name="index"),
    path("detail/<slug>/", views.activity_detail, name="activity_detail"),
    path("", views.index, name="index"),
    path("detail/<slug>/", views.activity_detail, name="activity_detail"),

    path("jeep-safari/", views.jeep_safari, name="jeep_safari"),
    path("elephant-safari/", views.elephant_safari, name="elephant_safari"),
    path("jungle-walk/", views.jungle_walk, name="jungle_walk"),
    path("canoe/", views.canoe, name="canoe"),
    path("bird-watching/", views.bird_watching, name="bird_watching"),
    path("village-tour/", views.village_tour, name="village_tour"),
    path("side-seen/", views.side_seen, name="side_seen"),
    path("tower-night/", views.tower_night, name="tower_night"),
    path("ebc/", views.ebc, name="ebc"),
    path("20000-lake/", views.lake, name="lake"),
    path("tharu-cultural-dance/", views.tharu_cultural_dance, name="tharu_cultural_dance"),
    path("tharu-cultural-museum/", views.tharu_cultural_museum, name="tharu_cultural_museum"),
    path("wildlife-museum/", views.wildlife_museum, name="wildlife_museum"),
    
    path("detail/<slug:slug>/room-type/<slug:at_slug>/", views.activity_type_detail, name="activity_type_detail")
]