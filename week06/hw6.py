#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

"""
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
具体要求：
定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
"""

class Animal(ABC):
    @abstractmethod
    def __init__(self, variety, figure, character):
        self.varietry=variety
        self.figure=figure
        self.character=character

    @property
    def is_beast(self):
        return True if self.figure == '中等' and self.character == '性格凶猛' else False

class Cat(Animal):
    sound = 'catcat'
    def __init__(self, variety, figure, character):
        self.varietry=variety
        self.figure=figure
        self.character=character
    @property
    def is_pet(self):
        return True if self.is_beast else False
class Dog(Animal):
    sound = 'dogdog'
    def __init__(self, variety, figure, character):
        self.varietry=variety
        self.figure=figure
        self.character=character
    @property
    def is_pet(self):
        print (self.is_beast)
        return True if self.is_beast else False


class Zoo:
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
    def add_an_animal_type(self, animal_to_add=None):
        if not hasattr(self, animal_to_add.__class__.__name__):
            setattr(self, animal_to_add.__class__.__name__, 1)


if __name__ == "__main__":
    z = Zoo('动物园')

    cat1 = Cat('食肉', '小', '温顺')
    print(cat1.__dict__)
    print(cat1.is_pet)
    dog1 =Dog('食肉','中型','性格凶猛')
    print(dog1.__dict__)
    print(dog1.is_pet)
    

    z.add_an_animal_type(cat1)
    
    z.add_an_animal_type(dog1)
    print(z.__dict__)
    hasattr(z, 'Cat')
    # have_cat = hasattr(z, 'Cat')
    # print(have_cat)
