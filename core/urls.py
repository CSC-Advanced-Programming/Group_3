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

    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # Equipment URLs
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),

    # Service URLs
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Participant URLs
    path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/create/', views.ParticipantCreateView.as_view(), name='participant_create'),
    path('participants/<int:pk>/', views.ParticipantDetailView.as_view(), name='participant_detail'),
    path('participants/<int:pk>/update/', views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),

    # ProjectParticipant URLs
    path('projectparticipants/', views.ProjectParticipantListView.as_view(), name='projectparticipant_list'),
    path('projectparticipants/create/', views.ProjectParticipantCreateView.as_view(), name='projectparticipant_create'),
    path('projectparticipants/<int:pk>/', views.ProjectParticipantDetailView.as_view(), name='projectparticipant_detail'),
    path('projectparticipants/<int:pk>/update/', views.ProjectParticipantUpdateView.as_view(), name='projectparticipant_update'),
    path('projectparticipants/<int:pk>/delete/', views.ProjectParticipantDeleteView.as_view(), name='projectparticipant_delete'),

    # Outcome URLs
    path('outcomes/', views.OutcomeListView.as_view(), name='outcome_list'),
    path('outcomes/create/', views.OutcomeCreateView.as_view(), name='outcome_create'),
    path('outcomes/<int:pk>/', views.OutcomeDetailView.as_view(), name='outcome_detail'),
    path('outcomes/<int:pk>/update/', views.OutcomeUpdateView.as_view(), name='outcome_update'),
    path('outcomes/<int:pk>/delete/', views.OutcomeDeleteView.as_view(), name='outcome_delete'),
]