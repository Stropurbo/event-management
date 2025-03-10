from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from tasks.models import Event, Category, Participant
from tasks.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from django.db.models import Q, Count, Max, Min, Avg
from django.utils import timezone

def home(request):
    search_q = request.GET.get('search', '')
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

def create_event(request):
    event_form = EventModelForm()
    
    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
        
            return redirect('dashboard')
        
    context = {
        "create_event" : event_form
    }
    return render(request, 'create_event.html', context)

def show_cat(request):    
   cat = Category.objects.all()   
   context = {
       'cat' : cat
   }
   return render(request, 'delete_cat.html', context)

def create_category(request):
    cat_form = CategoryModelForm()

    if request.method == 'POST':
        cat_form = CategoryModelForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            return redirect('dashboard')
        
    context = {
        'cat_form' : cat_form
    }

    return render(request, 'cat_form.html', context)

def create_participate(request):
    partici_form = ParticipantModelForm()

    if request.method == 'POST':
        partici_form = ParticipantModelForm(request.POST)
        if partici_form.is_valid():
            partici_form.save()
            return redirect('partici_form')
        
    context = {
        'partici_form' : partici_form
    }
    return render(request, 'partici_form.html', context)

def delete_participant(request, id):
    if request.method == "POST":
        par = get_object_or_404(Participant, id = id)
        par.delete()
        return redirect('dashboard')
    return redirect('dashboard')

def update_event(request, id):
    event = Event.objects.get(id = id)
    if request.method == 'POST':
        form = EventModelForm(request.POST, instance = event)
        if form.is_valid():
            form.save()
        return redirect('dashboard')
    else:
        form = EventModelForm(instance = event)
    
    context = {
        'update_event' : form
    }

    return render(request, 'update_event.html', context)

def delete_event(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id = id)
        event.delete()
        return redirect('dashboard')
    return redirect('dashboard')

def delete_cat(request):
    allcat = Category.objects.all()

    if request.method == 'POST':
        select_cat = request.POST.getlist('category')
        
        for cat_id in select_cat:
            category = get_object_or_404(Category, id=cat_id)
            category.delete()
        return redirect('delete_cat') 
    
    context = {
        'cat' : allcat
    }

    return render(request, 'delete_cat.html', context)


def event_details(request, id):
    event = Event.objects.prefetch_related('participants').get(id=id)
    participants = event.participants.all()
    context = {
        "event_details" : event,
        'participants' : participants
    }
    return render(request, 'dashboard.html', context)

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
    
    total_participate = Participant.objects.count()
    participants = Participant.objects.annotate(
        event_count = Count('event')
    ).prefetch_related('event')

    if type == 'today':
        events = Event.objects.filter(date = today)
    elif type == 'upcoming':
        events = Event.objects.filter(date__gte = today)
    elif type == 'completed':
        events = Event.objects.filter(date__lt = today)
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