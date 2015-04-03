from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from hashlib import sha1
import time, os, json, base64, hmac, urllib
from .models import BuildLog, Category, Partner, Project

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
        return form


class BuildLogNew(BuildLogBase, CreateView):
    initial = {'date': timezone.now()}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.project = Project.objects.latest_for_user(self.request.user)
        obj.save()

        return super(BuildLogNew, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BuildLogNew, self).get_context_data(*args, **kwargs)
        context['form_url'] = 'build:new'
        return context

class BuildLogUpdate(BuildLogBase, UpdateView):
    slug_field = 'log_id'
    slug_url_kwarg = 'log_id'

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

@login_required
def photo_upload_url(request):
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    if 's3_object_type' not in request.GET:
        return HttpResponse(json.dumps({}))

    mime_type = request.GET['s3_object_type']

    # FIXME: project from request
    # FIXME: buildlog number from request
    # FIXME: do actually need a better unique for this, but this will do for testing
    project = Project.objects.latest_for_user(request.user)
    object_name = "%s/%s/build/%s" % (request.user.id, project.id, time.time())

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

    response = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
         'url': url
      })
    return HttpResponse(response)