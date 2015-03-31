from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from plogs.planes.models import Plane

class CategoryManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user)

class Category(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)

    objects = CategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')
        verbose_name_plural = 'categories'

class PartnerManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user)

class Partner(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)

    objects = PartnerManager()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')

class Project(models.Model):
    plane = models.ForeignKey(Plane)
    date_started = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.plane

class BuildLog(models.Model):
    project = models.ForeignKey(Project)

    category = models.ForeignKey(Category)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    date = models.DateField()
    duration = models.PositiveSmallIntegerField('hours', blank=True)

    reference = models.CharField('manual section', max_length=255, blank=True)
    parts = models.CharField('part numbers', max_length=255, blank=True)

    summary = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.summary or "(no summary)"

    def get_absolute_url(self):
        return reverse('build:view', args=[str(self.id)])
    # images
