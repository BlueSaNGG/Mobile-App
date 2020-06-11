#转为执行文件时需要命名为main.py
from kivy.app import App
from kivy.lang import Builder  #连接kv
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior 
#引入hover
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("design.kv")  #引入kvfile

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction="left"
        self.manager.current="sign_up_screen"
    def login(self,uname,pword):
        with open("user.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:      
            self.manager.transition.direction="left"
            self.manager.current="login_screen_success"
        else:
            self.ids.login_wrong.text="Wrong username or password!"
    def forget(self):
        self.manager.transition.direction="left"
        self.manager.current="forget_password"

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("user.json") as file:
            users = json.load(file)
        users[uname]={"username":uname,"password":pword,
            "created":datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        #覆盖原本jsonfile
        with open("user.json",'w') as file:
            json.dump(users,file)
        self.manager.transition.direction="left"
        self.manager.current="sign_up_screen_success"
    def back(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"
    


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"

    def get_quotes(self,feel):
        feel=feel.lower() #转为小写
        available_feelings=glob.glob("quotes/*txt")
        #glob得到目录下每一个txt
        #path.stem得到文件名
        #name得到文件名+后缀
        available_feelings=[Path(filename).stem for filename in available_feelings]
        #去掉后缀
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",'r',encoding='UTF-8') as file:
                quotes=file.readlines()
                #得到list
            self.ids.quote.text=random.choice(quotes)
            #print(feel)
        else:
            self.ids.quote.text="Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    #ButtonBehavior要放在最前面！
    #image的顺序会影响behavior
    pass
#imagebutton 可以使用上述三种类的功能


class FindPassword(Screen):
    def change(self,uname,pword):
        with open("user.json") as file:
            users=json.load(file)
        if uname not in users.keys():
            self.ids.board.text="This username is not exist!"
        else:
            users[uname]={"username":uname,"password":pword,
                "created":datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            with open("user.json",'w') as file:
                json.dump(users,file)
            self.manager.transition.direction="right"
            self.manager.current="login_screen"
    def back(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"


class Rootwidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return Rootwidget()  #返回一个对象

if __name__=="__main__":
    MainApp().run()