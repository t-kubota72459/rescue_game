import RPi.GPIO as GPIO
import random
import game
import time

class Field:
    # 近接センサー
    POS = { 'A':17, 'B':22, 'C':27 }
    INV_POS = { v:k for k, v in POS.items() }

    # 赤外センサー
    IR = { 'A':13, 'B':26, 'C':6 }
    INV_IR = { v:k for k, v in IR.items() }

    # 光電センサー
    PHOTO = {'START':4, 'GOAL':9 }
    INV_PHOTO = { v:k for k, v in PHOTO.items() }

    def __init__(self, queue):
        """ Initializing sensors on the field. """
        GPIO.setmode(GPIO.BCM)
        for _ in self.POS.values():
            GPIO.setup(_, GPIO.IN)

        for _ in self.IR.values():
            GPIO.setup(_, GPIO.IN)

        for _ in self.PHOTO.values():
            GPIO.setup(_, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        ##
        ## トリガー検出後、2 秒間は反応を抑制する
        ##
        GPIO.add_event_detect(self.IR['A'], GPIO.FALLING, callback=self.mycallback, bouncetime=2000)
        GPIO.add_event_detect(self.IR['B'], GPIO.FALLING, callback=self.mycallback, bouncetime=2000)
        GPIO.add_event_detect(self.IR['C'], GPIO.FALLING, callback=self.mycallback, bouncetime=2000)

        self.life = 'A'
        self.queue = queue

    def measure5ms(self, channel):
        start_time = time.perf_counter()
        upto_time = start_time + 0.005  ## low signal keeps for 5ms
        while GPIO.input(channel) == 0:
            if upto_time < time.perf_counter():
                return True
            time.sleep(1e-3)
        return False

    def mycallback(self, channel):
        if self.measure5ms(channel):
            if self.need_help(channel):
                self.queue.put( (Field.INV_IR[channel], True) )
            else:
                self.queue.put( (Field.INV_IR[channel], False) )

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

if __name__ == '__main__':
    import time
    GPIO.cleanup()
    g = game.Game()
    while True:
        print("game is ready?:", g.is_ready())
        time.sleep(1)
