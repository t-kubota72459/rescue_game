import time
import field
import arduino

class Game:
    rescue_time = 120

    def __init__(self):
        self.field = field.Field(self)
        self.field.set_life()

    def set_life(self):
        return self.field.set_life()

    def get_life(self):
        return self.field.life

    def help_A(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger")
        if self.field.need_help(channel):
            arduino.play(7)
        else:
            arduino.play(3)

    def help_B(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger")
        if self.field.need_help(channel):
            arduino.play(8)
        else:
            arduino.play(3)

    def help_C(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger")
        if self.field.need_help(channel):
            arduino.play(9)
        else:
            arduino.play(3)

    def is_ready(self):
        return self.field.is_ready()

    def is_finished(self):
        return self.field.is_finished()

    def is_succeeded(self):
        return self.field.is_succeeded()

    def run(self):
        arduino.play(1)

    ##def goal(self, channel):
    ##    ''' called from event trigger of sensor'''
    ##  print("caught goal trigger")
    ##  arduino.play(4)
    ##  while arduino.busy():
    ##      time.sleep(0.5)

    def goal(self):
        arduino.play(4)

    def nogoal(self):
        arduino.play(10)

    def over(self):
        arduino.play(5)
    
    def cleanup(self):
        self.field.cleanup()

if __name__ == '__main__':
    try:
        game = Game()
        print(game)
        while True:
            print(game.field.ready())
            game.field.dump()
            time.sleep(1)

    except KeyboardInterrupt:
        game.cleanup()
