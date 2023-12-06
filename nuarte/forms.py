from django import forms
from .models import Instrumento, Historico, Perfil

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disponivel'].widget.attrs['class'] = 'form-check-input'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class HistoricoForm(forms.ModelForm):
    class Meta:
        model = Historico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
