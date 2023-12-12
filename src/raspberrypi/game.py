import time
import field
import arduino
import queue

class Game:
    rescue_time = 120
    sound_table = { "A" : 7, "B" : 8, "C" : 9 }


    def __init__(self):
        self.queue = queue.Queue(1)
        self.field = field.Field(self.queue)
        self.field.set_life()

    def set_life(self):
        return self.field.set_life()

    def get_life(self):
        return self.field.life

    def is_ready(self):
        return self.field.is_ready()

    def is_finished(self):
        return self.field.is_finished()

    def is_succeeded(self):
        return self.field.is_succeeded()

    
    def is_hit(self, pos):
        print(pos)
        arduino.play(self.sound_table[pos])

    def is_missed(self, pos):
        print(pos)
        arduino.play(3)

    def run(self):
        arduino.play(1)

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
