from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup, QListWidget, QFileDialog
import os 
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
app = QApplication([])
win = QWidget()
btn_dir = QPushButton("Папка")

win.resize(700, 400)
left = QPushButton('лево')
ridht = QPushButton('право')
zrk = QPushButton('зеркало')
rzk = QPushButton('резкость')
BLUR = QPushButton('Ч/Б')
list_ = QListWidget()
prin = QLabel('картинка')


row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(list_)
row1 = QHBoxLayout()
row1.addWidget(left)
row1.addWidget(ridht)
row1.addWidget(zrk)
row1.addWidget(rzk)
row1.addWidget(BLUR)
col2.addWidget(prin, 95) 
col2.addLayout(row1)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, exetensions):
    result = []
    for i in files:
        for r in exetensions:
#            if filename.endswith(exetensions): - посмотри на переменные в цикле
            if i.endswith(r):
#                result.append(filename)
                result.append(i)
    return(result)

def showFilenamesList():
    exetensions = ['.jpg', '.png', '.gif', '.jpeg', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), exetensions) 
    list_.clear()
    for e in filenames:
#        list_.addItem(filenames) - опять переменные
        list_.addItem(e)

class ImageProcessor():
    def __init__(self): #создай конструктор класса
        self.image = None
        self.original = None
        self.dir = None#ima
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        prin.hide()
        pixmapimage = QPixmap(path)
        w, h = prin.width(), prin.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        prin.setPixmap(pixmapimage)
        prin.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_left(self):#НА ЛЕВО
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_ridht(self):#НА ПРАВО
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip (self):#ЗЕРКАЛО
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)    

    def do_sharpness (self):

        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if list_.currentRow() >= 0:
        filename = list_.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


#(Image.Sharpness)

list_.currentRowChanged.connect(showChosenImage)

rzk.clicked.connect(workimage.do_sharpness)
BLUR.clicked.connect(workimage.do_bw)
ridht.clicked.connect(workimage.do_ridht)
left.clicked.connect(workimage.do_left)
zrk.clicked.connect(workimage.do_flip)
btn_dir.clicked.connect(showFilenamesList)
win.show()
app.exec()