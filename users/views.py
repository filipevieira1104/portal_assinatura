from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth import get_user_model
from documents.models import TermoResponsabilidade, Equipamento
from django.contrib import messages
from .forms import UserRegisterForm, ColaboradorAdminForm
from django import forms
import uuid

User = get_user_model()

# Create your views here.

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_form.html'
    fields = ['first_name', 'last_name', 'email', 'telefone', 'endereco', 'numero',
              'complemento', 'bairro', 'cidade', 'estado', 'cep']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'users/colaborador_list.html'
    context_object_name = 'users'
    ordering = ['first_name', 'last_name']

class UserDetailView(StaffRequiredMixin, DetailView):
    model = User
    template_name = 'users/colaborador_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['termos'] = TermoResponsabilidade.objects.filter(colaborador=user)
        return context

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.instance.is_active = False
        messages.success(self.request, 'Sua conta foi criada! Aguarde aprovação do administrador.')
        return super().form_valid(form)

class ColaboradorCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = ColaboradorAdminForm
    template_name = 'users/colaborador_form.html'
    success_url = reverse_lazy('users:colaborador_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastrar Novo Colaborador'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Obter o nome completo para a mensagem
        full_name = f"{form.instance.first_name} {form.instance.last_name}".strip()
        
        # Se foi gerada uma senha aleatória, exibir
        if hasattr(form.instance, 'random_password'):
            messages.success(
                self.request, 
                f'Colaborador {full_name} cadastrado com sucesso! '
                f'Username: {form.instance.username} | '
                f'Senha: {form.instance.random_password}'
            )
        else:
            messages.success(
                self.request, 
                f'Colaborador {full_name} cadastrado com sucesso!'
            )
            
        return response

class ColaboradorUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    template_name = 'users/colaborador_form.html'
    fields = ['username', 'first_name', 'last_name', 'email',
              'telefone', 'cargo', 'departamento', 'endereco',
              'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
    success_url = reverse_lazy('users:colaborador_list')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['termos'] = TermoResponsabilidade.objects.filter(colaborador=user)
        context['equipamentos'] = Equipamento.objects.filter(termos__colaborador=user).distinct()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_update.html'
    fields = ['first_name', 'last_name', 'email', 'telefone']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


