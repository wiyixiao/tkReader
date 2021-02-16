#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk

from src.custom.IniWr import IniWr
from src.custom.WorkTypeEnum import WorkType
from src.views.BaseFrame import BaseFrame
from src.views.PagesEnum import Pages


class BookMarkFrame(BaseFrame):
    def __init__(self, parent, root):
        super(BookMarkFrame, self).__init__(parent, root)
        self.root = root
        self.books = None
        self.urls = []  # 记录书签链接地址
        self._init_ui()

    def _init_ui(self):
        self.title_lable = tk.Label(self, text='书签', font=self.font)
        self.title_lable.pack()
        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.sb.set)
        self.listbox.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=2)
        self.sb.config(command=self.listbox.yview)

        self.listbox.bind("<KeyPress-u>", self.book_del)
        self.listbox.bind("<KeyPress-j>", self.open_url)

    def init_focus(self, url, rid):
        self.listbox.focus_set()
        self.listbox.delete(0, tk.END)
        self.listbox.select_set(0)
        self.urls.clear()

        self.thread_pool.run(self.set_book_list, (1,), None)

    def set_book_list(self, n):
        self.books = self.conf.read_val('BookMarks')
        if self.books is not None:
            for option in self.books:
                self.listbox.insert(tk.END, option)
                self.urls.append(self.books[option])

        self.listbox.select_set(0)
        # print(self.urls)
        print('书签加载完成')

    def open_url(self, event):
        try:
            index = self.listbox.curselection()[0]
            url = self.urls[index]
            self.root.show_frame(Pages.CONTENT, url)
        except Exception as e:
            print(e)

    def book_del(self, event):
        try:
            option = self.listbox.selection_get()
            print(option)
            self.conf.del_option('BookMarks', option)
            # 删除成功，重新加载
            self.init_focus('','')
        except Exception as e:
            print(e)


