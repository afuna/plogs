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

    @classmethod
    def default_categories(cls):
        return ('Avionics', 'Empennage', 'Engine', 'Fuselage', 'Miscellaneous', 'Prop', 'Tools', 'Wings')

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

class ProjectManager(models.Manager):
    def latest_for_user(self, user):
        return self.get_queryset().filter(plane__owner=user).order_by('-id').first()

class Project(models.Model):
    plane = models.ForeignKey(Plane)
    date_started = models.DateField(auto_now_add=True)

    objects = ProjectManager()

    def __unicode__(self):
        return "%s" % self.plane

class BuildLog(models.Model):
    project = models.ForeignKey(Project)
    log_id = models.PositiveIntegerField() # per-project

    category = models.ForeignKey(Category)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    date = models.DateField()
    duration = models.DecimalField('hours', blank=True, max_digits=5, decimal_places=2)

    reference = models.CharField('manual section', max_length=255, blank=True)
    parts = models.CharField('part numbers', max_length=255, blank=True)

    summary = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.summary or "(no summary)"

    def get_absolute_url(self):
        return reverse('build:view', args=[str(self.log_id)])

    def save(self, *args, **kwargs):
        """ Custom save logic. We want to have a per-project log id (instead of per-table). """
        if self.log_id is None:
            # Grab the highest current index (if it exists)
            try:
                recent = BuildLog.objects.filter(project=self.project).order_by('-log_id').first()
                self.log_id = recent.log_id + 1
            except AttributeError:
                self.log_id = 1

        if self.duration is None:
            self.duration = 0

        super(BuildLog, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('project', 'log_id')