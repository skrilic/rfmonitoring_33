__author__ = 'slaven'

from django import forms
from django.forms import ModelForm
from .models import Transmitter
from .models import FieldMeasurement


class TransmitterForm(ModelForm):
    class Meta:
        model = Transmitter
        fields = [
            'name',
            'licence_type',
            'callsign',
            'signature',
            'description',
            'enabled',
            'licence_state',
            'frequency',
            'erp',
            'transmitter_power',
            'antenna_height',
            'tower',
            'organization'
        ]


class FieldMeasurementForm(forms.ModelForm):
    class Meta:
        model = FieldMeasurement
        fields = (
            'title',
            'date',
            'operator',
            'equipment',
            'antenna',
            'description',
            'type',
            'scope',
            'report',
            'location',
            'status',
            # 'author'
        )
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'editable medium-editor-textarea',
                'placeholder': 'What and Why. Results and facts. Conclusion and remarks if any ...'
            }),
            'date': forms.SelectDateWidget()
        }
