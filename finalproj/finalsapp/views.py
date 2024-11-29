from django.shortcuts import render,redirect, get_object_or_404
from .models import DateTime, Record
from math import ceil
import plotly
import plotly.graph_objs as go
import json
import plotly.offline
from django.db.models import Q
from datetime import timedelta
from.forms import DateTimeForm



# Create your views here.
def index(request):
    return render(request, "finalsapp/welcome.html")

def add_record(request):
    if request.method == 'GET':
        form = DateTimeForm()
    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/finalsapp/records/1/')
    else:
        form = DateTimeForm()
    context = {"form": form, "action": "Add" }
    return render(request, 'finalsapp/record_form.html', context)

def update_record(request, pk):
    dt = DateTime.objects.get(id = pk)
    if request.method == 'GET':
        form = DateTimeForm(instance = dt)
    elif request.method == 'POST':
        form = DateTimeForm(request.POST, instance = dt)
        if form.is_valid():
            form.save()
            return redirect('/finalsapp/records/1/')
    context = {'form': form, 'action': 'Edit'}
    return render(request, 'finalsapp/record_form.html', context)
        
def delete_record(request, pk):
    dt = get_object_or_404(DateTime, id = pk)
    if request.method == 'GET':
        context = {'datetime': dt}
        return render(request, 'finalsapp/delete_record.html', context)
    elif request.method == 'POST':
        dt.delete()
        return redirect('/finalsapp/records/1/')
    
def list_records(request, pg):
    filter_date = request.GET.get('date')
    
    datetime_queryset = DateTime.objects.all()
    
    if filter_date:
        datetime_queryset = datetime_queryset.filter(
            datetime__date=filter_date
        )    
    
    records = datetime_queryset
    num_records = DateTime.objects.count()
    max_pg = ceil(num_records/50)
    second_to_last_pg = max_pg - 1
    next_pg = pg + 1
    prev_pg = pg - 1

    first = 50*(pg-1)
    last = 50*pg
    if last > num_records:
        last = num_records

    records_subset = records[first:last]

    context = {'records': records_subset, 'current_page': pg, 'max_pg': max_pg, 'second_to_last_pg': second_to_last_pg, 'next_pg': next_pg, 'prev_pg': prev_pg}

    return render(request, "finalsapp/list_records.html", context)

def datetime_detail(request, pk):
    dt = DateTime.objects.get(id=pk)

    # Get the rainfall and waterlevel values for the current datetime

    nangka_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.NANGKA, datetime=dt).value)
    boso_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.BOSO, datetime=dt).value)
    aries_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.ARIES, datetime=dt).value)
    campana_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.CAMPANA, datetime=dt).value)
    oro_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.ORO, datetime=dt).value)
    sto_nino_waterlevel= float(Record.objects.get(source_station_type=Record.WATERLEVEL, source_station_name=Record.STO_NINO, datetime=dt).value)

    # Make the interactive pyplot for the water level
    start_time = dt.datetime - timedelta(hours=24)
    end_time = dt.datetime + timedelta(hours=24)
    
    water_level_records = Record.objects.filter(
        source_station_type=Record.WATERLEVEL,
        source_station_name=Record.STO_NINO,
        datetime__datetime__range=[start_time, end_time]
    ).order_by('datetime__datetime')
    
    x_values = [record.datetime.datetime for record in water_level_records]
    y_values = [float(record.value) for record in water_level_records]
    
    trace_water = go.Scatter(
        x=x_values, 
        y=y_values, 
        mode='lines+markers',
        name='Sto. Nino'
    )
    
    layout_water = go.Layout(
        title=f'Water Level Records for Sto. Nino around {dt.datetime}',
        xaxis=dict(
            title='Datetime'
        ),
        yaxis=dict(title='Water Level'),
        height=600,
        width=1000,
        margin=dict(
            l=50,
            r=50,
            t=60,
            b=100
        )
    )
    
    # Create figure configuration for additional interactivity
    config = {
        'scrollZoom': True,  # Allow scrolling and zooming
        'displayModeBar': True,  # Show the mode bar with additional tools
        'responsive': True  # Make the plot responsive
    }
    
    # Create figure and convert to div
    fig_waterlevel = go.Figure(data=[trace_water], layout=layout_water)
    plot_div_waterlevel = plotly.offline.plot(fig_waterlevel, output_type='div', include_plotlyjs=True, config=config)
    rainfall_stations = [
        Record.NANGKA, 
        Record.BOSO, 
        Record.ARIES, 
        Record.CAMPANA, 
        Record.ORO
    ]
    
    rainfall_traces = []
    for station in rainfall_stations:
        rainfall_records = Record.objects.filter(
            source_station_type=Record.RAINFALL,
            source_station_name=station,
            datetime__datetime__range=[start_time, end_time]
        ).order_by('datetime__datetime')
        
        x_rainfall_values = [record.datetime.datetime for record in rainfall_records]
        y_rainfall_values = [float(record.value) for record in rainfall_records]
        
        rainfall_traces.append(go.Scatter(
            x=x_rainfall_values, 
            y=y_rainfall_values, 
            mode='lines+markers',
            name=f'{station} Rainfall'
        ))
    
    rainfall_layout = go.Layout(
        title=f'Rainfall Records around {dt.datetime}',
        xaxis=dict(
            title='Datetime',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=3, label="3d", step="day", stepmode="backward")                
                ])
            )
        ),
        yaxis=dict(title='Rainfall'),
        height=600,
        width=1000,
        margin=dict(l=50, r=50, t=60, b=100)
    )
    
    rainfall_config = {
        'scrollZoom': True,
        'displayModeBar': True,
        'responsive': True
    }
    
    fig_rainfall = go.Figure(data=rainfall_traces, layout=rainfall_layout)
    plot_div_rainfall = plotly.offline.plot(fig_rainfall, output_type='div', include_plotlyjs=True, config=rainfall_config)

    context = {
    'datetime': dt, 
    'Sto_Nino': sto_nino_waterlevel, 
    'Mt_Aries': aries_rainfall,
    'Boso_Boso': boso_rainfall,
    'Mt_Campana': campana_rainfall, 
    'Nangka': nangka_rainfall,
    'Mt_Oro': oro_rainfall,
    'plot_div_waterlevel': plot_div_waterlevel,
    'plot_div_rainfall': plot_div_rainfall
}

    return render(request, "finalsapp/datetime_detail.html", context)