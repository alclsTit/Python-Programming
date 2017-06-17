from tkinter import *
from tkinter import font
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk


# openapi로 이미지 url을 가져옴.
#url = "http://tong.visitkorea.or.kr/cms/resource/74/2396274_image2_1.JPG"

#전역
nextFlag = False

def Title():
    title_Tk = Tk()
    title_Tk.geometry("800x600+500+200")

    image = ImageTk.PhotoImage(file = "ScTitle.png")
    Screen = Label(title_Tk, image=image, height=600, width=800)
    Screen.pack()
    Screen.place(x=0, y=0)

    NextButton(title_Tk)
    title_Tk.mainloop()

def NextButton(Screen):
    TempFont = font.Font(Screen, size=16, weight='bold', family='Consolas')
    gmailButton = Button(Screen, font=TempFont, text="시작 하기", command = FlagFunc)
    gmailButton.pack()
    gmailButton.place(x=350, y=500)


def FlagFunc():
    global nextFlag
    nextFlag = True


def kkk():
    root = Tk()
    root.geometry("600x500+500+200")

    url = "http://cfile222.uf.daum.net/image/143A62144CBBFAE56F6CF6"
    # url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&ie=utf8&query=%EC%9A%B0%EB%A6%AC%EB%82%98%EB%9D%BC+%EC%A7%80%EB%8F%84#imgId=blog22501031%7C33%7C220175531420_20&vType=rollout"
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(root, image=image, height=400, width=400)
    label.pack()
    label.place(x=0, y=0)
    root.mainloop()