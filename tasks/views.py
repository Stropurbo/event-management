from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from tasks.models import Event, Category
from tasks.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
# from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView,TemplateView,CreateView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager_or_admin(user):
    return user.is_authenticated and (is_manager(user) or is_admin(user))


create_decorators = [login_required, permission_required("tasks.add_event", login_url="no_permission")]
update_decorators = [login_required, permission_required("tasks.change_event", login_url="no_permission")]
create_cat_decorator = [login_required, permission_required("tasks.add_category", login_url="no_permission")]
add_par_decorator = [login_required, permission_required("tasks.add_participant", login_url="no_permission")]
delete_par_decorator = [login_required, permission_required("tasks.delete_user", login_url="no_permission")]
delete_event_decorator = [login_required, permission_required("tasks.delete_event", login_url="no_permission")]
delete_cat_decorator = [login_required, permission_required("tasks.delete_category", login_url="no_permission")]


def home(request):
    search_q = request.GET.get('search', '').strip()

    if search_q:
        all_event = Event.objects.filter(
            Q(name__icontains = search_q) | Q(location__icontains=search_q)
        )
    else:
        all_event = Event.objects.all()

    all_event = all_event.annotate(join_count = Count('participants'))
    cat = Category.objects.all()    
    
    context ={
        "all_event" : all_event,
        'cat' : cat,            
        'search_q' : search_q
    }
    return render(request, 'home.html', context)

class Home(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'all_event'

    def get_queryset(self):
        search_q = self.request.GET.get('search', '').strip()
        category = self.request.GET.get('category', '')

        all_event = Event.objects.all()

        if search_q:
            all_event = all_event.filter(
                Q(name__icontains = search_q) | Q(location__icontains=search_q)
            )

        if category:
            all_event = all_event.filter(category__id=category)

        return all_event.annotate(join_count = Count('participants'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        return context

    
@login_required
@permission_required("tasks.add_event", login_url="no_permission")
def create_event(request):
    event_form = EventModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES)
        
        if event_form.is_valid():

            event = event_form.save()
            participants = event_form.cleaned_data['participants']
            event.participants.set(participants) # for save participant

            event.save()

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 

    context = {
        "create_event": event_form
    }
    return render(request, 'create_event.html', context)

@method_decorator(create_decorators, name="dispatch")
class CreateEvent(View):
    event_html = "create_event.html"

    def get(self, request, *args, **kwargs):
        event_form = EventModelForm()

        context = {
        "create_event": event_form  
        }

        return render(request, self.event_html, context)


    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)        
        if event_form.is_valid():

            event = event_form.save()
            participants = event_form.cleaned_data['participants']
            event.participants.set(participants) # for save participant

            event.save()

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 
        
@method_decorator(update_decorators, name="dispatch")
class UpdateEvent(View):
    update_template = "update_event.html"

    def get(self, request, *args, **kwargs):           
        event = get_object_or_404(Event, id=kwargs['id'])     
        form = EventModelForm(instance = event)

        context = {
            'update_event' : form
            }

        return render(request, self.update_template, context)

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs['id'])    
        form = EventModelForm(request.POST, request.FILES, instance = event)
        if form.is_valid():
            form.save()
        
        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event')
        else:
            return redirect('home')

@login_required
@permission_required("tasks.change_event", login_url="no_permission")
def update_event(request, id):
    event = Event.objects.get(id = id)
    
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES, instance = event)
        if form.is_valid():
            form.save()

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat')        
    
    else:
        form = EventModelForm(instance = event)
    
    context = {
        'update_event' : form
    }

    return render(request, 'update_event.html', context)


class ShowCategory(TemplateView):
    template_name = "delete_cat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = Category.objects.all()
        return context

def show_cat(request):    
   cat = Category.objects.all()   
   context = {
       'cat' : cat
   }
   return render(request, 'delete_cat.html', context)

