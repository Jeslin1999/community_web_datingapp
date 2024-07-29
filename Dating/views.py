from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import GenderselectForm,MessageForm, MediaForm
from account.forms import LoginForm
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, TemplateView, View, UpdateView
from .models import Genderselect, Friendconnection, Message, Media
from account.models import User,Employee, Jobseeker
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class GenderselectView(LoginRequiredMixin, FormView):
    template_name = 'Dating/selectgender.html'
    form_class = GenderselectForm
    success_url = reverse_lazy('Dating:gridview')
    def form_valid(self, form):
        genderselect, created = Genderselect.objects.update_or_create(
            user=self.request.user,
            defaults={'genderselect': form.cleaned_data['genderselect']}
        )
        return super().form_valid(form)
    

class LoginView(FormView):
    template_name = 'account/Login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
                login(self.request, user)
                gender_selection = Genderselect.objects.filter(user=self.request.user.id)
                if gender_selection.exists():
                    return redirect('Dating:gridview')
                else:
                    return redirect('Dating:selectgender') 
        else:
            return self.form_invalid(form) 


class Gridview(LoginRequiredMixin,ListView):
    model = User, Genderselect, Friendconnection
    template_name = 'Dating/gridview.html'
    context_object_name = 'users'

    def get_queryset(self):
        gender_selection = Genderselect.objects.filter(user=self.request.user.id).first()
        excluded_users = Friendconnection.objects.filter(send_by=self.request.user, not_interest=True).values_list('send_to_id', flat=True)
        if gender_selection:
                if gender_selection.genderselect == 'B':
                    return User.objects.exclude(Q(id=self.request.user.id) | Q(id__in=excluded_users) | Q(is_staff=True))

                elif gender_selection.genderselect == 'M':
                    return User.objects.filter(gender='Male').exclude(Q(id=self.request.user.id) | Q(id__in=excluded_users) | Q(is_staff=True))

                elif gender_selection.genderselect == 'F':
                    return User.objects.filter(gender='Female').exclude(Q(id=self.request.user.id) | Q(id__in=excluded_users) | Q(is_staff=True))
                
                queryset = queryset.prefetch_related('employee', 'jobseeker')
            
                return queryset
        
        return User.objects.none()
    

class LocationGridview(LoginRequiredMixin, ListView):
    model = User, Genderselect
    template_name = 'Dating/location.html'
    context_object_name = 'users'

    def get_queryset(self):
        gender_selection = Genderselect.objects.filter(user=self.request.user.id).first()
        excluded_users = Friendconnection.objects.filter(send_by=self.request.user, not_interest=True).values_list('send_to_id', flat=True)
        queryset = User.objects.exclude(Q(id=self.request.user.id) | Q(id__in=excluded_users) | Q(is_staff=True))
        
        if gender_selection:
            if gender_selection.genderselect == 'B':
                location = self.request.GET.get('location')
                if location:
                    queryset = queryset.filter(location=location)
                
            elif gender_selection.genderselect == 'M':
                location = self.request.GET.get('location')
                queryset = queryset.filter(gender='Male')
                if location:
                    queryset = queryset.filter(location=location)

            elif gender_selection.genderselect == 'F':
                location = self.request.GET.get('location')
                queryset = queryset.filter(gender='Female')
                if location:
                    queryset = queryset.filter(location=location)
     
        return queryset


class EducationGridview(LoginRequiredMixin, ListView):
    model = User, Genderselect
    template_name = 'Dating/education.html'
    context_object_name = 'users'

    def get_queryset(self):
        gender_selection = Genderselect.objects.filter(user=self.request.user.id).first()
        excluded_users = Friendconnection.objects.filter(send_by=self.request.user, not_interest=True).values_list('send_to_id', flat=True)
        queryset = User.objects.exclude(Q(id=self.request.user.id) | Q(id__in=excluded_users) | Q(is_staff=True))
        
        if gender_selection:
            if gender_selection.genderselect == 'B':
                qualification = self.request.GET.get('qualification')
                if qualification:
                    queryset = queryset.filter(qualification=qualification)
                
            elif gender_selection.genderselect == 'M':
                qualification = self.request.GET.get('qualification')
                queryset = queryset.filter(gender='Male')
                if qualification:
                    queryset = queryset.filter(qualification=qualification)

            elif gender_selection.genderselect == 'F':
                qualification = self.request.GET.get('qualification')
                queryset = queryset.filter(gender='Female')
                if qualification:
                    queryset = queryset.filter(qualification=qualification)
     
        return queryset
               

class UserDetailView(DetailView):
    model = User
    template_name = 'Dating/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        
        user.employee_details = Employee.objects.filter(user=user).first()
        user.jobseeker_details = Jobseeker.objects.filter(user=user).first()
        user.media_details = Media.objects.filter(user=user).all()
        
        return context
    

class GalleryView(LoginRequiredMixin, View):
    template_name = 'Dating/gallery.html'

    def get(self, request, *args, **kwargs):
        form = MediaForm()
        media = Media.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, self.template_name, {'form': form, 'media': media})

    def post(self, request, *args, **kwargs):
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_instance = form.save(commit=False)
            media_instance.user = request.user
            media_instance.save()
            return redirect(reverse_lazy('Dating:gallery'))
        media = Media.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, self.template_name, {'form': form, 'media': media})


class MediaDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        media = get_object_or_404(Media, pk=pk, user=request.user)
        if media:
            media.delete()
        return redirect(reverse_lazy('Dating:gallery'))
    

