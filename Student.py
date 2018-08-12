#!/usr/bin/python
# coding=utf-8


class Student(object):
    '''
        使用 property 装饰器简化属性的赋值， 对私有变量的赋值及取值处理
        @property.setter 注解函数赋值方法

    '''
    def __init__(self,_name,_home):
        self.name = _name
        self.home = _home

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self,home):
        self._home = home


if __name__ == '__main__':
    st = Student('jim','beijing')
    print(st.name)
    print(st.home)
    st.name = "juli"
    print(st.name)