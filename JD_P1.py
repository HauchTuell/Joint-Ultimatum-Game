import datetime
import time
from psychopy import visual, event, core, data
import pandas as pd
import random
from time import sleep
import os
import openpyxl
from openpyxl import load_workbook
from psychopy.hardware import keyboard
import subprocess
import win32gui
import win32api
import win32con

screen_width = 1920
screen_height = 1080
win_width = screen_width // 2
win_height = screen_height
win_pos = (0, 0)
win = visual.Window(size=(screen_width, screen_height), screen=1, fullscr=False, allowGUI=True, units='pix',
                    color='black', pos=win_pos)

kb = keyboard.Keyboard()

def get_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S.%f")
    formatted_time = formatted_time[:-3]
    return formatted_time

def time_ms(startTime):
    currentTime_ns = time.time_ns()
    wantedTime_ns = currentTime_ns - startTime
    wantedTime_ms = wantedTime_ns/1e6
    return(wantedTime_ms)


global_startTime = get_time()  # reference point for the start of the experiment
print(global_startTime)

# Some lists for the code
Readers = []  # Saving the responses of the respective partner
Offers = []  # Saving the offers by the dictator
Accumulated = []  # Total amount of money accumulated
Decisions = []  # Saving the first decision


##### LAB 7 PATHS (OG) #####
selfPath = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\P1Response.txt"
coPath = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\P2Response.txt"
offer_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Offer.txt"
offer_path2 = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Offer2.txt"
dec_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Decision.txt"
dec_path2 = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\Decision2.txt"
r_selfPath = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready.txt"
r_coPath = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready2.txt"
r3_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready3.txt"
r4_path = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\ready4.txt"
part_file = r"\\DESKTOP-FRV6AA4\Users\Somby Lab\Desktop\Tiam\Files\part_file.txt"
WhatsAppPath = ["cmd", "/C", "start whatsapp://send?phone=+4368120529803"]


pool_money = 10
num_trials = 20
base_trials = 20
experiment_done = 0
max_offer = 5

discussTimer = 90
decisionTimer = 10

#pool_text = visual.TextStim(win, text='Pool: ' + str(pool_money), height=30, pos=[0, 185])
#offer_text = visual.TextStim(win, text='Offer:', height=30, pos=[0, 135])
#ask_accept = visual.TextStim(win, text='Accept: a', height=50, pos=[-130, -150], color=[0, 255, 0])
#ask_reject = visual.TextStim(win, text='Reject: r', height=50, pos=[130, -150], color=[1, -1, -1])
#one_rejected = visual.TextStim(win, text='You have rejected. \n\n Waiting for partner', height=30, color=[1, -1, -1])
#one_accepted = visual.TextStim(win, text='You have accepted. \n\n Waiting for partner', height=30, color=[0, 255, 0])
#you_rejected = visual.TextStim(win, text='YOU have rejected', height=30, pos=[0, -50], color=[1, -1, -1])
#you_accepted = visual.TextStim(win, text='YOU have accepted', height=30, pos=[0, -50], color=[0, 255, 0])
#partner_rejected = visual.TextStim(win, text='Your PARTNER has rejected', height=30, pos=[0, 50], color=[1, -1, -1])
#partner_accepted = visual.TextStim(win, text='Your PARTNER has accepted', height=30, pos=[0, 50], color=[0, 255, 0])
#rejected = visual.TextStim(win, text='Your TEAM rejected the offer.\n\n' + 'No one receives anything', height=30, color=[1, -1, -1])
#no_unanimous different for JD
#no_unanimous = visual.TextStim(win, text='Decision not unanimous. Random decision', height=30, pos=[0, -50])
#partner_failed = visual.TextStim(win, text='Your partner failed to make a decision in time.\n\n' + 'Random decision', height=30)
#time_over = visual.TextStim(win, text='Your time is over - random decision', height=30, pos=[0, 0])
#timer_text = visual.TextStim(win, text='2:00', height=50, pos=[0, -50])
#decision = visual.TextStim(win, text='You can discuss now. \n\n' + 'Click here and press SPACE once you are ready to decide', height=25, pos=[0, -150])

### Waiting Signal ###
#waiting_signal = visual.TextStim(win, text='.', height = 50, pos=[0,-150])
#dot_timer = core.CountdownTimer(1.0)
#dot_index = 0
### Waiting Signal ###

class ExtortionateProposer:
    accumulated =[]
    accumulated2 = []
    responses = []
    def __init__(self, total_amount, max_offer):
        self.total_amount = total_amount
        self.total_reward = 0
        self.total_collected = 0
        self.previous_offer = None  # Track the previous offer
        self.previous_decision = None
        self.max_offer = max_offer
        self.previousOffers = []
        self.checkList = [self.__class__.responses, self.previousOffers]
        self.randOfferTime = random.randint(10,15)

    def select_offer(self):
        print("previous offer", self.previous_offer)
        if self.previous_offer is not None:
            #print('--- Player 1 ---')
            if 1 < self.previous_offer < max_offer:
                if self.previous_offer == 4:
                    weightsReject = [0.65, 0.45]
                    weightsAccept = [0.3, 0.7]
                elif self.previous_offer == 3:
                    weightsReject = [0.3, 0.7]
                    weightsAccept = [0.15, 0.85]
                else:
                    weightsReject = [0.1, 0.9]
                    weightsAccept = weightsReject
                offers_reject = [self.previous_offer, (self.previous_offer + 1)]
                offers_accept = [(self.previous_offer - 1), self.previous_offer]
            elif self.previous_offer == 1:
                weightsReject = [0.2, 0.8]
                weightsAccept = weightsReject
                offers_reject = [self.previous_offer, (self.previous_offer + 1)]
                offers_accept = [self.previous_offer, self.previous_offer]
            else:
                weightsReject = [1, 0]
                weightsAccept = [0.6, 0.4]
                offers_reject = [self.previous_offer, self.previous_offer]
                offers_accept = [(self.previous_offer - 1), self.previous_offer]
            print("Player 1 Responses", self.__class__.responses)
            self.previous_decision = self.__class__.responses[-1]
            if self.previous_decision == 'r' or self.previous_decision == 'r_rand':
                offer = random.choices(offers_reject, weightsReject)[0]
                #if offer == self.previous_offer:
                #    #print('not giving you any more than this')
                #else:
                #    #print('offer+1')
            else:
                offer = random.choices(offers_accept, weightsAccept)[0]
                #if offer == self.previous_offer:
                #    #print('no need to change')
                #else:
                #    #print('okay thanks idiot')
            print('offer:', offer, 'previous offer: ', self.previous_offer)
        else:
            # If no previous offer (first round), choose a random offer within the constraint
            offer = 3
            print('starting offer = ', offer)
        print("offer", offer)
        self.previousOffers.append(offer)
        self.previous_offer = offer  # Update the previous offer for the next round
        #self.accumulated.append(offer)
        #self.accumulated2.append(offer)
        #sleep(self.randOfferTime)
        return offer

