import time
import field
import arduino

class Game:
    rescue_time = 120
    name_table = ["フィールドＡ", "フィールドＢ", "フィールドＣ"]

    def __init__(self):
        self.search_result = [0, 0, 0]
        self.field = field.Field(self)
        self.field.set_life()

    def set_life(self):
        return self.field.set_life()

    def get_life(self):
        return self.field.life

    def help_A(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger A")
        if self.field.need_help(channel):
            self.search_result[0] = 1
            arduino.play(7)
        else:
            self.search_result[0] = -1
            arduino.play(3)

    def help_B(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger B")
        if self.field.need_help(channel):
            self.search_result[1] = 1
            arduino.play(8)
        else:
            self.search_result[1] = -1
            arduino.play(3)

    def help_C(self, channel):
        ''' called from event trigger sensor'''
        print("caught trigger C")
        if self.field.need_help(channel):
            self.search_result[2] = 1
            arduino.play(9)
        else:
            self.search_result[2] = -1
            arduino.play(3)

    def is_ready(self):
        return self.field.is_ready()

    def is_finished(self):
        return self.field.is_finished()

    def is_succeeded(self):
        return self.field.is_succeeded()

    def search(self):
        # 生命反応なし
        try:
            pos = self.search_result.index(-1)
            self.search_result[pos] = 0
            s = ""
            for v in self.search_result:
                s += str(v) + ","
            print("game.search_result:" + s)
            return (self.name_table[pos], "なし")
        except ValueError:
            pass

        # 生命反応あり
        try:
            pos = self.search_result.index(1)
            self.search_result[pos] = 0
            s = ""
            for v in self.search_result:
                s += str(v) + ","
            print("game.search_result:" + s)
            return (self.name_table[pos], "あり！！")
        except ValueError:
            s = ""
            for v in self.search_result:
                s += str(v) + ","
            print("game.search_result:" + s)
            return (None, "")

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
        self.search_result = [0, 0, 0]
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
