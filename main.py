from google_news_api import GoogleNewsClient
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import QPainter, QPalette
from qt_material import apply_stylesheet
from email.utils import parsedate_to_datetime
import webbrowser
import sys

WIDTH = 800
HEIGHT = 800

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Israel Last News")
        self.resize(800, 800)

        root_container = QWidget()
        root_layout = QVBoxLayout(root_container)
        
        header_container = QFrame()
        body_container = QFrame()

        header_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, header_container)
        body_layout = QVBoxLayout(body_container)

        root_layout.addWidget(header_container)
        root_layout.addWidget(body_container)
        titulo = QLabel("Central de Noticias")
        titulo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(titulo)

        scrollarea = QScrollArea()
        body_layout.addWidget(scrollarea)

        scroll_container = QWidget()
        scroll_container.setMinimumWidth(scrollarea.viewport().width())
        scroll_layout = QGridLayout(scroll_container)

        scrollarea.setWidgetResizable(True)
        scrollarea.setWidget(scroll_container)

        cols = 3

        for i in range(len(noticias)):
            row = i // cols
            col = i % cols

            noticia_card = QFrame()
            noticia_card.setObjectName("noticia-card")
            noticia_card_layout = QVBoxLayout(noticia_card)
            noticia_card.setMaximumWidth(WIDTH // 3)

            label_titulo = QLabel(noticias[i].title)
            label_titulo.setObjectName("noticia-title-label")
            label_titulo.setWordWrap(True)
            fecha_formateada = format_date(noticias[i].published)
            # label_fecha = QLabel(noticias[i].published)
            label_fecha = QLabel(fecha_formateada)
            label_fecha.setObjectName("noticia-fecha-label")
            link_button = QPushButton("Ir")
            link_button.setObjectName("")
            _ = link_button.setProperty("url", noticias[i].link)
            _ = link_button.clicked.connect(self.open_link_in_browser)
            noticia_card_layout.addWidget(label_titulo)
            noticia_card_layout.addWidget(label_fecha)
            noticia_card_layout.addWidget(link_button)
            scroll_layout.addWidget(noticia_card, row, col)
        self.setCentralWidget(root_container)

    def open_link_in_browser(self):
        btn = self.sender() 
        _ = webbrowser.open(btn.property("url"))

class Noticia():
    def __init__(self, title: str, published: str, link: str,):
        self.title: str = title
        self.published: str = published
        self.link: str = link

noticias: list[Noticia] = []
LAPSO = "24h"

client = GoogleNewsClient(
    language="es",
    country="AR",
    requests_per_minute=60,
    cache_ttl=300
    )

def load_qss(path: str):
    with open(path, "r") as f:
        return f.read()

def ordenar_noticias():
    print("ORDENADO")

def buscar_tema(tema: str):
    articles = []
    try: 
        articles = client.search(tema, when=LAPSO, max_results=50)
        return articles 
    except Exception as e: 
        print(f"Error: ${e}")

def format_date(fecha: str):
    parsed = parsedate_to_datetime(fecha)
    # format =  datetime.datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S")
    fecha = parsed.strftime("%H:%M\n%d %b %y\n%Z")
    return fecha
    

def custom_news() -> list[Noticia]:
    temas: list[Noticia] = []
    for i in range(9):
        n = Noticia(title=f"Lorem Impsum {i}", published="2026", link="localhost.com")
        temas.append(n)
    return temas

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_red.xml", css_file="./style.css")

    # temas_israel = custom_news()
    topicos = []

    topicos = buscar_tema("Israel")
    if topicos:
        for topico in topicos:
            n = Noticia(
                    title=topico["title"],
                    published=topico["published"],
                    link=topico["link"],
                    )
            noticias.append(n)
            # noticias.append(tema)

    ordenar_noticias()
    win = MainWindow()

    win.show()
    _ = app.exec()


if __name__ == "__main__":
    main()
    del client
