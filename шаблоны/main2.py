from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.config import Config

#file manager
import os
from os.path import join, dirname, abspath

#kivy3
from kivy3 import Renderer, Scene
from kivy3 import PerspectiveCamera
from kivy3.loaders import OBJLoader
from kivy3.extras.geometries import BoxGeometry
from kivy3.extras.geometries import SphereGeometry
from kivy3 import Material, Mesh

#kivy lang
from kivy.lang import Builder
from kivy.factory import Factory

#numpy
import numpy as np
import math

Builder.load_string('''
<MoveButton>:
    on_release: self.move(self.point1, self.text)

<CamNav@GridLayout>:
    cols: 3
    Widget:
    MoveButton:
        text: 'up'
        font_size: 13
    Widget:
    MoveButton:
        text: 'left'
        font_size: 13
    Label:
        text: 'cam'
    MoveButton:
        text: 'right'
        font_size: 13
    Widget:
    MoveButton:
        text: 'down'
        font_size: 13

<Fov@GridLayout>:
    cols: 1
    Widget:
    MoveButton:
        text: '+'
    Widget:
    MoveButton:
        text: '-'

''')

Folder = dirname(abspath(__file__))

class MoveButton(Button):
    def __init__(self, **kwargs):
        super(MoveButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.point1 = self.app.point1
        self.points = self.app.pp
        self.lines = self.app.ll
        self.k=self.app.theflag
        self.k0=self.app.theflag0
    def move(self, cube, direc, *args):
        if direc == 'up':
            self.k=self.app.theflag
            self.r = cube.pos.z*-1
            kx=self.k
            self.k+=2/180*math.pi
            ax=(math.pi - self.k)/2
            ay= math.pi/2 - ax
            #
            kax=(math.pi - kx)/2
            kay= math.pi/2 - kax
            if self.k<0.5*math.pi:
                self.app.camera.pos.y -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y += math.sin(ay)*2*math.sin(self.k/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(self.k/2)*self.r
            elif self.k>0.50*math.pi and self.k<1.00*math.pi:
                self.app.camera.pos.y += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y -= math.sin(ay)*2*math.sin(self.k/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(self.k/2)*self.r
            elif self.k>1.00*math.pi and self.k<1.50*math.pi:
                self.app.camera.pos.y -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y += math.sin(ay)*2*math.sin(self.k/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(self.k/2)*self.r
            elif self.k>1.50*math.pi and self.k<2.00*math.pi:
                self.app.camera.pos.y += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y -= math.sin(ay)*2*math.sin(self.k/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(self.k/2)*self.r

            else:
                self.k-=2.0*math.pi
            self.app.theflag = self.k
            print(self.app.camera.pos.z)
            self.app.camera.look_at(cube.pos)
        elif direc == 'down':
            self.k=self.app.theflag
            self.r = cube.pos.z*-1
            kx=self.k
            kk=self.k
            kk-=2/180*math.pi
            if(kk<0):
                kk= 2*math.pi + kk
            ax=(math.pi - kk)/2
            ay= math.pi/2 - ax
            #
            kax=(math.pi - kx)/2
            kay= math.pi/2 - kax
            if kk<0.5*math.pi:
                self.app.camera.pos.y -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y += math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(kk/2)*self.r
                #print(self.k)
            elif kk>0.50*math.pi and kk<1.00*math.pi:
                self.app.camera.pos.y += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y -= math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(kk/2)*self.r
            elif kk>1.00*math.pi and kk<1.50*math.pi:
                self.app.camera.pos.y -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y += math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(kk/2)*self.r
            elif kk>1.50*math.pi and kk<2.00*math.pi:
                self.app.camera.pos.y += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.y -= math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(kk/2)*self.r

            else:
                kk +=2.0*math.pi
            self.k = kk
            self.app.theflag = self.k
            print(self.k)
            self.app.camera.look_at(cube.pos)
        elif direc == 'right':
            self.k0=self.app.theflag0
            self.r = cube.pos.z*-1
            kx=self.k0
            self.k0+=2/180*math.pi
            ax=(math.pi - self.k0)/2
            ay= math.pi/2 - ax
            #
            kax=(math.pi - kx)/2
            kay= math.pi/2 - kax
            if self.k0<0.5*math.pi:
                self.app.camera.pos.x -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x += math.sin(ay)*2*math.sin(self.k0/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(self.k0/2)*self.r
            elif self.k0>0.50*math.pi and self.k0<1.00*math.pi:
                self.app.camera.pos.x += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x -= math.sin(ay)*2*math.sin(self.k0/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(self.k0/2)*self.r
            elif self.k0>1.00*math.pi and self.k0<1.50*math.pi:
                self.app.camera.pos.x -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x += math.sin(ay)*2*math.sin(self.k0/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(self.k0/2)*self.r
            elif self.k0>1.50*math.pi and self.k0<2.00*math.pi:
                self.app.camera.pos.x += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x -= math.sin(ay)*2*math.sin(self.k0/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(self.k0/2)*self.r

            else:
                self.k0-=2.0*math.pi
            self.app.theflag0 = self.k0
            print(self.k0)
            self.app.camera.look_at(cube.pos)

        elif direc == 'left':
            self.k0=self.app.theflag0
            self.r = cube.pos.z*-1
            kx=self.k0
            kk=self.k0
            kk-=2/180*math.pi
            if(kk<0):
                kk= 2*math.pi + kk
            ax=(math.pi - kk)/2
            ay= math.pi/2 - ax
            #
            kax=(math.pi - kx)/2
            kay= math.pi/2 - kax
            if kk<0.5*math.pi:
                self.app.camera.pos.x -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x += math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(kk/2)*self.r
                #print(self.k)
            elif kk>0.50*math.pi and kk<1.00*math.pi:
                self.app.camera.pos.x += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x -= math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(kk/2)*self.r
            elif kk>1.00*math.pi and kk<1.50*math.pi:
                self.app.camera.pos.x -= math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z += math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x += math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z -= math.cos(ay)*2*math.sin(kk/2)*self.r
            elif kk>1.50*math.pi and kk<2.00*math.pi:
                self.app.camera.pos.x += math.sin(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.z -= math.cos(kay)*2*math.sin(kx/2)*self.r
                self.app.camera.pos.x -= math.sin(ay)*2*math.sin(kk/2)*self.r
                self.app.camera.pos.z += math.cos(ay)*2*math.sin(kk/2)*self.r

            else:
                kk +=2.0*math.pi
            self.k0 = kk
            self.app.theflag0 = self.k0
            print(self.k0)
            self.app.camera.look_at(cube.pos)

        elif direc == '+':
            #self.app.camera.fov=150
            for point in self.points:
                point.pos.z += 5
            for line in self.lines:
                line.pos.z += 5
            cube.pos.z += 5
        elif direc == '-':
            for point in self.points:
                point.pos.z -= 5
            for line in self.lines:
                line.pos.z -= 5
            cube.pos.z -= 5


class TestApp(App):
        loader = OBJLoader()
        def _adjust_aspect(self, *args):
            rsize = self.renderer.size
            aspect = rsize[0] / float(rsize[1])
            self.renderer.camera.aspect = aspect

        def rotate_cube(self, *dt):
            pass
        def letstart (self, *dt):
            pass

        flag=0
        def load(self, *dt):
            os.startfile('thechs.py')#.exe
            #os.system("TASKKILL /F /IM python.exe")#3drb1.exe

        def callback(self, dt):
            print (' XXX ')

        def build(self):
            self.theflag=0
            self.theflag0=0
            self. distan= 1000 # дистанция до начальной точки (0,0,-50) что бы ничего не было за экраном (надо будет выстваить на изменение)
            bl= BoxLayout(orientation='vertical', size_hint = (.15, 1), spacing = 10, padding = 10)# левая панель
            al= AnchorLayout(anchor_x='left', anchor_y='center')# основная система интерфейса
            layout = GridLayout(cols = 2, spacing = 3, size_hint = (1, 1)) #сетка для кнопок поворота

            matrix = np.load('matrix0.npy', allow_pickle=True)
            print(matrix)
            #a=matrix['self.a']
            print(a)
            counter=int(int(matrix.size)/2)
            x = np.zeros(counter)
            y = np.zeros(counter)
            z = np.zeros(counter)
            soe = np.zeros((counter,counter))

            for i in range (2):
                if(i==0):
                    for j in range(counter):
                        for k in range (3):
                            #a=matrix[i,j]
                            if(k==0):
                                x[j] = a[k]*10
                            elif(k==1):
                                y[j] = a[k]*10
                            else:
                                z[j] = a[k]*10
                else:
                    for j in range(counter):
                        a=matrix[i,j]
                        for k in range (counter):
                            soe[j][k]=a[k]
            print(x,y,z)
            print(soe)
            # кнопка загрузки координат
            loader = Button(text='Load', on_press = self.load)
            bl.add_widget(loader)

            #starter = Button(text='Построить', on_press = self.letstart)
            #bl.add_widget(starter)

            bl.add_widget(Widget())
            # create renderer
            self.renderer = Renderer()

            # create scene
            scene = Scene()

            #lines
            k0=0
            k1=0
            lines_list = []
            for i in soe:
                for j in i:
                    if(j==1):
                        line0_geo = BoxGeometry(1, int(((y[k0]-y[k1])**2 + (x[k0]-x[k1])**2 + (z[k0]-z[k1])**2 )**0.5), 1)
                        #print(int(((abs(x[k0]-x[k1]) + abs(y[k0]-y[k1])+ abs(z[k0]-z[k1]))**0.5)),'length')
                        #print(int(abs(y[k0]-y[k1]) + abs(x[k0]-x[k1])+ abs(z[k0]-z[k1])))
                        line0_mat = Material()
                        self.line0 = Mesh(
                            geometry=line0_geo,
                            material=line0_mat
                        )  # default pos == (0, 0, 0)
                        self.line0.pos.x = int((x[k0]+x[k1])/2)
                        self.line0.pos.y = int((y[k0]+y[k1])/2)
                        self.line0.pos.z = int((z[k0]+z[k1])/2) - self.distan
                        if y[k0]-y[k1]==0 and x[k0]-x[k1]==0 and z[k0]-z[k1]!=0:
                            self.line0.rotation.x = 90
                        elif y[k0]-y[k1]==0 and x[k0]-x[k1]!=0 and z[k0]-z[k1]==0:
                            self.line0.rotation.z = 90
                        elif y[k0]-y[k1]!=0 and x[k0]-x[k1]==0 and z[k0]-z[k1]==0:
                        ###
                            fff=0
                        elif y[k0]-y[k1]!=0 and x[k0]-x[k1]!=0 and z[k0]-z[k1]==0:
                            self.line0.rotation.z = math.atan((x[k0]-x[k1])/(y[k0]-y[k1]))/math.pi*180
                        elif y[k0]-y[k1]!=0 and x[k0]-x[k1]==0 and z[k0]-z[k1]!=0:
                            #self.line0.rotation.x = math.atan((z[k0]-z[k1])/(y[k0]-y[k1]))/math.pi*180
                            self.line0.rotation.x = math.acos(abs(y[k0]-y[k1])/((x[k0]-x[k1])**2+(y[k0]-y[k1])**2+(z[k0]-z[k1])**2)**0.5)/math.pi*180
                            #print()
                        elif y[k0]-y[k1]==0 and x[k0]-x[k1]!=0 and z[k0]-z[k1]!=0:
                            self.line0.rotation.z = math.atan((x[k0]-x[k1])/(z[k0]-z[k1]))/math.pi*180*-1
                            self.line0.rotation.x = 90

                        ###
                        elif y[k0]-y[k1]!=0 and x[k0]-x[k1]!=0 and z[k0]-z[k1]!=0:
                            if((x[k0]<x[k1] and y[k0]<y[k1]) or (x[k0]>x[k1] and y[k0]>y[k1])):
                                #self.line0.rotation.z = math.atan((abs(z[k0]-z[k1]))/1.5/(abs(y[k0]-y[k1])))/math.pi*180
                                self.line0.rotation.z = math.acos(abs(y[k0]-y[k1])/((x[k0]-x[k1])**2+(y[k0]-y[k1])**2+(0)**2)**0.5)/math.pi*180*-1
                                #проблема
                            else:
                                self.line0.rotation.z = math.acos(abs(y[k0]-y[k1])/((x[k0]-x[k1])**2+(y[k0]-y[k1])**2+(0)**2)**0.5)/math.pi*180
                            #self.line0.rotation.x = math.atan((1.25*abs(x[k0]-x[k1]))/(abs(y[k0]-y[k1])))/math.pi*180*-1
                            if((z[k0]<z[k1] and y[k0]<y[k1]) or (z[k0]>z[k1] and y[k0]>y[k1])):
                                self.line0.rotation.x = math.acos(abs(y[k0]-y[k1])/((0)**2+(y[k0]-y[k1])**2+(z[k0]-z[k1])**2)**0.5)/math.pi*180
                                #проблема
                            else:
                                self.line0.rotation.x = math.acos(abs(y[k0]-y[k1])/((0)**2+(y[k0]-y[k1])**2+(z[k0]-z[k1])**2)**0.5)/math.pi*180*-1

                            #self.line0.rotation.x = math.acos(abs(y[k0]-y[k1])/((0)**2+(y[k0]-y[k1])**2+(z[k0]-z[k1])**2)**0.5)/math.pi*180*-1#there
                            print(self.line0.rotation.z)
                            print(self.line0.rotation.x)
                        lines_list.append(self.line0)
                    k1+=1
                k0+=1
                k1=0
            line0_geo = BoxGeometry(1, y[1]-y[0], 1)
            line0_mat = Material()
            self.line0 = Mesh(
                geometry=line0_geo,
                material=line0_mat
            )  # default pos == (0, 0, 0)
            self.line0.pos.z = int(z[0]) - self.distan

            #self.line3.rotation.x = 90

            #points
            point_list = []
            sumx=0
            sumy=0
            sumz=0
            sumcount=0
            loader = OBJLoader()

            for i in range (counter):
                point_geom=SphereGeometry(1.1)
                point_mat = Material()
                self.point0 = Mesh(
                    geometry=point_geom,
                    material=point_mat
                )
                self.point0.pos.x = int(x[i])
                self.point0.pos.y = int(y[i])
                self.point0.pos.z = int(z[i]) - self.distan
                self.point0.scale = (1, 1, 1)
                point_list.append(self.point0)
                sumx+=self.point0.pos.x
                sumy+=self.point0.pos.y
                sumz+=self.point0.pos.z
                sumcount+=1
                #scene.add(self.point0)

            point_geom=SphereGeometry()
            point_mat = Material()
            self.point1 = Mesh(
                geometry=point_geom,
                material=point_mat
            )
            self.point1.pos.x = sumx/sumcount
            self.point1.pos.y = sumy/sumcount
            self.point1.pos.z = sumz/sumcount
            self.point1.scale = (1, 1, 1)
            #scene.add(self.point1)
            self.camera = PerspectiveCamera(
                fov=100,    # размер окна т.е. чем больше фов тем больше масштаб
                aspect=0,  # "screen" ratio
                near=1,    # рендер от
                far=10000     # дистанция рендера
            )

            k0=0
            self.ll=[]
            for i in soe:
                for j in i:
                    if(j==1):
                        self.ll.append(lines_list[k0])
                        scene.add(lines_list[k0])
                        k0+=1

            for i in range (counter):
                scene.add(point_list[i])
                pass

            self.pp = point_list
            self.renderer.render(scene, self.camera)
            self.renderer.bind(size=self._adjust_aspect)
            al.add_widget(self.renderer)
            bl.add_widget(Factory.Fov())
            bl.add_widget(Factory.CamNav())
            al.add_widget(bl)
            return al

#if __name__ == "__main__":
TestApp().run()
