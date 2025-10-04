from django.urls import path
from . import views

urlpatterns = [
    

    path("create-campaign/", views.create_campaign, name="create_campaign"),
    path('campaign/<int:campaign_id>/edit/', views.edit_campaign, name='edit_campaign'),
    path('campaign/<int:campaign_id>/delete/', views.delete_campaign, name='delete_campaign'),


    path("my-campaigns/", views.my_campaigns, name="my_campaigns"),

    path('explore-campaigns/', views.explore_campaigns, name='explore_campaigns'),
    path('campaign/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path("campaign/<int:campaign_id>/donate/", views.donate_to_campaign, name="donate_to_campaign"),
    path('donation/success/<int:donation_id>/', views.donation_success, name='donation_success'),
    path("receipt/<int:donation_id>/", views.download_receipt, name="download_receipt"),
    path('campaign/<int:campaign_id>/add-update/', views.add_campaign_update, name='add_campaign_update'),
    path('donation-history/', views.ngo_donation_history, name='ngo_donation_history'),



]

