# Create your views here.
from django.shortcuts import render
from urlparse import urlparse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from models import Event, Segment, SongSegment, Activity, Participant, Role
from django.db.models import Max
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import redirect
from formsfields import ParticipantForm, ActivityForm, EventForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory, modelform_factory,\
    ModelForm
from django.utils.encoding import smart_unicode
from newproject.SongManager.views import JSONResponseMixin 
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView, BaseCreateView,\
    BaseDeleteView
from django.utils import simplejson
from newproject.SongManager.formsfields import SearchForm
from django.template.context import RequestContext
from django.template import Context, loader
from newproject.Event_Planner.formsfields import EventTemplateForm,\
    TemplateChoiceForm, EventCreateForm, AjaxActivityForm
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseServerError

#class SongUploadView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):

class EventListView(ListView):
    queryset=Event.objects.filter(is_template=False)
    context_object_name="event_list"
    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context.update({
                        'templates': TemplateChoiceForm()
                        }) 
        return context   

class OrderUpdateView(JSONResponseMixin, BaseUpdateView):
    model=Event
    def render_to_response(self, context):
        print self.request

        print "ajax"
        #HTTPRequest(self.request)
        print self.request.raw_post_data
        data=simplejson.loads(self.request.raw_post_data)
        #data = simplejson.loads(self.request.raw_post_data)
        print data['array']
    #            for item, value in self.request.POST.items():
    #                print item, value
    #                for v in value:
    #                    print v
    
        qs = Segment.objects.filter(event=self.object.pk)
        i=1;
        for s in data['array']:
            num = s.split('_')[1]
            qs.filter(pk=num).update(order=i)
            print i
            i=i+1
        return JSONResponseMixin.render_to_response(self, {})

class EventUpdateView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):
    model=Event
    #queryset=Event.objects.filter(is_template=False)
    template_name_suffix = '_form'
    form_class = EventForm
    context_object_name = "event"
    segment_queryset = Segment.objects.select_subclasses().order_by('order')
#    segment_queryset = Segment.objects.filter(event=self.object.pk).select_subclasses()

    def get_form_class(self):
        if hasattr(self, 'object') and self.object is not None:
            if self.object.is_template:
                return EventTemplateForm
            else:
                return EventForm
        return self.form_class

    def __init__(self, *args, **kwargs):
        super(EventUpdateView,self).__init__(*args, **kwargs)
        #self.segment_queryset = Segment.objects.filter(event=self.object.pk).select_subclasses()
        
    @method_decorator(permission_required('Event_Planner.change_event'))
    def dispatch(self, *args, **kwargs):
        
        return super(EventUpdateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        #Segmentformset = modelformset_factory(Segment, extra=0)
        #formset = Segmentformset(queryset=Segment.objects.filter(event=self.object.pk).select_subclasses().order_by('order'))
        #print formset
#        segments = Segment.objects.filter(event=self.object.pk)
        #context.update({'formset': formset})
        
        form_list = []
        segment_list = list(self.segment_queryset.filter(event=self.object.pk))
        i=0
        for seg in segment_list:
            new_form_class = modelform_factory(seg.__class__)
            new_form = new_form_class(instance=seg, prefix=(u'segment-'+smart_unicode(seg.pk)))
            #print new_form.as_p()
#            new_form.prefix = u'form-'+smart_unicode(i)
#            new_form.instance=seg
            #__init__(prefix=u'form'+smart_unicode(i), instance=seg)
            
            form_list.append(new_form)
            #print ModelForm(form_list[i]).as_p()
            i = i+1
        context.update({'formlist': form_list})
        form = SearchForm()
        context.update({'search_form': form,})
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.has_key('add_seg'):
            return redirect('segment_create_view', kwargs['pk'])
        if request.GET.has_key('add_songseg'):
            return redirect('songsegment_create_view', kwargs['pk'])
        return super(EventUpdateView, self).get(request, *args, **kwargs)
    
    def render_to_response(self, context):
        print self.request
        if self.request.is_ajax() or self.request.GET.has_key('xhr'):
            print "ajax"
            #HTTPRequest(self.request)
            print self.request.raw_post_data
            data=simplejson.loads(self.request.raw_post_data)
            #data = simplejson.loads(self.request.raw_post_data)
            print data['array']
#            for item, value in self.request.POST.items():
#                print item, value
#                for v in value:
#                    print v

            qs = Segment.objects.filter(event=self.object.pk)
            i=1;
            for s in data['array']:
                num = s.split('_')[1]
                qs.filter(pk=num).update(order=i)
                print i
                i=i+1
            return JSONResponseMixin.render_to_response(self, {})
        else:
            print "not ajax"
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)
    
