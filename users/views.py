from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from users.forms import CustomRegisterForm, AssignRoleForm,CreateGroupForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.db.models import Prefetch, Count, Q
from tasks.views import Event, Category
from django.utils import timezone

def is_manager(user):
    return "Manager" in [group.name for group in user.groups.all()]

def is_admin(user):
    return "Admin" in [group.name for group in user.groups.all()]

def is_manager_or_admin(user):
    return user.is_authenticated and (is_manager(user) or is_admin(user))

def Signup(request):
    form = CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()

            messages.success(request, "Confirmation mail sent. Please check you e-mail.")
            return redirect('login') 
        
        else:
            print("Form is no valid")

    return render(request, "register.html", {'form': form})

# def login_view(request):
#     form = AuthenticationForm()

#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     return render(request, "login.html", {'form':form})

def login_view(request): 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save() 
            return redirect('login')
        else:
            return HttpResponse("Invalid ID")
        
    except User.DoesNotExist:
        return HttpResponse("User Doesn't Found.")

@login_required
def logout_view(request):
        logout(request)
        return redirect('login')

@user_passes_test(is_manager_or_admin, login_url="no_permission")
def admin_dashboard(request):

    users = User.objects.prefetch_related(
        Prefetch('groups',  queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group"

    return render(request, "admin/dashboard.html", {'users': users})


@user_passes_test(is_manager_or_admin, login_url="no_permission")
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm() # for get request

    if request.method == "POST":
        form = AssignRoleForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data.get('role')
            group = Group.objects.filter(name=role).first()

            if group:
                user.groups.clear() # remove old data
                user.groups.add(group)

            return redirect('admin-dashboard')
    return render(request, "admin/assign_role.html", {'form': form})

@user_passes_test(is_manager_or_admin, login_url="no_permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("create_group")
        
    return render(request, 'admin/create_group.html', {'form':form})

@user_passes_test(is_manager_or_admin, login_url="no_permission")
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, "admin/group_list.html", {'groups': groups})

def no_permission(request):
    return render(request, "no_permission.html")

def admin_event(request):

    type = request.GET.get('type', 'all')
    today = timezone.now().date()
    events = Event.objects.all()

    event_count = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id', filter=Q(status = 'UPCOMING')),
        completed = Count('id', filter=Q(status = 'COMPLETED')),
        today_event = Count('id', filter=Q(date = today)),
        past_event = Count('id', filter=Q(date__lt = today))
    )

    if type == 'today':
        events = Event.objects.filter(date = today)
    elif type == 'upcoming':
        events = Event.objects.filter(date__gte = today)
    elif type == 'completed':
        events = Event.objects.filter(status = 'COMPLETED')
    elif type == 'past':
        events = Event.objects.filter(date__lt = today)
    elif type == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.all()

    context = {
        'event_count' : event_count,
        'events' : events,
    }

    return render(request, "admin_event.html", context)

@login_required
def user_dash(request):
    
    user = request.user

    user_join_event = Event.objects.filter(participants=user)

    context = {
        'user_join_event' : user_join_event,
        'event_count' : user_join_event.count()
    }

    return render(request, "user_dash.html", context)

