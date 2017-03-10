#!/usr/bin/env python
#encoding:utf-8

# sum=0
# for x in range(101):
# 	sum=sum+x
# print sum
# 计算1-100的和

# sum=0
# n=99
# while n>0:
# 	sum=sum+n
# 	n=n-2
# print sum
# 计算100以内奇数之和


# birth = int(raw_input('birth: '))
# if birth < 2000:
#     print '00前'
# else:
#     print '00后'
def create_adder(x):
    def adder(y):
        print x + y
        return x + y
    return adder

add_10 = create_adder(10)
add_10(3)   # 13

#####疑问:这里为什么用add_10,不是adder

# #匿名函数
# print (lambda x: x > 2)(3) #True
#
# #内置高阶函数
# print map(add_10,[1,2,3])  # [11,12,13]
#
# #####疑问:这里为什么用add_10,不是adder
# print 3 > 2
#
# #用def来新建函数
# def add(x,y):
#     print "x is %s and y is %s" % (x,y)
#     return x + y  #通过return来返回值
#
# #调用带参数的函数
# add(5,6) #输出结果"x is 5 and y is 6" 返回11
#
# #通过关键字赋值来调用函数
# add(y=6,x=5)  #顺序是无所谓的
#
# x = 0
# while x < 4:
#     print x
#     x += 1 #x = x + 1的简写
#
# print filter(lambda x: x > 5,[3,4,5,6,7])  # [6,7]

from math import ceil,floor
print ceil(3.3)   #4.0
print floor(3.3)   #3.0