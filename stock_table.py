import xlwings as xw
import check_data
import r_csv


class Stock_Table:
    def __init__(self):
        csv = r_csv.Read_csv()
        label_check_path, stock_path = csv.read_csv()

        self.path = stock_path
        self.wb = xw.Book(self.path)
        self.ws = self.wb.sheets(1)
       
    def input_date(self,today, lot_qty_dict):
        no_of_row = len(lot_qty_dict)
        self.max_row = self.ws.range(65536, 2).end('up').row
        self.ws.range((self.max_row + 1, 2), (self.max_row + no_of_row, 2)) .value = today
    
    def input_arrival(self, lot_qty_dict):
        max_row = self.ws.range(65536, 2).end('up').row
        i = max_row + 1
        for kye_lot in lot_qty_dict.keys():
            self.ws.range(i, 3).value = kye_lot
            i += 1
        i = max_row + 1
        for kye_value in lot_qty_dict.values():
            self.ws.range(i, 4).value = kye_value
            i += 1

    def input_shiped(self, lot_qty_dict):
        max_row = self.ws.range(65536, 2).end('up').row
        i = max_row + 1
        for kye_lot in lot_qty_dict.keys():
            self.ws.range(i, 5).value = kye_lot
            i += 1
        i = max_row + 1
        for kye_value in lot_qty_dict.values():
            self.ws.range(i, 6).value = kye_value
            i += 1
            









