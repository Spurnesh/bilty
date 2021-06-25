import string
import random
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.db.models import Q
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.views.generic import (CreateView, TemplateView, DetailView, ListView,
                                  UpdateView, DeleteView, FormView, View)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BiltyForm, UserForm
from .models import Bilty, User

# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {'form':  AuthenticationForm})

    def post(self, request):

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.filter(Q(username=username) |
                                       Q(phone=username)
                                       )
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("Inactive user.")
            else:
                return render(request, 'login.html', {'form':  AuthenticationForm, 'invalid_creds': form.errors})
        else:
            return render(request, 'login.html', {'form':  AuthenticationForm, 'invalid_creds': form.errors})

class Dashboard(TemplateView):
    template_name = 'base.html'

    def get(self, request):
        current_user = self.request.user
        # if not current_user.is_anonymous and current_user.groups.filter(name="student").exists() and not current_user.is_aadhar_verified:
        #     return redirect("/verify-id-proof/")
        return render(request, 'base.html')


class BiltyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = BiltyForm
    template_name = "addBilty.html"
    success_message = "%(consignor)s was created successfully"
    success_url = "/view-bilty"

    def form_valid(self, form):
        user = self.request.user
        obj = form.save(commit=False)
        obj.user=user
        obj.save()
        return super().form_valid(form)


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "addUser.html"
    success_message = "%(first_name)s was created successfully"
    success_url = "/view-user"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data.get('password'))
        obj.user_password = form.cleaned_data.get('password')
        obj.save()
        return super().form_valid(form)


# class BiltyListView(ListView):
#     model = Bilty
#     paginate_by = 20
#     template_name = 'viewBilty.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(RoleUpdateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['nos'] = NosNameFormSet(
#                 self.request.POST, instance=self.object)
#         else:
#             data['nos'] = NosNameFormSet(instance=self.object)
#         return data

class BiltyListView(ListView):
    template_name = 'viewBilty.html'

    def get(self, request):
        current_user = self.request.user
        if current_user.is_superuser:
            object_list = Bilty.objects.all()
        else:
            object_list = Bilty.objects.filter(user=current_user)
        return render(request, 'viewBilty.html', {'object_list': object_list})

class UserListView(ListView):
    model = User
    paginate_by = 20
    template_name = 'viewUser.html'