@method_decorator(create_cat_decorator, name="dispatch")
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = "cat_form.html"
    success_url = reverse_lazy('delete_cat')

    def form_valid(self, form):
        response =  super().form_valid(form)

        if self.request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif self.request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_form'] = self.get_form()
        return context

@login_required
@permission_required("tasks.add_category", login_url="no_permission")
def create_category(request):
    cat_form = CategoryModelForm()

    if request.method == 'POST':
        cat_form = CategoryModelForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin-dashboard') 
        else:
            return redirect('delete_cat') 
        
    context = {
        'cat_form' : cat_form
    }

    return render(request, 'cat_form.html', context)

@method_decorator(add_par_decorator, name="dispatch")
class CreateParticipant(CreateView):
    model = Event
    form_class = ParticipantModelForm
    template_name = "partici_form.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['partici_form'] = self.get_form()
        context['events'] = Event.objects.all()
        return context
    
    def form_valid(self, form):
        event = form.cleaned_data.get("event")
        participants = form.cleaned_data.get("participants")
        
        for participant in participants:
            event.participants.add(participant)
            messages.success(self.request, "Participant Added Successfull")

        if self.request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif self.request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat')
        

@login_required
@permission_required("tasks.add_participant", login_url="no_permission")
def create_participate(request):
    partici_form = ParticipantModelForm()
    events = Event.objects.all()

    if request.method == 'POST':
        partici_form = ParticipantModelForm(request.POST)
        event_id = request.POST.get("event")
        
        if partici_form.is_valid() and event_id:
            event = partici_form.cleaned_data.get("event")
            participants = partici_form.cleaned_data.get("participants")
        
            
            for participant in participants:
                participant.save()  
                event.participants.add(participant)

            messages.success(request, "Participant added Successfull")

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 

    context = {
        'partici_form': partici_form,
        'events': events,
    }
    return render(request, 'partici_form.html', context)


@method_decorator(delete_par_decorator, name="dispatch")
class DeleteParticipant(View):
    def post(self, request, event_id, user_id):
        event = get_object_or_404(Event, id=event_id)
        user = get_object_or_404(User, id=user_id)

        if user in event.participants.all():
            event.participants.remove(user)
            messages.success(request, f"Successfully removed {user.first_name} from the event.")
        
        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat')
        

@login_required
@permission_required("tasks.delete_user", login_url="no_permission")
def delete_participant(request, event_id, user_id):
    if request.method == "POST":

        event = get_object_or_404(Event, id=event_id)
        user = get_object_or_404(User, id=user_id)

        if user in event.participants.all():
            event.participants.remove(user)
            messages.success(request, f"Successfully removed {user.first_name} from the event.")

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 

    return redirect('dashboard')

@method_decorator(delete_event_decorator, name="dispatch")
class DeleteEvent(View):
    def post(self, request, id):
        event = get_object_or_404(Event, id=id)
        event.delete()

        messages.success(request, f"{event.name} Deleted Success")

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat')

@login_required
@permission_required("tasks.delete_event", login_url="no_permission")
def delete_event(request, id):
    event = get_object_or_404(Event, id = id)
    
    if request.method == 'POST':
        event.delete()
        
        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 
    

    return redirect('dashboard')

@method_decorator(delete_cat_decorator, name="dispatch")
class DeleteCategory(View):

    def post(self, request):        
        select_cat = request.POST.getlist('category')
        
        for cat_id in select_cat:
            category = get_object_or_404(Category, id=cat_id)
            category.delete()

        messages.success(request, "Category Deleted Success")

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 
        
    def get(self, request):
        allcat = Category.objects.all()
        context = {
            'cat' : allcat
        }
        return render(request, 'delete_cat.html', context)


