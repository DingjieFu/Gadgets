# 用户：夜卜小魔王

# 基于pyside2的GUI设计
import sys
import requests
from utils import TodayNews, NOI
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from PySide2.QtUiTools import QUiLoader


class UI(QMainWindow):  # 初始界面
    def __init__(self):
        super().__init__()
        self.menu = Menu()  # 生成Menu类对象
        self.main_window = QUiLoader().load(r'main_window.ui')  # load设计好的UI文件
        self.main_window.button.clicked.connect(self.open_new_window)  # 将button("开始使用")点击与函数关联起来

    def open_new_window(self):
        """ TODO: 在主界面按钮按下后调用菜单界面， 并关闭主界面 """
        self.menu.menu.show()
        self.main_window.close()


class Menu(QWidget):  # 菜单界面
    def __init__(self):
        super().__init__()
        self.menu = QUiLoader().load(r'menu.ui')
        self.menu.resize(400, 400)  # 更改界面大小为400X400
        self.urls = None  # 保存新闻url链接
        self.text = None  # 保存QlineEdit的内容
        self.menu.pushButton.clicked.connect(self.print_news_to_text_browser)  # 将pushButton("刷新")点击与函数关联起来
        self.menu.search.textChanged.connect(self.line_edit_text_changed)  # 将search("输入文本")改变与函数关联起来
        self.menu.search_button.clicked.connect(self.print_news_details)  # 将search_button("搜索")点击与函数关联

    def print_news_to_text_browser(self):
        """TODO：按下~刷新~显示top50新闻标题"""
        self.menu.text.clear()  # 每次调用前先清空textBrowser里的内容
        # 下面就是调用TodayNews类
        today_news = TodayNews(my_domain, my_headers, my_params)
        today_news.get_response()
        title_list, self.urls = today_news.separate_news()  # 随每次刷新而刷新
        for i, title in enumerate(title_list):
            self.menu.text.append(f"热门排行:{i + 1}, 标题:{title}")
            self.menu.text.moveCursor(self.menu.text.textCursor().End)

    def line_edit_text_changed(self):
        """ TODO: 记录文本框的数值 用于调出新闻 """
        self.text = int(self.menu.search.text())

    def print_news_details(self):
        noi = NOI()
        noi.resp = requests.get(self.urls[self.text - 1], headers=my_headers, params=my_params)
        news = noi.find_specific()
        self.menu.text.clear()  # 先清空textBrowser里的内容
        self.menu.text.append(news)
        self.menu.text.moveCursor(self.menu.text.textCursor().End)


my_domain = "https://www.toutiao.com/hot-event/hot-board/"
my_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38",
            "cookie": "ttcid=ecef452c9ce04960ad8734a1ca56713135; tt_webid=7006670530280162847; csrftoken=873d936cde78f1ea0684d27852e5de7d; tt_webid=7006670530280162847; __ac_nonce=06168056800d9606d2a6d; __ac_signature=_02B4Z6wo00f01hU2kagAAIDClTRr6iT3aTYVEpUAAOQzjq1Zjaf4vCFaBAAUsNx-HKr5F6PVC6-6tOpvlYn9Oh7qsFojMYsjxFKpY31kfsBZ-uoVedSJG92rtPZedY0rBDGeS105SSc-1pj521; s_v_web_id=verify_kuqspbfp_g7ymjREw_4ss8_42Bh_95eZ_wthN8QxwP2N2; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=45aac2c9-76af-461f-9cab-91189229ebce; ttwid=1%7CCVopD4s3fpussyFrIsGRFdIEvb4hotTPn7sDNoKNOaI%7C1634207523%7Cd5e8569b5329139b87fbd91de6863e4e4f3dadf76140a5ff82ae21d113b28931; MONITOR_WEB_ID=7006670530280162847; tt_scid=xfvw-zTodV0ixl-MacOKqJUzIeQ0F1qXDKF1m5Re5.dRx6vqkzWOA8gs-fZ6zbfV0eab"
        }
my_params = {
            "origin": "toutiao_pc",
            "_signature": "_02B4Z6wo00d01P0p8bgAAIDAfSsL-s2OYET9DfUAAF4o6UHXi8eI3zHY6KIDQPOLQpvlUP3u3jwmshjMj5KtFzLF6C9nIEolehcqA.ELzNuN-db5C-4-R18JABYy1hnL8GHqum5JcfBd9Tx4e4"
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.main_window.show()
    sys.exit(app.exec_())
