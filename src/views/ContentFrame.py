#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext

from src.custom.WorkTypeEnum import WorkType
from src.views.BaseFrame import BaseFrame


class ContentFrame(BaseFrame):
    def __init__(self, parent, root):
        super(ContentFrame, self).__init__(parent, root)
        self.root = root
        self.page_prev = ''
        self.page_next = ''
        self.page_title = ''
        self._init_ui()

    def _init_ui(self):
        self.title_lable = tk.Label(self, text='', font=self.font)
        self.title_lable.pack()
        self.scrt = scrolledtext.ScrolledText(self, font=self.font)
        self.scrt.pack(side=tk.LEFT, expand=tk.YES)
        self.scrt.tag_config("tag0", justify="left",background="#C7EDCC") # 护眼色

        # 绑定事件
        self.scrt.bind("<KeyPress-u>", self.page_prev_call)
        self.scrt.bind("<KeyPress-i>", self.page_next_call)
        pass

    def init_focus(self, url, rid):
        print(url)
        if self.scrt is not None:
            self.params['url'] = url
            self.params['element'] = ''
            self.params['call'] = self.set_content_txt
            self.params['type'] = WorkType.GET_CONTENT
            self.web_work(self.params)

    def set_content_txt(self, res):
        # 获取标题
        title = res.html.find('head title')[0].text
        # 获取内容
        content = res.html.find('div#nr1')[0].text

        if len(content) > 0:
            self.scrt.delete('1.0', tk.END)
            self.scrt.focus_set()
            # self.scrt.config(state=tk.NORMAL)

            # 获取分页链接
            self.page_prev = list(res.html.find('div.nr_page a#pb_prev')[0].absolute_links)[0]
            self.page_next = list(res.html.find('div.nr_page a#pb_next')[0].absolute_links)[0]

            # 标题
            self.page_title = title

            # print(self.page_prev, self.page_next)

            self.title_lable.config(text=title)
            self.scrt.insert(tk.INSERT,content,'tag0')

            self.scrt.mark_set(tk.INSERT, '0.1')
            self.scrt.see(tk.INSERT)
            # self.scrt.config(state=tk.DISABLED)

    def page_prev_call(self, event):
        # 更新url
        self.root.update_frame_url(self.page_prev)
        self.init_focus(self.page_prev,'')
        pass

    def page_next_call(self, event):
        self.root.update_frame_url(self.page_next)
        self.init_focus(self.page_next,'')
        pass

    def get_page_title(self):
        return self.page_title