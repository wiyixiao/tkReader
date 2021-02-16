#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse

from src.custom.WorkTypeEnum import WorkType
from src.views.BaseFrame import BaseFrame

import tkinter as tk

import json
import math

from src.views.PagesEnum import Pages

# 请求接口地址
x_base_api = 'https://api.bilibili.com/x/web-interface/newlist?'


class ChannelFrame(BaseFrame):
    def __init__(self, parent, root):
        super(ChannelFrame, self).__init__(parent, root)
        self.listbox = None
        self.root = root
        self.content_list = []  # 存储小说列表或章节列表数据
        self.page_prev_link = ''
        self.page_next_link = ''
        self.page_article_url = ''
        self.page_chapters = False # 当前页面是否为章节目录页面
        self._init_ui()

    def _init_ui(self):
        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.sb.set)
        self.listbox.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5)
        self.sb.config(command=self.listbox.yview)

        self.page_label = tk.Label(self, text='', font=self.font)
        self.page_label.pack()

        # 绑定事件
        self.listbox.bind("<KeyPress-u>", self.page_prev)
        self.listbox.bind("<KeyPress-i>", self.page_next)
        self.listbox.bind("<KeyPress-j>", self.open_url)

    def init_focus(self, url, rid):
        if self.listbox is not None:
            self.listbox.focus_set()
            self.content_list.clear()
            self.listbox.delete(0, tk.END)
            self.listbox.select_set(0)
            self.page_prev_link = ''
            self.page_next_link = ''

            self.listbox.insert(tk.END, 'loading ...')

            print(url)

            if self.page_chapters == True:
                # 获取当前章节目录列表
                # print('get chapters list')
                self.params['url'] = url
                self.params['element'] = 'div.lb_mulu ul a'
                self.params['call'] = self.set_chapters_list
                self.params['type'] = WorkType.GET_ELEMENT
                self.web_work(self.params)
            else:
                # 获取当前分类小说列表
                # print('get article list')
                self.page_article_url = url
                self.params['url'] = url
                self.params['element'] = 'table.list-item div.article'
                self.params['call'] = self.set_channel_list
                self.params['type'] = WorkType.GET_ELEMENT
                self.web_work(self.params)

            # 获取分页链接
            self.params['url'] = url
            self.params['element'] = 'table.page-book'
            self.params['call'] = self.set_page_data
            self.params['type'] = WorkType.GET_ELEMENT
            self.web_work(self.params)

            # 获取分页信息
            self.params['url'] = url
            self.params['element'] = 'div.page-book-turn'
            self.params['call'] = self.set_page_info
            self.params['type'] = WorkType.GET_ELEMENT
            self.web_work(self.params)

    def set_page_info(self, res):
        # 设置页数标签
        self.page_label.config(text=res[0].text)

    def set_page_data(self, res):
        page_data = res[0].find('a')
        size = len(page_data)
        if size == 2:
            self.page_prev_link = list(page_data[0].absolute_links)[0]  # 上一页
            self.page_next_link = list(page_data[1].absolute_links)[0]  # 下一页
        elif size == 4:
            # 包含四个选项，首页、上一页、下一页、尾页
            self.page_prev_link = list(page_data[1].absolute_links)[0]  # 上一页
            self.page_next_link = list(page_data[2].absolute_links)[0]  # 下一页
        # print(self.page_prev_link, self.page_next_link)

    def set_channel_list(self, res):
        try:
            self.listbox.delete(0, tk.END)

            for item in res:
                content = {}
                # 此处获取小说的标题、作者、阅读量、是否完结、链接地址
                a_link = item.find('a')[0]
                span_end = item.find('span.red')

                title = a_link.text
                author = item.find('span.mr15')[0].text
                read = item.find('span.count')[0].text
                url = list(a_link.absolute_links)[0].replace('book', 'chapters') # 直接替换为章节链接

                if len(span_end) > 0:
                    span_end = span_end[0].text
                else:
                    span_end = ''

                self.listbox.insert(tk.END, ("%s - %s -- %s - %s" % (title, author, read, span_end)))

                # print('url: %s' % url)

                content['title'] = title
                content['author'] =author
                content['read'] = read
                content['end'] = span_end
                content['url'] = url

                # 添加到列表
                self.content_list.append(content)

        except Exception as e:
            print(e)

    def set_chapters_list(self, res):
        try:
            self.listbox.delete(0, tk.END)

            for a in res:
                content = {}
                url = list(a.absolute_links)[0].replace('chapters', 'book') # 替换回来
                title = a.text

                content['title'] = title
                content['url'] = url

                self.listbox.insert(tk.END, ("%s" % title))

                # 添加到列表
                self.content_list.append(content)

        except Exception as e:
            print(e)

    # 上一页
    def page_prev(self, event):
        self.init_focus(self.page_prev_link,'')

    # 下一页
    def page_next(self, event):
        self.init_focus(self.page_next_link,'')

    def open_url(self, event):
        try:

            count = len(self.content_list)
            if count <= 0:
                print("list is null")
                return
            index = self.listbox.curselection()[0]
            url = self.content_list[index]['url']

            if self.page_chapters == False:
                # 打开章节目录列表
                self.page_chapters = True
                self.root.show_frame(Pages.CHANNEL, url)
            else:
                # 跳转至阅读页面
                # self.page_chapters = False
                self.root.show_frame(Pages.CONTENT, url)
        except Exception as e:
            print(e)

    def is_chapters(self):
        return self.page_chapters

    def set_page_chapters(self, state):
        self.page_chapters = state

    def get_article_url(self):
        return self.page_article_url
