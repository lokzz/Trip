import lokzzpylib
from nicegui import ui, app
from starlette.requests import Request
import time
import json
import os
import re

##formatting
print('|----------------|--------------------------------|')


if 'spots.json' in os.listdir():
    with open('spots.json') as json_file:
        knowndict = json.load(json_file)
else:
    open('spots.json', 'w').close()
    knowndict = ["None"]

print("| {} | data load               [done] |".format(time.strftime("%d/%m %H:%M:%S")))

with open('log.txt', 'a') as f:
    f.write('|----------------|--------------------------------|\n')
    f.write('| {} | server restarted               |\n'.format(time.strftime("%d/%m %H:%M:%S")))
    f.write('|                |                                |\n')
    f.close()

def write_log(data, console=True, format=True):
    if format:
        addspecs = 30 - len(data)
        for i in range(addspecs):
            data += " "
        data = ("| {} | {} |".format(time.strftime("%d/%m %H:%M:%S"), data))
        with open('log.txt', 'a') as f:
            f.write(data+"\n")
    else:
        with open('log.txt', 'a') as f:
            f.write(data+"\n")
    if console:
        write_console(data, False)

def write_console(text, format=True):
    if format:
        addspecs = 30 - len(text)
        for i in range(addspecs):
            text += " "
        print("| {} | {} |".format(time.strftime("%d/%m %H:%M:%S"), text))
    else:
        print(text)

def reload_spots():
    with open('spots.json') as json_file:
        knowndict = json.load(json_file)

def make_spot(name):
    if name == "":
        ui.notify("what are you trying to do")
    else:
        with open('spots.json', 'w') as json_file:
            try:
                open("trips/"+name+".json", "x")
                newtrip = open("trips/"+name+".json", "w")
                if knowndict == ["None"]:
                    json.dump(name, json_file)
                else:
                    knowndict.append(name)
                    json.dump(knowndict, json_file)
                defaultdict = {"name": name, "date": "", "estarrival": "", "location": "", "description": ""}
                json.dump(defaultdict, newtrip)
                ui.open("spots?name=_"+str(name))
            except:
                ui.notify(f"spot \"{name}\" already exists.")
                tabs.set_value('spots')

def del_spot(name):
    knowndict.remove(name)
    os.remove("trips/"+name+".json")
    ui.notify("spot deleted")

def open_spot(spot):
    spot = str(spot)
    spot = spot.replace("'", "")
    if not spot == "Choose":
        if spot == "None":
            ui.notify("what are you trying to do")
        else:
            if spot in knowndict:
                ui.open("spots?name=_"+str(select1.value))
            else:
                ui.notify("spot does not exist")
    else:
        ui.notify("select a spot")


print("| {} | function load           [done] |".format(time.strftime("%d/%m %H:%M:%S")))
print('|----------------|--------------------------------|')

#MainPage
def update():
    timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")
    reload_spots()
    select1.update()

with ui.header().style('background-color: #3874c8').classes('items-center justify-between'):
    ui.markdown('## This is **spot**.')
with ui.footer().style('background-color: #3874c8'):
    current_time = time.strftime("%H:%M:%S")
    timelabel1 = ui.label("It's currently " + current_time)

with ui.tabs() as tabs:
    spot = ui.tab('spots', icon='flight_takeoff')
    ui.tab('modify', icon='add_box')
    ui.tab('About', icon='info')
with ui.tab_panels(tabs, value=spot):
    with ui.tab_panel('spots'):
        with ui.row():
            spotlabel1 = ui.label("Select spot:")
            select1 = ui.select(knowndict, value="None", on_change=lambda selected: write_log("[" + str(selected.value) + "]" + " chosen"))
            loadbutton1 = ui.button("Go", on_click=lambda: open_spot(select1.value))
    with ui.tab_panel('modify'):
        with ui.row():
            Creatlabel1 = ui.label("Create spot:")
            newspotbox = ui.input(value="", label="name:").on('keydown.enter', lambda: make_spot(newspotbox.value))
            loadbutton2 = ui.button("Make", on_click=lambda: make_spot(newspotbox.value))
        with ui.row():
            Deletlabel1 = ui.label("Delete spot:")
            deletspotbox = ui.select(knowndict, value="None")
            loadbutton3 = ui.button("Delete", on_click=lambda: del_spot(deletspotbox.value))
    with ui.tab_panel('About'):
        ui.label('Made with pain, by Jack.')
        ui.label('Made in Python, with NiceGUI.')
        ui.label('Project started on 4 Jun, 2023.')
        ui.link('source code here', 'https://github.com/lokzz/trip')
#MainPageEnd

#spotsPage
@ui.page('/spots')
def spots(request: Request):
    def update():
        timelabel1.set_text("It's currently " + time.strftime("%H:%M:%S") + " In HKT.")
    def save(oldjson, name, date, estarrival, loc, desc, realname):
        oldjson["name"] = name
        oldjson["date"] = date
        oldjson["estarrival"] = estarrival
        oldjson["location"] = loc
        oldjson["description"] = desc
        json.dump(oldjson, open("trips/"+realname+".json", "w"))
        write_log("writing new data to " + realname)
    
    with ui.header().style('background-color: #3874c8'):
        with ui.column():
            ui.markdown('## This is **spot**.')
            spotheader = ui.markdown()
    with ui.footer().style('background-color: #3874c8'):
        current_time = time.strftime("%H:%M:%S")
        timelabel1 = ui.label("It's currently " + current_time)
    
    requestedspot = str(request._query_params)
    requestedspot = requestedspot.replace("name=_", "")
    spotheader.set_content("Chosen spot: **{}**".format(requestedspot))
    if (requestedspot+".json") in os.listdir("trips"):
        spotjson = json.load(open("trips/"+requestedspot+".json"))
        write_log("[" + requestedspot + "]" +" called")
        spotname = ui.input(value=spotjson["name"], label="name:")
        spotdate = ui.input(value=spotjson["date"], label="date:")
        spotarriv = ui.input(value=spotjson["estarrival"], label="arrive at:")
        spotloc = ui.input(value=spotjson["location"], label="location:")
        spotdesc = ui.input(value=spotjson["description"], label="description:")
        ui.button("Save", on_click=lambda: save(spotjson, spotname.value, spotdate.value, spotarriv.value, spotloc.value, spotdesc.value, requestedspot))
    else:
        ui.label("spot not found.")
        ui.button("GO BACK", on_click=lambda: ui.open("/"))
    
    ui.timer(interval=1, callback=lambda: update())
#spotsPageEnd

def on_connect(ip):
    theip = str(ip.ip)
    addspecs = 15 - len(theip)
    add = ""
    for i in range(addspecs):
        add += " "
    adddiv2 = 1
    adddiv2 = addspecs // 2
    adddiv3 = ""
    for i in range(adddiv2):
        adddiv3 += "."
    addlist = re.findall(adddiv3, add)
    addlist1 = addlist[0]
    addlist2 = addlist[1]
    addlist1_1 = addlist1[:-1] + '@'
    if not (addspecs % 2) == 0:
        addlist2 += " "
    add = addlist1_1 + addlist2
    theip = add + theip
    write_log('new connection ' + theip, True)

app.on_connect(on_connect)
ui.timer(interval=0.1, callback=lambda: update())
ui.run(port=80,title="Jack's site",dark=True)