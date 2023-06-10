import json

import environ
from kivy.app import App
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

env = environ.Env()

environ.Env.read_env()

HOST = env('HOST', default="localhost")


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 50
        self.spacing = 20

        # Create widgets
        self.logo_image = Image(
            source='logo.png', size_hint=(1, None), height=100)
        self.message_label = Label(
            size_hint=(1, None), height=40, font_size='16sp', color=(1, 0, 0, 1))
        self.username_input = TextInput(
            hint_text='Логин', multiline=False, size_hint=(1, None), height=40)
        self.password_input = TextInput(
            hint_text='Пароль', password=True, multiline=False, size_hint=(1, None), height=40)
        self.login_button = Button(
            text='Войти', size_hint=(1, None), height=40)
        self.logout_button = Button(
            text='Выйти', size_hint=(1, None), height=40)
        self.greeting_label = Label(
            text='', size_hint=(1, None), height=40, font_size='16sp')

        # Bind event handlers
        self.login_button.bind(on_release=self.login)
        self.logout_button.bind(on_release=self.logout)

        # Add widgets to the screen
        self.add_widget(self.logo_image)
        self.add_widget(self.message_label)
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)
        self.add_widget(self.logout_button)
        self.add_widget(self.greeting_label)

        self.update_view(is_logged_in=False)

    def update_view(self, is_logged_in):
        self.login_button.disabled = is_logged_in
        self.logout_button.disabled = not is_logged_in
        self.username_input.disabled = is_logged_in
        self.password_input.disabled = is_logged_in
        self.greeting_label.text = ''

    def login(self, *args):
        username = self.username_input.text
        password = self.password_input.text
        auth_data = {'username': username, 'password': password}
        headers = {'Content-type': 'application/json'}
        UrlRequest(
            HOST,
            on_success=self.login_success,
            on_failure=self.login_failure,
            req_body=json.dumps(auth_data),
            req_headers=headers
        )

    def login_success(self, req, result):
        # Handle successful user login
        self.message_label.text = "Успешный вход: {}".format(
            result)
        self.update_view(is_logged_in=True)
        self.greeting_label.text = "Приветствуем {}".format(
            self.username_input.text)

    def login_failure(self, req, result):
        # Handle unsuccessful user login
        self.message_label.text = "Неудачный вход: {}".format(
            result.get('detail'))
        self.username_input.text = ''
        self.password_input.text = ''

    def logout(self, *args):
        # Handle user logout
        self.username_input.text = ''
        self.password_input.text = ''
        self.message_label.text = ''
        self.update_view(is_logged_in=False)


class MyApp(App):
    def build(self):
        # Set the application title
        self.title = 'Автомедик - IAS_Control'

        # Set black background color
        Window.clearcolor = (0, 0, 0, 1)
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
