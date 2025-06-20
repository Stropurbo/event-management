from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from users.forms import CustomRegisterForm,EditProfileForm, AssignRoleForm,CreateGroupForm,CustomChangePasswordForm,CustomPasswordResetForm,CustomPasswordConfirm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.db.models import Prefetch, Count, Q
from tasks.views import Event, Category
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView,CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,LoginView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.generic.edit import FormView
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

def is_manager(user):
    return "Manager" in [group.name for group in user.groups.all()]

def is_admin(user):
    return "Admin" in [group.name for group in user.groups.all()]

def is_manager_or_admin(user):
    return user.is_authenticated and (is_manager(user) or is_admin(user))

# create_decorators = [login_required, permission_required("tasks.add_event", login_url="no_permission")]


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

class SignupView(FormView):
    template_name = "registration/register.html"
    form_class = CustomRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        
        messages.success(self.request, "Confirmation mail sent. Please check you e-mail.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, "Invalid form submission. Please check the details.")
        return super().form_invalid(form)


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

class ActivateUser(View):   
    def get(self, request, user_id, token):
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
    
@method_decorator(user_passes_test(is_manager_or_admin, login_url="no_permission"), name="dispatch")
class AdminDashbaord(View):

    def get(self, request, *args, **kwargs):

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


@method_decorator(user_passes_test(is_manager_or_admin, login_url="no_permission"), name="dispatch")
class AssignRole(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = AssignRoleForm()
        context = {
            'form' : form,
            'user' : user
        }
        return render(request, "admin/assign_role.html", context)
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = AssignRoleForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data['role']
            group = Group.objects.filter(name=role).first()

            if group:
                user.groups.clear()
                user.groups.add(group)

            return redirect('admin-dashboard')
        context = {
            'form' : form,
            'user' : user
        }
        return render(request, "admin/assign_role.html", context)


@user_passes_test(is_manager_or_admin, login_url="no_permission")
def assign_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        print(f"User found: {user}")  # Debugging
    except User.DoesNotExist:
        print("User not found!")  # Debugging
        return HttpResponse("User not found!", status=404)

    form = AssignRoleForm() 

    if request.method == "POST":
        form = AssignRoleForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data.get('role')
            group = Group.objects.filter(name=role).first()

            if group:
                user.groups.clear() 
                user.groups.add(group)

            return redirect('admin-dashboard')
    return render(request, "admin/assign_role.html", {'form': form})

@method_decorator(user_passes_test(is_manager_or_admin, login_url="no_permission"), name="dispatch")
class CreateGroup(CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = "admin/create_group.html"   
    success_url = reverse_lazy("create_group")

@user_passes_test(is_manager_or_admin, login_url="no_permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("create_group")
        
    return render(request, 'admin/create_group.html', {'form':form})

@method_decorator(user_passes_test(is_manager_or_admin, login_url="no_permission"), name="dispatch")
class GroupList(ListView):
    model = Group
    template_name = "admin/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

@user_passes_test(is_manager_or_admin, login_url="no_permission")
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, "admin/group_list.html", {'groups': groups})



def no_permission(request):
    return render(request, "no_permission.html")

class AdminEvent(ListView):
    model = Event
    template_name = "admin_event.html"
    context_object_name = "events"

    def get_queryset(self):
        type = self.request.GET.get('type', 'all')
        today = timezone.now().date()
        events = Event.objects.all()

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

        return events
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        today = timezone.now().date()

        context['event_count'] = Event.objects.aggregate(
        total = Count('id'),
        upcoming = Count('id', filter=Q(status = 'UPCOMING')),
        completed = Count('id', filter=Q(status = 'COMPLETED')),
        today_event = Count('id', filter=Q(date = today)),
        past_event = Count('id', filter=Q(date__lt = today))
    )
        return context


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


class UserDash(LoginRequiredMixin, ListView):
    model = Event
    template_name = "user_dash.html"
    context_object_name = "user_join_event"

    def get_queryset(self):
        return Event.objects.filter(participants=self.request.user)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['event_count'] = self.get_queryset().count()
        return context

@login_required
def user_dash(request):
    user = request.user
    user_join_event = Event.objects.filter(participants=user)

    context = {
        'user_join_event' : user_join_event,
        'event_count' : user_join_event.count()
    }

    return render(request, "user_dash.html", context)

class ChangePassword(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy('login')
    form_class = CustomChangePasswordForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy('login')
    html_email_template_name = "registration/reset_email.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, "A Reset E-mail Sent. Please Check Your E-mail")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Password Reset Successfull")
        return super().form_valid(form)

"""

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/profile_update.html"
    context_object_name = 'form'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        # user_profile = UserProfile.objects.get(user=self.request.user)
        # context['form'] = self.form_class(instance=self.object, userprofile=user_profile)
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "accounts/profile_update.html"
    context_object_name = 'form'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')


class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "accounts/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['bio'] = user.bio
        context['location'] = user.location
        context['profession'] = user.profession
        context['profile_image'] = user.profile_image
        context['phone_number'] = user.phone_number


        return context
    