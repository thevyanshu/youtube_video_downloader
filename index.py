from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from PyQt5.QtWebEngineWidgets import *

from PyQt5.uic import loadUiType
import urllib.request
import pafy
import humanize

ui,_ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        #self.InitUI()
        self.Handel_Button()
        self.YouTube()
        
    
    def Handel_Button(self):
        ## Handel all the buttons in the app
        #self.pushButton_4.clicked.connect(self.Download)
        self.pushButton_3.clicked.connect(self.Handel_Browse)
        
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        
        self.pushButton_6.clicked.connect(self.Playlist_Download)
        self.pushButton_2.clicked.connect(self.Playlist_Save_Browse)
        #self.pushButton_7.clicked.connect(self.YoutubePlayer)
    
    def Handel_progressive(self):
        ## calculate the progress
        pass
    
    def Handel_Browse(self):
        ## enable browsing to our os , pich save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All files(*.*)")
        print(save_location)
        
        self.lineEdit_4.setText(str(save_location))
    
    def YouTube(self, label="Youtube"):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://www.youtube.com"))
        self.tabWidget.addTab(browser,label)

    ################Browsing Youtube video #################################

    ################################################################
    ######For single Video #################################
    def Get_Video_Data(self):
        video_url = self.lineEdit_3.text()
        
        if video_url == '' :
            QMessageBox.warning(self, "Data Error", "Provide a valid video URL")
            
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)
            
            video_stream = video.allstreams
            for stream in video_stream:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} -{}".format(stream.mediatype, stream.extension , stream.quality, size)
                self.comboBox.addItem(data)
        
    def Download_Video(self):
        pass
    
    def Video_Progress(self):
        pass
    #################################################
    ############For playlist#########################
    
    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()
        
        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid playist URL or save location")
            
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']
            
            self.lcdNumber_2.display(len(playlist_videos))
            
            
        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))
        
        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()
        
        QApplication.processEvents()
        
        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()
            
            current_video_in_download += 1
            
    
    def Playlist_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar.setValue(download_percentage)
            #remaining_time = round(time/60 , 2)
            
            QApplication.processEvents()
            
    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)
    
        
        
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
