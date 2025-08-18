from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch,multitask,run_task

#Clear Console
# print("\x1b[H\x1b[2J", end="")

# https://docs.pybricks.com/_/downloads/en/v3.3.0/pdf/
# REFERENCE MOVEMENTS FOR CURVE. parameter 1st is radius, 2nd angle
# drive_base.curve(120, 360)   # Drives Clockwise Fwd (forward right side)
# drive_base.curve(-120, 360)   # Drives CounterClockwise in Rev (reverse right)
# drive_base.curve(120, -360)  # Drives Counterclockwise Fwd (forward left)
# drive_base.curve(-120, -360)  # Drives Clockwise in Rev (reverse left)
#  Run attachment motors until its stalled.Parameter:1st angle, 2nd torque
# R_attach.run_until_stalled(-1000, duty_limit=50)

# Set up all devices. The left side is the name of the devices. Change it as per your needs
Sparky = PrimeHub()
L_color = ColorSensor(Port.E)
R_color = ColorSensor(Port.F)
L_drive = Motor(Port.C, Direction.COUNTERCLOCKWISE)
R_drive = Motor(Port.D, Direction.CLOCKWISE)
drive_base = DriveBase(L_drive, R_drive, 62.4, 115)
R_attach = Motor(Port.B, Direction.COUNTERCLOCKWISE)
L_attach = Motor(Port.A, Direction.CLOCKWISE)
Sparky.speaker.volume(20)
#Timers for specific mission timing (specific mission timing), swap timing (between missions) and total time
missiontime = StopWatch()
swaptime = StopWatch()
totaltime = StopWatch()
#Menu hub display and selection program
# Initialize variables.
ACTIVEPROGRAM = 0
#Program list is alpha numeric. Modidy and change the list as needed. Make sure the "Main loop/interface that allows for selecting and launching programs" in the very end matches the alpha numeric list below.

PROGRAM_LIST = ['1','2','3','4','5','6','7','W','C']

#Functions to select the next/prior programs
def prior_program(active, prog_list):
    "Selects the prior program"
    active = (active - 1) % len(prog_list)
    return active
def next_program(active, prog_list):

    "Selects the next program"
    active = (active + 1) % len(prog_list)
    return active
def wait_for_color(desired_color,dist):
    # While the color is not the desired color, we keep moving.
    drive_base.reset()
    while not (L_color.color() == desired_color or drive_base.distance() == dist):
        drive_base.drive(200, 0)
        wait(20)
#Main programs are defined below
#you can define as many def programs as needed. You just need to call out the programs you need in the Main loop/interface at the end of the program (# Main loop/interface that allows for selecting and launching programs). 

def Geared_Collection():
    # 18.3 seconds (no squid, all krills (except one near trident), sea bed, plakton, water sample, all corals)
    #squid takes +5 seconds with crab cage mission.
    #start with collect attachment all the way UP
    drive_base.settings(straight_speed=1000)
    drive_base.settings(turn_rate=150)
    drive_base.use_gyro(True)
    # Get to the first krill and coral
    await drive_base.curve(760,-20)
    #Collect the first krill and coral
    await drive_base.straight(200)
    #Second 2nd krill and curve towards plankton
    await drive_base.curve(200,75)
    #Run the gear collect and turn to collect the plankton
    await multitask(drive_base.turn(20),L_attach.run_angle(5000,-890))
    #curve away from plankton
    await drive_base.curve(-85,120)
    #Curve left towards left home
    await multitask(drive_base.curve(350,-45),L_attach.run_angle(5000,445))
    # Drop the seabed arm and drive straight towards seabed sample
    await multitask(drive_base.straight(410),R_attach.run_angle(200,-250),L_attach.run_angle(5000,-445)) #old 390
    #Turn to collect seabed
    drive_base.settings(turn_rate=100)
    await drive_base.turn(65)
    #Straight to collect seabed
    await drive_base.straight(70)
    #Lift seabed sample
    await R_attach.run_angle(200,250)
    #Turn towards water sample
    await drive_base.turn(-62) #old 65
    #Drive towards water sample and lift collect arm
    await multitask(drive_base.straight(290),L_attach.run_angle(5000,890))
    # First turn towards water sample
    await drive_base.turn(-15)
    # Drives straight to collect the water sample and the krill
    await drive_base.straight(290) #Old:290  2. 310 3.290 4. 270
    # Turns towards the the last coral
    await drive_base.turn(-52) #old:-70
    # Does a curve towards the home area
    await drive_base.straight(200)
    await drive_base.curve(500,60) #old 500,80
    # Comes back for easily attachment takeoff
    # await drive_base.straight(-150)
    # await drive_base.turn(45)
    drive_base.use_gyro(False)