extortionist1 = ExtortionateProposer(pool_money, max_offer)

def confSend(offer, path):
    while True:
        if os.path.getsize(path) == 0:
            with open(path, 'w') as f3:
                f3.write(str(offer))
                f3.close()
                break
        else:
            sleep(0.5)

def confResponse(path):
    while True:
        if os.path.getsize(path) > 0:
            with open(path, 'r') as decision:
                Reply = decision.read()
            if Reply in ['a', 'r','a_rand', 'r_rand']:
                print(f"P1 Decision", Reply)
                sleep(1)
                with open(path, 'w'):
                    pass
                return Reply
        else:
            sleep(0.5)

def confResponseJoint(phase, path):
    while True:  # while True check for:
        if os.path.getsize(path) > 0:
            with open(path, 'r') as decision:
                Reply = decision.read()
            if Reply in ['a', 'r','a_rand', 'r_rand']:
                print("Team Decision", Reply)
            with open(offer_path, 'w') as offer:
                pass
            return Reply
        else:
            sleep(0.5)

def openWhatsApp(path):
    subprocess.Popen(WhatsAppPath, shell=True)
    time.sleep(0.5)

    hwnd = win32gui.FindWindow(None, 'WhatsApp')
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    window_width = screen_width // 2 + 18
    window_height = screen_height -20
    win32gui.MoveWindow(hwnd, -10,0, window_width, window_height, True)

    return hwnd

def closeWhatsApp():
    hwnd = win32gui.FindWindow(None, 'WhatsApp')
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    #win32gui.PostMessage(openFunction, win32con.WM_CLOSE,0,0)

### Welcome phase ###
# Participants see the instructions based on the phase (Alone - Joint - Alone2)
def welcome(phase_welcome):
    back_slide = visual.TextStim(win, text='Back (press LEFT)', height=20, pos=[-150, -250])
    next_slide = visual.TextStim(win, text='Next (press RIGHT)', height=20, pos=[150, -250])
    phaseText = visual.TextStim(win, text='PHASE', height=50, pos=[0, 250])
    if phase_welcome == 0:
        phaseText.text += ' 1'
        welcome_stimuli = [visual.TextStim(win, text = 'Welcome! \n\n In this game you will be matched with someone (called the proposer) and play for '+str(base_trials)+' turns. Each turn the proposer receives points and must distribute them between you and themselves.', height=25, pos =[0,0]),
                           visual.TextStim(win, text = 'The proposer can decide how many points they give to you and how many they keep for themselves. \n\n You can accept or reject the offer. If you reject, none of you receives anything.\n\n The more points you collect throughout the game, the higher the bonus to your reimbursement will be after the experiment.', height = 25, pos= [0,0]),
                           visual.TextStim(win, text = 'If you fail to make a decision within the time limit, the computer will randomly decide for you. \n\n', height = 25, pos =[0,0]),
                           visual.TextStim(win, text = 'We will first do a TEST RUN - then the real experiment will begin.\n\n AFTER pressing SPACE for this slide, you will NOT BE ABLE TO GO BACK and read the rules anymore.',height = 25, pos= [0,0])]

    if phase_welcome == 1:
        phaseText.text += ' 2'
        ##2nd one different for JD
        welcome_stimuli = [visual.TextStim(win, text = 'You will make decisions together with a partner for ' +str(num_trials)+' turns. \n\n You can again accept or reject so noone receives anything. \n\n Your team will have to make unanimous decisions.', height=25, pos =[0,0]),
                           visual.TextStim(win, text = 'Before you make your decision, you will have '+str(discussTimer)+' seconds to discuss via the chat. \n\n The chat will open after the instructions \n\n You may end the discussion before the time runs out.', height = 25, pos= [0,0]),
                           visual.TextStim(win, text = 'A random decision will be made for you if you fail to agree within the time limit.', height = 25, pos =[0,0]),
                           visual.TextStim(win, text = 'There will be a TEST RUN again.\n\n AFTER THIS SLIDE the test run will start.\n\n Press SPACE once you are ready.',height = 25, pos= [0,0])]

    if phase_welcome == 2:
        phaseText.text += ' 3'
        welcome_stimuli = [visual.TextStim(win, text = 'Now you will decide on your own as the recipient again. \n\n You can again accept and keep the offer or reject so both of you receive nothing.', height=25, pos =[0,0]),
                           visual.TextStim(win, text = 'You will again play for '+str(base_trials)+' turns each. You cannot use the chat anymore.', height = 25, pos= [0,0]),
                           visual.TextStim(win, text = 'If you fail to make a decision within the time limit, the computer will randomly decide for you. \n\n', height = 25, pos =[0,0]),
                           visual.TextStim(win, text = 'There is NO TEST RUN this time.\n\n AFTER THIS SLIDE the game will start. \n\n Please press SPACE now.',height = 25, pos= [0,0])]

    stimuli_order = [0, 1, 2, 3]
    i = 0
    while i < len(stimuli_order):
        phaseText.draw()
        welcome_stimuli[stimuli_order[i]].draw()
        if i > 0:
            back_slide.draw()
        if i != len(stimuli_order) - 1:
            next_slide.draw()
        win.flip()
        keys = event.waitKeys(keyList=['left', 'right', 'space'])
        if 'right' in keys and i < len(stimuli_order)-1:
            i += 1
        if 'left' in keys and i > 0:
            i -= 1
        if 'space' in keys and i < len(stimuli_order):
            i += 1

