from django import forms

from mailings.models import Client, Message, Mailing


class StyleFormMixin:
    """Миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Client"""

    class Meta:
        model = Client
        exclude = ('user',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Message"""

    class Meta:
        model = Message
        exclude = ('user',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Mailing"""

    class Meta:
        model = Mailing
        exclude = ('status', 'user')
        widgets = {
            'time':  forms.TimeInput(
                attrs={'type': 'time', }
            ),
            'date': forms.DateInput(
                attrs={'type': 'date', }
            )
        }