#!/usr/bin/env python3.0
#Behavioral Audiogram Program for Quail - 2 Choice Procedure
#Uses servo to cover/uncover food under cage
#Toggle for sound trial training and testing
#7/27/2017 by Evan Hill & Sarah Strawn

import time, random
import RPi.GPIO as GPIO
from tkinter import *
from tkinter.messagebox import *
from Adafruit_PWM_Servo_Driver import PWM


GPIO.setmode(GPIO.BCM)


def trial(value, sound): #all trials
    global b_press, stop_t, r_window, rwd_rt, timer
    sound_on = sound
    if value == 1:
        GPIO.output(5, 1)
        GPIO.remove_event_detect(24)
        GPIO.remove_event_detect(26)
        GPIO.add_event_detect(24, GPIO.FALLING, callback = lambda *args: trial(2, sound), bouncetime=100)
    elif value == 2 and sound_on == 1:
        GPIO.remove_event_detect(24)
        GPIO.remove_event_detect(26)
        GPIO.output(5, 1)
        GPIO.output(17, 1)
##        if trial_led == 0 and w_countdown == 0:
##            GPIO.output(5, 0)
##        if trial_led == 1: # and w_countdown == 0:
##            GPIO.output(5, 1)
##        w.after(750, lambda *args: GPIO.output(5, 0))
        stop_t = time.time() + 2 #defines stop time as current time + 2s
        b_press = time.time() #changes button press default to current time
        
        GPIO.add_event_detect(24, GPIO.FALLING, callback = lambda *args: b_timer(stop_t, 2), bouncetime=100)
##        GPIO.add_event_detect(26, GPIO.FALLING, callback = lambda *args: b_timer(stop_t, 2), bouncetime=100)
        GPIO.output(23,1) #Green LED on
        timer = w.after(2000, lambda *args: stop(sound))
##        if sound == 2:
##            sound_trigger()
    elif value == 2 and sound_on == 2:
        GPIO.remove_event_detect(24)
        GPIO.remove_event_detect(26)
        GPIO.output(5, 1)
        GPIO.output(17, 1)
##        if trial_led == 0 and w_countdown == 0:
##            GPIO.output(5, 0)
##        if trial_led == 1: # and w_countdown == 0:
##            GPIO.output(5, 1)
##        w.after(750, lambda *args: GPIO.output(5, 0))
        stop_t = time.time() + 2 #defines stop time as current time + 2s
        b_press = time.time() #changes button press default to current time
##        GPIO.add_event_detect(24, GPIO.FALLING, callback = lambda *args: b_timer(stop_t, 2), bouncetime=100)
        GPIO.add_event_detect(26, GPIO.FALLING, callback = lambda *args: b_timer(stop_t, 1), bouncetime=100)
        GPIO.output(23,1) #Green LED on
        sound_trigger()
        timer = w.after(2000, lambda *args: stop(sound))
##        if sound == 2:
        


master = Tk()

master.title("Behavioral Audiogram - Conditioned Suppression/Avoidance") #labels window

pwm = PWM(0x40)

##count = 0 #counter to record number of sound presentations
reward_count = 0 #number of rewards dispensed
wp_count = 0 #warning peck counter
wp_set = 2 #alters wp value for test vs train
##w_train = 1
safe_resp = [] #creates a string that records safe trials
warning_resp = [] #same for warning trials
w_countdown = -1 #safe trial countdown to sound trial
p_output = 0 #defines performance output
s_output = 0 #toggles GPIO pin 12 off and on to trigger sound
x = 21 #wrap-around after 20 trial results
x_coord = 120 #x-coordinates for trial result outputs
y = 10 #y-coordinates for trial result outputs
canvas_width = 600 #window width
canvas_height = 1000 #window height
servoMin = 340 # Cover food dish
servoMax = 200  # Dispense reward
pwm.setPWMFreq(60) # Set frequency to 60 Hz
rwd_dur = 2024 #defaults reward duration to 2.0 seconds
rwd_rt = 0 #defaults reward presentation rate to continuous 
rwd_rem = 0 #defines the FR/VR schedule
b_press = 0 #defines button press recording variable
stop_t = 0 #defines time at which trial is ended
r_window = 0.50 #defines response classification window, set to 500 ms
f_alarms = 0
fa_counter = 0
hits = 0
##resp_ext = 0.05 #extends peck duraion 50 ms
fa_fix = 0 #value of 1 repeats silent trial immediately following a false alarm
starter = 0
reward = 0
eto = 0
time_out = 5000 #Defaults eto length to 5s
timer = 0
sound = 0
warn_rew = 0 #defaults program to reward hits
##trial_led = 0 #defaults to training mode
t1_check = 1000 #checks the status of the first silent trial in a series
w_press = 0 #checks to see if warning button pressed

