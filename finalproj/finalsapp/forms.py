from django import forms
from django.forms import ModelForm
from .models import DateTime, Record

class DateTimeForm(ModelForm):
    nangka_rainfall = forms.DecimalField(required=True, label='Nangka Rainfall')
    boso_rainfall = forms.DecimalField(required=True, label='Boso-Boso Rainfall')
    aries_rainfall = forms.DecimalField(required=True, label='Mt. Aries Rainfall')
    campana_rainfall = forms.DecimalField(required=True, label='Mt. Campana Rainfall')
    oro_rainfall = forms.DecimalField(required=True, label='Mt. Oro Rainfall')
    sto_nino_water_level = forms.DecimalField(required=True, label='Sto. Nino Water Level')

    class Meta:
        model = DateTime
        fields = ['datetime']
        widgets = {
            'datetime': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    # This removes milliseconds from the datetime
                    'step': '1'
                }
            )
        }

    def save(self, commit=True):
        datetime_instance = super().save(commit=False)
        
        if commit:
            datetime_instance.save()
        
        records_to_create = []
        
        stations_rainfall = [
            ('nangka_rainfall', Record.NANGKA, Record.RAINFALL),
            ('boso_rainfall', Record.BOSO, Record.RAINFALL),
            ('aries_rainfall', Record.ARIES, Record.RAINFALL),
            ('campana_rainfall', Record.CAMPANA, Record.RAINFALL),
            ('oro_rainfall', Record.ORO, Record.RAINFALL)
        ]
        
        stations_water_level = [
            ('sto_nino_water_level', Record.STO_NINO, Record.WATERLEVEL)
        ]
        
        for field_name, station_name, station_type in stations_rainfall:
            value = self.cleaned_data.get(field_name)
            if value is not None:
                record = Record(
                    source_station_type=station_type,
                    source_station_name=station_name,
                    value=value,
                    datetime=datetime_instance
                )
                if commit:
                    record.save()
                else:
                    records_to_create.append(record)
        
        for field_name, station_name, station_type in stations_water_level:
            value = self.cleaned_data.get(field_name)
            if value is not None:
                record = Record(
                    source_station_type=station_type,
                    source_station_name=station_name,
                    value=value,
                    datetime=datetime_instance
                )
                if commit:
                    record.save()
                else:
                    records_to_create.append(record)
        
        return datetime_instance