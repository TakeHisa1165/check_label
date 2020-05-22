# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
# リスト項目
itm = [1,2,3,' 文字列1','文字列2','文字列3' ,
[' 概ね',' どんな型でも',' 項目にできます']]
# レイアウト
layout = [[sg.Listbox(itm ,size =(35 ,7) ,
# default_values =[[’ 概ね’,’ どんな型でも’,’ 項目にできます’]] ,
# select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE
 ),
sg.Button('Check')]]
# ウィンドウ作成
window = sg.Window("psguiListbox01.py", layout)
# イベントループ
while True:
    event , values = window.read () # イベントの読み取り（ イベント待ち）
    print(itm) # 確認表示
    if event == None: # 終了条件（ None: クローズボタン）
        break
# 終了処理
window.close ()