# Synchronizing phase start - players press Space, function writes "ok" into their specified file
# (ready for Player1 - ready2 for Player2 - ready3 for Player3)

def start(phase_start):
    phase = phase_start
    waiting_signal = visual.TextStim(win, text='.', height = 50, pos=[0,-150])
    dot_timer = core.CountdownTimer(1.0)
    dot_index = 0

    start = visual.TextStim(win, text='Please press Space once you are ready', height=30)
    pressedSpace = visual.TextStim(win, text="Waiting for other players", height=30)
    Ready = visual.TextStim(win, text="Everyone is ready.\n\n" + "The TEST RUN will now start", height=30)
    welcome(phase)
    with open(r_selfPath, 'w') as ready:
        ready.write('ok')
    with open(r3_path, 'w') as readyControll:
        readyControll.write('ok')
    pressedSpace.draw()
    waiting_signal.draw()
    win.flip()
    startTime = time.time_ns()
    while True:
        pressedSpace.draw()
        waiting_signal.draw()
        win.flip()
        if dot_timer.getTime() <= 0:
            waiting_signal.text += '.'
            dot_timer.reset()
            dot_index += 1
            if dot_index == 3:
                dot_index = 0
                waiting_signal = visual.TextStim(win, text='.', height=50, pos=[0, -150])
        if phase_start == 0:
            ok = 0
            #ok3 = 0
            #if os.path.getsize(r3_path) > 0:
            #    with open(r3_path, 'r') as ready3:
            #        ok3 = ready3.read()
            if os.path.getsize(r_coPath) > 0:
                with open(r_coPath, 'r') as ready:
                    ok = ready.read()
            if ok == 'ok': #and ok3 == 'ok':
                Ready.draw()
                win.flip()
                core.wait(1.5)
                with open (r_coPath, 'w') as ready:
                    pass
                break
        elif phase_start == 1:
            ok = 0
            #ok3 = 0
            #if os.path.getsize(r3_path) > 0:
            #    with open(r3_path, 'r') as ready3:
            #        ok3 = ready3.read()
            if os.path.getsize(r_coPath) > 0:
                with open(r_coPath, 'r') as ready:
                    ok = ready.read()
            if ok == 'ok': #and ok3 == 'ok':
                Ready.draw()
                win.flip()
                core.wait(1.5)
                with open (r_coPath, 'w') as ready:
                    pass
                break
        else:
            ok = 0
            if os.path.getsize(r_coPath) > 0:
                with open(r_coPath, 'r') as ready:
                    ok = ready.read()
            if ok == 'ok':
                Ready.draw()
                win.flip()
                core.wait(1.5)
                with open(r_coPath, 'w') as ready:
                    pass
                break

#Create a predefined data dictionary:
## Different for JD
dataDict = {'Offer': 0, 'Round_TimeOffer': 0, 'Global_TimeOffer': 0, 'Decision': 0, 'Round_TimeDecision': 0, 'Global_TimeDecision':0, 'Round_TimeC': 0, 'Global_TimeC': 0, 'TimeStamp': 0, 'Accumulated':0, 'Phase':0, 'Dyad':0}

#Appending new values to dictionary
def makedicts(key, value):
    if key in dataDict:         #if key in the defined dictionary
        dataDict[key] = value   #then take that key and append the new value to it
    if key == '0' and value == 0: #values 0 for both --> prints dictionary
        print(dataDict)


### FRONT-END ###
#Display money in pool
def draw_initial(phase):
    if phase == 0:
        if count == 1:
            round_number = visual.TextStim(win, text='Test round', height=30)
        if count > 1:
            round_number = visual.TextStim(win, text= 'Round ' + str(count-1) + ' / ' + str(base_trials), height = 30)
    if phase == 1:
        if count_1 == 1:
            round_number = visual.TextStim(win, text='Test round', height=30)
        if count_1 > 1:
            round_number = visual.TextStim(win, text= 'Round ' + str(count_1-1) + ' / ' + str(num_trials), height = 30)
    if phase == 2:
        round_number = visual.TextStim(win, text= 'Round ' + str(count_2) + ' / ' + str(base_trials), height = 30)
    initial_text = visual.TextStim(win, text='\n\n\n There are ' + str(pool_money) + ' points in the pool', height=30)
    initial_text.draw()
    round_number.draw()
    win.flip()
    core.wait(2.0)

#Read offer from dictator from file "path3"
def readoffer(phase):
    waiting_signal = visual.TextStim(win, text='.', height = 50, pos=[0,-150])
    dot_timer = core.CountdownTimer(1.0)
    dot_index = 0

    wait_offer_text = visual.TextStim(win, text='Please wait for an offer', height=30)

    wait_offer_text.draw()
    waiting_signal.draw()
    win.flip()
    randOfferTime = random.randint(3,8)
    if phase == 0 or phase == 2:
        timerOffer = core.CountdownTimer(randOfferTime)
    else:
        timerOffer = core.CountdownTimer(randOfferTime)
    while True:
        wait_offer_text.draw()
        waiting_signal.draw()
        win.flip()
        if dot_timer.getTime() <= 0:
            waiting_signal.text += '.'
            dot_timer.reset()
            dot_index += 1
            if dot_index == 3:
                dot_index = 0
                waiting_signal = visual.TextStim(win, text='.', height=50, pos=[0, -150])
        if timerOffer.getTime() <= 0:
            #if phase == 0 or phase == 2:
            offer = extortionist1.select_offer()
            with open(offer_path, 'w') as offerP1:
                offerP1.write(str(offer))
            with open(r3_path, 'w') as offerP1:
                offerP1.write(str(offer))
            extortionist1.accumulated.append(offer)
            #extortionist1.accumulated.append(offer)
            #try:
            #    with open(offer_path, 'r') as offer:
            #        Offer = offer.read()
                #if Offer:
            offerTime = time.time_ns()
            timeLocal = time_ms(offerTime)
            makedicts('Round_TimeOffer', timeLocal)
            makedicts('Global_TimeOffer', get_time())
            Offers.append(int(offer))
            if len(Offers) > 0:
                Offer_Dict = Offers[0]
                makedicts('Offer', Offer_Dict)
                core.wait(1)
                break
            #except:
            #    sleep(0.2)

