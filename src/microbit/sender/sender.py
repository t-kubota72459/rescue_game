##
## sender.py
##
## ロボットを操作してゴールを決めろ！
##
## micro:bit 送信側プログラム
## ボタンの状態と加速度センサーの値を送信する
##
## Copyright (c) 2022 Hiroshima Politechnical Callege.
##

from microbit import *
import radio
import utime

##
## 初期設定
##
VERSION = "1.0"
CHANNEL = 1
DEBUG = False

def button_stats():
    """
    A, B ボタンの状態を文字列で返す関数
    """
    s = "B,N"
    if button_a.was_pressed() and button_b.is_pressed():   # A と B を押している
        s = "B,C"
    elif button_b.was_pressed() and button_a.is_pressed(): # A と B を押している
        s = "B,C"
    elif button_a.is_pressed() and button_b.is_pressed(): # A と B を押している        
        s = "B,C"
    elif button_a.is_pressed():  # A のみ押している
        s = "B,A"
    elif button_b.is_pressed():  # B のみ押している
        s = "B,B"
    utime.sleep_ms(50)
    return s

##
## メイン
##
uart.init(9600)
uart.write("**** SENDER {}****\r\n".format(VERSION))
uart.write("CHANNEL:{}\r\n".format(CHANNEL))

radio.config(channel=CHANNEL)
radio.on()

while True:
    bt = button_stats()                     # ボタンの状態を取得
    accl = accelerometer.get_values()       # X, Y, Z 軸方向の G を取得
    accl_msg = "A,{},{},{}".format(accl[0], accl[1], accl[2])

    radio.send(bt)
    radio.send(accl_msg)
    if DEBUG:
        uart.write("sending: ")
        uart.write("{},{},{},{}\r\n".format(bt, accl[0], accl[1], accl[2]))
    sleep(200)
