from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from tasks.models import Event, Category
from tasks.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.contrib import messages

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager_or_admin(user):
    return user.is_authenticated and (is_manager(user) or is_admin(user))

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


def show_cat(request):    
   cat = Category.objects.all()   
   context = {
       'cat' : cat
   }
   return render(request, 'delete_cat.html', context)

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
            return redirect('admin-dashboard') 
        else:
            return redirect('delete_cat') 
    
    context = {
        'cat' : allcat
    }

    return render(request, 'delete_cat.html', context)


def event_details(request, id):
    event = Event.objects.prefetch_related('participants').get(id=id) # ev.id
    participants = event.participants.all() # par.id

    context = {
        "event_details" : event,
        'participants' : participants
    }
    return render(request, 'dashboard.html', context)

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


def event_details_view(request, id):
    event = Event.objects.get(id=id)
    return render(request, "event_details_view.html", {'event': event})

def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        messages.warning(request, "You have already in this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "Congratulations, You have Successfully Enrolled this Event.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

    