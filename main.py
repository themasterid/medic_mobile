import environ
import requests
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

env = environ.Env()
environ.Env.read_env()
HOST = env('HOST', default="localhost")


class LoginScreen(BoxLayout):
    login_inputs_container = None
    username_input = None
    password_input = None

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 50
        self.spacing = 20

        # Create widgets
        self.logo_image = Image(
            source='logo.png', size_hint=(1, None), height=100)
        self.message_label = Label(size_hint=(
            1, None), height=40, font_size='16sp', color=(1, 0, 0, 1))
        self.greeting_label = Label(text='', size_hint=(
            1, None), height=40, font_size='16sp')

        # Create login inputs container
        self.login_inputs_container = BoxLayout(orientation='vertical')
        self.username_input = TextInput(
            hint_text='Логин', multiline=False, size_hint=(1, None), height=40)
        self.password_input = TextInput(
            hint_text='Пароль', password=True, multiline=False, size_hint=(1, None), height=40)
        self.login_button = Button(
            text='Вход', size_hint=(1, None), height=40)
        self.logout_button = Button(
            text='Выход', size_hint=(1, None), height=40)

        # Bind event handlers
        self.login_button.bind(on_release=self.login)
        self.logout_button.bind(on_release=self.logout)

        # Add widgets to the screen
        self.add_widget(self.logo_image)
        self.add_widget(self.message_label)
        self.add_widget(self.login_inputs_container)
        self.login_inputs_container.add_widget(self.username_input)
        self.login_inputs_container.add_widget(self.password_input)
        self.add_widget(self.login_button)
        self.add_widget(self.logout_button)
        self.add_widget(self.greeting_label)

        self.update_view(is_logged_in=False)

    def update_view(self, is_logged_in):
        self.login_button.disabled = is_logged_in
        self.logout_button.disabled = not is_logged_in
        self.greeting_label.text = ''

        if is_logged_in:
            # Hide the login inputs container
            self.login_inputs_container.opacity = 0
        else:
            # Show the login inputs container
            self.login_inputs_container.opacity = 1

    def login(self, *args):
        username = self.username_input.text
        password = self.password_input.text
        auth_data = {'username': username, 'password': password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(HOST, json=auth_data, headers=headers)

        if response.status_code == 201:
            result = response.json()
            auth_token = result.get('auth_token', '')
            self.login_success(auth_token)
        else:
            self.login_failure(response.text)

    def login_success(self, auth_token):
        # Handle successful user login

        self.message_label.text = "Успешный вход"
        self.update_view(is_logged_in=True)
        self.greeting_label.text = f"Приветствуем {self.username_input.text}"

    def login_failure(self, error_message):
        # Handle unsuccessful user login
        self.message_label.text = ''
        if self.username_input.text or self.password_input.text in ['']:
            self.message_label.text = (
                'Поля логин или пароль'
                ' не могут быть пусты!'
            )
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
        Window.clearcolor = (0, 0.5, 0.5, 1)
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
