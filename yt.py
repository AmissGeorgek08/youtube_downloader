#imports
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from pytube import YouTube

#main class
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    #ui
    def initUI(self):

        #labels, widgets, buttons
        url_label = QLabel('YouTube URL:', self)
        self.url_edit = QLineEdit(self)
        self.folder_label = QLabel('', self)
        folder_button = QPushButton('Select Folder', self)
        folder_button.clicked.connect(self.select_folder)
        self.audio_button = QRadioButton('Audio', self)
        video_button = QRadioButton('Video', self)
        video_button.setChecked(True)
        download_button = QPushButton('Download', self)
        download_button.clicked.connect(self.download)
        self.message_label = QLabel('', self)
        layout = QVBoxLayout()
        layout.addWidget(url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.folder_label)
        layout.addWidget(folder_button)
        layout.addWidget(self.audio_button)
        layout.addWidget(video_button)
        layout.addWidget(download_button)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

        #window
        self.setWindowTitle('YouTube Downloader')
        self.setWindowIcon(QtGui.QIcon('logo.png')) #logo image png file
        self.resize(400, 500)
        self.show()

    #select folder
    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_name = QFileDialog.getExistingDirectory(self, 'Select Folder', '/', options=options)
        self.folder_name = folder_name
        self.folder_label.setText(f'Folder: {folder_name}')

    #download file
    def download(self):
        url = self.url_edit.text()
        try:
            yt = YouTube(url)
            if self.audio_button.isChecked():
                stream = yt.streams.get_audio_only()
                out_file = stream.download(self.folder_name)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            else:
                stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
                stream.download(self.folder_name)
            self.message_label.setStyleSheet('color: green')
            self.message_label.setText('Download Completed!')
            self.url_edit.setText('')

        #error checker
        except Exception as e:
            self.message_label.setStyleSheet('color: red')
            self.message_label.setText(str(e))

#run command
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    sys.exit(app.exec_())