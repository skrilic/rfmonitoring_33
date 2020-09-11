from django import forms
from django.forms.widgets import TextInput
from .models import RFmonSiteLog, AssetLog


class RFmonSiteLogForm(forms.ModelForm):
    class Meta:
        model = RFmonSiteLog
        fields = (
            'rfmonsite',
            'logevent',
            'details',
            'datetime',
            'report'
        )
        widgets = {
            'details': forms.Textarea(attrs={
                'class': 'editable medium-editor-textarea',
                'placeholder': 'Facts, findings and notes ...'
            }),
            'datetime': forms.SelectDateWidget()
        }


class AssetLogForm(forms.ModelForm):
    class Meta:
        model = AssetLog
        fields = (
            'asset',
            'logevent',
            'details',
            'datetime',
            'expiration',
            'document'
        )
        widgets = {
            'details': forms.Textarea(attrs={
                'class': 'editable medium-editor-textarea',
                'placeholder': "Describe what's going on with the item ..."
            }),
            'datetime': forms.SelectDateWidget(),
            'expiration': forms.SelectDateWidget()
        }
