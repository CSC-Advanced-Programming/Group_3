from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Program, Facility
from django.contrib import messages
from django.db.models import ProtectedError

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