@login_required
@permission_required("tasks.delete_category", login_url="no_permission")
def delete_cat(request):
    allcat = Category.objects.all()

    if request.method == 'POST':
        select_cat = request.POST.getlist('category')
        
        for cat_id in select_cat:
            category = get_object_or_404(Category, id=cat_id)
            category.delete()

        if request.user.groups.filter(name="Admin").exists():
            return redirect('dashboard')  
        elif request.user.groups.filter(name="Manager").exists():
            return redirect('admin_event') 
        else:
            return redirect('delete_cat') 
    
    context = {
        'cat' : allcat
    }

    return render(request, 'delete_cat.html', context)

class EventDetails(DetailView):
    model = Event
    template_name = "dashboard.html"
    context_object_name = 'event_details'
    pk_url_kwarg = id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        participants = event.participants.all()

        context['participants'] = participants
        
        return context
    

def event_details(request, id):
    event = Event.objects.prefetch_related('participants').get(id=id) # ev.id
    participants = event.participants.all() # par.id

    context = {
        "event_details" : event,
        'participants' : participants
    }
    return render(request, 'dashboard.html', context)

@method_decorator(user_passes_test(is_manager_or_admin, login_url="no_permission"), name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        type = self.request.GET.get('type', 'all')
        today = timezone.now().date()

        event_count = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id', filter=Q(status = 'UPCOMING')),
        completed = Count('id', filter=Q(status = 'COMPLETED')),
        today_event = Count('id', filter=Q(date = today)),
        past_event = Count('id', filter=Q(date__lt = today))
        )

        total_participate = User.objects.filter(rsvp_event__isnull=False).count()
        participants = User.objects.annotate(event_count = Count('rsvp_event'))
        
        if type == 'today':
            events = Event.objects.filter(date = today)
        elif type == 'upcoming':
            events = Event.objects.filter(date__gte = today)
        elif type == 'completed':
            events = Event.objects.filter(status = "COMPLETED")
        elif type == 'past':
            events = Event.objects.filter(date__lt = today)
        elif type == 'all':
            events = Event.objects.all()
        else:
            events = Event.objects.all()

        context = {
        'event_count' : event_count,
        'total_participate' : total_participate,
        'participants' : participants,
        'events' : events,
        }

        return context



@user_passes_test(is_manager_or_admin, login_url="no_permission")
def dashboard(request):
    type = request.GET.get('type', 'all')
    today = timezone.now().date()

    event_count = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id', filter=Q(status = 'UPCOMING')),
        completed = Count('id', filter=Q(status = 'COMPLETED')),
        today_event = Count('id', filter=Q(date = today)),
        past_event = Count('id', filter=Q(date__lt = today))
    )
    
    total_participate = User.objects.filter(rsvp_event__isnull=False).count()

    participants = User.objects.annotate(event_count = Count('rsvp_event'))
    
    if type == 'today':
        events = Event.objects.filter(date = today)
    elif type == 'upcoming':
        events = Event.objects.filter(date__gte = today)
    elif type == 'completed':
        events = Event.objects.filter(status = "COMPLETED")
    elif type == 'past':
        events = Event.objects.filter(date__lt = today)
    elif type == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.all()

    context = {
        'event_count' : event_count,
        'total_participate' : total_participate,
        'participants' : participants,
        'events' : events,
    }

    return render(request, 'dashboard.html', context)

class EventDetailsView(TemplateView):
    template_name = "event_details_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, id=self.kwargs['id'])
        context["event"] = event
        return context
    

def event_details_view(request, id):
    event = Event.objects.get(id=id)
    return render(request, "event_details_view.html", {'event': event})


class RSVP_EVENT(View):
    def post(self, request, event_id, *args, **kwargs):

        event = get_object_or_404(Event, id=event_id)

        if request.user in event.participants.all():
            messages.warning(request, "You have already in this event.")
        else:
            event.participants.add(request.user)
            messages.success(request, "Congratulations, You have Successfully Enrolled this Event.")

        return redirect(request.META.get('HTTP_REFERER', 'home'))


def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        messages.warning(request, "You have already in this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "Congratulations, You have Successfully Enrolled this Event.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

    