class EventDetailView(DetailView):
    model=Event
    #queryset=Event.objects.filter(is_template=False)
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        segments = Segment.objects.filter(event=self.object.pk).order_by('order')
        context.update({'segments': segments})
        return context
class EventDeleteView(DeleteView):
#    pass
    @method_decorator(permission_required('Event_Planner.delete_event'))
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)

    model = Event
    def get_success_url(self):
        return reverse('event_list_view')

class ActivityCreateView(CreateView):
    model=Activity
    form_class = ActivityForm

    @method_decorator(permission_required('Event_Planner.add_activity'))
    def dispatch(self, *args, **kwargs):
        return super(ActivityCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        if self.request.POST.has_key('segment_event'):
            return super(ActivityCreateView, self).get_initial()
        url = self.request.path
        print url
        match = resolve(urlparse(url)[2])
        print match.kwargs['pk']
        segment = Segment.objects.get(pk=match.kwargs['pk'])
        initial = {
                   'segment_event': segment,
                   }
        return initial
    
    def get_success_url(self):
        print self.kwargs
        match = resolve(urlparse(self.request.path)[2])
        
        return reverse('event_update_view', args=[match.kwargs['event_id']])
    def render_to_response(self, context):
        context.update({'curr_url': self.request.path})
        return super(ActivityCreateView, self).render_to_response(context)

class AjaxActivityCreateView(JSONResponseMixin, BaseCreateView):
    model=Activity
    form_class = AjaxActivityForm
    template_name='Event_Planner/ajax_activity_form.html'
    activity_list_template_name='Event_Planner/new_activity_form.html'

    @method_decorator(permission_required('Event_Planner.add_activity'))
    def dispatch(self, request, *args, **kwargs):
        print "dispatch reached"
        return super(AjaxActivityCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        print self.request.POST
        if self.request.POST.has_key('segment_event'):
            return super(AjaxActivityCreateView, self).get_initial()
        url = self.request.path
        print url
        match = resolve(urlparse(url)[2])
        print match.kwargs['pk']
        segment = Segment.objects.get(pk=match.kwargs['pk'])
        initial = {
                   'segment_event': segment,
                   }
        return initial
    def post(self, request, *args, **kargs):
        self.object=None
        print "post reached"
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            c = RequestContext(self.request, Context())
            print c
            
            c.update({'segment': form.instance.segment_event})
            print c
            t = loader.get_template(self.activity_list_template_name)
            print t
            activities = t.render(c)
            print activities
            return JSONResponseMixin.render_to_response(self, {'success':"Activity saved",
                                                               'activities': activities})
        else:
            print "invalid form"
            if form._errors.has_key('participant_name'):
                print "no part name"
            else:
                print "other error"
            print "returning form invalid"
            return self.form_invalid(form)
        

            

    def render_to_response(self, context):
        print"render"
        context.update({'curr_url': self.request.path})
        print context
        c = RequestContext(self.request, context)
        t = loader.get_template(self.template_name)
        segdata = t.render(c)
        #ajax_dictionary.update({'html': segdata})
#        response = super(SingleObjectTemplateResponseMixin, self).render_to_response(context)
#        print response.content
        print segdata
        con = Context()
        con.update({'data': segdata})
        return JSONResponseMixin.render_to_response(self, {'data':segdata})

class ActivityDeleteView(DeleteView):
#    pass
    model = Activity
    
    @method_decorator(permission_required('Event_Planner.delete_activity'))
    def dispatch(self, *args, **kwargs):
        return super(ActivityDeleteView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        match = resolve(urlparse(self.request.path)[2])
        return reverse('event_update_view', args=[match.kwargs['event_id']]) 
#    def get_context_data(self, **kwargs):
#        context = super(ActivityDeleteView, self).get_context_data(**kwargs)
#        context.update({'segment': self.request.path})            
class ParticipantCreateView(CreateView):
    form_class = ParticipantForm
    template_name = "Event_Planner/generic_form.html"

    @method_decorator(permission_required('Event_Planner.add_partcipant'))
    def dispatch(self, *args, **kwargs):
        return super(ParticipantCreateView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context):
        if self.request.GET.has_key('back_url'):
            context.update({'back_url': self.request.GET['back_url']})
        return super(ParticipantCreateView, self).render_to_response(context)
    
    def get_success_url(self):
        if self.request.GET.has_key('back_url'):
            return self.request.GET['back_url']
        return reverse('event_list_view')
    
class RoleCreateView(CreateView):
    template_name = "Event_Planner/generic_form.html"
    model = Role

    @method_decorator(permission_required('Event_Planner.add_role'))
    def dispatch(self, *args, **kwargs):
        return super(RoleCreateView, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context):
        if self.request.GET.has_key('back_url'):
            context.update({'back_url': self.request.GET['back_url']})
        return super(RoleCreateView, self).render_to_response(context)
    
    def get_success_url(self):
        if self.request.GET.has_key('back_url'):
            return self.request.GET['back_url']
        return reverse('event_list_view')


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    @method_decorator(permission_required('Event_Planner.add_event'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('can_create_template'):
            self.form_class=EventCreateForm
        return super(EventCreateView, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('event_update_view', args=[self.object.pk])
    def render_to_response(self, context):
        print "createview render to response"
        print context
        return super(EventCreateView, self).render_to_response(context)

class MassCreateView(EventCreateView):
    def form_valid(self, form):
        response = super(MassCreateView, self).form_valid(form)
        SongSegment(order=1, title='Processional', event=self.object).save()
        SongSegment(order=2, title='Gloria', event=self.object).save()
        SongSegment(order=3, title='Responsorial Psalm', event=self.object).save()
        SongSegment(order=4, title='Gospel Acclamation', event=self.object).save()
        SongSegment(order=5, title='Preparation of the Gifts', event=self.object).save()
        SongSegment(order=6, title='Holy', event=self.object).save()
        SongSegment(order=7, title='Mystery of Faith', event=self.object).save()
        SongSegment(order=8, title='Great Amen', event=self.object).save()
        SongSegment(order=9, title='Lamb of God', event=self.object).save()
        SongSegment(order=10, title='Communion', event=self.object).save()
        SongSegment(order=11, title='Song of Praise', event=self.object).save()
        SongSegment(order=12, title='Recessional', event=self.object).save()
        #segment.save()
        return response

class TemplateCreateView(EventCreateView):
    form_class=EventForm
    
#    @method_decorator(permission_required('Event_Planner.can_create_template'))
#    def dispatch(self, *args, **kwargs):
#        return super(EventCreateView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        print request.GET
        if self.request.GET.has_key('template'):
            self.template=self.request.GET['template']
        return super(TemplateCreateView, self).post(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super(TemplateCreateView, self).form_valid(form)        
        if hasattr(self, 'template') and self.template is not None:
            segments = Segment.objects.select_subclasses().filter(event=self.template)
            for segment in segments:
                print segment
                print segment.pk
                segment.pk=None
                segment.id=None
                segment.event = self.object
                segment.save()
                print "new ID:"
                print segment.id
        return response
        
            
    
class SegmentCreateView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseCreateView):
    model = Segment
    template_name_suffix = '_form'
    title = None
    @method_decorator(permission_required('Event_Planner.add_segment'))
    def dispatch(self, *args, **kwargs):
        return super(SegmentCreateView, self).dispatch(*args, **kwargs)
    
    def get_initial(self):
        if self.request.POST.has_key('event'):
            return super(SegmentCreateView, self).get_initial()
        if (self.request.META.has_key('HTTP_REFERER')):
            url = self.request.META['HTTP_REFERER']
        else:
            url = self.request.path
        match = resolve(urlparse(url)[2])
        event = Event.objects.get(pk=match.kwargs['pk'])
        max_order = event.segment_set.aggregate(Max('order'))
        if max_order['order__max']:
            new_order = max_order['order__max'] + 1
        else:
            new_order = 1
        if self.title:
            title = self.title
        else:
            title = "segment"
        initial = {
                   'event': event,
                   'order': new_order,
                   'title': title,
                   }
        return initial
        
    def get_success_url(self):

            print self.object.event.pk
            return reverse('event_update_view', args=[self.object.event.pk])

#    def get(self, request, *args, **kargs):
#        print request
#        if request.is_ajax() or request.GET.has_key('xhr'):
#            print "ajax"
#            ajax_dictionary = {}
#            c = Context()
#            print c
#            form = self.get_form(self.get_form_class())
#            print form
#            c.update({
#                      'form': form,
#                    }) 
#            print c
#            #c.update(self.initial)
#            #print c
#            t = loader.get_template('Event_Planner/new_seg_form.html')
#            segdata = t.render(c)
#            print segdata
#            ajax_dictionary.update({'html': segdata})
##            #HTTPRequest(self.request)
##            print self.request.raw_post_data
##            data=simplejson.loads(self.request.raw_post_data)
##            #data = simplejson.loads(self.request.raw_post_data)
##            print data['array']
###            for item, value in self.request.POST.items():
###                print item, value
###                for v in value:
###                    print v
##
##            qs = Segment.objects.filter(event=self.object.pk)
##            i=1;
##            for s in data['array']:
##                num = s.split('_')[1]
##                qs.filter(pk=num).update(order=i)
##                print i
##                i=i+1
#            return JSONResponseMixin.render_to_response(self, ajax_dictionary)
#        else:
#            print "not ajax"
#            return super(SegmentCreateView, self).get(request, *args, **kargs)
            #return SingleObjectTemplateResponseMixin.render_to_response(self, context)       
    def get_form_kwargs(self):
        kwargs = super(SegmentCreateView, self).get_form_kwargs()
        print "segmentcreateview - "
        if self.object:
            kwargs.update({'prefix': (u'segment-'+smart_unicode(self.object.pk))})
        print kwargs
        return kwargs
    def render_to_response(self, context):
        print self.request
        if self.request.is_ajax() or self.request.GET.has_key('xhr'):
            ajax_dictionary = {}
            initial = self.get_initial()
            self.object = self.model(order=initial['order'], title=initial['title'], event=initial['event'])
            self.object.save()
            prefix=(u'segment-'+smart_unicode(self.object.pk))
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            c={
                      'form': form,
                      'event': initial['event']
                      }
            c = RequestContext(self.request, c)
            t = loader.get_template('Event_Planner/new_seg_form.html')
            segdata = t.render(c)
            ajax_dictionary.update({'html': segdata})
            return JSONResponseMixin.render_to_response(self, ajax_dictionary)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)




class SongSegmentCreateView(SegmentCreateView):
    model = SongSegment
    
    @method_decorator(permission_required('Event_Planner.add_songsegment'))
    def dispatch(self, *args, **kwargs):
        return super(SongSegmentCreateView, self).dispatch(*args, **kwargs)
        

   
class SegmentUpdateView(UpdateView):
    queryset = Segment.objects.select_subclasses()
    
    @method_decorator(permission_required('Event_Planner.change_segment'))
    def dispatch(self, *args, **kwargs):
        return super(SegmentUpdateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(SegmentUpdateView, self).get_form_kwargs()
        print "segmentupdateview - "
        match = resolve(urlparse(self.request.path)[2])
        kwargs.update({'prefix': (u'segment-'+smart_unicode(match.kwargs['pk']))})
        print kwargs
        return kwargs
    
    def get_success_url(self):
        print self.object.event.pk
        return reverse('event_update_view', args=[self.object.event.pk])
    
class JSONSegmentUpdateView(JSONResponseMixin, BaseUpdateView):
    queryset = Segment.objects.select_subclasses()
    
    @method_decorator(permission_required('Event_Planner.change_segment'))
    def dispatch(self, *args, **kwargs):
        return super(JSONSegmentUpdateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(JSONSegmentUpdateView, self).get_form_kwargs()
        print "jsonsegmentupdateview - "
        match = resolve(urlparse(self.request.path)[2])
        kwargs.update({'prefix': (u'segment-'+smart_unicode(match.kwargs['pk']))})
        print kwargs
        return kwargs
    def form_valid(self, form):
        # save form
        print "saving"
        print form
        #result =  BaseUpdateView.form_valid(self, form)
        form.save()
        print "saved"
        # return nothing
        return self.render_to_response({})
    #### TODO: present elegant form invalid response
    def form_invalid(self, form):
        print "form invalid"
        print form
        return HttpResponseServerError("could not save form")
#        return BaseUpdateView.form_invalid(self, form)
#    def post(self, *args, **kargs):
#        print "IN POST"
#        self.object = self.get_object()
#        self.object.delete()
#        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
#        print "after super post"
#        return self.render_to_response({})
#    def get_success_url(self):
#        print self.object.event.pk
#        return reverse('event_update_view', args=[self.object.event.pk])
    
class SongSegmentUpdateView(SegmentUpdateView):
    queryset=Segment.objects.select_subclasses()
    model = SongSegment
    def get_object(self, queryset=None):
        ### this method must be called via post.
        ### this method should NEVER be called via get.  
        print "get object!!!!!!!!!"
        self.object = super(SongSegmentUpdateView, self).get_object(queryset)
        
        if isinstance(self.object, SongSegment):
            pass
        elif self.object is not None:
            print "is reg segment"
            seg = self.object
            self.object = SongSegment()
            self.object.pk = seg.pk
            #self.object.delete()
            #self.object=None
        print "end get object"
        return self.object

class SegmentDeleteView(DeleteView):

    model = Segment

    @method_decorator(permission_required('Event_Planner.delete_segment'))
    def dispatch(self, *args, **kwargs):
        
        return super(SegmentDeleteView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self):
        match = resolve(urlparse(self.request.path)[2])
        return reverse('event_update_view', args=[match.kwargs['event_id']]) 
    
#################TODO: ADD PERMISSIONS DECORATORS TO JSON views
    
    
class JSONSegmentDeleteView(JSONResponseMixin, BaseDeleteView):
    model = Segment
    def post(self, *args, **kargs):
        print "IN POST"
        self.object = self.get_object()
        self.object.delete()
        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
        print "after super post"
        return self.render_to_response({})
    
class JSONActivityDeleteView(JSONResponseMixin, BaseDeleteView):
    model = Activity
    def post(self, *args, **kargs):
        print "IN POST"
        self.object = self.get_object()
        self.object.delete()
        #super(JSONSegmentDeleteView, self).post(*args, **kargs)
        print "after super post"
        return self.render_to_response({})
    
# non-generic views

def JSONRoleListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        roles = Role.objects.filter(name__icontains=term)
    else:
        roles = Role.objects.all()
    role_list = []
    for role in roles:
        role_list.append(smart_unicode(role))
        
    response = HttpResponse(simplejson.dumps(role_list,  ensure_ascii=False))
    return response
    
        
def JSONParticipantListView(request):
    term = None
    if request.GET.has_key('term'):
        term = request.GET['term']
    if term:
        participants = Participant.objects.filter(name__icontains=term) 
    else:
        participants = Participant.objects.all()
    participant_list = []
    for participant in participants:
        participant_list.append(smart_unicode(participant))
        
    response = HttpResponse(simplejson.dumps(participant_list,  ensure_ascii=False))
    return response
    