import csv
import os
import gui_test
import PySimpleGUI as sg

class Read_csv:
    def __init__(self):
        pass

    def read_csv(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            with open('path.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    label_check_path = row["label_check_path"]
                    stock_path = row["stock_path"]
                    return label_check_path, stock_path
        except FileNotFoundError:
            sg.popup_ok('初期設定が必要です。\nラベルチェックファイルと入出庫ファイルを選んでください')
            gui_test.Select_File()
    
            

if __name__ == "__main__":
    a = Read_csv()
    a.read_csv()