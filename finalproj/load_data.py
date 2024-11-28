from finalsapp.models import DateTime, Record
import csv

print('hi')

f = open("July2022.csv", 'r')
reader = csv.reader(f)

for row in reader:
    date_time = DateTime.objects.create(datetime = row[7])
    Record.objects.create(
        source_station_type = Record.RAINFALL,
        source_station_name = Record.ARIES,
        value = row[1],
        datetime = date_time
    )
    Record.objects.create(
        source_station_type = Record.RAINFALL,
        source_station_name = Record.BOSO,
        value = row[2],
        datetime = date_time
    )
    Record.objects.create(
        source_station_type = Record.RAINFALL,
        source_station_name = Record.CAMPANA,
        value = row[3],
        datetime = date_time
    )
    Record.objects.create(
        source_station_type = Record.RAINFALL,
        source_station_name = Record.NANGKA,
        value = row[4],
        datetime = date_time
    )
    Record.objects.create(
        source_station_type = Record.RAINFALL,
        source_station_name = Record.ORO,
        value = row[5],
        datetime = date_time
    )
    Record.objects.create(
        source_station_type = Record.WATERLEVEL,
        source_station_name = Record.STO_NINO,
        value = row[6],
        datetime = date_time
    )

f.close()