from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#kivy lang
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.label import Label
#numpy
import numpy as np
import math

#file manager
import os
from os.path import join, dirname, abspath
Builder.load_string('''
<MoveButton>:
    on_release: self.next()
<Fov@GridLayout>:
    cols: 1
    MoveButton:
        text: 'Ввод'
''')
class MoveButton(Button):
    def __init__(self, **kwargs):
        super(MoveButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.lab = self.app.lb
        self.outputxt = self.app.textinput
        self.counter = 0
        self.col=0
        self.klist = []
        self.slist = []
        self.flag=0
        self.counterer=0
        self.b=0
        self.a=0
        self.i=0
        self.flag1=0#это для создания разных матриц
    def next(self, *args):
        if(self.flag==0):
            out = int(self.outputxt.text)
            if self.counter == 0:
                self.col=out * 3
            #print(self.col,self.counter)
                self.lab.text='введите координату Х точки 1 '
            else:
                if self.counter<=self.col:
                    oc=''
                    if((self.counter+1) %3 == 0):
                        oc='Z'
                    elif((self.counter) %3 == 0):
                        oc='X'
                    else:
                        oc='Y'
                        #print(self.counter+1)
                    if self.counter<self.col:
                        self.lab.text='введите координату '+ oc +' точки '+ str(int(self.counter/3)+1)
                    else:
                        self.lab.text='в какие точки будет следовать точка 1'
                    self.klist.append(int(self.outputxt.text))
            if self.counter == self.col:
                self.a = np.zeros(int(self.col/3))
                k=0
                print(len(self.klist))
                #print('yse')
                #print(a)
                thelist1=[]
                for i in range (int(self.col/3)):
                    thelist = []
                    for j in range (3):
                        print(3*self.col/3,k)
                        print(self.klist[k])
                        thelist.append(self.klist[k])
                        k+=1
                    thelist1.append(thelist)
                self.a=np.asarray(thelist1)
                print('yse')
                print(self.a)
                self.flag=1
                #self.counter=-1
            self.counter+=1
        else:################
            text=self.outputxt.text
            if text != '-':
                for i in text:
                    self.slist.append(i)
                if self.counterer == 0:
                    self.b = np.zeros((int(self.col/3),int(self.col/3)))
                self.counterer+=1
                k=0
                f=0
                th=0#разряды
                hund=0
                ten=0
                one=0
                print(self.slist,'строка')
                self.counter=0
                self.slist.append(' ')
                for j in self.slist:
                    print(self.counter,'счетчик')
                    print(len(self.slist),'длинна')
                    flag=0
                    if self.counter == len(self.slist)-1:
                        flag=1
                        print(flag)
                    if(j == ' ' or flag == 1):
                        chislo = th*1000+hund*100+ten*10+one
                        print(chislo,'число')
                        f=0
                        th=0#разряды
                        hund=0
                        ten=0
                        one=0
                        for z in range (int(self.col/3)+1):
                            if z == chislo:
                                if z!=0:
                                    self.b[self.i, z-1]=1
                                    print('внесли',self.counter,chislo)
                                    if flag== 1:
                                        self.i+=1
                                        self.lab.text='в какие точки будет следовать точка ' + str(self.i+1)
                                        if self.i == int(self.col/3):
                                            self.lab.text='Матрица следования введена'
                                            np.save('matrix0', self.a, self.b)
                                        self.slist = []
                    else:
                        if f==0:
                            if j != '\n':
                                one=int(j)
                                f+=1
                                print(one,'нашли')
                        elif f==1:
                            if j != '\n':
                                ten=one
                                one=int(j)
                                f+=1
                        elif f==2:
                            if j != '\n':
                                hund=ten
                                ten=one
                                one=int(j)
                                f+=1
                        elif f==3:
                            if j != '\n':
                                th=hund
                                hund=ten
                                ten=one
                                one=int(j)
                                f+=1
                        else:
                            print("более 9999 точек меняй прогу")

                    self.counter+=1
            else:
                self.i+=1
                self.lab.text='в какие точки будет следовать точка ' + str(self.i+1)
                if self.i == int(self.col/3):
                    self.lab.text='Матрица следования введена'
                    np.save('matrix0', self.a, self.b)
                self.slist = []
                print('tt')
            print(self.b,'массив')
            #np.append(self.a,self.b)
class TestApp(App):
        def go(self,x):
            pass
        def build(self):
            bl = BoxLayout(orientation='vertical')
            self.lb = Label(text='Введите количество точек')
            self.textinput = TextInput(text='')
            bl.add_widget(self.lb)
            bl.add_widget(Factory.Fov())
            bl.add_widget(self.textinput)
            return bl

if __name__ == "__main__":
    TestApp().run()
