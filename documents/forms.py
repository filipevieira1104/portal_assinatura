from django import forms
from .models import DocumentoModelo
from tinymce.widgets import TinyMCE

class ModeloDocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoModelo
        fields = ['titulo', 'conteudo', 'versao', 'arquivo_word', 'ativo']
        widgets = {
            'conteudo': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remova classes CSS conflitantes se estiver usando crispy forms
        if 'conteudo' in self.fields:
            self.fields['conteudo'].widget.attrs.pop('class', None)
        
        # Tornar o campo conteúdo não obrigatório se arquivo_word for enviado
        self.fields['conteudo'].required = False
        self.fields['arquivo_word'].help_text = "Se preferir, faça upload de um arquivo Word (.docx) em vez de usar o editor de texto."