class SendrequestView(LoginRequiredMixin, View):
    success_url = reverse_lazy('Dating:user_detail')

    def post(self, request, *args, **kwargs):
        send_to_user = get_object_or_404(User, id=self.kwargs['user_id'])
        friend_request, created = Friendconnection.objects.get_or_create(send_by=self.request.user, send_to=send_to_user)
        
        if created:
            return redirect('Dating:user_detail', pk=self.kwargs['user_id'])
        else:
            return redirect('Dating:user_detail', pk=self.kwargs['user_id'])
        

class SendhtmlView(View):
    def get(self, request):
        user = request.user
        friends = Friendconnection.objects.filter(send_by=user, status=False) | Friendconnection.objects.filter(send_to=user, status=False)
        friends_list = []
        for friend in friends:
            if friend.send_by == user:
                friends_list.append(friend.send_to)
            else:
                friends_list.append(friend.send_by)
        context = {'friends': friends_list}
        return render(request, 'Dating/friends_list.html', context)

class RemovelistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        send_to_user = get_object_or_404(User, id=self.kwargs['user_id'])
        friend_connection = get_object_or_404(
            Friendconnection,
            Q(send_by=self.request.user, send_to=send_to_user, status=False) | 
            Q(send_by=self.request.user, send_to=send_to_user, short_list=True) |
            Q(send_by=self.request.user, send_to=send_to_user, status=True)
        )
        friend_connection.delete()
        return redirect(reverse_lazy('Dating:gridview'))
    

class Accepthtmlview(LoginRequiredMixin, TemplateView):
    template_name = 'Dating/request_re.html'

    def get(self, request):
        user = request.user
        pending_requests = Friendconnection.objects.filter(send_to=user, status=False)
        request_senders = [request.send_by for request in pending_requests]

        context = {
            'pending_requests': pending_requests,
            'request_senders': request_senders,
            'count': pending_requests.count()
        }
        return render(request, 'Dating/request_re.html', context)
    

class AcceptRequestView(LoginRequiredMixin, UpdateView):
    model = Friendconnection
    fields = ['status']

    def get_object(self, queryset=None):
        friend_request = get_object_or_404(Friendconnection, id=self.kwargs['request_id'], send_to=self.request.user)
        return friend_request

    def form_valid(self, form):
        form.instance.status = True
        form.instance.save()
        return redirect('Dating:user_detail', pk=self.request.user.id)

    def form_invalid(self, form):
        return redirect('Dating:accept_requests', pk=self.request.user.id)
    

class RejectRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        friend_request = get_object_or_404(Friendconnection, id=request_id, send_to=request.user)
        if friend_request:
            friend_request.delete()
        return redirect('Dating:accept_requests')
    

class FriendsListView(View):
    def get(self, request):
        user = request.user
        friends = Friendconnection.objects.filter(send_by=user, status=True) | Friendconnection.objects.filter(send_to=user, status=True)
        friends_list = []
        for friend in friends:
            if friend.send_by == user:
                friends_list.append(friend.send_to)
            else:
                friends_list.append(friend.send_by)
        context = {'friends': friends_list}
        return render(request, 'Dating/friends_list.html', context)
    

class ShortlistView(LocationGridview, View):
    success_url = reverse_lazy('Dating:user_detail')

    def post(self, request, *args, **kwargs):
        send_to_user = get_object_or_404(User, id=self.kwargs['request_id'])
        friend_request, created = Friendconnection.objects.get_or_create(send_by=self.request.user, send_to=send_to_user)
        
        if created:
            friend_request.short_list = True
            friend_request.save()
            return redirect('Dating:user_detail', pk=self.kwargs['request_id'])
        else:
            friend_request.short_list = True
            friend_request.save()
            return redirect('Dating:user_detail', pk=self.kwargs['request_id'])
        

class ShorthtmlView(View):
    def get(self, request):
        user = request.user
        friends = Friendconnection.objects.filter(send_by=user, short_list=True) | Friendconnection.objects.filter(send_to=user, short_list=True)
        friends_list = []
        for friend in friends:
            if friend.send_by == user:
                friends_list.append(friend.send_to)
            else:
                friends_list.append(friend.send_by)
        context = {'friends': friends_list}
        return render(request, 'Dating/friends_list.html', context)
    
    

class NotinterestedView(LocationGridview, View):
    success_url = reverse_lazy('Dating:user_detail')

    def post(self, request, *args, **kwargs):
        send_to_user = get_object_or_404(User, id=self.kwargs['request_id'])
        friend_request, created = Friendconnection.objects.get_or_create(send_by=self.request.user, send_to=send_to_user)
        
        if created:
            friend_request.not_interest = True
            friend_request.save()
            return redirect('Dating:gridview')
        else:
            friend_request.not_interest = True
            friend_request.save()
            return redirect('Dating:gridview')
    
    

class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'Dating/chat_room.html'
    success_url = 'Dating:messages'

    def get(self, request, id):
        receiver = get_object_or_404(User, id=id)
        

        messages_between = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('-timestamp')

        form = MessageForm()
        context = {
            'form': form,
            'receiver': receiver,
            'messages': messages_between,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        receiver = get_object_or_404(User, id=id)
        
        messages_between = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('-timestamp')

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('Dating:send_message', id=id) 

        context = {
            'form': form,
            'receiver': receiver,
            'messages': messages_between,
        }
        return render(request, self.template_name, context)