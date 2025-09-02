from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Program, Facility, Service
from django.contrib import messages
from django.db.models import ProtectedError
# Service Views
from django.db.models import Q

class ServiceListView(ListView):
    model = Service
    template_name = "core/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class FacilityServiceListView(ListView):
    model = Service
    template_name = "core/facility_service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        facility_id = self.kwargs.get("facility_id")
        return Service.objects.filter(facility__facility_id=facility_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["facility"] = Facility.objects.get(facility_id=self.kwargs.get("facility_id"))
        return context

class ServiceCreateView(CreateView):
    model = Service
    fields = ["facility", "name", "description", "category", "skill_type"]
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")

class ServiceUpdateView(UpdateView):
    model = Service
    fields = ["facility", "name", "description", "category", "skill_type"]
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "core/service_confirm_delete.html"
    success_url = reverse_lazy("service_list")

class ServiceDetailView(DetailView):
    model = Service
    template_name = "core/service_detail.html"
    context_object_name = "service"


class HomeView(TemplateView):
    template_name = "core/home.html"

class ProgramListView(ListView):
    model = Program
    template_name = "core/program_list.html"
    context_object_name = "programs"

class ProgramDetailView(DetailView):
    model = Program
    template_name = "core/program_detail.html"
    context_object_name = "program"

class ProgramCreateView(CreateView):
    model = Program
    fields = ["name", "description", "national_alignment", "focus_areas", "phases"]
    template_name = "core/program_form.html"
    success_url = reverse_lazy("program_list")

class ProgramUpdateView(UpdateView):
    model = Program
    fields = ["name", "description", "national_alignment", "focus_areas", "phases"]
    template_name = "core/program_form.html"
    success_url = reverse_lazy("program_list")

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "core/program_confirm_delete.html"
    success_url = reverse_lazy("program_list")

# Facility Views
class FacilityListView(ListView):
    model = Facility
    template_name = "core/facility_list.html"
    context_object_name = "facilities"

class FacilityDetailView(DetailView):
    model = Facility
    template_name = "core/facility_detail.html"
    context_object_name = "facility"

class FacilityCreateView(CreateView):
    model = Facility
    fields = ["name", "location", "description", "partner_organization", "facility_type", "capabilities"]
    template_name = "core/facility_form.html"
    success_url = reverse_lazy("facility_list")

class FacilityUpdateView(UpdateView):
    model = Facility
    fields = ["name", "location", "description", "partner_organization", "facility_type", "capabilities"]
    template_name = "core/facility_form.html"
    success_url = reverse_lazy("facility_list")

class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = "core/facility_confirm_delete.html"
    success_url = reverse_lazy("facility_list")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this facility because it is referenced by other records.")
            return self.get(request, *args, **kwargs)