GPIO.setup(5, GPIO.OUT) #button LED
GPIO.setup(17, GPIO.OUT) #RED button LED
GPIO.setup(23, GPIO.OUT) #LED indicating trial in progress
GPIO.setup(21, GPIO.OUT) #operates shock relay
GPIO.setup(12, GPIO.OUT) #operates sound relay
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets up GPIO for top button
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets up GPIO for bottom button
 
def trial_router(value):
    global w_countdown, count, starter, rwd_rt, eto, timer, sound, reward, wp_set
    w.after_cancel(eto)
    w.after_cancel(timer)
    w.after_cancel(sound)
    w.after_cancel(reward)
    wp_count = 0
    w.after(1, lambda *args: pwm.setPWM(15, 0, servoMin)) #covers food reservoir
    if w_countdown < 0:
        w_countdown = 1
    if value == 0:
        count = 0
        w.delete('countdown', 'reward')
        w_countdown = random.randint(2, 6)
        w.create_text(553, 910, text=(w_countdown), anchor = W, tags = 'countdown')
        w.create_text(553, 930, text = reward_count, anchor = W, tags = 'reward')
        starter = w.after(1, lambda *args: trial(1, 1))
    elif value == 1:
        w.delete('countdown', 'reward')
        w.create_text(553, 910, text=(w_countdown), anchor = W, tags = 'countdown')
        w.create_text(553, 930, text = reward_count, anchor = W, tags = 'reward')
        starter = w.after(1, lambda *args: trial(1, 1))
    elif value == 2:
        if wp_set == 1:
            w.after(1, lambda *args: GPIO.output(5, 0))
        w.delete('countdown', 'reward')
        w.create_text(553, 910, text='Now!', fill = "red", anchor = W, tags = 'countdown')
        w.create_text(553, 930, text = reward_count, anchor = W, tags = 'reward')
        starter = w.after(1, lambda *args: trial(1, 2))
   

def sound_trigger(): #uncomment to add multiple pulses
    global count, r_window, sound
##    count += 1
    w.after(1, lambda *args: GPIO.output(12, 1))
    w.after(21, lambda *args: GPIO.output(12, 0))
##    if count < 3: #trigger sound for 2 pulses, 1/s. 
##        GPIO.output(12, 1)
##        w.after(20, lambda *args: GPIO.output(12, 0))
##        sound = w.after(1000, sound_trigger)

def b_timer(stop_t, value): #records time at which button was pressed
    global b_press, wp_count, wp_set, w_press
    b_press = stop_t - time.time() #can add time to time.time() to have a "peck extension"
    wp_count += 1
    if wp_count == wp_set and w_countdown == 0:
        w.after(1, lambda *args: GPIO.output(5, 0)) #turn off button LED
    if value == 1:
        w_press += 1
##        b_press = 0

##    elif wp_count > wp_set and value == 2:
##        b_press = 0

def stop(value): #checks if button was pressed
    global rwd_rt, w_countdown, wp_count, eto, w_press
    w.after(1, lambda *args: GPIO.output(23, 0))
    w.after(2, lambda *args: GPIO.output(5, 0))
    w.after(2, lambda *args: GPIO.output(17, 0))
    w.after(1, lambda *args: GPIO.remove_event_detect(24))
    w.after(2, lambda *args: GPIO.remove_event_detect(26))
    w.update_idletasks()
    w_countdown -= 1
