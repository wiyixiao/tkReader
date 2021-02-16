#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import time


from src.views.BaseFrame import BaseFrame

from src.custom.WorkTypeEnum import WorkType
from src.views.PagesEnum import Pages

LARGE_FONT = ("Verdana", 12)

# 主站目录
url = 'https://m.qb50.com/'


class HomeFrame(BaseFrame):
    def __init__(self, parent, root):
        super(HomeFrame, self).__init__(parent, root)
        self.root = root
        self.channel_links = []
        self._init_ui()

    def _init_ui(self):
        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.sb.set)
        self.listbox.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5)
        self.sb.config(command=self.listbox.yview)

        # 绑定分页切换事件
        self.listbox.bind("<KeyPress-j>", self.open_channel)

    def init_focus(self):
        if self.listbox is not None:
            self.listbox.focus_set()
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, 'loading ...')
            self.listbox.select_set(0)

            # 获取链接列表
            self.params['url'] = url
            self.params['element'] = 'div#submenu ul a'
            self.params['call'] = self.channel_list_set
            self.params['type'] = WorkType.GET_ELEMENT
            self.web_work(self.params)

    # 更新列表
    def channel_list_set(self, reslist):
        # 清空
        self.listbox.delete(0, tk.END)
        self.channel_links.clear()
        # 序号
        index = 0
        # 添加到列表
        for a in reslist:
            self.channel_links.append(list(a.absolute_links)[0])
            self.listbox.insert(tk.END, ("%s" % a.text))
            index+=1
        # 添加完本链接
        self.channel_links.append(url + '/full/1.html')
        self.listbox.insert(tk.END, '完本')

        self.listbox.select_set(0)

    def open_channel(self, event):
        pass
        select_index = self.listbox.curselection()[0] # 单选
        # 跳转至当前分类的列表页
        self.root.show_frame(Pages.CHANNEL, self.channel_links[select_index])





