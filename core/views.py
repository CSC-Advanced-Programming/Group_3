from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Program

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
