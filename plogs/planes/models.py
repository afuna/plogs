from django.db import models
from django.contrib.auth.models import User

class Kit(models.Model):
    manufacturer = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        serial_number = ""
        if self.serial_number:
            serial_number = " #%s" % self.serial_number
        return "%s%s" % (self.model, serial_number) or "<%s #%d>" % (self.__class__.__name__, self.id)

class Engine(models.Model):
    manufacturer = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    horsepower = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        hp, serial_number = "", ""
        if self.serial_number:
            serial_number = " #%s" % self.serial_number
        if self.horsepower:
            hp = " %s HP" % self.horsepower
        return "%s%s%s" % (self.model, hp, serial_number) or "<%s #%d>" % (self.__class__.__name__, self.id)


class Prop(models.Model):
    manufacturer = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, blank=True)

    PROP_TYPES = (
                  ('FP', 'Fixed Pitch'),
                  ('CS', 'Constant Speed')
                 )
    prop_type = models.CharField(max_length=2, choices=PROP_TYPES)

    def __unicode__(self):
        prop_type, serial_number = "", ""
        if self.serial_number:
            serial_number = " #%s" % self.serial_number
        if self.prop_type:
            prop_type = " %s" % self.get_prop_type_display()
        return "%s%s%s" % (self.model, prop_type, serial_number) or "<%s #%d>" % (self.__class__.__name__, self.id)

class PlaneManager(models.Manager):
    def for_user(self, user):
        return self.filter(owner=user)

class Plane(models.Model):
    owner = models.ForeignKey(User)

    kit = models.ForeignKey(Kit)
    engine = models.ForeignKey(Engine)
    prop = models.ForeignKey(Prop)

    objects = PlaneManager()

    def __unicode__(self):
        return "%s" % self.kit
