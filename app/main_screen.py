import sys
import subprocess
import time
from app.constants.Constants import Constants

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QColor

"""Main Screen Class"""


class MainScreen(QWidget):
    """ Base Function."""

    def __init__(self):
        super().__init__()
        self.product = Constants.APACHE_KAFKA
        self.open_file_text_field = QLineEdit()
        self.application_image = QLabel(self)
        self.setWindowTitle(Constants.APPLICATION_WINDOW_TITLE)
        self.setGeometry(300, 300, 500, 350)
        self.center()
        self.UI()

    """Main Screen UI"""

    def UI(self):
        main_wrapper = QVBoxLayout()

        header_wrapper = QHBoxLayout()
        content_wrapper = QHBoxLayout()

        application_title = QLabel(Constants.APPLICATION_TITLE, self)
        self.application_image.setPixmap(QPixmap(Constants.KAFKA_BASE_IMAGE).scaled(300, 100))

        # Header Wrapper Content.
        header_wrapper.setContentsMargins(80, 20, 20, 30)
        header_wrapper.addWidget(application_title)
        header_wrapper.addWidget(self.application_image)
        header_wrapper.addSpacing(30)

        # Choose File Wrapper
        version_wrapper = QVBoxLayout()

        file_wrapper = QVBoxLayout()
        radio_wrapper = QHBoxLayout()

        apache_kafka = QRadioButton(Constants.APACHE_KAFKA)
        apache_kafka.setChecked(True)
        apache_kafka.toggled.connect(lambda: self.productCheckedInRadioButton(apache_kafka))
        confluent_kafka = QRadioButton(Constants.CONFLUENT_KAFKA)
        choose_folder_button = QPushButton(Constants.CHOOSE_FOLDER)
        choose_folder_button.clicked.connect(self.chooseFile)
        radio_wrapper.addWidget(apache_kafka)
        radio_wrapper.addWidget(confluent_kafka)
        file_wrapper.addWidget(self.open_file_text_field)
        file_wrapper.addWidget(choose_folder_button)

        version_wrapper.addLayout(radio_wrapper)
        version_wrapper.addLayout(file_wrapper)
        version_wrapper.setContentsMargins(100, 10, 20, 30)

        # Start and Stop Button Content wrapper.
        button_wrapper = QVBoxLayout()
        start_button = QPushButton(Constants.START_BUTTON)
        start_button.clicked.connect(self.startkafka)
        start_button.setGeometry(30, 30, 30, 30)
        stop_button = QPushButton(Constants.STOP_BUTTON)
        stop_button.clicked.connect(self.stopKafka)
        stop_button.setGeometry(30, 30, 30, 30)
        button_wrapper.addWidget(start_button)
        button_wrapper.addWidget(stop_button)
        button_wrapper.setContentsMargins(100, 10, 20, 30)

        # Content wrapper
        content_wrapper.addLayout(button_wrapper)
        content_wrapper.addLayout(version_wrapper)

        # Main wrapper
        main_wrapper.addLayout(header_wrapper)
        main_wrapper.addLayout(content_wrapper)

        # Set layout.
        self.setLayout(main_wrapper)
        self.show()

    """Center the application to the screen"""

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    """Choose the file"""

    def chooseFile(self):
        print("Open File")
        file_path = QFileDialog.getExistingDirectory(self, Constants.SELECT_FOLDER, "", QFileDialog.ShowDirsOnly)
        print(file_path)
        is_file_path_empty = self.validateTextFieldEmpty(file_path)
        if not is_file_path_empty:
            self.open_file_text_field.setText(file_path)
            self.open_file_text_field.setCursorPosition(0)
            palette = QPalette()
            palette.setColor(QPalette.Base, QColor('darkGray'))
            palette.setColor(QPalette.Text, QColor('black'))
            self.open_file_text_field.setPalette(palette)
            self.open_file_text_field.setReadOnly(True)

    """Start the Kafka and Zookeeper Server"""

    def startkafka(self):
        print("startKafka")
        kafka_file_path = self.open_file_text_field.text()
        is_text_field_empty = self.validateTextFieldEmpty(kafka_file_path)
        zookeeper_config, kafka_config = self.configPathBasedOnProduct(self.product)
        if not is_text_field_empty:
            subprocess.Popen(["sh", Constants.ZOOKEEPER_START_SERVER_PATH, zookeeper_config],
                             cwd=kafka_file_path)
            time.sleep(3)
            subprocess.Popen(["sh", Constants.KAFKA_START_SERVER_PATH, kafka_config],
                             cwd=kafka_file_path)
        else:
            QMessageBox.information(self, "Alert", "Please select the kafka folder")

    """Stop the Kafka and Zookeeper Server"""

    def stopKafka(self):
        print("stopKafka")
        kafka_file_path = self.open_file_text_field.text()
        is_text_field_empty = self.validateTextFieldEmpty(kafka_file_path)
        if is_text_field_empty:
            QMessageBox.information(self, "Alert", "Please select the kafka folder")
        else:
            is_server_stop = self.stopServerAlert()
            if is_server_stop:
                subprocess.Popen(["sh", Constants.KAFKA_STOP_SERVER_PATH], cwd=kafka_file_path)
                time.sleep(1)
                subprocess.Popen(["sh", Constants.ZOOKEEPER_STOP_SERVER_PATH], cwd=kafka_file_path)
            else:
                print("OMG.. I gonna die after running a whole day.")

    """Close the main application"""

    def closeMainApplication(self, event):
        print("closeMainApplication")
        reply = QMessageBox.question(self, 'Close Application',
                                     "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    """Stop the server"""

    def stopServerAlert(self):
        print("stopServerAlert")
        reply = QMessageBox.question(self, 'Stop Server',
                                     "Are you sure to stop the server?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def validateTextFieldEmpty(self, stringToBeValidated):
        print("validateTextFieldNotEmpty")
        if stringToBeValidated != "":
            return False
        else:
            return True

    def configPathBasedOnProduct(self, productName):
        if productName == Constants.APACHE_KAFKA:
            return Constants.APACHE_ZOOKEEPER_START_SERVER_CONFIG, Constants.APACHE_KAFKA_START_SERVER_CONFIG
        elif productName == Constants.CONFLUENT_KAFKA:
            return Constants.CONFLUENT_ZOOKEEPER_START_SERVER_CONFIG, Constants.CONFLUENT_KAFKA_START_SERVER_CONFIG

    def productCheckedInRadioButton(self, button):
        if button.text() == Constants.APACHE_KAFKA:
            if button.isChecked():
                self.product = Constants.APACHE_KAFKA
            else:
                self.product = Constants.CONFLUENT_KAFKA
        else:
            self.product = Constants.CONFLUENT_KAFKA
        print(self.product)

"""Main Application"""


def main():
    app = QApplication(sys.argv)
    mainScreen = MainScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
