from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.utils import timezone
from .models import BuildLog, Category, Partner, Project

class BuildLogBase(FormMixin):
    model = BuildLog
    fields = ['date', 'duration', 'category', 'reference', 'parts', 'partner', 'summary', 'notes']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuildLogBase, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(BuildLogBase, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.for_user(self.request.user)
        form.fields['partner'].queryset = Partner.objects.for_user(self.request.user)
        return form


class BuildLogNew(BuildLogBase, CreateView):
    initial = {'date': timezone.now()}

    def form_valid(self, form):
        obj = form.save(commit=False)

        if not form['duration'].value():
            obj.duration = 0

        obj.project = Project.objects.filter(plane__owner=self.request.user).last()
        obj.save()

        return super(BuildLogNew, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogNew, self).get_context_data(*args, **kwargs)
        context['form_url'] = 'build:new'
        return context

class BuildLogUpdate(BuildLogBase, UpdateView):
    def form_valid(self, form):
        obj = form.save(commit=False)

        if not form['duration'].value():
            obj.duration = 0
        obj.save()

        return super(BuildLogUpdate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogUpdate, self).get_context_data(*args, **kwargs)
        context['form_url'] = 'build:edit'
        return context

class BuildLogDetail(DetailView):
    model = BuildLog
    slug_field = 'log_id'
    slug_url_kwarg = 'log_id'

    def get_queryset(self):
        project = Project.objects.latest_for_user(self.request.user)
        project_queryset = BuildLog.objects.get_queryset().filter(project=project)

        return project_queryset

