#!/usr/bin/python3
# -*- coding: utf-8 -*-
###     version #0.3.0              ###
###     package by auto-py-to-exe   ###
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import time
import gzip
 
def un_gz(file_name):
    """ungz zip file"""
    f_name = file_name.replace(".gz", "")
    #获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    #创建gzip对象
    open(f_name, "wb+").write(g_file.read())
    #gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()
    #关闭gzip对象

class stdf2atdf(QWidget):
    stdf_input=""
    def __init__(self):
        super(stdf2atdf, self).__init__()
        # 窗口标题
        self.setWindowTitle('stdf2atdf')
        # 定义窗口大小
        self.resize(500, 200)
        self.QLabl = QLabel(self)
        self.QLabl.setGeometry(0, 100, 4000, 38)
        # 调用Drops方法
        self.setAcceptDrops(True)
        # 控制按钮
        button_open = QPushButton('Convert', self)
        button_open.clicked.connect(self.execute_conversion)
        button_open.move(300, 100)

        # button_close = QPushButton('Close', self)
        # button_close.clicked.connect(self.execute_close)
        # button_close.move(50, 100)

    def execute_conversion(self,evn):
        if self.stdf_input=="":
            # print('ERROR: empty stdf file')
            self.setWindowTitle('ERROR: Empty stdf file!') 
        else:
            input_file=self.stdf_input.split('\n')
            for single_file in input_file:
                if len(single_file)<11:
                    break
                single_file= single_file[8:] # remove the subfix "file:///"
                end_ext=single_file[-3:] # use for postfix judge if end with ".gz" will need to untar action
                if end_ext==".gz":
                    un_gz(single_file)
                    single_file=single_file[:-3]
                # print('stdf2atdf ongoing...')
                self.setWindowTitle('stdf2atdf ongoing...') 
                # time.sleep(0.5) 
                try:
                    subprocess.check_output("stdfatdf "+single_file+" "+single_file+".atdf",stderr=subprocess.STDOUT)
                except Exception as e: # subprocess.CalledProcessError as e:
                    QMessageBox.critical(self,'ERROR','ERROR in convertion'+str(e),QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                    self.setWindowTitle('ERROR: Convert Fail')
                    self.stdf_input=""
                else:
                    # self.assertEqual(verbose, b'',"Unexpected info-level messages in simple request")
                    self.setWindowTitle('Convert Done')
                    self.QLabl.setText('Output ATDF File：\n' + single_file+".atdf")
                    self.stdf_input=""
                    self.QLabl.setWordWrap(True)

        # cmd = 'bash say_hello.sh &'
        # print('cmd: {}'.format(cmd))
        # subprocess.call(cmd, shell=True)


    # def execute_close(self):
    #     for process in ['bash say_hello.sh']:
    #         for pid in get_pid(process):
    #             print("kill process {}".format(pid))
    #             subprocess.Popen("kill -9 {}".format(pid), shell=True)

    # 鼠标拖入事件
    def dragEnterEvent(self, evn):
        self.setWindowTitle('Loading...')
        
        self.QLabl.setText('Input STDF File：\n' + evn.mimeData().text())
        self.QLabl.setWordWrap(True)
        self.stdf_input = evn.mimeData().text()
        # 鼠标放开函数事件
        evn.accept()

    # 鼠标放开执行
    def dropEvent(self, evn):
        self.setWindowTitle('Loading Done')

    # def dragMoveEvent(self, evn):
    #     print('Waiting Loading')
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainSys = stdf2atdf()
    mainSys.show()
    sys.exit(app.exec_())
