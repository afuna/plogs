from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from hashlib import sha1
import time, os, json, base64, hmac, urllib
from django.contrib.auth.models import User
from .models import BuildLog, Category, Partner, Project, BuildLogImage

class BuildLogBase(FormMixin):
    model = BuildLog
    fields = ['date', 'duration', 'category', 'reference', 'parts', 'partner', 'summary', 'notes']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuildLogBase, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(BuildLogBase, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.for_user(self.request.user).order_by('name')
        form.fields['partner'].queryset = Partner.objects.for_user(self.request.user).order_by('name')
        form.fields['partner'].help_text ="<a href='%s'>Add</a>" % reverse_lazy(
            'build:partner_new',
            kwargs={"username": self.request.user})
        return form


class BuildLogNew(BuildLogBase, CreateView):
    initial = {'date': timezone.now()}

    def form_valid(self, form):
        buildlog = form.save(commit=False)
        project_name = self.kwargs['project_name']
        buildlog.project = Project.objects.for_user(self.request.user, project_name=project_name).first()
        buildlog.save()

        # now make sure all the images have this buildlog
        images = BuildLogImage.objects.from_build_new()
        for image in images:
            image.build = buildlog
            image.save()

        return super(BuildLogNew, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogNew, self).get_context_data(*args, **kwargs)
        context['form_url'] = reverse_lazy('build:new',
                                           kwargs={
                                               "project_name": self.kwargs['project_name'],
                                               "username": self.request.user,
                                           })
        return context

class BuildLogUpdate(BuildLogBase, UpdateView):
    slug_field = 'log_id'
    slug_url_kwarg = 'log_id'

    def get_queryset(self):
        user = self.request.user
        project_name = self.kwargs['project_name']
        project = Project.objects.for_user(user, project_name=project_name).first()

        log_id = self.kwargs['log_id']
        project_queryset = BuildLog.objects.filter(log_id=log_id, project=project)
        return project_queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogUpdate, self).get_context_data(*args, **kwargs)
        context['images'] = BuildLogImage.objects.for_build(build=context['object'])
        context['form_url'] = reverse_lazy('build:edit',
                                           kwargs={
                                               "project_name": self.kwargs['project_name'],
                                               "log_id": self.kwargs['log_id'],
                                               "username": self.request.user,
                                           })
        context['project_name'] = self.kwargs['project_name']
        return context

class BuildLogDetail(DetailView):
    model = BuildLog
    slug_field = 'log_id'
    slug_url_kwarg = 'log_id'

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs["username"])

        project_name = self.kwargs['project_name']
        project = Project.objects.for_user(user, project_name=project_name).first()

        project_queryset = BuildLog.objects.filter(project=project)
        return project_queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogDetail, self).get_context_data(*args, **kwargs)
        context['images'] = BuildLogImage.objects.for_build(build=context['object'])
        return context

class PartnerNew(CreateView):
    model = Partner
    fields = ['name']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PartnerNew, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('build:partner_list',
                            kwargs={"username": self.request.user})

    def get_context_data(self, *args, **kwargs):
        context = super(PartnerNew, self).get_context_data(*args, **kwargs)
        context['form_url'] = reverse_lazy('build:partner_new',
                                           kwargs={"username": self.request.user})
        return context

    def form_valid(self, form):
        partner = form.save(commit=False)
        partner.user = self.request.user
        partner.save()
        return super(PartnerNew, self).form_valid(form)

class PartnerList(ListView):
    model = Partner

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PartnerList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Partner.objects.filter(user=self.request.user)

@login_required
def photo_upload_url(request):
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    if 's3_object_type' not in request.GET:
        return HttpResponse(json.dumps({}))

    mime_type = request.GET['s3_object_type']
    object_name = request.GET['s3_object_name']
    project_name, buildlog_id = object_name.split("-")

    project = Project.objects.for_user(request.user, project_name=project_name).first()
    build = None
    if buildlog_id:
        build = BuildLog.objects.get(project=project, log_id=buildlog_id)
    image = BuildLogImage(project=project, build=build, url='')
    image.save()

    object_name = "build/%s/%s/%d" % (request.user.id, project.id, image.image_id)

    expires = long(time.time()+60)
    amz_headers = ["x-amz-acl:public-read"]

    md5 = ""
    put_request = "\n".join(["PUT",
                             "%s" % md5,
                             mime_type,
                             str(expires),
                             "\n".join(amz_headers),
                             "/%s/%s" % (S3_BUCKET, object_name),
                            ])

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    image.url = url
    image.save()

    response = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
         'url': url
      })
    return HttpResponse(response)