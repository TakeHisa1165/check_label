import PySimpleGUI as sg
import datetime
import check_data
import stock_table
import csv
import w_csv
class Input_Windows:
    def __init__(self):
        self.lot_no_list = []
        self.now = datetime.datetime.today()
        self.now_year = self.now.year 
        self.now_month = self.now.month
        self.now_day = self.now.day
        self.str_day = "今日の日付:{}年{}月{}日".format(self.now_year, self.now_month, self.now_day)
        
        
        print(self.str_day)

        self.year_list = [self.now_year - 1, self.now_year, self.now_year + 1]
        self.month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.day_list = [i for i in range(1, 32)]

        self.cd = check_data.Check_Data()

    
    def main_window(self):
        sg.theme('systemdefault')

        frame1 = [
            [sg.Text('検査日を選んでください', font=('メイリオ', 14))],
            [sg.Listbox(self.year_list,size=(5,3),key="year", font=('メイリオ', 14)),sg.Text("年", font=('メイリオ', 14)), sg.Listbox(self.month_list, size=(5,3), key="month",font=('メイリオ', 14)),sg.Text("月", font=('メイリオ', 14)),
                                sg.Listbox(self.day_list, size=(5,3),key="day", font=('メイリオ', 14)),sg.Text("日", font=('メイリオ', 14)), sg.Submit(button_text='日付入力', font=('メイリオ', 14))],
            [sg.InputText('入力された日付を表示', key='-DATE-', font=('メイリオ', 14))],
            ]

        frame2 = [
            [sg.Submit(button_text='名前を付けて保存', font=('メイリオ', 14))]
        ]
        frame3 = [
            [sg.Submit(button_text='上書き保存', font=('メイリオ', 14))]
        ]
        frame4 = [
            [sg.Submit(button_text="在庫表へ", font=('メイリオ', 14))]
        ]


        layout = [
            [sg.MenuBar([["設定",["ファイル設定"]]], key="menu1",font=('メイリオ', 14))],
            [sg.Text(text=self.str_day, font=('メイリオ', 14))],
            [sg.Frame("検査日", frame1, font=('メイリオ', 14))],
            [sg.Text('QRコード読み込み欄', font=('メイリオ', 14))],
            [sg.Multiline(size=(100,5), key='QR'), sg.Submit(button_text="入力", font=('メイリオ', 14))],
            # [sg.Output(size=(100,5),  key='-LIST-') ],
            [sg.Submit("チェック", font=('メイリオ', 14)),sg.Submit('一覧をクリア', font=('メイリオ', 14))],
            [sg.Frame('上書き保存', frame3, font=('メイリオ', 14)), sg.Frame("名前を付けて保存", frame2, font=('メイリオ', 14)), sg.Frame('在庫表へ切り替え', frame4 ,font=('メイリオ', 14))]
            ]

        window = sg.Window('QRコード読み込み', layout)

        while True:
            event, values = window.read()
            if event is None:
                break

            if event == "入力":
                self.code_no = values["QR"]
                print(values["QR"])
                lot_numbesr = values["QR"]
                self.lot_no_list = lot_numbesr.splitlines()
                if self.lot_no_list[-1] == '':
                    self.lot_no_list.pop(-1)
                else:
                    pass
                self.cd.input_data(self.lot_no_list)
                

                # self.lot_no_list.append(self.code_no)

                # output window用
                # for lot in self.lot_no_list:
                #     print(lot)
                #     self.lot_no_list = []
 
            
            if event == "チェック":
                self.cd.check_lot()
                self.cd.count_qty()
                    

            if event == "一覧をクリア":
                self.lot_no_list.clear()
                # window['-LIST-'].update('')
                window['QR'].update('')
            
            if event == '日付入力':
                self.year = values["year"]
                self.month = values["month"]
                self.day = values["day"]
                self.today = "{}年{}月{}日".format(self.year[0], self.month[0], self.day[0])
                window['-DATE-'].update(self.today)
                self.cd.input_inspect_day(self.today)

            if event == "名前を付けて保存":
                self.cd.save_as_file()
            
            if event == "上書き保存":
                self.cd.save_file()

            if event == "在庫表へ":
                try:
                    a = Stock_Gui(today=self.today)
                    a.stock_gui()
                except AttributeError:
                    sg.popup_error('日付を入力してください')

            if values["menu1"] == "ファイル設定":
                Select_File()
                
        
        window.close()


class Stock_Gui:
    def __init__(self,today):
        self.today = today
        self.cd = check_data.Check_Data()
        

    def stock_gui(self):
        
        sg.theme('systemdefault')
        layout = [
            [sg.Text("在庫表へ転記", font=('メイリオ', 14))],
            [sg.Submit(button_text='入庫', font=('メイリオ', 14)), sg.Submit(button_text="出庫", font=('メイリオ', 14)) ],
        ]
        
        window = sg.Window("2ページめ", layout)

        while True:
            event, values = window.read()
            if event is None:
                print('終了')
                break

            if event == "入庫":
                self.cd.cal_qty_per_lot(event)
                lot_qty_dict = self.cd.lot_qty_dict
                self.st = stock_table.Stock_Table()
                self.st.input_date(today=self.today, lot_qty_dict=lot_qty_dict)
                print(event)

            if event == "出庫":
                self.cd.cal_qty_per_lot(event)
                lot_qty_dict = self.cd.lot_qty_dict
                self.st = stock_table.Stock_Table()
                self.st.input_date(today=self.today, lot_qty_dict=lot_qty_dict)
  
        window.close()


class Select_File:
    def __init__(self):
        self.path_dict = self.select_file()
        
    def select_file(self):

        sg.theme('SystemDefault')

        layout = [
            [sg.Text('ラベルチェック用ファイルを選んでください', size=(50, 1), font=('メイリオ', 14))], 
            [sg.InputText(font=('メイリオ', 14)),sg.FilesBrowse('開く', key='File1', font=('メイリオ', 14))],
            [sg.Text('入出庫管理ファイルを選んでください', size=(50, 1), font=('メイリオ', 14))], 
            [sg.InputText(font=('メイリオ', 14)),sg.FilesBrowse('開く', font=('メイリオ', 14))],
            [sg.Submit(button_text='設定', font=('メイリオ', 14)), sg.Submit(button_text="閉じる", font=('メイリオ', 14))]
        ]

        # セクション 2 - ウィンドウの生成z
        window = sg.Window('ファイル選択', layout)

        # セクション 3 - イベントループ
        while True:
            event, values = window.read()

            if event is None:
                print('exit')
                break

            if event == '設定':
                path_dict = {}
                label_check_path = values[0]
                path_dict["label_check_path"] = label_check_path
                stock_path = values[1]
                path_dict["stock_path"] = stock_path
                csv = w_csv.Write_csv()
                csv.write_csv(path_dict=path_dict)
                
               
                return path_dict
            
            if event == '閉じる':
                break




        #  セクション 4 - ウィンドウの破棄と終了
        window.close()

if __name__ == "__main__":
    a = Input_Windows()
    a.main_window()
