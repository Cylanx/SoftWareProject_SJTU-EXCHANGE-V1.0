#Copyright by Cylanx
#This program designed to SJTU class SoftWare
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import time
import profile
import pickle
import os
import pstats

LOG_LINE_NUM = 0        #用于记录窗口操作记录的行数
ITEM_DICT = dict()      #用于本地保存数据，数据类型dict以便添加各种属性
file_path = os.path.join(os.path.dirname(__file__), 'Item_Data.txt')    #本地数据保存在根目录下的txt文件中
if os.path.exists(file_path):
    ITEM_DICT = pickle.load(open(file_path, 'rb'))

class MY_GUI():
    def __init__(self,init_window_name):
        global ITEM_DICT
        self.init_window_name = init_window_name
    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("物品交换EXCHANGE SJTU.V1.0")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.input_data_label = Label(self.init_window_name, text="物品名称")
        self.input_data_label.grid(row=0, column=0)
        self.output_data_label = Label(self.init_window_name, text="仓库物品列表")
        self.output_data_label.grid(row=0, column=12)

        self.input_info_label = Label(self.init_window_name, text="物品信息")
        self.input_info_label.grid(row=6, column=0)
        self.output_info_label = Label(self.init_window_name, text="仓库物品信息")
        self.output_info_label.grid(row=9, column=12)

        self.log_label = Label(self.init_window_name, text="操作记录")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.input_data_Text = Text(self.init_window_name, width=65, height=18)  #原始数据录入框
        self.input_data_Text.grid(row=1, column=0, rowspan=5, columnspan=10)
        self.output_data_Text = Text(self.init_window_name, width=65, height=23)  #处理结果展示
        self.output_data_Text.grid(row=1, column=12, rowspan=8, columnspan=10)

        self.input_info_Text = Text(self.init_window_name, width=65, height=18)  #原始数据录入框
        self.input_info_Text.grid(row=7, column=0, rowspan=5, columnspan=10)
        self.output_info_Text = Text(self.init_window_name, width=65, height=23)  #处理结果展示
        self.output_info_Text.grid(row=10, column=12, rowspan=8, columnspan=10)

        self.log_data_Text = Text(self.init_window_name, width=65, height=9)  # 日志框
        self.log_data_Text.grid(row=14, column=0, columnspan=10)
        #按钮,点击之后调用相应函数
        self.add_button = Button(self.init_window_name, text="添加物品", bg="lightblue", width=10,command=self.add_item)  # 调用内部方法  加()为直接调用
        self.add_button.grid(row=1, column=11)

        self.del_button = Button(self.init_window_name, text="删除物品", bg="lightblue", width=10,command=self.delete_item)  # 调用内部方法  加()为直接调用
        self.del_button.grid(row=2, column=11)

        self.show_button = Button(self.init_window_name, text="显示物品", bg="lightblue", width=10,command=self.show_item)  # 调用内部方法  加()为直接调用
        self.show_button.grid(row=3, column=11)

        self.search_button = Button(self.init_window_name, text="查找物品", bg="lightblue", width=10,command=self.search_item)  # 调用内部方法  加()为直接调用
        self.search_button.grid(row=4, column=11)
    #功能函数

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)
    #添加物品子程序
    def add_item(self):
        item_name = self.input_data_Text.get(1.0, END).strip().replace("\n", "")
        item_info = self.input_info_Text.get(1.0, END).strip().replace("\n", "")
        ITEM_DICT[item_name]= item_info
        self.write_log_to_Text("INFO:Add success")
        self.input_data_Text.delete(1.0, END)
        self.output_data_Text.delete(1.0, END)
        self.input_info_Text.delete(1.0, END)
        self.output_info_Text.delete(1.0, END)
        self.save()
    #删除物品子程序
    def delete_item(self):
        item_name = self.input_data_Text.get(1.0, END).strip().replace("\n", "")
        del ITEM_DICT[item_name]
        self.write_log_to_Text("INFO:Del success")
        self.input_data_Text.delete(1.0, END)
        self.output_data_Text.delete(1.0, END)
        self.input_info_Text.delete(1.0, END)
        self.output_info_Text.delete(1.0, END)
        self.save()
    #展示物品子程序
    def show_item(self):
        self.output_data_Text.delete(1.0, END)
        self.output_info_Text.delete(1.0, END)
        self.output_data_Text.insert(1.0, ''.join(["|" + item_name + "|" for item_name in ITEM_DICT.keys()]))
    #搜索物品子程序
    def search_item(self):
        item_name = self.input_data_Text.get(1.0, END).strip().replace("\n", "")
        Finding = 1 if item_name in ITEM_DICT.keys() else -1
        self.input_data_Text.delete(1.0, END)
        if Finding==-1 :
            self.output_data_Text.delete(1.0, END)
            self.output_info_Text.delete(1.0, END)
            self.output_data_Text.insert(1.0, "None")
            self.write_log_to_Text("INFO:Cannot Find The Item")
        else :
            self.output_data_Text.delete(1.0, END)
            self.output_data_Text.insert(1.0, item_name)
            self.output_info_Text.delete(1.0, END)
            self.output_info_Text.insert(1.0, ITEM_DICT[item_name])
            self.write_log_to_Text("INFO:Successfully Find The Item")
    #存储数据到本地子程序
    def save(self):
        with open(file_path, 'wb') as f:
            pickle.dump(ITEM_DICT, f)
    #关闭窗口询问
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.init_window_name.destroy()

def gui_start():
    init_window = Tk()
    PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    PORTAL.set_init_window()
    init_window.protocol('WM_DELETE_WINDOW', PORTAL.on_closing)
    init_window.mainloop()

#以下为选择执行程序还是查看程序测试的统计数据
MODE = "exec"
if MODE == "test":
    profile.run("gui_start()",'mystats')
    p = pstats.Stats('mystats')
    p.strip_dirs().sort_stats(-1).print_stats()
elif MODE == "exec":
    gui_start()