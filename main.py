from nicegui import ui, app
import time
import json

##read json from data.json into knowndict
with open('data.json') as json_file:
    knowndict = json.load(json_file)

def write_log(data):
    with open('log.txt', 'a') as f:
        f.write(data+"\n")

def update():
    timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")

##header & time
ui.markdown('## This is **Trip**.')

current_time = time.strftime("%H:%M:%S")
timelabel1 = ui.label("It's currently " + current_time)

##content
with ui.tabs() as tabs:
    ui.tab('Trips', icon='flight_takeoff')
    ui.tab('About', icon='info')

with ui.tab_panels(tabs, value='Home'):
    with ui.tab_panel('Home'):
        ui.label("Select Trip:")
        select1 = ui.select(knowndict, value=1, on_change=lambda selected: write_log(str(selected.value)))
    with ui.tab_panel('About'):
        ui.label('Made with pain, by Jack.')
        ui.label('Project started on 4 Jun, 2023.')

ui.timer(interval=0.1, callback=lambda: update())

ui.run(port=80,title="Jack's site",dark=True,language='en-US')