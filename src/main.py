#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from src.utils.Util import Util
from src.custom.IniWr import IniWr
from src.views.FrameManager import FrameManager

# 配置文件管理器
import src.vars.GlobalManager as gm

# 配置文件路径
CONFIG_PATH = '../docs/conf.ini'

# 初始化全局变量
gm._init()
gm.set_value('conf', IniWr(CONFIG_PATH))

# 初始化界面
conf = gm.get_value('conf')
app = FrameManager(conf, False)


def run():
    app.mainloop()
