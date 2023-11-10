#!/usr/bin/env python
##
## レスキューゲーム 
##
## Copyright (c) 2023, Hiroshima Prefectural Technical Junior College
##

import PySimpleGUI as sg
from enum import Enum
import time
import arduino
import repeater
import game
import visitor

##
## 状態遷移
##
class s: IDLE = 0; INIT = 1; READY = 2;  ACTIVE = 3; FIN_TIMEOVER = 4; FIN_SUCC = 5; FIN_FAIL = 6; ERROR = 7;

## ゲーム
game = game.Game()


## スコア記録
recode_list = []
best_recode = { "name": "",
                "time": 0 }

## 来場者記録ファイル
fn = "/home/takaya/repos/rescue_game/src/raspberrypi/visitor.txt"

## 画面デザイン
sg.theme('LightBlue')
tab1_layout = [
        [sg.Text('おなまえ：'), sg.Input(size=(15,1), key='-INPUT1-'), sg.Button("とうろく", key="-REGIST-"), sg.Button("スタート", key="-START-", disabled=True)],
        [sg.Text('', expand_x=True, key='-NAME-')],
        [sg.Frame("のこりじかん", [[sg.Push(), sg.T('00:00', font=("", 120), pad=(30, 30), key="-TEXT1-"), sg.Push()]], expand_x=True)],
        ]

tab2_layout = [
        [sg.Frame('最高スコア',
            [[sg.Text('なまえ', size=(20, 1)),     sg.Text(size = (8,1), key="-BEST-NAME-")],
             [sg.Text('救出タイム', size=(20, 1)), sg.Text(size = (8,1), key="-BEST-TIME-")]])],
        [sg.Text('_'*40)],
        [sg.Table([[" "*15, " "*15] for _ in range(5)], headings=["なまえ", "救出時間"], auto_size_columns=True, justification="left", key="-TABLE-")]
        ]

tab3_layout = [
        [sg.Text('生存者の場所', size=(20,1))],
        [sg.Text('_'*20, size=(20,1), key="-LIFE-")],
        [sg.Text('来場者', size=(20,1))],
        [sg.Text(str(visitor.read(fn)), size=(20,1), key="-VISITOR-")],
        ]

tab4_layout = [
        [sg.Push(), sg.Button('Vol Up',   button_color=('black', 'FloralWhite'), font=("", 32), size=(22, 1), key='-VOLUP-'), sg.Push()],
        [sg.Push(), sg.Button('Vol Down', button_color=('black', 'FloralWhite'), font=("", 32), size=(22, 1), key='-VOLDOWN-'), sg.Push()],
        [sg.Push(), sg.Button('Prev', button_color=('black', 'LemonChiffon'), font=("", 32), size=(10, 1), key='-PREV-'),
         sg.Button('Next', button_color=('black', 'LemonChiffon'), font=("", 32), size=(10, 1), key='-NEXT-'), sg.Push()],
        [sg.VPush() ],
        [sg.Push(), sg.Button('Stop',     button_color=('black', 'seashell'), font=("", 32), size=(22, 1), key='-STOP-'), sg.Push()]
        ]

# The TabgGroup layout - it must contain only Tabs
tab_group_layout = [[sg.Tab('レスキューゲーム', tab1_layout, key='-TAB1-', expand_x=True),
                     sg.Tab('スコア', tab2_layout, key='-TAB2-', expand_x=True),
					 sg.Tab('生存者ポジション', tab3_layout, key='-TAB3-'),
                     sg.Tab('サウンドテスト', tab4_layout, key='-TAB4-', expand_x=True) ]]

# The window layout - defines the entire window
layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')]]
window = sg.Window('レスキューゲーム！', layout, font=("", 24), no_titlebar=False, resizable=True, size=(1024,520))

def update_display(_min, _sec):
    window['-TEXT1-'].update(f'{"%02d" % int(_min)}:{"%02d" % int(_sec)}')

def init_display():
    if not game.is_ready():
        sg.popup_ok("セッティングを確認してください\n" + game.field.dump(), font=("", 16), no_titlebar=True, keep_on_top=True)
        return False

    window["-NAME-"].update( f'がんばれ！ {values["-INPUT1-"]}隊員！') 
    window['-TEXT1-'].update( f'{"%02d" % 2}:{"%02d" % 0}' )
    window['-START-'].update( disabled=False )
    return True

