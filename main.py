from nicegui import ui, app
from starlette.requests import Request
import time
import json
import os

##formatting
print('|--------------------------------------|')


if 'trips.json' in os.listdir():
    with open('trips.json') as json_file:
        knowndict = json.load(json_file)
else:
    open('trips.json', 'w').close()
    knowndict = ["None"]
print("| {} | data load          [done] |".format(time.strftime("%H:%M:%S")))


def write_log(data):
    with open('log.txt', 'a') as f:
        f.write(data+"\n")

def reload_trips():
    with open('trips.json') as json_file:
        knowndict = json.load(json_file)

def make_trip(name):
    if name == "":
        ui.notify("what are you trying to do")
    ##write to trips.json (add current trips aswell (we will be overriding old file (this is really bad)))
    else:
        with open('trips.json', 'w') as json_file:
            if knowndict == ["None"]:
                json.dump(name, json_file)
            else:
                knowndict.append(name)
                json.dump(knowndict, json_file)

def open_trip(trip):
    trip = str(trip)
    write_log(trip)
    trip = trip.replace("'", "")
    write_log(trip)
    if not trip == "Choose":
        if trip == "None":
            ui.notify("what are you trying to do")
        else:
            if trip in knowndict:
                ui.open("trips?name=_"+str(select1.value))
            else:
                ui.notify("trip nonexist")
    else:
        ui.notify("select a trip")


print("| {} | function load      [done] |".format(time.strftime("%H:%M:%S")))
print('|--------------------------------------|')

#MainPage
def update():
    timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")
    reload_trips()
    select1.update()

with ui.header().style('background-color: #3874c8').classes('items-center justify-between'):
    ui.markdown('## This is **Trip**.')
with ui.footer().style('background-color: #3874c8'):
    current_time = time.strftime("%H:%M:%S")
    timelabel1 = ui.label("It's currently " + current_time)

with ui.tabs() as tabs:
    ui.tab('Trips', icon='flight_takeoff')
    ui.tab('Create', icon='add_box')
    ui.tab('About', icon='info')
with ui.tab_panels(tabs, value='Trips'):
    with ui.tab_panel('Trips'):
        with ui.row():
            triplabel1 = ui.label("Select Trip:")
            select1 = ui.select(knowndict, value="Choose", on_change=lambda selected: write_log(str(selected.value)))
            loadbutton1 = ui.button("Go", on_click=lambda: open_trip(select1.value))
    with ui.tab_panel('Create'):
        with ui.row():
            Creatlabel1 = ui.label("Create Trip:")
            newtripbox = ui.input(value="", label="name:", )
            loadbutton2 = ui.button("Make", on_click=lambda: make_trip(newtripbox.value))
    with ui.tab_panel('About'):
        ui.label('Made with pain, by Jack.')
        ui.label('Made in Python, with NiceGUI.')
        ui.label('Project started on 4 Jun, 2023.')
        ui.link('source code here', 'https://github.com/lokzz/Trip')
#MainPageEnd

#TripsPage
@ui.page('/trips')
def trips(request: Request):
    def update():
        timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")
    
    with ui.header().style('background-color: #3874c8'):
        with ui.column():
            ui.markdown('## This is **Trip**.')
            tripheader = ui.markdown()
    with ui.footer().style('background-color: #3874c8'):
        current_time = time.strftime("%H:%M:%S")
        timelabel1 = ui.label("It's currently " + current_time)
    
    requestedtrip = str(request._query_params)
    requestedtrip = requestedtrip.replace("name=_", "")
    ##check length of requestedtrip
    tripheader.set_content("Chosen trip: {}".format(requestedtrip))
    

    ui.timer(interval=1, callback=lambda: update())
#TripsPageEnd


ui.timer(interval=0.1, callback=lambda: update())
ui.run(port=80,title="Jack's site",dark=True,language='en-US')