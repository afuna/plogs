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
        """Get the latest project for the user. This will eventually be replaced
        by the last project the user has touched."""
        return self.filter(plane__owner=user).order_by('-id').first()

    def for_user(self, user, project_name=None):
        queryset = self.filter(plane__owner=user)

        if project_name:
            queryset = queryset.filter(plane__kit__model=project_name)

        return queryset

class Project(models.Model):
    plane = models.ForeignKey(Plane)
    date_started = models.DateField(auto_now_add=True)

    objects = ProjectManager()

    def owner(self):
        """Return the user that owns this project."""
        return self.plane.owner

    def __unicode__(self):
        return "%s" % self.plane

class BuildLogStatisticsManager(models.Manager):
    def for_project(self, project):
        statistics = BuildLog.objects.filter(project=project).aggregate(hours=models.Sum('duration'), sessions=models.Count('id'))

        if statistics['hours'] is None:
            statistics['hours'] = 0

        # FIXME: add gathering of these statistics
        statistics['dollars'] = 0

        return statistics

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

    objects = models.Manager()
    statistics = BuildLogStatisticsManager()

    def owner(self):
        return self.project.owner()

    def __unicode__(self):
        return "%d %s" % (self.log_id, self.summary or "(no summary)")

    def get_absolute_url(self):
        return reverse('build:view',
                       kwargs={
                           "log_id": str(self.log_id),
                           "project_name": self.project.plane.kit.model,
                           "username": self.project.plane.owner.username,
                       })

    def save(self, *args, **kwargs):
        """ Custom save logic. We want to have a per-project log id (instead of per-table). """
        if self.log_id is None:
            # Grab the highest current index (if it exists)
            try:
                recent = BuildLog.objects.filter(project=self.project).latest('log_id')
                self.log_id = recent.log_id + 1
            except BuildLog.DoesNotExist:
                self.log_id = 1

        if self.duration is None:
            self.duration = 0

        super(BuildLog, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('project', 'log_id')

class BuildLogImageManager(models.Manager):
    def from_build_new(self, project):
        return self.filter(project=project, build=None)

    def for_build(self, build):
        return self.filter(build=build)

class BuildLogImage(models.Model):
    project = models.ForeignKey(Project)
    url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True)

    # may have uploaded the image without having created the build yet
    build = models.ForeignKey(BuildLog, null=True, related_name='images')

    # per project
    image_id = models.PositiveIntegerField()

    objects = BuildLogImageManager()

    def __unicode__(self):
        return "%s (%s)" % (self.caption, self.url)
    def save(self, *args, **kwargs):
        """Custom save logic. We want to have a per-project image id (instead of per-table)"""
        if self.image_id is None:
            # Grab the highest current index (if it exists)
            try:
                recent = BuildLogImage.objects.filter(project=self.project).latest('image_id')
                self.image_id = recent.image_id + 1
            except BuildLogImage.DoesNotExist:
                self.image_id = 1

        super(BuildLogImage, self).save(*args, **kwargs)