##    if value == 1 and b_press > r_window and safe_resp.__len__() == 0:
##        w_countdown +=1
##        eto = w.after(time_out, lambda *args: trial_router(1))
##    elif value == 1 and b_press > r_window and safe_resp.__len__()%t1_check == 0:
##        w_countdown +=1
##        eto = w.after(time_out, lambda *args: trial_router(1))
    if value == 1 and b_press <= r_window and rwd_rt == 0:
        rwd_rt = random.randint(0,rwd_rem) #randomizer for variable ratio schedule
        w.after(5, lambda *args: give_reward(1)) #records a correct rejection with reward
    elif value == 1 and rwd_rt > 0 and b_press <= r_window:
        rwd_rt -=1
        w.after(5, lambda *args: give_noreward(1)) #records a correct rejection and no reward
    elif value == 1 and b_press > r_window and fa_fix == 0:
        w.after(350, lambda *args: give_noreward(2)) #records false alarm and moves to next silent trial
    elif value == 1 and b_press > r_window and fa_fix == 1:
        w.after(350, lambda *args: give_noreward(3)) #records false alarm and moves repeats silent trial
    elif value == 2 and w_press <= 1:
        w_press = 0
        w.after(1, lambda *args: GPIO.output(21, 1)) #activate shock relay
        w.after(1000, lambda *args: give_noreward(4)) #records a miss, sets shock duration to 1 s
    elif value == 2: #and w_press > r_window: # and warn_rew == 0: #rwd_rt == 0:
##        rwd_rt = random.randint(0,rwd_rem) #randomizer for variable ratio schedule
        w_press = 0
        if warn_rew == 0:
            w.after(1, lambda *args: GPIO.output(21, 0))
            w.after(20, lambda *args: give_reward(5)) #records a hit and gives reward
        elif warn_rew == 1:
            w.after(1, lambda *args: GPIO.output(21, 0))
            w.after(20, lambda *args: give_noreward(5)) #records a hit and no reward
##    elif value == 2 and b_press > r_window and warn_rew == 1: #rwd_rt > 0:
##        rwd_rt -=1
##        w.after(1, lambda *args: GPIO.output(21, 0))
##        w.after(20, lambda *args: give_noreward(4)) #records a hit and no reward

def give_reward(value):
    global reward_count, safe_resp, warning_resp, reward, fa_counter, t1_check
    w.update_idletasks()
    w.after(3, lambda *args: pwm.setPWM(15, 0, servoMax)) #dispenses reward
    w.after(rwd_dur, lambda *args: slow_close(servoMax)) #sets timer to cover food dish
    delay = rwd_dur + 1000
    if value == 1: #Reward for safe trial
        fa_counter = 0
        reward_count += 1
        safe_resp.append(1)
        w.after(5, lambda *args: calculations(1))
        if w_countdown == 0: #makes next trial a sound trial
            reward = w.after(delay, lambda *args: trial_router(2))
        else: #makes next trial a silent trial
            reward = w.after(delay, lambda *args: trial_router(1)) 
    else: #Reward for warning trial
        reward_count += 1
        t1_check = safe_resp.__len__()
        warning_resp.append(0)
        w.after(5, lambda *args: calculations(4))
        reward = w.after(delay, lambda *args: trial_router(0))
        
def slow_close(value):
    if value < servoMin:
        value += 5
        w.after(17, lambda *args: pwm.setPWM(15, 0, value))
        w.after(17, lambda *args: slow_close(value))

