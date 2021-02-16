#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,platform

class Util(object):
    def __init__(self):
        super(Util, self).__init__()

    @staticmethod
    def get_screen_center(tk):
        x = (tk.winfo_screenwidth() - tk.winfo_width()) / 2
        y = (tk.winfo_screenheight() - tk.winfo_height()) / 2
        return x, y

    @staticmethod
    def get_screen_pos(tk):
        return tk.winfo_x(), tk.winfo_y()

    @staticmethod
    def project_root_path(project_name=None):
        """
        获取当前项目根路径
        :param project_name:
        :return: 根路径
        """
        if Util.get_platform() == 'Windows':
            PROJECT_NAME = 'tkReader' if project_name is None else project_name
            project_path = os.path.abspath(os.path.dirname(__file__))
            root_path = project_path[:project_path.find("{}\\".format(PROJECT_NAME)) + len("{}\\".format(PROJECT_NAME))]
            # print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))
            return root_path.replace('\\', '/')
        else:
            return '/home/cpi/games/Python/tkReader/'

    @staticmethod
    def get_seconds(time):
        h = int(time[0:2])
        # print("时：" + str(h))
        m = int(time[3:5])
        # print("分：" + str(m))
        s = int(time[6:8])
        # print("秒：" + str(s))
        ms = int(time[9:12])
        # print("毫秒：" + str(ms))
        ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
        return ts

    @staticmethod
    def get_platform():
        return platform.system()
