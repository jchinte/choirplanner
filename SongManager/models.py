from django.db import models
from django.utils.encoding import smart_unicode

# Create your models here.
class Composer(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    
    
    def __unicode__(self):
        return (smart_unicode(self.first_name) + smart_unicode(' ') + smart_unicode(self.last_name))
    
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.tag_name

            

class Song(models.Model):
    title = models.CharField(max_length=200)
    composers = models.ManyToManyField(Composer, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    first_line = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ["title"]
        
    @models.permalink
    def get_absolute_url(self):
        return ('song_detail_view', [str(self.id)])
    
    @models.permalink
    def get_update_url(self):
        return ('song_update_view', [str(self.id)])
    
    @models.permalink
    def get_delete_url(self):
        return ('song_delete_view', [str(self.id)])


class SongFile(models.Model):
    #filename = models.CharField(max_length=200)
    file = models.FileField(upload_to='songs')
    song = models.ForeignKey(Song)
    comments = models.CharField(max_length=300, blank=True)
    filetypes = models.ManyToManyField('FileType')
    
    def name(self):
        print "Name is called"
        return self.__unicode__()
    
    def __unicode__(self):
        s = (str(self.file.name)).split('/')
        print "__unicode__"
        print s
        return s[len(s)-1]

class FileType(models.Model):
    type = models.CharField(max_length=80)