def give_noreward(value):
    global safe_resp, warning_resp, eto, w_countdown , fa_counter, reward, t1_check
    w.update_idletasks()
    if value == 1: #no reward for safe trial
        fa_counter = 0
        safe_resp.append(1)
        w.after(5, lambda *args: calculations(2))
        if w_countdown == 0: #makes next trial a sound trial
            reward = w.after(500, lambda *args: trial_router(2))
        else: #makes next trial a silent trial
            reward = w.after(500, lambda *args: trial_router(1)) 
    elif value == 2: #no reward for false alarm, no correction
        fa_counter += 1
        safe_resp.append(0)
        if safe_resp.__len__() == 1: #prevents first trial false alarms
            safe_resp.remove(0)
            w_countdown +=1
            eto = w.after(time_out, lambda *args: trial_router(1))
        elif safe_resp.__len__()%(t1_check + 1) == 0:
            safe_resp.remove(0)
            w_countdown +=1
            eto = w.after(time_out, lambda *args: trial_router(1))
        elif w_countdown == 0: #prevents moving on to sound trial
            w_countdown += 2
            if fa_counter == 1:
                w.after(5, lambda *args: calculations(3))
            elif fa_counter > 1:
                safe_resp.remove(0)
            eto = w.after(time_out, lambda *args: trial_router(1))
        else: #moves to next silent trial
            fa_counter = 0
            w.after(5, lambda *args: calculations(3))
            eto = w.after(time_out, lambda *args: trial_router(1)) 
    elif value == 3: #no reward for false alarm with correction
        safe_resp.append(0)
        w_countdown += 1
        fa_counter += 1
        if safe_resp.__len__() == 1: #prevents first trial false alarms
            fa_counter = 0
            safe_resp.remove(0)
            eto = w.after(time_out, lambda *args: trial_router(1))
        elif safe_resp.__len__()%(t1_check + 1) == 0:
            fa_counter = 0
            safe_resp.remove(0)
            eto = w.after(time_out, lambda *args: trial_router(1))
        elif fa_counter == 1:
                w.after(5, lambda *args: calculations(3))
        elif fa_counter > 1:
            safe_resp.remove(0)
        eto = w.after(time_out, lambda *args: trial_router(1))
    elif value == 4: #no reward for miss
        t1_check = safe_resp.__len__()
        warning_resp.append(1)
        w.after(1, lambda *args: GPIO.output(21, 0))
        w.after(5, lambda *args: calculations(5))
        eto = w.after(500, lambda *args: trial_router(0))
    elif value == 5: #unrewarded hit
        t1_check = safe_resp.__len__()
        w.after(5, lambda *args: calculations(4))
        warning_resp.append(0)
        w.after(500, lambda *args: trial_router(0))

def calculations(value):
    global x_coord, p_output, f_alarms, hits
    w.update_idletasks()
    x_coord += 20
    if warning_resp.__len__() >= 7 and safe_resp.__len__()%t1_check == 0:
        w.after(50, lambda *args: clear())
    if warning_resp.__len__() == 0 and safe_resp.__len__() == 0:
        f_alarms = int(0*1000)/1000
        hits = int(1*1000)/1000
    elif warning_resp.__len__() == 0 and safe_resp.__len__() > 0:
        f_alarms = int((safe_resp.count(0)/safe_resp.__len__())*1000)/1000
        hits = int(1*1000)/1000
    else:
        f_alarms = int((safe_resp.count(0)/safe_resp.__len__())*1000)/1000
        hits = int((warning_resp.count(0)/warning_resp.__len__())*1000)/1000
    p_output = int(((hits - (hits * f_alarms))*1000))/1000
    if value == 1:
        w.after(5, lambda *args: write_text(1))
    elif value == 2:
        w.after(5, lambda *args: write_text(2))
    elif value == 3:
        w.after(5, lambda *args: write_text(3))
    elif value == 4:
        w.after(5, lambda *args: write_text(4))
    elif value == 5:
        w.after(5, lambda *args: write_text(5))
    else:
        w.after(5, lambda *args: write_text(6))

