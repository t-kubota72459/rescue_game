##
## motor_command.py
##
## ロボットを操作してゴールを決めろ！
##
## モーター動作命令関数
## モーターに左右・前進・後退の命令を出す
##
## Copyright (c) 2022 Hiroshima Politechnical College.
##

from microbit import *
from k_motor import KMotor

def rotate_left(r):
    """
    その場で 500 ms 左回転
    """
    r.motor_on(KMotor.MOTOR_1, KMotor.FORWARD, 90)
    r.motor_on(KMotor.MOTOR_2, KMotor.REVERSE, 90)
    sleep(500)
    r.motor_brake(KMotor.MOTOR_1)
    r.motor_brake(KMotor.MOTOR_2)


def rotate_right(r):
    """
    その場で 500 ms右回転
    """
    r.motor_on(KMotor.MOTOR_1, KMotor.REVERSE, 90)
    r.motor_on(KMotor.MOTOR_2, KMotor.FORWARD, 90)
    sleep(500)
    r.motor_brake(KMotor.MOTOR_1)
    r.motor_brake(KMotor.MOTOR_2)


def turn_left(r, direction, speed):
    """
    左に曲がる
    """
    r.motor_on(KMotor.MOTOR_1, direction, speed=speed)
    r.motor_on(KMotor.MOTOR_2, direction, speed=int(speed * 0.2))


def turn_right(r, direction, speed):
    """
    右に曲がる
    """
    r.motor_on(KMotor.MOTOR_1, direction, speed=int(speed * 0.2))
    r.motor_on(KMotor.MOTOR_2, direction, speed=speed)


def stop(r):
    """
    止まる
    """
    r.motor_brake(KMotor.MOTOR_1)
    r.motor_brake(KMotor.MOTOR_2)


def forward(r, speed):
    """
    前進
    """
    _run(r, KMotor.FORWARD, speed)


def reverse(r, speed):
    """
    後退
    """
    _run(r, KMotor.REVERSE, speed)


def _run(r, direction, speed):
    """
    指定方向に進む
    """
    r.motor_on(KMotor.MOTOR_1, direction, speed=speed)
    r.motor_on(KMotor.MOTOR_2, direction, speed=speed)
