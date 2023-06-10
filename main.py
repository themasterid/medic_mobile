from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        auth_data = {'username': username, 'password': password}
        headers = {'Content-type': 'application/json'}
        UrlRequest('http://127.0.0.l/auth/login/', on_success=self.login_success,
                   on_failure=self.login_failure, req_body=json.dumps(auth_data), req_headers=headers)
        
    def login_success(self, req, result):
        # Обработка успешного входа пользователя
        print("Успешный вход:", result)
        
    def login_failure(self, req, result):
        # Обработка неудачного входа пользователя
        print("Неудачный вход:", result)

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
