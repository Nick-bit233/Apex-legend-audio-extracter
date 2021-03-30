import os
import re
import logging
from logging import handlers
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import *
from form import Ui_Form


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


class mainForm(QWidget):
    def __init__(self):
        # 调用父类构造函数，初始化空窗口
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)

        # 设置类成员
        self.qList = []
        # 日志对象
        self.log = Logger('debug.log', level='debug')

        # 设置信号
        self.ui.toolButton_gamePos.clicked.connect(self.open_file_game)
        self.ui.toolButton_savePos.clicked.connect(self.open_file_txtsave)
        self.ui.pushButton_scan.clicked.connect(self.on_scan)
        self.ui.pushButton_opentxt.clicked.connect(self.open_txtlist)
        self.ui.pushButton_readtxt.clicked.connect(self.read_txtlist)
        self.ui.pushButton_index.clicked.connect(self.index_search)
        self.ui.pushButton_down.clicked.connect(self.download_mes)

        self.ui.lineEdit_audioPath.textChanged.connect(self.on_audiopath_changed)

        self.ui.comboBox_legend.currentIndexChanged.connect(self.legend_chosen)
        self.ui.pushButton_diag.clicked.connect(self.search_diag)
        self.ui.pushButton_effect.clicked.connect(self.search_effect)
        self.ui.commandLinkButton.clicked.connect(self.about)

    # 获得音源列表txt文件所在地址
    def get_txtPos(self):
        gamePos = self.ui.lineEdit_gamePath.text()
        txtPos = self.ui.lineEdit_savePath.text()
        if txtPos == "":
            txtPos = gamePos + "/miles_audio/audio_list.txt"
        else:
            if txtPos[-1] == '/':
                txtPos = txtPos + "audio_list.txt"
            else:
                txtPos = txtPos + "/audio_list.txt"
        return txtPos

    # 点击扫描按钮，调用MSD获得音频列表，写入txt文件
    def on_scan(self):
        try:
            self.ui.listWidget.clear()

            gamePos = self.ui.lineEdit_gamePath.text()
            print(gamePos)
            headPos = gamePos[0:2]
            txtPos = self.get_txtPos()
            print(headPos, txtPos)
            audioPos = self.ui.lineEdit_audioPath.text()

            if not os.path.isfile(gamePos + "\\MSD.exe"):
                QMessageBox.critical(self, "错误", "请检查MSD.exe文件是否在相应目录下")
                return

            cmdMSD = ""
            if audioPos != "":
                audioPos = '.' + audioPos
                cmdMSD = ''' %s & cd "%s" & .\\msd --folder=%s 0 & .\\msd  --folder=%s -l > "%s" ''' \
                         % (headPos, gamePos, audioPos, audioPos, txtPos)
            else:
                cmdMSD = ''' %s & cd "%s" & .\\msd 0 & .\\msd -l > "%s" ''' % (headPos, gamePos, txtPos)
            print(cmdMSD)
            self.log.logger.info(cmdMSD)
            q = os.popen(cmdMSD)
            q.close()
            cnt = 0
            with open(txtPos, 'r') as flist:
                for cnt, _ in enumerate(flist):
                    pass
            cnt += 1
            self.ui.label_nAudio.setText(str(cnt))
            self.ui.spinBox.setMaximum(cnt - 1)

            self.ui.pushButton_opentxt.setEnabled(True)
            self.ui.pushButton_readtxt.setEnabled(True)

        except Exception as e:
            print(e)
            self.log.logger.error(e)
            QMessageBox.critical(self, "错误", "请确认路径参数正确后重试！", QMessageBox.Close)

    # 从txt文件中读取音频名称，展示到列表中,并初始化搜索框
    def read_txtlist(self):
        txtPos = self.get_txtPos()

        # 获得所有音频名称的列表
        with open(txtPos, 'r') as flist:
            for line in flist:
                self.qList.append(line)
        self.ui.listWidget.addItems(self.qList)

        # 连接信号：双击调用MSD播放音频
        self.ui.listWidget.itemDoubleClicked.connect(self.play_one_aduio)

        # 启用查找按钮
        self.ui.pushButton_index.setEnabled(True)
        self.ui.pushButton_diag.setEnabled(True)
        self.ui.pushButton_effect.setEnabled(True)
        self.ui.pushButton_down.setEnabled(True)

        self.init_diag_combo()

        # 防止重复读取，读取后禁用按钮
        self.ui.pushButton_readtxt.setEnabled(False)

    # 按照序号搜索
    def index_search(self):
        # 获得数字框的数字
        id = int(self.ui.spinBox.text())

        # 清除列表中的所有项目，再加入新项目
        self.ui.listWidget.clear()
        self.ui.listWidget.addItem(self.qList[id])

        # 允许重新读取整个列表
        self.ui.pushButton_readtxt.setEnabled(True)

    # 打开选择文件夹窗口
    def open_file_game(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", ".")
        print(filepath)
        self.ui.lineEdit_gamePath.setText(filepath)

    def open_file_txtsave(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", ".")
        print(filepath)
        self.ui.lineEdit_savePath.setText(filepath)

    # 用默认程序打开txt文件
    def open_txtlist(self):
        gamePos = self.ui.lineEdit_gamePath.text()
        txt = self.ui.lineEdit_savePath.text()
        if txt == "":
            txt = gamePos + "\\miles_audio"
        head = txt[0:2]
        command = '''%s & \
        cd %s & \
        start .\\audio_list.txt
        ''' % (head, txt)
        try:
            p_res = os.popen(command)
            print(p_res.read())
        except Exception as e:
            print(e)

    # 播放一次音频（会将wav文件存储到默认音频目录）
    def play_one_aduio(self):
        thread = Thread(target=self.playThreadFunc)
        thread.start()

    def playThreadFunc(self):
        try:
            gamePos = self.ui.lineEdit_gamePath.text()
            headPos = gamePos[0:2]
            item = self.ui.listWidget.selectedItems()[0]
            id = item.text().split(',')[0]
            print(id)

            audioPos = self.ui.lineEdit_audioPath.text()
            cmdMSD = ""
            if audioPos != "":
                audioPos = '.' + audioPos
                cmdMSD = '''%s & \
                cd %s & \
                .\\msd --folder=%s %s
                ''' % (headPos, gamePos, audioPos, id)
            else:
                cmdMSD = '''%s & \
                cd %s & \
                .\\msd %s
                ''' % (headPos, gamePos, id)
            p_res = os.popen(cmdMSD)
            print(p_res.read())
        except Exception as e:
            print(e)
            self.log.logger.error(e)

    def download_mes(self):
        thread = Thread(target=self.DownThreadFunc)
        thread.start()

    # 另存音频到指定地址
    def DownThreadFunc(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择保存文件路径", ".")
        print(filepath)
        try:
            gamePos = self.ui.lineEdit_gamePath.text()
            headPos = gamePos[0:2]
            item = self.ui.listWidget.selectedItems()[0]
            id = item.text().split(',')[0]
            print(id)

            audioPos = self.ui.lineEdit_audioPath.text()
            cmdMSD = ""
            if audioPos != "":
                audioPos = '.' + audioPos
                cmdMSD = '''%s & \
                cd %s & \
                .\\msd -m --folder=%s --out=%s %s
                ''' % (headPos, gamePos, audioPos, filepath, id)
            else:
                cmdMSD = '''%s & \
                cd %s & \
                .\\msd -m --out=%s %s
                ''' % (headPos, gamePos, filepath, id)
            p_res = os.popen(cmdMSD)
            if p_res.read() != "":
                os.popen("start %s" % filepath)
        except Exception as e:
            print(e)
            self.log.logger.error(e)

    def on_audiopath_changed(self):
        self.ui.pushButton_readtxt.setEnabled(False)
        self.ui.pushButton_index.setEnabled(False)
        self.ui.pushButton_diag.setEnabled(False)
        self.ui.pushButton_effect.setEnabled(False)
        self.ui.pushButton_down.setEnabled(False)

    def init_diag_combo(self):
        legendList = []
        for each in self.qList:
            # print(each)
            result = re.search(r"[0-9]+,diag_(ap|mp)_([a-zA-Z]{4,})_", each)
            if result is not None:
                l = result.group(2)
                # print(each, l)
                if l not in legendList:
                    legendList.append(l)
        self.ui.comboBox_legend.addItems(legendList)

    def legend_chosen(self):
        actionList = []
        self.ui.comboBox_action.clear()
        legend = self.ui.comboBox_legend.currentText()
        for each in self.qList:
            # print(each)
            result = re.search(r"[0-9]+,diag_(ap|mp)_%s_([a-zA-Z]+)_" % legend, each)
            if result is not None:
                l = result.group(2)
                print(each, l)
                if l not in actionList:
                    actionList.append(l)
        actionList.append("[None]")
        self.ui.comboBox_action.addItems(actionList)

    def search_diag(self):
        legend = self.ui.comboBox_legend.currentText()
        action = self.ui.comboBox_action.currentText()
        key = self.ui.lineEdit_diag.text()
        items = []
        result = ""
        for each in self.qList:
            if action == "[None]":
                result = re.search(r"([0-9]+),diag_(ap|mp)_%s_.*%s.*" % (legend, key), each, flags=re.IGNORECASE)
            else:
                result = re.search(r"([0-9]+),diag_(ap|mp)_%s_%s_.*%s.*" % (legend, action, key), each,
                                   flags=re.IGNORECASE)
            if result is not None:
                id = int(result.group(1))
                if id not in items:
                    items.append(self.qList[id])
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(items)
        # 允许重新读取整个列表
        self.ui.pushButton_readtxt.setEnabled(True)

    def search_effect(self):
        key = self.ui.lineEdit_effect.text()
        items = []
        for each in self.qList:
            result = re.search(r"([0-9]+),((?!diag).)*%s((?!diag).)*" % key, each, flags=re.IGNORECASE)
            if result is not None:
                id = int(result.group(1))
                if id not in items:
                    items.append(self.qList[id])
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(items)
        # 允许重新读取整个列表
        self.ui.pushButton_readtxt.setEnabled(True)

    def about(self):
        QMessageBox.about(self, "关于", "Apex 音频提取器v0.2 \n Github：Nick-bit233")


if __name__ == '__main__':
    app = QApplication([])
    wid = mainForm()
    wid.show()
    app.exec_()
