import nicegui
import time

text = "truly a web moment"
##grab current time
current_time = time.strftime("%H:%M:%S")
timelabel1 = nicegui.ui.label(current_time)
basiclabel1 = nicegui.ui.label(text)

nicegui.ui.timer(interval=0.1, callback=lambda: timelabel1.set_text(time.strftime("%H:%M:%S")))

nicegui.ui.run(port=80,title="Jack's site",dark=True,language='en-US')