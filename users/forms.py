from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import uuid

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'cpf', 'rg',
            'telefone', 'data_nascimento', 'cargo', 'departamento', 'endereco',
            'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar alguns campos opcionais para facilitar o registro inicial
        self.fields['cargo'].required = False
        self.fields['departamento'].required = False
        self.fields['data_nascimento'].required = False
        self.fields['complemento'].required = False
        
        # Adicionar widgets e classes para melhorar a aparência do formulário
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar placeholders úteis
        self.fields['cpf'].widget.attrs.update({'placeholder': '000.000.000-00'})
        self.fields['cep'].widget.attrs.update({'placeholder': '00000-000'})
        self.fields['telefone'].widget.attrs.update({'placeholder': '(00) 00000-0000'})

class ColaboradorAdminForm(forms.ModelForm):
    """Formulário para administradores criarem novos colaboradores"""
    
    password1 = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput,
        required=False,
        help_text="Deixe em branco para gerar uma senha aleatória."
    )
    password2 = forms.CharField(
        label='Confirmação de senha', 
        widget=forms.PasswordInput,
        required=False,
        help_text="Digite a mesma senha novamente para verificação."
    )
    
    # Campo para exibir a senha gerada (não é salvo no modelo)
    generated_password = forms.CharField(
        label='Senha gerada',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        help_text="Esta senha foi gerada automaticamente. Anote-a para informar ao usuário."
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'telefone', 'cargo', 'departamento', 
            'endereco', 'numero', 'complemento', 'bairro', 
            'cidade', 'estado', 'cep', 'is_staff'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes para melhorar a aparência
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        # Tornar username opcional (será gerado automaticamente se vazio)
        self.fields['username'].required = False
        self.fields['username'].help_text = "Opcional. Será gerado automaticamente se deixado em branco."
        
        # Adicionar placeholders
        self.fields['telefone'].widget.attrs.update({'placeholder': '(00) 00000-0000'})
        self.fields['cep'].widget.attrs.update({'placeholder': '00000-000'})
        
        # Esconder o campo de senha gerada até que seja necessário
        self.fields['generated_password'].widget.attrs.update({'style': 'display: none;'})
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Se ambos estiverem vazios, gerar senha aleatória
        if not password1 and not password2:
            # Gerar senha aleatória
            random_password = uuid.uuid4().hex[:8]
            # Armazenar no campo virtual para exibição
            self.instance.random_password = random_password
            return ''
            
        # Verificar se as senhas coincidem
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não conferem.')
            
        return password2
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Gerar username baseado no nome se estiver vazio
        if not self.cleaned_data.get('username'):
            first_name = self.cleaned_data.get('first_name', '').lower()
            last_name = self.cleaned_data.get('last_name', '').lower()
            
            # Criar username baseado no nome ou aleatório
            if first_name and last_name:
                username = f"{first_name}.{last_name}"
                # Verificar duplicidade
                count = 1
                temp_username = username
                while User.objects.filter(username=temp_username).exists():
                    temp_username = f"{username}{count}"
                    count += 1
                username = temp_username
            else:
                # Gerar username aleatório
                username = f"user_{uuid.uuid4().hex[:8]}"
                
            user.username = username
            
        # Definir senha
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        elif hasattr(self.instance, 'random_password'):
            # Usar a senha aleatória gerada
            user.set_password(self.instance.random_password)
            
        if commit:
            user.save()
            
        return user
