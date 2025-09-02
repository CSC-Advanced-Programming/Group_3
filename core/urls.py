from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/create/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/update/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Facility URLs
    path('facilities/', views.FacilityListView.as_view(), name='facility_list'),
    path('facilities/create/', views.FacilityCreateView.as_view(), name='facility_create'),
    path('facilities/<int:pk>/', views.FacilityDetailView.as_view(), name='facility_detail'),
    path('facilities/<int:pk>/update/', views.FacilityUpdateView.as_view(), name='facility_update'),
    path('facilities/<int:pk>/delete/', views.FacilityDeleteView.as_view(), name='facility_delete'),
]