def window_def(value):
    global r_window
    w.delete('rsp_rate')
    if value == 0:
        if r_window <= 1.4:
            r_window = int((r_window*10)+1)/10
        else:
            r_window = 1.50
        w.create_text(100, 225, text = r_window, anchor = W, tags = 'rsp_rate')
    else:
        if r_window <= 0.2:
            r_window = 0.2
        else:
            r_window = int((r_window*10)-1)/10
        w.create_text(100, 225, text = r_window, anchor = W, tags = 'rsp_rate')

    
def reward_rt(value):
    global rwd_rem, warn_rew, rwd_rt
    warn_rew = 0
    w.delete('rwd_rate')
    if value == 0:
        rwd_rem = 0
        rwd_rt = rwd_rem
        w.create_text(90, 150, text = (rwd_rt + 1), anchor = W, tags = 'rwd_rate')
    elif value == 1:
        con_rt.deselect()
        if rwd_rem <= 8:
            rwd_rem += 1
        else:
            rwd_rem += 10
        rwd_rt = random.randint(0,(rwd_rem + 1))
        w.create_text(75, 150, text = "VR ", anchor = W, tags = 'rwd_rate')
        w.create_text(95, 150, text = int((rwd_rem + 1)), anchor = W, tags = 'rwd_rate')
    elif value == 2:
        con_rt.deselect()
        if rwd_rem > 10:
            rwd_rem -= 10
        elif rwd_rem <= 1:
            rwd_rem = 1
        else:
            rwd_rem -= 1
        rwd_rt = random.randint(0,(rwd_rem+1))
        w.create_text(75, 150, text = "VR ", anchor = W, tags = 'rwd_rate')
        w.create_text(95, 150, text = int((rwd_rem + 1)), anchor = W, tags = 'rwd_rate')

        
def edit_rwd_dur(value):
    global rwd_dur
    if value == 0:
        rwd_dur += 500
        w.delete('rwd')
        w.create_text(100, 545, text = ((((rwd_dur-24)/1000)*100)/100.0), anchor = W, tags = 'rwd')
    elif value ==1:
        rwd_dur -= 500
        w.delete('rwd')
        w.create_text(100, 545, text = ((((rwd_dur-24)/1000)*100)/100.0), anchor = W, tags = 'rwd')

def edit_eto(value):
    global time_out
    w.delete('eto_dur')
    if value == 0:
        time_out += 5000
        w.create_text(100, 280, text = int(time_out/1000), anchor = W, tags = 'eto_dur')
    else:
        if time_out <= 5000:
            time_out = 5000
        else:
            time_out -= 5000
        w.create_text(100, 280, text = int(time_out/1000), anchor = W, tags = 'eto_dur')
  
def FA_prev(value):
    global fa_fix
    if value == 1:
        prev2.deselect()
        fa_fix = 1
    else:
        prev1.deselect()
        fa_fix = 0

def train_test(value1, value2):
    global wp_set #, trial_led
    wp_set = value1
    #trial_led = value2
    if value2 == 0:
        t_test2.deselect()
##        wp_set = 6
##        trial_led = 0
    else:
        t_test1.deselect()
##        wp_set = 1000
##        trial_led = 1

def w_rew(value):
    global warn_rew
    warn_rew = value
    if value == 0:
        wrew2.deselect()
    else:
        wrew1.deselect()


