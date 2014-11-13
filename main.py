from random import random
from kivy.app import App
from kivy.uix.button import Button
from uix.stack_layout import StackLayout

def r():
    return random() * 100.0 + 20.0

class LayoutTest(App):
    def build(self):
        rl = StackLayout()
        for i in range(40):
            rl.add_widget(Button(size_hint=(r(), r())))
        return rl

LayoutTest().run()