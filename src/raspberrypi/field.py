import RPi.GPIO as GPIO
import random
import game

class Field:
    # 近接センサー
    POS = { 'A':17, 'B':22, 'C':27 }
    INV_POS = { v:k for k, v in POS.items() }

    # 赤外センサー
    IR = { 'A':11, 'B':5, 'C':0 }
    INV_IR = { v:k for k, v in IR.items() }

    # 光電センサー
    PHOTO = {'START':4, 'GOAL':9 }
    INV_PHOTO = { v:k for k, v in PHOTO.items() }

    def __init__(self, game):
        """ Initializing sensors on the field. """

        GPIO.setmode(GPIO.BCM)
        for v in self.POS.values():
            GPIO.setup(v, GPIO.IN)

        for v in self.IR.values():
            GPIO.setup(v, GPIO.IN)
        GPIO.add_event_detect(self.IR['A'], GPIO.FALLING, callback=game.help_A, bouncetime=3000)
        GPIO.add_event_detect(self.IR['B'], GPIO.FALLING, callback=game.help_B, bouncetime=3000)
        GPIO.add_event_detect(self.IR['C'], GPIO.FALLING, callback=game.help_C, bouncetime=3000)

        for v in self.PHOTO.values():
            GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        ## GPIO.add_event_detect(self.PHOTO['GOAL'], GPIO.FALLING, callback=game.goal, bouncetime=20000)
        ## GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=100)
        ## GPIO.add_event_detect(27, GPIO.FALLING, callback=my_callback, bouncetime=100)
        ## GPIO.add_event_detect(22, GPIO.FALLING, callback=my_callback, bouncetime=100)

        self.life = 'A'

    def set_life(self):
        self.life = random.sample(['A', 'B', 'C'], 1)[0]

    def get_life(self):
        return self.life

    def need_help(self, channel):
        return self.IR[self.life] == channel    ## 助けを要す

    def is_ready(self):
        """ exam field setting """
        # 近接センサー
        for v in self.POS.values():
            if GPIO.input( v ) == GPIO.HIGH:
                return False

        # 光電センサー
        if GPIO.input( self.PHOTO['START'] ) == GPIO.HIGH:  ## ロボが置かれていない
            return False

        if GPIO.input( self.PHOTO['GOAL'] ) == GPIO.LOW:    ## カプセルが残っている
            return False

        return True

    def is_started(self):
        """ triggerd start sensor """
        return GPIO.input( self.PHOTO['START'] ) == GPIO.HIGH

    def is_finished(self):
        """ triggerd goal sensor """
        return GPIO.input( self.PHOTO['GOAL'] ) == GPIO.LOW

    def is_succeeded(self):
        """ triggerd goal sensor """
        return GPIO.input( self.POS[self.life] ) == GPIO.HIGH

    def dump(self):
        s = ""
        s += "近接:" + str( [ GPIO.input(v) for v in self.POS.values() ] ) + "\n"
        s += "光電:" + str( [ GPIO.input(v) for v in self.PHOTO.values() ] )
        return s

    def cleanup(self):
        for v in self.IR.values():
            GPIO.remove_event_detect(v)
