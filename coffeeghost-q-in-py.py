# -*- coding:utf-8 -*-
# Quick Python Script Explanation for Programme
# 给程序员的超快速Python脚本解说
import os

def main():
    print 'Hello World!'

    print "这是Alice\'的问候。"
    print '这是Bob\'的问候。'

    foo(5,10)

    print '=' * 10
    print '这将直接执行'+os.getcwd()

    counter = 0     #变量得先实例化才可进一步计算
    counter += 1
    print counter
    '''这是我自己加的多行注释
    '''

    food =['苹果','杏子','李子','梨']
    for i in food:
        print '俺就爱整只:'+i

    print '数到10'
    for i in range(10):
        print i

def foo(param1,secondParam):
    result = param1 + secondParam
    print '%s 加 %s 等于 %s'%(param1,secondParam,result)
    if result < 50:
        print '这个'
    elif (result >= 50) and ((param1 == 42) or (secondParam == 24)):
        print '那个'
    else:
        print '嗯...'
    return result

if __name__=='__main__':
    main()