def sec2str(_):
    _min = _ // 60
    _sec = _ % 60
    return f"{_min}分 {_sec}秒"

def update_recode(remaining_time):
    global recode_list
    _ = {"name": values["-INPUT1-"], "time":120 - int(remaining_time)}
    recode_list.append( _ )
    recode_list = sorted(recode_list, key=lambda x:x["time"])[:10]
    window["-TABLE-"].update([[v["name"], sec2str(v["time"])] for v in recode_list])
    window["-BEST-NAME-"].update(recode_list[0]["name"])
    window["-BEST-TIME-"].update(sec2str(recode_list[0]["time"]))

##
## 初期状態
##
stat = s.IDLE
downcounter = 100 # 10 sec. till BGM starts (BGM までの時間)

while True:
    event, values = window.read(timeout=100)
    ## print(stat, event, values)

    ## 終了
    if event == sg.WIN_CLOSED:
        break

    if stat == s.IDLE or stat == s.INIT:
        if event == "-REGIST-":
            if init_display():
                game.set_life()
                window['-LIFE-'].update( f'{game.get_life()}' )
                stat = s.INIT
        elif event == "-VOLUP-":
            arduino.up()
        elif event == "-VOLDOWN-":
            arduino.down()
        elif event == "-PREV-":
            arduino.prev()
        elif event == "-NEXT-":
            arduino.next()
        elif event == "-STOP-":
            arduino.stop()
        elif event == "__TIMEOUT__":
            downcounter -= 1
            if downcounter <= 0 and not arduino.busy():
                arduino.play(6)
                downcounter = 100

    ##
    ## GAME START
    ##
    if stat == s.INIT:
        if event == "-START-":
            game.run()
            sg.popup("救助開始！\n", font=("", 32), auto_close=True, auto_close_duration=1, non_blocking=True, keep_on_top=True, button_type=5)
            stat = s.READY

    ##
    ## ROBO MOVE
    ##
    if stat == s.READY:
        end_time = time.time() + game.rescue_time
        if game.field.is_started(): ## Robo moved
            stat = s.ACTIVE

    ##
    ## PLAYING
    ##
    if stat == s.ACTIVE:
        remaining_time = end_time - time.time()
        _min, _sec = divmod(max(remaining_time, 0), 60)
        update_display(_min, _sec)

        (pos, alive) = game.search()
        if pos is not None:
            sg.popup(f'{pos} に生命反応 {alive}', font=("", 32), auto_close=True, auto_close_duration=3, non_blocking=True, no_titlebar=True, keep_on_top=True, button_type=5)

        if remaining_time <= 0:
            stat = s.FIN_TIMEOVER
        elif game.is_finished():
            if game.is_succeeded(): ## 救出成功
                stat = s.FIN_SUCC
            else:                   ## 救出失敗
                stat = s.FIN_FAIL

    ##
    ## TIME OVER
    ##
    if stat == s.FIN_TIMEOVER:
        game.over()
        sg.popup("ざんねん！！\nゲームオーバー！！\n", font=("", 32), auto_close=True, auto_close_duration=3, no_titlebar=True, keep_on_top=True, button_type=5)
        update_recode(max(remaining_time, 0))

    ##
    ## 救出成功
    ##
    if stat == s.FIN_SUCC:
        game.goal()
        sg.popup("ゲームクリア！！\nおめでとう！！\n", font=("", 32), auto_close=True, auto_close_duration=3, no_titlebar=True, keep_on_top=True, button_type=5)
        update_recode(max(remaining_time, 0))

    ##
    ## 救出失敗
    ##
    if stat == s.FIN_FAIL:
        game.nogoal()
        sg.popup("ざんねん\nもう一度トライしよう！！", font=("", 32), auto_close=True, auto_close_duration=3, no_titlebar=True, keep_on_top=True, button_type=5)

    ##
    ## 終了時の共通処理
    ##
    if stat in (s.FIN_TIMEOVER, s.FIN_SUCC, s.FIN_FAIL):
        window['-VISITOR-'].update(str(visitor.oneup(fn)))
        downcounter = 100
        stat = s.IDLE

repeater.cancel()
game.cleanup()
window.close()