def left_Coraltree_diver_shark():
    # The main program starts here.
    # Align at 2nd line
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=1000)
    drive_base.settings(turn_rate=150)
    #Move a litte forward before turning
    #this can maybe change to 15 if the lift axle keeps getting caught
    await drive_base.straight(20)
    #turn slightly away from home
    await drive_base.turn(21)
    # drive straight halfway between kraken and diver
    await drive_base.straight(640)
    #turn towards diver
    await drive_base.turn(-109) #old -111
    await L_attach.run_angle(1000,270)
    # right for passive push for coral bud, shark release and diver pick
    drive_base.reset()
    await drive_base.straight(150)
    print('Distance',drive_base.distance())
    await multitask(L_attach.run_angle(500, -200),R_attach.run_until_stalled(1000, duty_limit=50))
    await L_attach.run_angle(1000, -150) #-130
    wait(500)
    await L_attach.run_angle(500,150)
    drive_base.settings(straight_speed=150)
    await drive_base.straight(-40)#old -45
    await drive_base.curve(-85,-94)
    drive_base.settings(straight_speed=300)
    await drive_base.straight(230) #Old:220
    await R_attach.run_until_stalled(-1000, duty_limit=50)
    wait(500)
    drive_base.settings(straight_speed=1000)
    #come back home backwards fast
    await drive_base.straight(-50)
    await drive_base.turn(20)
    await drive_base.straight(-720)
    drive_base.use_gyro(False)
def left_side_treasure():
    # Align at 2nd line
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=350)
    drive_base.settings(turn_rate=150)
    #drive straight towards coral tree
    await drive_base.straight(165) #old 215
    #curve and face kraken
    await drive_base.curve(340,92) #old radius:300 #old angle 95
    drive_base.settings(straight_speed=80) #old: 100
    #move forward to lift sunken ship and collect treasure
    await drive_base.straight(140) #old 180
    wait(500)
    # Comes back and turns towards home
    drive_base.settings(straight_speed=1000)
    await drive_base.straight(-90)
    # await drive_base.curve(-350,90)
    await drive_base.turn(-60)
    await drive_base.straight(-545)
    drive_base.use_gyro(False)
def left_side_trident_krill_collection():
    # Align at 2nd line
    ###TRIDENT MISSION###
    drive_base.use_gyro(True)
    #Adjust below speed or tweak distances for main bot to be consistent
    drive_base.settings(straight_speed=350)
    drive_base.settings(turn_rate=150)
    #Drive a little forward from home
    await drive_base.straight(85)
    #Turn and go right
    await drive_base.turn(80)
    await drive_base.straight(550)#560
    #turn left to face misson model
    await drive_base.turn(-37)
    #drive straight into mission model
    #the rubber pieces should push the trident
    #lower drive speed if its not consistent
    await drive_base.straight(280)#270
    #lower attachment. gears might slip, its ok.
    # await L_attach.run_angle(1000,2900)
    #wait 0.5 second so the rubber piece is fully holding the trident
    #wait(1000)
    #pull the trident vertically up
    await L_attach.run_angle(1000,-2900)
    #come back slightly to pull out the funnel beams
    await drive_base.straight(-80)
    #turn to collect krill
    await drive_base.turn(-40)
    #krill somtimes is moved around, so need to move straight a bit
    await drive_base.straight(40)
    #turn towards home and collect krill
    await drive_base.turn(-40)
    drive_base.settings(straight_speed=500)
    await drive_base.straight(-100)
    await drive_base.turn(-60)
    #go home fast
    await drive_base.straight(800)
    drive_base.use_gyro(False)