def calc_he_gets():
    if len(Offers) > 0:
        he_gets = pool_money-int(Offers[0])
        return he_gets

#Write own decision in response file
def write(reply):
    #print('trying')
    with open(selfPath, 'w') as p1res:
        p1res.write(str(reply))
        #print('wrote')
        p1res.close()

#Send final team decision to Decision.txt
def sendDecision():
    if len(Readers) > 0:
        Be = [i[0] for i in Readers[0]]
        Decision = Be[0]
        P1Decision = Decision[0]
        with open(dec_path, 'w') as decision:
            decision.write(str(P1Decision))
            decision.close()
        extortionist1.responses.append(P1Decision)



# Reading Decisions when playing alone
def read_alone(phase, counter):
    pool_text = visual.TextStim(win, text='Pool: ' + str(pool_money), height=30, pos=[0, 185])
    offer_text = visual.TextStim(win, text='Offer:', height=30, pos=[0, 135])
    ask_accept = visual.TextStim(win, text='Accept: a', height=50, pos=[-130, -150], color=[0, 255, 0])
    ask_reject = visual.TextStim(win, text='Reject: r', height=50, pos=[130, -150], color=[1, -1, -1])
    offer_he = visual.TextStim(win, text='They get: ' + str(calc_he_gets()), height=30, pos=[-130, 50])
    offer_you = visual.TextStim(win, text='You get: ' + str(Offers[0]), height=30, pos=[130, 50])
    single_accepted = visual.TextStim(win, text='You accepted the offer.\n\n' + 'You receive ' + str(Offers[0]) + ' points', height=30, color=[0, 255, 0])
    single_rejected = visual.TextStim(win, text='You rejected the offer.\n\n' + 'No one receives anything', height=30, color=[1, -1, -1])
    time_over = visual.TextStim(win, text='Your time is over - random decision', height=30, pos=[0, 0])
    rand_num = random.randrange(1, 11)
    accepted_keys = ['a', 'r']
    timer_text = visual.TextStim(win, text='2:00', height=50, pos=[0, -50])
    timeDecision = time.time_ns()

    index = 0
    timer = core.CountdownTimer(decisionTimer)
    makedicts('Round_TimeC', 0)
    makedicts('Global_TimeC', 0)
    makedicts('TimeStamp', 0)
    if Offers[0] != 0:
        while timer.getTime() > 0:
            pool_text.draw()
            offer_text.draw()
            offer_he.draw()
            offer_you.draw()
            ask_accept.draw()
            ask_reject.draw()
            timer_text.text = '{:0>2d}:{:0>2d}'.format(int(timer.getTime() // 60), int(timer.getTime() % 60))  # Timer
            timer_text.draw()
            win.flip()
            kb.getKeys(clear=True)
            keys = kb.getKeys(accepted_keys, waitRelease=False, clear=True)
            if timer.getTime() <= 0:
                makedicts('TimeStamp', get_time())
                time_over.draw()
                win.flip()
                core.wait(3)
                if rand_num <= 5:
                    single_accepted.draw()
                    Readers.append(['a', 'a'])
                    Accumulated.append(int(Offers[0]))
                    Decisions.append(['a_rand', 0])
                    rand_decision = 'a_rand'
                if rand_num > 5:
                    single_rejected.draw()
                    Readers.append(['r', 'r'])
                    Accumulated.append(int(0))
                    Decisions.append(['r_rand', 0])
                    rand_decision = 'r_rand'
                write(rand_decision)
                DecisionDict = tuple(Decisions)
                makedicts('Decision', DecisionDict)
                makedicts('Round_TimeDecision', 0)
                makedicts('Global_TimeDecision', get_time())
                sendDecision()
                win.flip()
                core.wait(2.0)
                break
            if len(keys) > 0:
                pressedKey = keys[0].name
                timeLocal = time_ms(timeDecision)
                #timeLocal = int(timer.getTime())
                Decisions.append([pressedKey, timeLocal])
                DecisionDict = tuple(Decisions)
                makedicts('Decision', DecisionDict)
                makedicts('Round_TimeDecision', timeLocal)
                makedicts('Global_TimeDecision', get_time())
                if pressedKey == 'a':
                    single_accepted.draw()
                    win.flip()
                    Readers.append(['a', 'a'])
                    Accumulated.append(int(Offers[0]))
                    core.wait(2.0)
                if pressedKey == 'r':
                    single_rejected.draw()
                    win.flip()
                    Readers.append(['r', 'r'])
                    Accumulated.append(int(0))
                    core.wait(2.0)
                sendDecision()
                if phase == 0:
                    if counter == 1:
                        makedicts('Accumulated', 0)
                    if counter > 1:
                        makedicts('Accumulated', Accumulated[-1])
                if phase == 2:
                    makedicts('Accumulated', Accumulated[-1])
                break

#Displaying offer and choice options + reading and matching choice with partner
def read():
    # Prepare text for the offer stimuli
    pool_text = visual.TextStim(win, text='Pool: ' + str(pool_money), height=30, pos=[0, 185])
    offer_text = visual.TextStim(win, text='Offer:', height=30, pos=[0, 135])
    ask_accept = visual.TextStim(win, text='Accept: a', height=50, pos=[-130, -150], color=[0, 255, 0])
    ask_reject = visual.TextStim(win, text='Reject: r', height=50, pos=[130, -150], color=[1, -1, -1])
    offer_he = visual.TextStim(win, text='They get: ' + str(calc_he_gets()), height=30, pos=[-130, 50])
    offer_you = visual.TextStim(win, text='You get: ' + str(Offers[0]), height=30, pos=[130, 50])
    one_rejected = visual.TextStim(win, text='You have rejected. \n\n Waiting for partner', height=30,
                                   color=[1, -1, -1])
    one_accepted = visual.TextStim(win, text='You have accepted. \n\n Waiting for partner', height=30,
                                   color=[0, 255, 0])
    you_rejected = visual.TextStim(win, text='YOU have rejected', height=30, pos=[0, -50], color=[1, -1, -1])
    you_accepted = visual.TextStim(win, text='YOU have accepted', height=30, pos=[0, -50], color=[0, 255, 0])
    partner_rejected = visual.TextStim(win, text='Your PARTNER has rejected', height=30, pos=[0, 50], color=[1, -1, -1])
    partner_accepted = visual.TextStim(win, text='Your PARTNER has accepted', height=30, pos=[0, 50], color=[0, 255, 0])
    rejected = visual.TextStim(win, text='Your TEAM rejected the offer.\n\n' + 'No one receives anything', height=30,
                               color=[1, -1, -1])
    accepted = visual.TextStim(win, text='Your TEAM accepted the offer.\n\n' + 'You receive ' + str(Offers[0]) + ' points', height=30, color=[0, 255, 0])
    no_unanimous = visual.TextStim(win, text='Decision not unanimous. Random decision', height=30, pos=[0, -50])
    partner_failed = visual.TextStim(win,
                                     text='Your partner failed to make a decision in time.\n\n' + 'Random decision',
                                     height=30)
    time_over = visual.TextStim(win, text='Your time is over - random decision', height=30, pos=[0, 0])
    rand_num = random.randrange(1, 11)
    accepted_keys = ['a','r']
    dot_timer = core.CountdownTimer(1.0)
    dot_index = 0
    waiting_signal_accept = visual.TextStim(win, text='.', height = 50, pos=[0,-150], color=[0, 255, 0])
    waiting_signal_reject = visual.TextStim(win, text='.', height = 50, pos=[0,-150], color=[1, -1, -1])
    timer_text = visual.TextStim(win, text='2:00', height=50, pos=[0, -50])
    timeDecision = time.time_ns()

    index = 0
    timer = core.CountdownTimer(decisionTimer)
    if Offers[0] != 0:
        while True:
            if index == 1:
                with open(coPath, "w") as p2res: #empty coPath at index == 1 for JD
                    pass
                makedicts('Accumulated', Accumulated[-1])
                break
            while timer.getTime() > 0:
                if index > 0:
                    break
                pool_text.draw()
                offer_text.draw()
                offer_he.draw()
                offer_you.draw()
                ask_accept.draw()
                ask_reject.draw()
                timer_text.text = '{:0>2d}:{:0>2d}'.format(int(timer.getTime() // 60), int(timer.getTime() % 60)) #Timer
                timer_text.draw()
                win.flip()
                kb.getKeys(clear=True)
                keys = kb.getKeys(accepted_keys, waitRelease=False, clear=True)
                #Timer for decision period --> if over: random decision
                if timer.getTime() <= 0:
                    makedicts('TimeStamp', get_time())
                    time_over.draw()
                    win.flip()
                    core.wait(3)
                    while True:
                        if os.path.getsize(coPath) > 0:
                            with open(coPath, 'r') as p2res:
                                P2 = p2res.read()
                            if P2:
                                if P2 == 'a_rand':
                                    accepted.draw()
                                    Readers.append(['a', 'a'])
                                    Decisions.append(['a_rand', 0])
                                    rand_decision = 'a_rand'
                                    Accumulated.append(int(Offers[0]))
                                if P2 == 'r_rand':
                                    rejected.draw()
                                    Readers.append(['r', 'r'])
                                    Decisions.append(['r_rand', 0])
                                    rand_decision = 'r_rand'
                                    Accumulated.append(int(0))
                            if not P2 or P2 == 'a' or P2 == 'r':
                                if rand_num <= 5:
                                    accepted.draw()
                                    Readers.append(['a', 'a'])
                                    Decisions.append(['a_rand', 0])
                                    rand_decision = 'a_rand'
                                    Accumulated.append(int(Offers[0]))
                                if rand_num > 5:
                                    rejected.draw()
                                    Readers.append(['r', 'r'])
                                    Decisions.append(['r_rand', 0])
                                    rand_decision = 'r_rand'
                                    Accumulated.append(int(0))
                        if os.path.getsize(coPath) == 0:
                            if rand_num <= 5:
                                accepted.draw()
                                Readers.append(['a', 'a'])
                                Decisions.append(['a_rand', 0])
                                rand_decision = 'a_rand'
                                Accumulated.append(int(Offers[0]))
                            if rand_num > 5:
                                rejected.draw()
                                Readers.append(['r', 'r'])
                                Decisions.append(['r_rand', 0])
                                rand_decision = 'r_rand'
                                Accumulated.append(int(0))
                        write(rand_decision)
                        DecisionDict = tuple(Decisions) #tuple(Decisions) only for JD
                        timeLocal = int(timer.getTime())
                        makedicts('Decision', DecisionDict)
                        makedicts('Round_TimeDecision', timeLocal)
                        makedicts('Global_TimeDecision', get_time())
                        sendDecision() ##ONLY for P1
                        win.flip()
                        core.wait(2)
                        index += 1  #index += 1 only for JD
                        break
                #Key press: display decision
                if len(keys) > 0:
                    pressedKey = keys[0].name
                    #timeLocal = int(timer.getTime())
                    timeLocal = time_ms(timeDecision)
                    Decisions.append([pressedKey, timeLocal])
                    DecisionDict = tuple(Decisions)
                    makedicts('Decision', DecisionDict)
                    makedicts('Round_TimeDecision', timeLocal)
                    makedicts('Global_TimeDecision', get_time())
                    if pressedKey == 'a':
                        one_accepted.draw()
                        win.flip()
                        core.wait(1.5)
                        write(pressedKey)
                    if pressedKey == 'r':
                        one_rejected.draw()
                        win.flip()
                        core.wait(1.5)
                        write(pressedKey)
                    #Periodically read if partner made a choice
                    while True:
                        if pressedKey == 'a':
                            one_accepted.draw()
                            waiting_signal_accept.draw()
                        if pressedKey == 'r':
                            one_rejected.draw()
                            waiting_signal_reject.draw()
                        win.flip()
                        if dot_timer.getTime() <= 0:
                            if pressedKey == 'a':
                                waiting_signal_accept.text += '.'
                            if pressedKey == 'r':
                                waiting_signal_reject.text += '.'
                            dot_timer.reset()
                            dot_index += 1
                            if dot_index == 3:
                                dot_index = 0
                                if pressedKey == 'a':
                                    waiting_signal_accept = visual.TextStim(win, text='.', height = 50, pos=[0,-150], color=[0,255,0])
                                if pressedKey == 'r':
                                    waiting_signal_reject = visual.TextStim(win, text='.', height = 50, pos=[0,-150], color=[1, -1, -1])
                        if os.path.getsize(coPath) > 0:
                            with open(coPath, 'r') as p2res:
                                P2 = p2res.read()
                            if P2 and not Readers:
                                if pressedKey == P2:
                                    index += 1 #index += 1 only for JD
                                    Readers.append([pressedKey, P2])
                                    makedicts('TimeStamp', 0)
                                    if pressedKey == 'a':
                                        you_accepted.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        you_accepted.draw()
                                        partner_accepted.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        accepted.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        sendDecision() ##ONLY for P1
                                        Accumulated.append(int(Offers[0]))
                                        makedicts('Accumulated', Accumulated[-1])
                                        break
                                    if pressedKey == 'r':
                                        you_rejected.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        you_rejected.draw()
                                        partner_rejected.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        rejected.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        sendDecision() ##ONLY for P1
                                        Accumulated.append(int(0))
                                        makedicts('Accumulated', Accumulated[-1])
                                        break
                                if pressedKey != P2:
                                    index += 1
                                    timeLocal=time_ms(timeDecision)
                                    if P2 == 'a_rand':
                                        partner_failed.draw()
                                        win.flip()
                                        core.wait(3.0)
                                        accepted.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        Readers.append(['a', 'a'])
                                        sendDecision()
                                        Readers.pop(0)
                                        with open(coPath, "w") as p2res:
                                            pass
                                        Decisions.pop(0)
                                        Accumulated.append(int(Offers[0]))
                                        break
                                    if P2 == 'r_rand':
                                        partner_failed.draw()
                                        win.flip()
                                        core.wait(3.0)
                                        rejected.draw()
                                        win.flip()
                                        core.wait(1.5)
                                        Readers.append(['r', 'r'])
                                        sendDecision()
                                        Readers.pop(0)
                                        with open(coPath, "w") as p2res:
                                            pass
                                        Decisions.pop(0)
                                        Accumulated.append(int(0))
                                        break
                                    if P2 == 'r':
                                        partner_rejected.draw()
                                        no_unanimous.draw()
                                        win.flip()
                                        core.wait(3.0)
                                        if rand_num <= 5:
                                            accepted.draw()
                                            Readers.append(['a', 'a'])
                                            Decisions.append(['a_rand', timeLocal])
                                            dis_decision = 'a_rand'
                                            Accumulated.append(int(Offers[0]))
                                        if rand_num > 5:
                                            rejected.draw()
                                            Readers.append(['r', 'r'])
                                            Decisions.append(['r_rand', timeLocal])
                                            dis_decision = 'r_rand'
                                            Accumulated.append(int(0))
                                        write(dis_decision)
                                        win.flip()
                                        DecisionDict = tuple(Decisions)
                                        makedicts('Decision', DecisionDict)
                                        makedicts('Global_TimeDecision', get_time())
                                        sendDecision()
                                        core.wait(2.0)
                                    if P2 == 'a':
                                        partner_accepted.draw()
                                        no_unanimous.draw()
                                        win.flip()
                                        core.wait(3.0)
                                        if rand_num <= 5:
                                            accepted.draw()
                                            Readers.append(['a', 'a'])
                                            Decisions.append(['a_rand', timeLocal])
                                            dis_decision = 'a_rand'
                                            Accumulated.append(int(Offers[0]))
                                        if rand_num > 5:
                                            rejected.draw()
                                            Readers.append(['r', 'r'])
                                            Decisions.append(['r_rand', timeLocal])
                                            dis_decision = 'r_rand'
                                            Accumulated.append(int(0))
                                        write(dis_decision)
                                        win.flip()
                                        DecisionDict = tuple(Decisions)
                                        makedicts('Decision', DecisionDict)
                                        makedicts('Global_TimeDecision', get_time())
                                        sendDecision()
                                        core.wait(2.0)
                                    if Readers:
                                        Readers.pop(0)
                                    break
                        else:
                            sleep(0.5)

def waitDiscussion():
    waitDiscussion = visual.TextStim(win, text='Please wait while your partner exits the discussion screen', height=25)
    finishedDiscussion = visual.TextStim(win, text='The discussion ended. \n\n Continuing', height=25)
    waiting_signal = visual.TextStim(win, text='.', height=50, pos=[0, -150])
    dot_timer = core.CountdownTimer(1.0)
    dot_index = 0

    with open(r_selfPath, 'w') as discussed:
        discussed.write('discussed1')
        discussed.close()
    while True:
        waitDiscussion.draw()
        waiting_signal.draw()
        win.flip()
        if dot_timer.getTime() <= 0:
            waiting_signal.text += '.'
            dot_timer.reset()
            dot_index += 1
            if dot_index == 3:
                dot_index = 0
                waiting_signal = visual.TextStim(win, text='.', height=50, pos=[0, -150])
        if os.path.getsize(r_coPath) > 0:
            try:
                with open(r_coPath, 'r') as partnerDiscussed:
                    finish = partnerDiscussed.read()
                    if finish == 'discussed2':
                        partnerDiscussed.close()
                        finishedDiscussion.draw()
                        win.flip()
                        with open(r_coPath, 'w') as partnerDiscussed:
                            pass
                        core.wait(1.5)
                        break
            except:
                sleep(0.2)

# Discussion period
def discuss():
    # Prepare text for the offer stimuli
    pool_text = visual.TextStim(win, text='Pool: ' + str(pool_money), height=30, pos=[0, 150])
    offer_text = visual.TextStim(win, text='Offer:', height=30, pos=[0, 100])
    offer_he = visual.TextStim(win, text='They get: ' + str(calc_he_gets()), height=30, pos=[-130, 15])
    offer_you = visual.TextStim(win, text='You get: ' + str(Offers[0]), height=30, pos=[130, 15])
    #click_here = visual.TextStim(win, text='Click HERE AND PRESS SPACE to stop the discussion', height=25, pos=[0, -150])
    #arrow = visual.TextStim(win, text=u'\u2190', height=200, pos=[0, 250])
    #whatsApp = visual.TextStim(win, text='Click on the left window to use the chat', height=25, pos=[0, 300])
    accepted_keys = ['space']
    timer_text = visual.TextStim(win, text='2:00', height=50, pos=[0, -100])
    pressSpace = visual.TextStim(win, text='Press SPACE to exit the discussion', height=30, pos=[0, -200])
    discussion = visual.TextStim(win, text='DISCUSSION', height=70, pos=[0, 300])
    timeDiscuss = time.time_ns()

    timer = core.CountdownTimer(discussTimer)
    if Offers[0] != 0:
        while timer.getTime() > 0:
            discussion.draw()
            pool_text.draw()
            offer_text.draw()
            offer_he.draw()
            offer_you.draw()
            #click_here.draw()
            #whatsApp.draw()
            #arrow.draw()
            timer_text.text = '{:0>2d}:{:0>2d}'.format(int(timer.getTime() // 60), int(timer.getTime() % 60))  # Timer
            timer_text.draw()
            pressSpace.draw()
            win.flip()
            keys = event.getKeys()
            if 'space' in keys:  # Press SPACE if you wish to make a decision before the time for discussing runs out - if timer runs out just reject the offer by default?
                #timeLocal = int(timer.getTime())
                timeLocal = time_ms(timeDiscuss)
                makedicts('Round_TimeC', timeLocal)  # append the timestamp for the C-button press into the data dictionary
                makedicts('Global_TimeC', get_time())
                waitDiscussion()
                read()  #read() here only JD
                break
            if timer.getTime() <= 0:
                makedicts('TimeStamp', get_time())
                waitDiscussion()
                read() #read() here only JD
                break

#Display transition from test run to real experiment
def experiment_start(phase):
    exp_start = visual.TextStim(win, text='The test run has ended. \n\n The real experiment will start now.', height=30)
    exp_start.draw()
    win.flip()
    if Accumulated:
        if phase == 0:
            Accumulated.pop(0)
        if phase == 1:
            Accumulated.pop(base_trials) #there are x elements in the list before phase 1 starts and the x+1 element that is appended in the test of phase 1 has the index of base_trials because the first of bas_trials+1 was popped above

#Announce next trial
def next_trial():
    next_round = visual.TextStim(win, text='The next round is about to start...', height=30)
    next_round.draw()
    win.flip()

#Announce last trial
def last_trial(phase):
    if count > base_trials:
        accumulated = sum(Accumulated)
        if phase == 0:
            bye = visual.TextStim(win, text='You have accumulated ' + str(
                accumulated) + ' points in this phase.\n\n' + 'You will now play together.' + ' Please wait for the instructions',
                                  height=30)
    if count_1 > num_trials:
        accumulated = sum(Accumulated[-num_trials:])
        if phase == 1:
            bye = visual.TextStim(win, text='Your team has accumulated ' + str(
                accumulated) + ' points.\n\n' + 'You will now play alone again.\n\n' + 'Please wait for the instructions',
                                  height=30)
    if count_2 == base_trials:
        accumulated = sum(Accumulated)
        if phase == 2:
            bye = visual.TextStim(win, text='You have accumulated ' + str(accumulated) + ' points in total. \n\n The game is now over. \n\n' + 'Please wait for the next task.',height=30)
    bye.draw()
    win.flip()
    if phase == 2:
        Accumulated.clear()

#Empty lists and files for each trial
def empty_lists():
    lists = [Readers, Offers]
    for i in lists:
        if len(i) != 0:
            i.pop(0)
    Decisions.clear()
    with open(coPath, "w") as p2res:
        pass

def waitPartner():
    wait_partner = visual.TextStim(win, text='The others are still playing.' + '\n\n Please wait while they are finishing their game', height=25)
    finished = visual.TextStim(win, text='Everybody is finished. \n\n Please wait for the instructions', height=25)
    waiting_signal = visual.TextStim(win, text='.', height=50, pos=[0, -150])
    dot_timer = core.CountdownTimer(1.0)
    dot_index = 0

    with open(r_selfPath, 'w') as fi:
        fi.write('yes1')
        fi.close()
    while True:
        wait_partner.draw()
        waiting_signal.draw()
        win.flip()
        if dot_timer.getTime() <= 0:
            waiting_signal.text += '.'
            dot_timer.reset()
            dot_index += 1
            if dot_index == 3:
                dot_index = 0
                waiting_signal = visual.TextStim(win, text='.', height = 50, pos=[0,-150])
        if os.path.getsize(r_coPath) > 0:
            try:
                with open(r_coPath, 'r') as ready:
                    finish = ready.read()
                    if finish == 'yes2':
                        ready.close()
                        finished.draw()
                        win.flip()
                        with open(r_coPath, 'w') as ready:
                            pass
                        core.wait(1.0)
                        break
            except:
                sleep(0.5)

##After the experiment:
def participant_numbers(command):
    #Reading the file
    with open(part_file, "r+") as file:
        lines = file.readlines()
        if not lines:
            last_row = 0 #If the file is empty start from 0
        if lines:
            last_row = lines[-1]
        #Extracting the number from the last row
        if last_row == 0:
            current_number = 1
            if command == 1:
                file.write("Participant_1\n")
                print("Participant_1")
            else:
                print('Only Dyad Number')
        else:
            last_number = int(last_row.split("_")[1].strip())
            current_number = last_number + 1
            ###only P1 to write the Participant number in the file###
            if command == 1:
                file.write(f"Participant_{current_number}\n")
                return (current_number)
            else:
                #print('returns number?')
                #print('current number:', current_number)
                return (current_number)

## Start trials
count = 0
count_1 = 0
count_2 = 0
start(0)
trial_data=[]

for trial in range(base_trials+1):
  finished = visual.TextStim(win, text='The first phase is over now. \n\n You will now play as a team', height=30)
  round_startTime = time.time()
  count += 1
  draw_initial(0)
  readoffer(0) #Only with phase for Player 2
  read_alone(0, count)
  core.wait(1.5)
  makedicts('Phase',0)
  #dyadNumber = participant_numbers(0)
  #print('dyadNumber:', dyadNumber)
  makedicts('Dyad', participant_numbers(0))
  makedicts('0', 0)   #print the dictionary for control
  trial_data.append({'Trial':f'Trial_{count}', **dataDict})
  if count == 1:
      experiment_start(0)
      core.wait(3.0)
      empty_lists()
  if 1 < count < base_trials+1:
      empty_lists()
  if count == base_trials+1:
      last_trial(0)
      core.wait(4.0)
      empty_lists()
      with open (offer_path) as deletebeforeJoint:
          pass
      extortionist1.previous_offer = None
      waitPartner()

#roleRandomizer(win, roles)
win.close()
win_pos = (win_width, 0)
win = visual.Window(size=(win_width, win_height), screen=1, fullscr=False, allowGUI=True, units='pix',
                    color='black', pos=win_pos)
start(1)
openWhatsApp(WhatsAppPath)
for trial in range(num_trials+1):
    round_startTime = time.time()
    count_1 += 1
    draw_initial(1)
    readoffer(1) #Only with phase for Player 2
    discuss() #discuss() here only for JD
    # pool_money -= int(you_get[0])  ####This is in case that the Pool money should not stay the same - although I think it would be better it does####
    core.wait(1.5)
    makedicts('Phase', 1)
    makedicts('0', 0)  # print the dictionary for control
    makedicts('Dyad', participant_numbers(0))
    trial_data.append({'Trial': f'Trial_{count_1}', **dataDict})
    if count_1 == 1:
        experiment_start(1)
        core.wait(3.0)
        empty_lists()
    if 1 < count_1 < num_trials + 1:
        empty_lists()
    if count_1 == num_trials + 1:
        last_trial(1)
        core.wait(4.0)
        empty_lists()
        extortionist1.previous_offer = None
        closeWhatsApp()

win.close()
win_pos = (0, 0)
win = visual.Window(size=(screen_width, screen_height), screen=1, fullscr=False, allowGUI=True, units='pix',
                    color='black', pos=win_pos)
start(2)
for trial in range(base_trials):
    finished = visual.TextStim(win,
                               text='The game is now over. \n\n' + 'Please wait for the next task.',
                               height=30)
    round_startTime = time.time()
    count_2 += 1
    draw_initial(2)
    readoffer(2) #Only with phase for Player 2
    read_alone(2, count_2)
    core.wait(1.5)
    makedicts('Phase', 2)
    makedicts('0', 0)  # print the dictionary for control
    makedicts('Dyad', participant_numbers(0))
    trial_data.append({'Trial': f'Trial_{count_2}', **dataDict})
    if 0 < count_2 < base_trials:
        empty_lists()
    if count_2 == base_trials:
        last_trial(2)
        core.wait(5.0)
        empty_lists()
        extortionist1.previous_offer = None
        ###NO NEED TO WAIT FOR PARTNER ANYMORE RIGHT?###
        #with open(r_selfPath, 'w') as ready:
        #    ready.write('yes1')
        #if os.path.getsize(r_coPath) > 0:
        #    try:
        #        with open(r_coPath, 'r') as ready:
        #            finish = ready.read()
        #            if finish == 'yes2':
        #                ready.close()
        #                finished.draw()
        #                win.flip()
        #                with open(r_coPath, 'w') as ready:
        #                    pass
        #                core.wait(1.0)
        #                break
        #    except:
        #        sleep(0.2)



result_df = pd.DataFrame(trial_data).set_index('Trial')
with pd.ExcelWriter('JD_P1.xlsx', engine='openpyxl',mode='a') as writer: #Excel name JD_P1 for JD_P1
    result_df.to_excel(writer, sheet_name=f"Participant_{participant_numbers(1)}")

experiment_done += 1

if experiment_done == 1:
    win.close()
    print("Experiment done")
    import HEXACO_P1
    def hexaco():
        HEXACO_P1.participant_number()
        HEXACO_P1.get_empty_col()
        HEXACO_P1.welcome()
        HEXACO_P1.save_workbook()
        HEXACO_P1.bye()
        HEXACO_P1.close_workbook()
        HEXACO_P1.thank_you()
    hexaco()
win.close()
core.quit()