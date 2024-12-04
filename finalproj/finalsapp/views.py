from django.shortcuts import render,redirect, get_object_or_404
from .models import DateTime, Record
from math import ceil
import plotly
import plotly.graph_objs as go
import plotly.offline
from django.db.models import Case, When
from datetime import timedelta
from.forms import DateTimeForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "finalsapp/welcome.html")

def add_record(request):
    if request.method == 'GET':
        form = DateTimeForm()
    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        submitted_datetime = form.data.get('datetime')
        existing_datetime = DateTime.objects.filter(datetime=submitted_datetime).exists()
        
        if existing_datetime:
            messages.warning(request, 'The given datetime already exists in the database.')
        
        if form.is_valid() and not existing_datetime:
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
    context = {'form': form, 'action': 'Edit', 'datetime': dt}
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
    records = DateTime.objects.order_by('datetime')
    num_records = DateTime.objects.count()
    max_pg = ceil(num_records/50)
    second_to_last_pg = max_pg - 1
    next_pg = pg + 1
    prev_pg = pg - 1

    first_entry = 50*(pg-1)
    last_entry = 50*pg
    if last_entry > num_records:
        last_entry = num_records

    records_subset = records[first_entry:last_entry]

    context = {'records': records_subset, 'current_page': pg, 'max_pg': max_pg, 'second_to_last_pg': second_to_last_pg, 'next_pg': next_pg, 'prev_pg': prev_pg}

    return render(request, "finalsapp/list_records.html", context)

def datetime_detail(request, pk):
    dt = DateTime.objects.get(id=pk)

    # Get the rainfall and waterlevel values for the current datetime

    # nangka_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.NANGKA, datetime=dt).value)
    # boso_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.BOSO, datetime=dt).value)
    # aries_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.ARIES, datetime=dt).value)
    # campana_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.CAMPANA, datetime=dt).value)
    # oro_rainfall = float(Record.objects.get(source_station_type=Record.RAINFALL, source_station_name=Record.ORO, datetime=dt).value)
    # sto_nino_waterlevel= float(Record.objects.get(source_station_type=Record.WATERLEVEL, source_station_name=Record.STO_NINO, datetime=dt).value)

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
        yaxis=dict(title='Water Level (m)'),
        height=600,
        width=1000,
        margin=dict(
            l=50,
            r=50,
            t=60,
            b=100
        )
    )
    
    config = {
        'scrollZoom': True,  
        'displayModeBar': True,  
        'responsive': True  
    }
    
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
        yaxis=dict(title='Rainfall (mm)'),
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
        # 'Sto_Nino': sto_nino_waterlevel, 
        # 'Mt_Aries': aries_rainfall,
        # 'Boso_Boso': boso_rainfall,
        # 'Mt_Campana': campana_rainfall, 
        # 'Nangka': nangka_rainfall,
        # 'Mt_Oro': oro_rainfall,
        'plot_div_waterlevel': plot_div_waterlevel,
        'plot_div_rainfall': plot_div_rainfall
    }

    return render(request, "finalsapp/datetime_detail.html", context)

def query_records(request):
    filter_date = None
    filter_time = None
    search_station_name = 'All Stations'
    search_station_type = 'All Records'
    query_datetime = False
    query_station = False
    
    datetimes = DateTime.objects.order_by('datetime')  # Sort datetimes from oldest to newest
    records = Record.objects.all()
    queryset = None

    # https://stackoverflow.com/questions/11586038/how-to-get-the-value-from-the-drop-down-box-django
    if request.GET.get('station'):
        search_station_name = request.GET.get('station')

        if search_station_name != "All Stations":
            queryset = records
            queryset = queryset.filter(
                source_station_name__iexact=search_station_name
            )
            record = queryset[0]
            search_station_type = f'{record.source_station_type} Records'

            if request.GET.get('date'):
                filter_date = request.GET.get('date')
                queryset = queryset.filter(
                    datetime__datetime__date=filter_date
                )
                query_datetime = True
            
            if request.GET.get('time'):
                filter_time = request.GET.get('time')
                queryset = queryset.filter(
                    datetime__datetime__time=filter_time
                )
                query_datetime = True

            if request.GET.get('sort'):
                queryset = queryset.order_by('-value')
        
        elif search_station_name == 'All Stations':
            queryset = datetimes

            if request.GET.get('date'):
                filter_date = request.GET.get('date')
                queryset = queryset.filter(
                    datetime__date=filter_date
                )
                query_datetime = True
            
            if request.GET.get('time'):
                filter_time = request.GET.get('time')
                queryset = queryset.filter(
                    datetime__time=filter_time
                )
                query_datetime = True
            
            if request.GET.get('sort'):
                sort_station = request.GET.get('sort')

                records = records.filter(
                    source_station_name__iexact=sort_station
                )
                records = records.order_by('-value')

                # https://blog.kinsacreative.com/articles/manually-order-a-queryset-to-match-a-predefined-li/
                ids = []

                for record in records:
                    ids.append(record.datetime.id)

                preserved_ordering = Case(*[When(id=id, then=position) for position, id in enumerate(ids)])
                queryset = queryset.filter(id__in=ids).order_by(preserved_ordering)

        query_station = True

    context = {'records': queryset, 'query_dt': query_datetime, 'query_station': query_station, 'search_station_name': search_station_name, 'search_station_type': search_station_type,}
    
    return render(request, "finalsapp/query_records.html", context)