def left_side_Vessel_latch_drop_samples():
    # Start Program here:
    #On Program three
    #Nikhil
    #the first bold line from the left 
    #not covering the bottom line
    #(dropper)2nd thin line from the 3rdbold line on the right
    # The main program starts here
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=500)
    drive_base.settings(turn_rate=150)
    #Drive to knock samples into ship
    drive_base.straight(270) #Old:280
    # wait(500)
    drive_base.settings(straight_speed=350)
    #drive to drop arm into the ship ring
    drive_base.straight(170) #old 200
    R_attach.run_angle(500,270)
    drive_base.settings(straight_speed=350)
    #drive towars crab cage and stop slightly after crab cage base
    drive_base.straight(420)#390
    #Turn left slighty to straighten the bot
    drive_base.turn(-7) #old-5
    # #Drive straight to get close to the latch
    drive_base.straight(360) #Old:240
    drive_base.straight(-100)
    R_attach.run_angle(500,-270)
    # wait(500)
    drive_base.settings(straight_speed=500)
    drive_base.straight(400)
    drive_base.turn(20)
    drive_base.straight(300)
    drive_base.use_gyro(False)
def right_side_crab():
    drive_base.settings(straight_speed=1000)
    drive_base.settings(turn_rate=150)
    drive_base.use_gyro(True)
    #The first three commands will get you to the mission 
    drive_base.straight(120)
    drive_base.turn(-90)
    drive_base.straight(330)
    # Flips crab in position
    L_attach.run_angle(5000,-140)
    L_attach.run_angle(5000,140)
    # Comes back to lower flipper
    drive_base.straight(-65)#Old:50 and then 60
    R_attach.run_angle(1000,-440)
    # Goes forward to flip Crab to get 40 pts
    drive_base.straight(90)#Old:90 andthen 100
    R_attach.run_angle(1100,440)
    #reversing home before squid
    drive_base.straight(-330)
    #turn towards squid
    drive_base.turn(-135)
    #pushes squid mission
    drive_base.straight(-385)
    # Goes home
    drive_base.settings(straight_speed=1000)
    drive_base.straight(545)
    drive_base.use_gyro(False)
def right_side_boat_whale_sonar():
    #Program settings
    drive_base.settings(straight_speed=500)#Old:300
    drive_base.settings(turn_rate=100)
    drive_base.use_gyro(True)
    Sparky.imu.reset_heading(0)
    L_attach.reset_angle(0)
    # Drives towards Boat mission
    drive_base.straight(375)#Old:350
    drive_base.turn(-45)
    drive_base.straight(105)
    #Uses async function for consistensy 
    async def main():
        drive_base.settings(straight_speed=200) #Old:200
        await multitask(drive_base.straight(-100), R_attach.run_angle(200,-170))#Old:-150
    run_task(main())
    #Drives and curves towards Whale mission
    drive_base.straight(-200)
    R_attach.run_angle(1000, 359)
    drive_base.settings(straight_speed=500)#Old:300
    drive_base.straight(410) #Old:420
    drive_base.curve(90, 90)
    # Completes mission
    drive_base.straight(270)
    wait(1000)
    drive_base.straight(-300)
    #Comes back and turns towards the Sonar mission
    drive_base.turn(-42)#Old:-80
    drive_base.settings(turn_rate=150)
    drive_base.straight(150)
    drive_base.turn(-14)
    #Performing Sonar mission
    L_attach.run_time(1000,1200) #Rotates one full rotation on sonar
    L_attach.run_angle(1000,-180) #This moves axle away from sonar verticals
    wait(500)
    #Drives home
    drive_base.straight(-400) #Old:800
    drive_base.turn(-25)
    drive_base.straight(-400)
    drive_base.use_gyro(False) 
