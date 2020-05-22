import PySimpleGUI as sg
import check_data

#  セクション1 - オプションの設定と標準レイアウト

class Ui_window:
    def __init__(self):
        sg.popup_ok('確認ようファイルを開きます')

    def select_file(self):

        sg.theme('SystemDefault')

        layout = [
            [sg.Submit('スタート'), sg.Submit('保存'),], 
        ]

        # セクション 2 - ウィンドウの生成z
        window = sg.Window('ファイル選択', layout)

        # セクション 3 - イベントループ
        while True:
            event, values = window.read()

            if event is None:
                print('exit')
                break

            if event == 'スタート':
                a = check_data.Check_Data()
                a.check_lot()
            
            if event == '保存':
                file_save = check_data.Check_Data()
                file_save.save_file()
                




        #  セクション 4 - ウィンドウの破棄と終了
        window.close()



if __name__ == "__main__":
    a = Ui_window()
    a.select_file()
