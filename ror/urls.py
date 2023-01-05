from django.urls import path, include
from ror import views

app_name = 'ror'
urlpatterns = [
    path(
        'register/',
        views.RegisterAffiliations.as_view(),
        name='register_affiliations'),
    path(
        'about/',
        views.about,
        name='about'),
]
