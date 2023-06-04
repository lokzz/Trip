from nicegui import ui, app
import time
import json

##init
with open('data.json') as json_file:
    knowndict = json.load(json_file)
###
print("{} | data load           done".format(time.strftime("%H:%M:%S")))


##init end
##functions
def write_log(data):
    with open('log.txt', 'a') as f:
        f.write(data+"\n")

def open_trip(trip):
    if not trip == "Choose":
        if trip in knowndict:
            ui.open("trips/"+select1.value)
        else:
            ui.notify("trip not found (how)")
    else:
        ui.notify("select a trip (pls)")

def update():
    timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")
###
print("{} | function load       done".format(time.strftime("%H:%M:%S")))

##header & footer.
with ui.header().style('background-color: #3874c8').classes('items-center justify-between'):
    ui.markdown('## This is **Trip**.')

with ui.footer().style('background-color: #3874c8'):
    current_time = time.strftime("%H:%M:%S")
    timelabel1 = ui.label("It's currently " + current_time)


##content
with ui.tabs() as tabs:
    ui.tab('Trips', icon='flight_takeoff')
    ui.tab('About', icon='info')

with ui.tab_panels(tabs, value='Trips'):
    with ui.tab_panel('Trips'):
        with ui.row():
            triplabel1 = ui.label("Select Trip:")
            select1 = ui.select(knowndict, value="Choose", on_change=lambda selected: write_log(str(selected.value)))
            loadbutton1 = ui.button("Go", on_click=lambda: open_trip(select1.value))
    with ui.tab_panel('About'):
        ui.label('Made with pain, by Jack.')
        ui.label('Project started on 4 Jun, 2023.')

ui.timer(interval=0.1, callback=lambda: update())

ui.run(port=80,title="Jack's site",dark=True,language='en-US')