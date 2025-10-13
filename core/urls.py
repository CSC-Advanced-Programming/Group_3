"""URL configuration for the core app."""
from django.urls import path
from .interfaces.controllers import (
    program_views,
    facility_views,
    project_views,
    equipment_views,
    service_views,
    participant_views,
    project_participant_views,
    outcome_views
)

urlpatterns = [
    path('', program_views.HomeView.as_view(), name='home'),
    path('programs/', program_views.ProgramListView.as_view(), name='program_list'),
    path('programs/<int:pk>/', program_views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/create/', program_views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/update/', program_views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<int:pk>/delete/', program_views.ProgramDeleteView.as_view(), name='program_delete'),

    # Facility URLs
    path('facilities/', facility_views.FacilityListView.as_view(), name='facility_list'),
    path('facilities/create/', facility_views.FacilityCreateView.as_view(), name='facility_create'),
    path('facilities/<int:pk>/', facility_views.FacilityDetailView.as_view(), name='facility_detail'),
    path('facilities/<int:pk>/update/', facility_views.FacilityUpdateView.as_view(), name='facility_update'),
    path('facilities/<int:pk>/delete/', facility_views.FacilityDeleteView.as_view(), name='facility_delete'),

    # Project URLs
    path('projects/', project_views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', project_views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', project_views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', project_views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', project_views.ProjectDeleteView.as_view(), name='project_delete'),

    # Equipment URLs
    path('equipment/', equipment_views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/create/', equipment_views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/', equipment_views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/<int:pk>/update/', equipment_views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', equipment_views.EquipmentDeleteView.as_view(), name='equipment_delete'),

    # Service URLs
    path('services/', service_views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', service_views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/', service_views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/update/', service_views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', service_views.ServiceDeleteView.as_view(), name='service_delete'),

    # Participant URLs
    path('participants/', participant_views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/create/', participant_views.ParticipantCreateView.as_view(), name='participant_create'),
    path('participants/<int:pk>/', participant_views.ParticipantDetailView.as_view(), name='participant_detail'),
    path('participants/<int:pk>/update/', participant_views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', participant_views.ParticipantDeleteView.as_view(), name='participant_delete'),

    # ProjectParticipant URLs
    path('projectparticipants/', project_participant_views.ProjectParticipantListView.as_view(), name='projectparticipant_list'),
    path('projectparticipants/create/', project_participant_views.ProjectParticipantCreateView.as_view(), name='projectparticipant_create'),
    path('projects/<int:project_id>/add-participant/', project_participant_views.ProjectParticipantForProjectCreateView.as_view(), name='project_participant_create'),
    path('projectparticipants/<int:pk>/', project_participant_views.ProjectParticipantDetailView.as_view(), name='projectparticipant_detail'),
    path('projectparticipants/<int:pk>/update/', project_participant_views.ProjectParticipantUpdateView.as_view(), name='projectparticipant_update'),
    path('projectparticipants/<int:pk>/delete/', project_participant_views.ProjectParticipantDeleteView.as_view(), name='projectparticipant_delete'),

    # Outcome URLs
    path('outcomes/', outcome_views.OutcomeListView.as_view(), name='outcome_list'),
    path('outcomes/create/', outcome_views.OutcomeCreateView.as_view(), name='outcome_create'),
    path('outcomes/<int:pk>/', outcome_views.OutcomeDetailView.as_view(), name='outcome_detail'),
    path('outcomes/<int:pk>/update/', outcome_views.OutcomeUpdateView.as_view(), name='outcome_update'),
    path('outcomes/<int:pk>/delete/', outcome_views.OutcomeDeleteView.as_view(), name='outcome_delete'),
]