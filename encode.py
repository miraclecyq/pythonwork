#!/usr/bin/env python
# -*- coding: utf-8 -*-

# encode.py
age=int(raw_input(u'请输入你的年龄:'.encode('gbk')).decode('gbk'))
name=raw_input(u'和姓名：'.encode('gbk')).decode('gbk')
if age > 18:
	print '''hello,pretty %s
please play ball with us %d times''' % (name,5)
else:
	print '''hello,little %s
please play ball with us %d times''' % (name,3)