def write_text(value): #update: for each if statement, have the creation of a new value at the x,y coordinates. then put only one creation of new text
    global reward_count, x_coord, y, write, p_output, safe_resp, resp_count, f_alarms, hits
    w.delete('calc_output', 'countdown', 'reward')
    w.create_text(140, 910, text = safe_resp.count(0), anchor = W, tags = 'calc_output')
    w.create_text(286, 910, text = warning_resp.count(0), anchor = W, tags = 'calc_output')
    w.create_text(140, 930, text = safe_resp.__len__(), anchor = W, tags = 'calc_output')
    w.create_text(286, 930, text = warning_resp.__len__(), anchor = W, tags = 'calc_output')
    w.create_text(553, 930, text = reward_count, anchor = W, tags = 'reward')
    w.create_text(286, 950, text = hits, anchor = W, tags = 'calc_output')
    w.create_text(140, 950, text = f_alarms, anchor = W, tags = 'calc_output')
    w.create_text(553, 910, text=(w_countdown), anchor = W, tags = 'countdown')
    w.update_idletasks()
    if value == 0:
        w.create_text(553, 950, text = "0", anchor = W, tags = 'calc_output')
        w.update_idletasks()
    elif value == 1: 
        w.create_text(x_coord, y, text="S", fill="light green", tags = 'safe')
        w.create_text(553, 950, text = p_output, anchor = W, tags = 'calc_output')
        w.update_idletasks()
    elif value == 2:
        w.create_text(x_coord, y, text="S", fill="white", tags = 'safe')
        w.create_text(553, 950, text = p_output, anchor = W, tags = 'calc_output')
        w.update_idletasks()
    elif value == 3:  
        w.create_text(x_coord, y, text="F", fill="yellow", tags = 'safe')
        w.create_text(553, 950, text = p_output, anchor = W, tags = 'calc_output')
        w.update_idletasks()
    elif value == 4:
        w.create_text(x_coord, y, text="H", fill="light green", tags = 'safe')
        w.create_text(553, 950, text = p_output, anchor = W, tags = 'calc_output')
        x_coord = 120
        y+=20
        w.update_idletasks()
    elif value == 5:
        w.create_text(x_coord, y, text="M", fill="red", tags = 'safe')
        w.create_text(553, 950, text = p_output, anchor = W, tags = 'calc_output')
        x_coord = 120
        y+=20
        w.update_idletasks()

def key_press(event): #event handeler for key strokes
    global eto, timer, sound, reward, starter
    if event.char == "C": #clear screen
        clear()
    elif event.char == "p": #pause without opening food container
        stoper()
    elif event.keysym == "Escape": #close program
        ending()
    elif event.keysym == "space": #start trials
        if w_countdown == -1:
            w.after(1, lambda *args: trial_router(0))
        elif w_countdown == 0:
            w.after(1, lambda *args: trial_router(2))
        else:
            w.after(1, lambda *args: trial_router(1))
    elif event.char == "o": #open food container, pause program
        w.after_cancel(eto)
        w.after_cancel(timer)
        w.after_cancel(sound)
        w.after_cancel(reward)
        w.after_cancel(starter)
        w.after(1, lambda *args: GPIO.remove_event_detect(24))
##        w.after(2, lambda *args: GPIO.remove_event_detect(26))
        w.after(1, lambda *args: GPIO.output(5, 0))
        w.update_idletasks()
        w.after(3, lambda *args: pwm.setPWM(15, 0, servoMax)) #dispenses reward
    elif event.char =="c":
        w.after(5, lambda *args: slow_close(servoMax))
    elif event.char =="r":
        reset()
    elif event.char == "l":
        w.after(1, lambda *args: GPIO.output(5, 1))
    elif event.char == "k":
        w.after(1, lambda *args: GPIO.output(5, 0))

        
def clear(): #opens dialogue box to confirm clearing screen and resetting everything but reward count 
    global resp_count, x_coord, y, safe_resp, warning_resp, rwd_rt, w_countdown, eto, timer, sound, reward, fa_counter, starter
    w.after_cancel(eto)
    w.after_cancel(timer)
    w.after_cancel(sound)
    w.after_cancel(reward)
    w.after_cancel(starter)
    if askyesno('Clear Screen', 'Are you sure you want to clear the screen? All data will be lost.'):
        safe_resp = []
        warning_resp = []
        w_countdown = -1
        x_coord = 120
        y = 10
        fa_counter = 0
        w.after(1, lambda *args: GPIO.remove_event_detect(24))
##        w.after(2, lambda *args: GPIO.remove_event_detect(26))
        w.after(2, lambda *args: GPIO.output(5, 0))
        w.update_idletasks()
        w.delete('safe', 'countdown') #'calc_output',
    else:
        w.after(500, lambda *args: trial_router(0))