def right_coral_reef():
    drive_base.settings(straight_speed=50)
    drive_base.settings(turn_rate=150)
    drive_base.use_gyro(True)
    # Goes forward and comes back
    drive_base.straight(80) #old 40
    drive_base.settings(straight_speed=300)
    drive_base.straight(-80)
    drive_base.use_gyro(False)
def sub_angler_shark_squid():
    #Program settings
    drive_base.settings(straight_speed=500)
    drive_base.settings(turn_rate=100)
    drive_base.use_gyro(True)
    Sparky.imu.reset_heading(0)
    # Drives toward shark drop off
    drive_base.curve(100,-62)
    drive_base.settings(straight_speed=500)
    #Drop off shark and corals
    drive_base.straight(730)
    drive_base.settings(straight_speed=200)
    # Comes back and turns towards Submersible
    drive_base.straight(-110) #Old:-80
    drive_base.turn(39)#Old:50
    # Goes towards mission and lowers collection attachment
    async def main():
        drive_base.settings(straight_speed=350)
        await multitask(drive_base.straight(420), L_attach.run_until_stalled(-100000,duty_limit=50))
        # Lifts both attachments to gain more points
        await multitask(R_attach.run_angle(500,720), L_attach.run_until_stalled(100000,duty_limit=50))
    print('Time before angler:', totaltime.time())
    run_task(main())
    # wait(2000)
    # Comes back and turns towards Angler
    drive_base.straight(-120)
    drive_base.turn(-65)
    # Finish mission
    drive_base.straight(130)
    drive_base.straight(-120)
    # Turns robot on squid cricle
    drive_base.turn(-20)
    drive_base.use_gyro(False)

#set the stop button to the bluetooth for emergency stop in middle of  run
Sparky.system.set_stop_button(Button.BLUETOOTH)
# Main loop/interface that allows for selecting and launching programs
while True:
    # Display the active program
    Sparky.display.char(PROGRAM_LIST[ACTIVEPROGRAM])
    # Turn the light green
    Sparky.light.on(Color.GREEN)
    if Button.LEFT in Sparky.buttons.pressed():
        # The left button goes back to the previous program
        ACTIVEPROGRAM = prior_program(ACTIVEPROGRAM, PROGRAM_LIST)
        Sparky.speaker.beep(500, 200)
    elif Button.RIGHT in Sparky.buttons.pressed():
        # The right button advances to the next program
        ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        Sparky.speaker.beep(500,200)
    elif Button.CENTER in Sparky.buttons.pressed():
        # The center button launches the currently selected program
        # Note you can also have this be the bluetooth button/other buttons do this as well
        if '1' in PROGRAM_LIST[ACTIVEPROGRAM]:
            missiontime.reset()
            totaltime.reset()
            run_task(Geared_Collection())
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            print('Total Time:',totaltime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '2' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            run_task(left_Coraltree_diver_shark())
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            print('Total Time:',totaltime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '3' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            run_task(left_side_treasure())
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            print('Total Time:',totaltime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '4' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            run_task(left_side_trident_krill_collection())
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '5' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            left_side_Vessel_latch_drop_samples()
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '6' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            right_side_crab()
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif '7' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            right_side_boat_whale_sonar()
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif 'C' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            right_coral_reef()
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            print('Total Time:', totaltime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        elif 'W' in PROGRAM_LIST[ACTIVEPROGRAM]:
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'swap time:', swaptime.time())
            missiontime.reset()
            sub_angler_shark_squid()
            print('program Number:',PROGRAM_LIST[ACTIVEPROGRAM],'mission time:',missiontime.time())
            print('Total Time:', totaltime.time())
            swaptime.reset()
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        else:
            pass
    else:
        wait(10)


