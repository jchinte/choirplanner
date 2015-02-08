from django.db import models
from SongManager.models import Song
from model_utils.managers import InheritanceManager
from django.contrib.auth.models import User
#from inheritance import ParentModel, ChildManager

# Create your models here.
class Event(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, blank=True)
    is_template = models.BooleanField(default=False)
    

    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('event_detail_view', [str(self.pk)])#, [str(self.id)])
    
    class Meta:
        permissions = (
            ("can_create_template", "Can create an event template"),
        )
    
class Segment(models.Model):
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    event = models.ForeignKey(Event)
    
    objects = InheritanceManager()
#    objects = models.Manager()
#    children = ChildManager()
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ["order"]
 #   def get_parent_model(self):
 #       return Segment
    
class LinkedSegment(Segment):
    link = models.URLField()

class SongSegment(Segment):
    song = models.ForeignKey(Song, blank=True, null=True)
    
    
class Role(models.Model):
    name = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name
#    participants = models.ManyToManyField(User, through='Activity')
    #participants = models.ManyToManyField('Participant', through='Activity')
    
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    roles = models.ManyToManyField(Role, through='Activity')
    
    def __unicode__(self):
        return self.name
    
class Activity(models.Model):
    role = models.ForeignKey(Role)
    participant = models.ForeignKey(Participant)
    segment_event = models.ForeignKey(Segment)
    send_reminder = models.BooleanField()
    
    
