from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DeleteView
from webapp.models import Issue
from django.utils.http import urlencode
from webapp.forms import IssueForm, SearchForm
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(ListView):
    model = Issue
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    ordering = "-update_time"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["query"] = urlencode({"search": self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data["search"]


class IssueView(TemplateView):
    template_name = 'issues/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        return context


class AddIssue(LoginRequiredMixin, FormView):
    template_name = 'issues/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:issue_detail", kwargs={"issue_pk": self.issue.pk})


class UpdateIssue(LoginRequiredMixin, FormView):
    template_name = "issues/update.html"
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Issue, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue"] = self.issue
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:project_detail", kwargs={"pk": self.issue.project.pk})


class DeleteIssue(LoginRequiredMixin, DeleteView):
    template_name = 'issues/delete.html'
    form_class = IssueForm
    model = Issue
    context_object_name = 'issues'

    def get_success_url(self):
        id = self.kwargs.get("pk")
        project = get_object_or_404(Issue, pk=id)
        return reverse('webapp:project_detail', kwargs={"pk": project.project.pk})
