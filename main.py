from PIL import Image
from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import math


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._make_ui()

    input_image_path = output_image_path = ""

    def choose_input_file(self):
        self.input_image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Выберите файл", "input.png", "PNG изображения (*.png)"
        )
        if self.input_image_path:
            self.input_file_path_label.setText(self.input_image_path)
            self.input_file_path_label.adjustSize()

    def choose_output_file(self):
        self.output_image_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Выберите файл", "output.png", "PNG изображения (*.png)"
        )
        if self.output_image_path:
            self.output_file_path_label.setText(self.output_image_path)
            self.output_file_path_label.adjustSize()

    def get_ratio(self, pixels):
        heigh = math.ceil(math.sqrt(pixels))
        return (heigh, heigh)

    def start(self):
        if self.input_image_path and self.output_image_path:
            input_image = Image.open(self.input_image_path)
            input_image_pixels = input_image.load()
            colors = set()
            for y in range(input_image.height):
                for x in range(input_image.width):
                    colors.add(input_image_pixels[(x, y)])

            output_image = Image.new("RGBA", self.get_ratio(len(colors)))
            output_image_pixels = output_image.load()
            colors_iter = iter(
                sorted(
                    list(colors)
                    + [
                        (255, 255, 255, 255)
                        for _ in range(
                            output_image.width * output_image.height - len(colors)
                        )
                    ],
                    key=lambda x: (0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], x[3]),
                ),
            )
            for y in range(output_image.height):
                for x in range(output_image.width):
                    output_image_pixels[(x, y)] = next(colors_iter)
            output_image.save(self.output_image_path)
            QtWidgets.QMessageBox.information(
                None,
                "Готово!",
                f"Результат сохранен по пути {self.output_image_path}\nКоличество цветов: {len(colors)}",
            )
            scaled_pixmap = QPixmap(self.output_image_path).scaled(
                self.pic.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation
            )
            self.pic.setPixmap(scaled_pixmap)
        else:
            QtWidgets.QMessageBox.critical(
                None, "Не указаны пути", "Укажите пути к файлам"
            )

    def _make_ui(self):
        self.setFixedSize(500, 300)
        self.setWindowTitle("FVColor")

        self.input_file_button = QtWidgets.QPushButton(self)
        self.input_file_button.move(20, 20)
        self.input_file_button.setText("Исходный файл")
        self.input_file_button.clicked.connect(self.choose_input_file)

        self.input_file_path_label = QtWidgets.QLabel(self)
        self.input_file_path_label.move(140, 0)
        font = self.input_file_path_label.font()
        font.setPointSize(8)
        self.input_file_path_label.setFont(font)
        self.input_file_path_label.setWordWrap(True)

        self.output_file_button = QtWidgets.QPushButton(self)
        self.output_file_button.move(20, 50)
        self.output_file_button.setText("Выходной файл")
        self.output_file_button.clicked.connect(self.choose_output_file)

        self.output_file_path_label = QtWidgets.QLabel(self)
        self.output_file_path_label.move(140, 70)
        font = self.output_file_path_label.font()
        font.setPointSize(8)
        self.output_file_path_label.setFont(font)
        self.output_file_path_label.setWordWrap(True)

        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.move(20, 80)
        self.start_button.setText("Стартуем")
        self.start_button.clicked.connect(self.start)

        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setGeometry(300, 0, 2, 300)

        self.pic = QtWidgets.QLabel(self)
        self.pic.move(320, 20)
        self.pic.setFixedSize(160, 160)
        self.pic.setScaledContents(True)

        self.show()
        sys.exit(app.exec())


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
