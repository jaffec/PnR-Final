import pigo
import time  # import just in case students need
import datetime
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        self.start_time = datetime.datetime.utcnow()

        self.next_right = True

        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 106
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 20
        self.HARD_STOP_DIST = 30
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 136
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 138
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def switch_turn(self,enc):
        if self.next_right:
            self.encR(enc)
        else:
            self.encL(enc)
        self.next_right = not self.next_right




    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("test restore", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()


    # YOU DECIDE: How does your GoPiggy dance?

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        for distance in self.scan:
            if distance and distance < 200 and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > 200 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self): #Runs check looks around 360 degrees before moving
        self.servo(self.MIDPOINT)  # Looks straight ahead
        for x in range(4):
            if not self.is_clear():
                return False
            print("Check Distance")
            self.encR(8)
        print("Safe to dance!")
        return True

    def to_the_right(self):
        "subroutine of dance method"
        for x in range(3):
            self.servo(40)
            self.encR(5)
            self.encF(10)
            self.servo(40)
        print("--- Went to the right ---")

    def to_the_left(self):
        for x in range(3):
            self.servo(40)
            self.encL(7)
            self.encF(10)
        print("and then left...")

    def back_it_up(self):
        for x in range(3):
            self.servo(150)
            self.encB(10)
            self.encR(7)
            self.encL(7)
            self.encF(11)
            self.encB(11)
    def return_to_sender(self):
        for x in range(1):
            self.servo(50)
            self.servo(150)
            self.encR(5)
            self.encF(7)
        print("ad unknown, return to sender")
        print("--- Bringing it back ---")
        ####Will add shape on final project###
        #def square(self):
        #   for x in range(3):
        #      self.encF(18)
        #     self.encR(14)
        print("Now for some basic shapes")

    def restore(self):
        """
        Uses self.turn_track to reorient to original heading
        """
        print("Restoring Direction")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def test_restore_heading(self):
        self.encR(5)
        self.encL(15)
        self.encR(10)
        self.encR(10)
        self.encL(7)
        self.restore()

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print ("It took you %d seconds to run this" % difference)

        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.switch_turn(5)
                if not self.is_clear():
                    self.switch_turn(9)
                if not self.is_clear():
                    self.encB(5)
                    self.restore()



                  #check right and go right if clear

                    #look left 2 times and then go
    def smooth_turn(self):
        self.right_rot()
        start - datetime.datetime.utcnow()
        self.servo(self.MIDPOINT)
        while true:
            if self.dist() > 100:
                self.stop()
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds=10):
                self.stop()
            time.sleep(.2)


    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.1)
        self.stop()





def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
