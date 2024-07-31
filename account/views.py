from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import EmailForm, UpdateForm, RegisterForm, OTPForm, EmployeeForm, JobseekerForm, ChangePasswordForm, ForgotEmailForm, ForgotPasswordForm
from django.views.generic import FormView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import User, EmailOTP, Relationship, Employee ,Jobseeker,Forgotpassword
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .utils import send_otp_via_email, send_password_via_email


def index(request):
    return render(request,'account/index.html')

def send_otp(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_otp, created = EmailOTP.objects.get_or_create(email=email)
            email_otp.generate_otp()
            send_otp_via_email(email_otp.email, email_otp.otp)
            return redirect('account:verify_otp')
    else:
        form = EmailForm()
    return render(request, 'account/send_otp.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            try:
                email_otp = EmailOTP.objects.get(email=email, otp=otp)
                email_otp.is_verified = True
                email_otp.save()
                return redirect('account:register')
            except EmailOTP.DoesNotExist:
                messages.error(request, 'Invalid email or OTP.')
    else:
        form = OTPForm()
    return render(request, 'account/verify_otp.html', {'form': form})

        

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('account:employeeinfo')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_email_verified = True
        user.save()
        login(self.request, user)
        return redirect('account:employeeinfo')
        

class EmployeeinfoView(LoginRequiredMixin,View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account:logina')
        employee_form = EmployeeForm()
        jobseeker_form = JobseekerForm()
        return render(request, 'account/employeeinfo.html', {
            'employee_form': employee_form,
            'jobseeker_form': jobseeker_form
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('account:logina')
        if 'employee_submit' in request.POST:
            employee_form = EmployeeForm(request.POST)
            jobseeker_form = JobseekerForm()
            if employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = request.user
                employee.save()
                return redirect('account:relationship')
        elif 'jobseeker_submit' in request.POST:
            jobseeker_form = JobseekerForm(request.POST)
            employee_form = EmployeeForm()
            if jobseeker_form.is_valid():
                jobseeker = jobseeker_form.save(commit=False)
                jobseeker.user = request.user
                jobseeker.save()
                return redirect('account:relationship')
        return render(request, 'employeeinfo.html', {
            'employee_form': employee_form,
            'jobseeker_form': jobseeker_form
        })
    

class RelationshipView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return render(request, 'account/relationship.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if 'short_submit' in request.POST:
            short_relationship = Relationship(
                user=request.user,
                relation='short',
            )
            short_relationship.save()
            return redirect('Dating:selectgender') 
        elif 'long_submit' in request.POST:
            pass
        return render(request, 'relationship.html')


class ProfileListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        
        for user in users:
            user.images = user.images
            user.employee_details = Employee.objects.filter(user=self.request.user)
            user.jobseeker_details = Jobseeker.objects.filter(user=self.request.user)
        
        return context
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'account/register.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        # Ensure the object being updated is the currently logged-in user
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        if user == request.user:
            user.delete()
            return redirect('account:index')
        else:
            return redirect('account:profile')
        
        
class LogoutView(TemplateView):
   def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect(reverse_lazy('Dating:login'))
   

class PaymentOptionsView(TemplateView):
    template_name = 'account/packages.html'


def forgotpassword(request):
    if request.method == 'POST':
        form = ForgotEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_password, created = Forgotpassword.objects.get_or_create(email=email)
            email_password.generate_password()
            send_password_via_email(email_password.email, email_password.new_password)
            return redirect('account:verify_password')
    else:
        form = ForgotEmailForm()
    return render(request, 'account/forgot_password.html', {'form': form})


def verify_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                Forgotpassword.objects.filter(email=email).update(is_verified=True)
                return redirect('Dating:login')
            
            except User.DoesNotExist:
                return redirect('account:forgot_password')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'account/new_password.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                return redirect('Dating:login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
            return redirect('account:change_password')
    else:
        form = ChangePasswordForm()
    return render(request, 'account/change_password.html', {'form': form})
    
        