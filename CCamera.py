## MAC : B0:C5:54:3A:D1:71
import numpy as np
import random
import socket
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import cv2

class CCamera():
    def __init__(self,ip,resL,resC):
        self.addrIP=ip
        self.resolutionL=resL
        self.resolutionC=resC
        self.image=np.zeros((resL,resC))
        self.imageOrigine=np.zeros((resL,resC))
        self.seuil=0
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        print("Connexion : ",self.addrIP)
        self.sock.connect((self.addrIP, 80))

    def deconnexion(self):
        print("Deconnexion : ",self.addrIP)
        self.sock.close()

    def captureImage(self):
        url = 'http://'+self.addrIP+'/Image.jpg'
        r = requests.get(url, auth=('admin', 'user2017'))
        ## Conversion en niveau de gris
        img=Image.open(BytesIO(r.content)).convert('L')
        img = np.array(img)
        self.resolutionL,self.resolutionC=img.shape
        ##Segmentation par seuillage
        seuil = 220
        self.seuil, self.image = cv2.threshold(image, seuil, 255, cv2.THRESH_BINARY)
        self.imageOrigine=img
        return img        

    def loadImage(self,chemin):
        img = cv2.imread(chemin,cv2.IMREAD_GRAYSCALE)
##        print(img.shape)
##        plt.imshow(img)
##        plt.show()
        self.imageOrigine = img
        self.seuil, self.image = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)##+cv2.THRESH_OTSU)
##        print(self.seuil)
        plt.imshow(self.image,cmap = 'gray')
        plt.show()
        self.resolutionL,self.resolutionC=img.shape

    def barycentre(self,img):
        ##Erosion Dilatation
        noyau = np.ones((5,5),np.int8)
        img = cv2.erode(self.image,noyau,1)
        img = cv2.dilate(img,noyau,1)
        ##Determination du contour
        x=y=0
        img2,contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy.any():
            cnt=contours[0]
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            x=int(x)
            y=int(y)
            ##Affichage du contour
            cv2.circle(self.imageOrigine,(x,y),int(radius),(0,255,0),2)
            plt.imshow(self.imageOrigine)
            plt.show()
        ##Renvoi des coordonnées du barycentre
        return ([x,self.resolutionL-y])
            
