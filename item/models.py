from django.db import models
from django.contrib.auth.models import User
import eav
from eav.models import Attribute

#class Attribute(models.Model):
#    name = models.CharField(max_length=20)


class Item(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
#    attributes = models.ManyToManyField(Attribute, through='ItemAttribute')

    def __unicode__(self):
        return self.name

    def add_attribute(self, attribute, value):
        self.eav[attribute] = value
        self.save()
        #Attribute.objects.create(name='Weight', datatype=Attribute.TYPE_FLOAT)
        #item_attribute = ItemAttribute(attribute=attribute, value=value, item=self)

        #item_attribute.save()

eav.register(Item)

#class ItemAttribute(models.Model):
#    attribute = models.ForeignKey(Attribute)
#    item = models.ForeignKey(Item)
#    value = models.CharField(max_length=50)