def stoper():
    global eto, timer, sound, reward, starter
    w.after_cancel(eto)
    w.after_cancel(timer)
    w.after_cancel(sound)
    w.after_cancel(reward)
    w.after_cancel(starter)
    w.after(1, lambda *args: GPIO.remove_event_detect(24))
    w.after(2, lambda *args: GPIO.output(5, 0))
    w.update_idletasks()
                       
def reset(): #opens dialogue box to confirm clearing screen and resetting all variables 
    global reward_count, resp_count, x_coord, y, safe_resp, warning_resp, rwd_rt, hits, f_alarms, eto, timer, sound, w_countdown, fa_counter, starter
    w.after_cancel(eto)
    w.after_cancel(timer)
    w.after_cancel(sound)
    w.after_cancel(reward)
    w.after_cancel(starter)
    if askyesno('Reset', 'Are you sure you want to reset program? All data will be lost.'):
        reward_count = 0
        f_alarms = int(0*1000)/1000
        hits = int(1*1000)/1000
        safe_resp = []
        warning_resp = []
        w_countdown = -1
        rwd_rt = 0
        x_coord = 120
        y = 10
        fa_counter = 0
        w.after(1, lambda *args: GPIO.remove_event_detect(24))
        w.after(2, lambda *args: GPIO.output(5, 0))
        w.update_idletasks()
        w.delete('calc_output', 'safe', 'countdown', 'reward')
        w.after(50, lambda *args: write_text(0))
    
def ending(): #opens dialogue box to confirm program exit
##    w.unbind_all('<Key>')
    if askyesno('Exit', 'Are you sure you want to quit?'):
        w.quit()
##        pwm.setPWM(15, 0, servoMax)
        GPIO.cleanup()
        master.destroy()
        


w = Canvas(master, width = canvas_width, height = canvas_height, bg = "light gray") #draws window
w.bind_all('<Key>', key_press) #binds keyboard to window, allowing for keyboard control of program
w.pack()                       

w.create_rectangle(130, 0, 1000, 900, fill = "black")
w.create_text(37, 910, text="False Alarms: ", anchor = W)
w.create_text(200, 910, text="Hits: ", anchor = W)
w.create_text(85, 930, text="Total: ", anchor = W)
w.create_text(200, 930, text="Total: ", anchor = W)
w.create_text(39, 950, text="Performance: ", anchor = W)
w.create_text(450, 950, text="H-H*FP: ", anchor = W)
w.create_text(200, 950, text="Performance: ", anchor = W)
w.create_text(450, 930, text="Rewards: ", anchor = W)
w.create_text(450, 910, text="Next Warning: ", anchor = W)

start_b = Button(w, text = 'Start', command=lambda *args: trial_router(0))
start_b.configure(width = 10)
start_b_window = w.create_window(10, 20, anchor=W, window=start_b, tags = 'start')

clear_b = Button(w, text = 'Clear', command = clear)
clear_b.configure(width = 10)
clear_b_window = w.create_window(10, 50, anchor=W, window=clear_b)

reset_b = Button(w, text = 'Reset', command=reset)
reset_b.configure(width = 10)
reset_b_window = w.create_window(10, 80, anchor=W, window=reset_b)

button = Button(w, text = 'Exit', command=ending)
button.configure(width = 10)
button_window = w.create_window(10, 110, anchor=W, window=button)


w.create_text(10, 150, text="Rwd Rate: ", anchor = W)
w.delete('rwd_rate')
w.create_text(100, 150, text = (rwd_rt + 1), anchor = W, tags = 'rwd_rate')
con_rt = Checkbutton(w, text = ' Continuous', command=lambda *args: reward_rt(0))
con_rt.configure(width = 10, anchor=W)
con_rt_window = w.create_window(10, 170, anchor=W, window=con_rt)
con_rt.select()

plus_rt = Button(w, text = " + ", command=lambda *args: reward_rt(1))
plus_rt.configure(width = 3)
plus_rt_window = w.create_window(10, 195, anchor = W, window=plus_rt)

