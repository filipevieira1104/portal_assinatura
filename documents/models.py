from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from tinymce.models import HTMLField
from django import forms
from tinymce.widgets import TinyMCE

class Equipamento(models.Model):
    TIPO_CHOICES = [
        ('NOTEBOOK', 'Notebook'),
        ('DESKTOP', 'Desktop'),
        ('MONITOR', 'Monitor'),
        ('CELULAR', 'Celular'),
        ('TABLET', 'Tablet'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('EM_USO', 'Em Uso'),
        ('MANUTENCAO', 'Em Manutenção'),
        ('INATIVO', 'Inativo'),
    ]
    
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField('Marca', max_length=100)
    modelo = models.CharField('Modelo', max_length=100)
    numero_serie = models.CharField('Número de Série', max_length=100, unique=True)
    descricao = models.TextField('Descrição')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_aquisicao = models.DateField('Data de Aquisição')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    observacoes = models.TextField('Observações', blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipamentos'
    )
    
    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        
    def __str__(self):
        return f"{self.tipo} - {self.marca} {self.modelo} ({self.numero_serie})"

class DocumentoModelo(models.Model):
    titulo = models.CharField('Título', max_length=200)
    conteudo = HTMLField('Conteúdo')
    versao = models.CharField('Versão', max_length=10)
    arquivo_word = models.FileField('Arquivo Word', upload_to='documentos/modelos/', blank=True, null=True, 
                                   help_text="Upload de um arquivo Word (.docx) como modelo")
    ativo = models.BooleanField('Ativo', default=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_modificacao = models.DateTimeField('Última Modificação', auto_now=True)
    
    class Meta:
        verbose_name = 'Modelo de Documento'
        verbose_name_plural = 'Modelos de Documentos'
        
    def __str__(self):
        return f"{self.titulo} - v{self.versao}"

class TermoResponsabilidade(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ENVIADO = 'ENVIADO', 'Enviado'
        ASSINADO = 'ASSINADO', 'Assinado'
        RECUSADO = 'RECUSADO', 'Recusado'
        CANCELADO = 'CANCELADO', 'Cancelado'
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    colaborador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='termos_responsabilidade'
    )
    modelo = models.ForeignKey(
        DocumentoModelo,
        on_delete=models.PROTECT,
        related_name='termos'
    )
    equipamentos = models.ManyToManyField(
        Equipamento,
        related_name='termos',
        through='ItemTermo'
    )
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_envio = models.DateTimeField('Data de Envio', null=True, blank=True)
    data_assinatura = models.DateTimeField('Data da Assinatura', null=True, blank=True)
    ip_assinatura = models.GenericIPAddressField('IP da Assinatura', null=True, blank=True)
    hash_assinatura = models.CharField('Hash da Assinatura', max_length=64, blank=True)
    arquivo_pdf = models.FileField(
        'Arquivo PDF',
        upload_to='documentos/termos/',
        null=True,
        blank=True
    )
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Termo de Responsabilidade'
        verbose_name_plural = 'Termos de Responsabilidade'
        
    def __str__(self):
        return f"Termo {self.uuid} - {self.colaborador.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.ENVIADO and not self.data_envio:
            self.data_envio = timezone.now()
        super().save(*args, **kwargs)
    
    def pode_assinar(self, user):
        """Verifica se o usuário pode assinar este termo"""
        if user.is_staff:
            return True
        # Se não for staff, só pode assinar se for o colaborador associado ao termo
        return user == self.colaborador

class ItemTermo(models.Model):
    termo = models.ForeignKey(TermoResponsabilidade, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    data_entrega = models.DateField('Data de Entrega')
    estado_entrega = models.TextField('Estado na Entrega')
    data_devolucao = models.DateField('Data de Devolução', null=True, blank=True)
    estado_devolucao = models.TextField('Estado na Devolução', blank=True)
    
    class Meta:
        verbose_name = 'Item do Termo'
        verbose_name_plural = 'Itens do Termo'
        
    def __str__(self):
        return f"{self.equipamento} - {self.termo.colaborador.get_full_name()}"

class DocumentoModeloForm(forms.ModelForm):
    class Meta:
        model = DocumentoModelo
        fields = ['titulo', 'conteudo', 'versao', 'ativo']
        widgets = {
            'conteudo': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
