from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('available/', views.available_elections_view, name='available_elections'),
    path('vote/<int:election_id>/', views.vote_view, name='vote'),
    path('results/<int:election_id>/', views.results_view, name='results'),
    # Add voting and dashboard routes here
]
