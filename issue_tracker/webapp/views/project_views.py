from django.views.generic import ListView, DetailView, CreateView
from webapp.models import Project, Issue
from django.urls import reverse


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/index.html'


class ProjectDetailedView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issues"] = Issue.objects.filter(task=self.object.pk)
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/create.html'
    fields = ['start_date', 'finish_date', 'project_name', 'project_summary']

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_list')
