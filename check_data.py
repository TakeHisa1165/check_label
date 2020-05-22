import xlwings as xw
import PySimpleGUI as sg
import sys
import stock_table
import r_csv


class Check_Data:
    def __init__(self):
        csv = r_csv.Read_csv()
        try:
            label_check_path, stock_path = csv.read_csv()
        except TypeError:
            sg.popup_ok('初期設定が完了しました。\nプログラムを終了します。\nソフトウェアを再起動してください。')
            sys.exit()

        self.path = label_check_path
        self.wb = xw.Book(self.path)
        self.ws = self.wb.sheets(1)
        self.st = stock_table.Stock_Table()
        

    def check_lot(self):
        self.max_row1 = self.ws.range(10000,5).end("up").row
        self.ws.range((5, 8), (self.max_row1 +1 , 8)).clear()
        for i in range(5, self.max_row1 + 1):
            lot_no1 = self.ws.range(i, 5).value
            self.ws.range(i, 8).value = "ロットNo.は{}桁です".format(len(str(lot_no1)))
            if len(str(lot_no1)) != 12:
                sg.popup_error('ロットNo.の桁数が間違っています。\nロットNo.を確認してください。')
                self.ws.range(i, 8).color = (255, 0, 0)
                break            
            else:
                pass
        sg.popup_ok('チェックが完了しました')


    def save_as_file(self):
        file_no = self.ws.range("C1").value
        file_name = "ラベル確認" + file_no + ".xlsx"
        self.wb.save("D:\\デスクトップ\\会社関係\\保管\\" + file_name)
        sg.popup_ok("終了します")
        sys.exit()

    def save_file(self):
        self.wb.save()
        sg.popup_ok('上書き保存しました')


    def count_qty(self):
        self.max_row1 = self.ws.range(10000,5).end("up").row
        qty = (self.max_row1 - 4)  * 120
        self.ws.range("I2").value = str(qty) + "個"
        self.ws.range("I2").color = (255, 255, 255)

    def input_data(self, lot_no_list):
        i = 5
        for lot in lot_no_list:
            if len(lot) == 102:
                self.ws.range(i, 2).value = lot[0:9]
                self.ws.range(i, 5).value = str(lot[66:77])
                self.ws.range(i, 6).value = str(lot[77:83])
                self.ws.range(i, 7).value = lot[95:98]
                i += 1

            else:
                sg.popup_error('{}枚目に、通常と異なるQRコードを読み込んでいます。\nバーコードを読み込んでいませんか？'
                                .format(i - 4))
                break
        self.wb.save()


    def input_inspect_day(self, day):
        self.ws.range("C1").value = day

    # ロット毎の数量を計算
    def cal_qty_per_lot(self, event):
        lot_list = []
        self.max_row1 = self.ws.range(10000,5).end("up").row
        for i in range(5, self.max_row1 + 1):
            lot = self.ws.range(i, 5).value
            lot_list.append(lot)
            set_lot_list = set(lot_list)
            lot_list = list(set_lot_list)
        
        
        self.lot_qty_dict = {}
        for lot in lot_list:
            result_qty = 0
            for i in range(5, self.max_row1 + 1):
                lot_no = self.ws.range(i, 5).value
                if lot_no == lot:
                    qty = self.ws.range(i, 7).value
                    result_qty = result_qty + qty
            self.lot_qty_dict.setdefault(lot, result_qty)
        
        if event == "入庫":
            self.st.input_arrival(self.lot_qty_dict)
        else:
            self.st.input_shiped(self.lot_qty_dict)



        


    




if __name__ == "__main__":
    a = Check_Data()
    a.check_lot()