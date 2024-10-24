import time
import os
from datetime import datetime, timedelta
from playsound import playsound

def set_alarm(alarm_time):
    print(f"Alarm is set for {alarm_time.strftime('%H:%M:%S')}")
    
    while datetime.now() < alarm_time:
        time.sleep(1)  # Check every second
    
    print("Wake up! The time is now", datetime.now().strftime('%H:%M:%S'))

    current_path = os.path.dirname(os.path.abspath(__file__))
    playsound(os.path.join(current_path, 'data', 'alarm_sound.mp3'))

# Set the alarm for 8 hours from now
current_time = datetime.now()
alarm_time = current_time + timedelta(seconds=5)

set_alarm(alarm_time)