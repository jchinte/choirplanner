# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader
from django.template.context import RequestContext
from models import Song, SongFile, Composer
from formsfields import  SongFileForm
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

def search(request):
    return HttpResponse("You're searching songs.")


def upload(request):
    print "upload function reached"
    if not request.POST:
        print "get handler"
        return HttpResponse("This is GET")
    print "post"
    xhr = request.GET.has_key('xhr')
    print "xhr is " 
    form = SongFileForm(request.POST, request.FILES)
    if form.is_valid():
        print "valid"
        form.save()
        if xhr:
            return HttpResponse(simplejson.dumps({'success': True}), mimetype='application/javascript')
        else:
            return HttpResponse("valid")
    print "invalid"
    return HttpResponse("invalid")
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
        

@csrf_exempt
def modify(request):
    if not request.POST:
        return HttpResponse("This is GET")
    xhr = request.GET.has_key('xhr')
    response_dict = {}
    title = request.POST.get('title', False)
    composer_list_string = request.POST.get('composers', False)
    tag_list = request.POST.get('tags', False)
    songID = request.POST.get('id', False)
    s = Song()
    s.id = songID
    s.title = title
    print s.title
    print s.id
    s.save()
    
    s.composers.clear()
    composer_list = composer_list_string.split(';')
    print "list created"
    first = last = ""
    for composer in composer_list:
        #case last, first
        print "composer: " + composer
        if "," in composer:
            composer_names = composer.split(',', 1)
            last = composer_names[0].strip()
            first = composer_names[1].strip()
        #case first last
        else:
            print "first last format"
            composer_names = composer.split(' ')
            print len(composer_names)
            if len(composer_names) == 1:
                last = composer_names[0].strip()
                first = ""
            else:
                print "first and last names"
                first = " ".join(composer_names[0:len(composer_names)-1]).strip()

                last = composer_names[len(composer_names)-1].strip()
        #search for composer
        print "first: " + first + " and last: " + last
        c, created = Composer.objects.get_or_create(first_name=first, last_name=last)
        print "first: " + c.first_name + " last: " + c.last_name
        #c = Composer(first_name=first, last_name=last)
        
        #add to song
        s.composers.add(c)
    #s.save()    
    print "saved!"
    response_dict.update({'title': title,
                          'composer_list': composer_list,
                          'tag_list': tag_list})
    if xhr:
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')