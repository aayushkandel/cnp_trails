from django.urls import path
from . import views

app_name="partner_dashboard"
urlpatterns = [
    # Dashboard home (optional)
    

    # Update form for partner + activity
    path('partner/update/<str:ppid>/', views.update_partner_activity, name='update_partner_activity'),
    # partner_dashboard/urls.py\
    path('activity-gallery/', views.partner_activity_gallery, name='partner_activity_gallery'),
    # partner_dashboard/urls.py
    # path('room/<str:rtid>/custom-calendar/',views.custom_room_calendar,name='custom_room_calendar'),
    path('activity-gallery/<str:partner_id>/', views.partner_activity_gallery, name='partner_activity_gallery_with_id'),
    path('activity-gallery/delete/<str:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),
   

]