minus_rt = Button(w, text = " - ", command=lambda *args: reward_rt(2))
minus_rt.configure(width = 3)
minus_rt_window = w.create_window(70, 195, anchor = W, window=minus_rt)


w.create_text(10, 225, text="Resp Window:", anchor = W)
w.delete('rsp_rate')
w.create_text(100, 225, text = r_window, anchor = W, tags = 'rsp_rate')

plus_rsp = Button(w, text = " + ", command=lambda *args: window_def(0))
plus_rsp.configure(width = 3)
plus_rsp_window = w.create_window(10, 250, anchor = W, window=plus_rsp)

minus_rsp = Button(w, text = " - ", command=lambda *args: window_def(1))
minus_rsp.configure(width = 3)
minus_rsp_window = w.create_window(70, 250, anchor = W, window=minus_rsp)


w.create_text(10, 280, text="ETO:", anchor = W)
w.delete('eto_dur')
w.create_text(100, 280, text = int(time_out/1000), anchor = W, tags = 'eto_dur')

plus_eto = Button(w, text = " + ", command=lambda *args: edit_eto(0))
plus_eto.configure(width = 3)
plus_eto_window = w.create_window(10, 305, anchor = W, window=plus_eto)

minus_eto = Button(w, text = " - ", command=lambda *args: edit_eto(1))
minus_eto.configure(width = 3)
minus_eto_window = w.create_window(70, 305, anchor = W, window=minus_eto)


w.create_text(10, 335, text = 'Reward Hits?', anchor=W)
wrew1 = Checkbutton(w, text = ' Yes ', command=lambda *args: w_rew(0))
wrew1.configure(width = 10, anchor = W)
wrew1_window = w.create_window(10, 355, anchor = W, window = wrew1)

wrew2 = Checkbutton(w, text = ' No ', command=lambda *args: w_rew(1))
wrew2.configure(width = 10, anchor = W)
wrew2_window = w.create_window(10, 375, anchor = W, window = wrew2)
wrew1.select()


w.create_text(10, 405, text = 'Correct FPs?', anchor=W)
prev1 = Checkbutton(w, text = ' Yes ', command=lambda *args: FA_prev(1))
prev1.configure(width = 10, anchor = W)
prev1_window = w.create_window(10, 425, anchor = W, window = prev1)

prev2 = Checkbutton(w, text = ' No ', command=lambda *args: FA_prev(0))
prev2.configure(width = 10, anchor = W)
prev2_window = w.create_window(10, 445, anchor = W, window = prev2)
prev2.select()


w.create_text(10, 475, text = 'Procedure', anchor=W)
t_test1 = Checkbutton(w, text = ' Training ', command=lambda *args: train_test(1, 0))
t_test1.configure(width = 10, anchor = W)
t_test1_window = w.create_window(10, 495, anchor = W, window = t_test1)

t_test2 = Checkbutton(w, text = ' Testing ', command=lambda *args: train_test(1000, 1))
t_test2.configure(width = 10, anchor = W)
t_test2_window = w.create_window(10, 515, anchor = W, window = t_test2)
t_test1.select()


w.create_text(10, 545, text="Reward Time: ", anchor = W)
w.delete('rwd')
w.create_text(100, 545, text = ((((rwd_dur-24)/1000)*100)/100.0), anchor = W, tags = 'rwd')

plus_rwd = Button(w, text = " + ", command=lambda *args: edit_rwd_dur(0))
plus_rwd.configure(width = 3)
plus_rwd_window = w.create_window(10, 570, anchor = W, window=plus_rwd)

minus_rwd = Button(w, text = " - ", command=lambda *args: edit_rwd_dur(1))
minus_rwd.configure(width = 3)
minus_rwd_window = w.create_window(70, 570, anchor = W, window=minus_rwd)


w.after(1, lambda *args: GPIO.output(21, 0))
w.after(1, lambda *args: GPIO.output(5, 0))
w.after(1, lambda *args: GPIO.output(23, 0))
w.after(500, write_text(0))

mainloop()

      


