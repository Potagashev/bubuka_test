import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.cookies
from jinja2 import Environment, PackageLoader, select_autoescape

from constants import COOKIE_NAME

from utils import \
    get_login_by_cookie, \
    delete_cookie, \
    get_password_by_login, \
    create_user, \
    update_cookie, \
    check_cookie, \
    generate_cookie


class HttpProcessor(BaseHTTPRequestHandler):

    def do_GET(self):
        status = 200
        is_authorized = False
        login = None

        if self.path == '/':
            is_authorized = check_cookie(headers=self.headers)
            all_cookies = http.cookies.SimpleCookie(self.headers['Cookie'])
            given_cookie = all_cookies[COOKIE_NAME].value
            login = get_login_by_cookie(given_cookie)
            template_name = 'index.html'

        elif self.path == '/login':
            # сюда можно только если не авторизован(нет кук), иначе редирект на главную
            is_authorized = check_cookie(headers=self.headers)
            template_name = 'login.html'

        elif self.path == '/logout':
            # some logic with logging out
            # удалить куки
            all_cookies = http.cookies.SimpleCookie(self.headers['Cookie'])
            given_cookie = all_cookies[COOKIE_NAME].value
            delete_cookie(given_cookie)
            template_name = 'logout.html'

        elif self.path == '/signup':
            # сюда можно только если не авторизован(нет кук), иначе редирект на главную
            is_authorized = check_cookie(headers=self.headers)
            template_name = 'signup.html'

        else:
            template_name = 'not_found.html'
            status = 404

        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        env = Environment(
            loader=PackageLoader('server'),
            autoescape=select_autoescape()
        )
        template = env.get_template(template_name)
        response_body = bytes(template.render(login=login, is_authorized=is_authorized), encoding='utf-8')
        self.wfile.write(response_body)

    def do_POST(self):
        status = 200
        is_authorized = False
        login = None
        message = None

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        # создаем куки и при переадресации передаем их
        # сюда идем по кнопке входа
        if self.path == '/':
            template_name = "login.html"

            login = form.getvalue('login')
            password = form.getvalue('password')

            if password == get_password_by_login(login):
                template_name = 'index.html'
                is_authorized = True

                self.send_response(status)
                self.send_header('Content-type', 'text/html')

                cookie = http.cookies.SimpleCookie()
                cookie[COOKIE_NAME] = generate_cookie(login, password)
                for morsel in cookie.values():
                    self.send_header("Set-Cookie", morsel.OutputString())

                update_cookie(login=login, given_cookie=cookie[COOKIE_NAME].value)
            else:
                is_authorized = False
                status = 403
                message = 'Неправильный логин или пароль!'
                self.send_response(status)
                self.send_header('Content-type', 'text/html')

            self.end_headers()

        # сюда идем после ввода данных для регистрации
        elif self.path == '/login':
            template_name = "login.html"

            login = form.getvalue('login')
            email = form.getvalue('email')
            password = form.getvalue('password')

            create_user(
                login=login,
                email=email,
                password=password
            )
            is_authorized = False

            self.send_response(status)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = 'Регистрация прошла успешно!'
        else:
            template_name = 'not_found.html'
            status = 404
            self.send_response(status)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        env = Environment(
            loader=PackageLoader('server'),
            autoescape=select_autoescape()
        )
        template = env.get_template(template_name)
        response_body = bytes(template.render(
            login=login,
            status=status,
            message=message,
            is_authorized=is_authorized),
            encoding='utf-8'
        )
        self.wfile.write(response_body)


def runserver(server_class=HTTPServer, handler_class=HttpProcessor):
    server_address = ('127.0.0.1', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == '__main__':
    runserver()
