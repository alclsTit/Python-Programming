# -*- coding: cp949 -*-
loopFlag = 1
from tkinter import font
from internetbook import*

#이미지 모듈---------------------------------------
from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk

#--------------------------------------------------

server = "apis.data.go.kr"
regKey = 'XhKqnYiL44B3YdVVzKn2K2HUJ0tJJMUAAveunEp5YXfcfJhkpnUmo98E%2FlRE1X5CjqWTRCstJYzKwAHNCZ8lVQ%3D%3D'

import tkinter.messagebox

RenderText = None

def InitTopText():
    TempFont = font.Font(g_Tk, size =20, weight = 'bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text = "[전국 병원 찾기 서비스]")
    MainText.pack()
    MainText.place(x=20)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=23, height=4, borderwidth=14, relief='ridge'
                            ,yscrollcommand=ListBoxScrollbar.set)
    SearchListBox.insert(0, "위치기반검색")
    SearchListBox.insert(1, "이름기반검색")
    SearchListBox.insert(2, "위치+이름기반검색")
    #임시
    SearchListBox.insert(3, "이미지검색")

    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font=TempFont, width=26, borderwidth=12, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=165)

def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)
    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')

    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    gmailButton = Button(g_Tk,font= TempFont, text="이메일 보내기", command = OpenMailWindow)

    gmailButton.pack()
    SearchButton.pack()

    SearchButton.place(x=330, y=165)
    gmailButton.place(x=300, y = 100)

#-----------------------------------------------------------------------------------------------------------
#이미지
def MakeImage(ImageName):
     getDaumImageData(ImageName)
     root = Tk()
     root.geometry("1024x1024+500+200")

     url = str(ImageItemList[0][3])
     with urllib.request.urlopen(url) as u:
         raw_data = u.read()


     with urllib.request.urlopen(url) as u:
         raw_data = u.read()

     im = Image.open(BytesIO(raw_data))
     image = ImageTk.PhotoImage(im)

     #Label()
     #ImageHeight = ImageItemList[0][1]
     #ImageWidth = ImageItemList[0][0]

     label = Label(root, image = image, height=400, width=400)
     label.pack()
     label.place(x=0, y=0)

     root.mainloop()

#-----------------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------------------------
def InitMailTkSendButton(Tk_Label):
    TempFont = font.Font(Tk_Label, size=12, weight='bold', family='Consolas')
    gmailButton = Button(Tk_Label, font=TempFont, text="이메일 보내기", command=SendGmail)
    gmailButton.pack()
    gmailButton.place(x=300, y=500)

def InputMailTkLabel(Tk_Label, height):
    global InputLabel
    TempFont = font.Font(Tk_Label, size=15, weight='bold', family= '굴림체')
    InputLabel = Entry(Tk_Label, font=TempFont, width=26, borderwidth=12, relief="ridge")
    InputLabel.pack()
    InputLabel.place(x=10, y=height)

def MailTk():
    mail_Tk = Tk()
    mail_Tk.geometry("450x600+750+200")

    #이름
    TempFont = font.Font(mail_Tk, size=20, weight='bold', family='a낙서')
    MainText = Label(mail_Tk, font=TempFont, text="메일 보내기")
    MainText.pack()
    MainText.place(x=20)

    for i in range(4):
        InputMailTkLabel(mail_Tk,100 + i * 80)

    InitMailTkSendButton(mail_Tk)

    mail_Tk.mainloop()

def OpenMailWindow():
    MailTk()
    #sendMain()
    
def SendGmail():
    RenderText.insert(INSERT, "이메일이쟝")


#-----------------------------------------------------------------------------------------------------------
#메일

def SearchButtonAction():
   global SearchListBox

   RenderText.configure(state = 'normal')
   RenderText.delete(0.0, END)
   SearchIndex = SearchListBox.curselection()[0]
   if SearchIndex == 0:                         #위치 기반 검색
       SearchInfoAddr()
   elif SearchIndex == 1:                       #이름 기반 검색
       SearchInfoName();
   elif SearchIndex == 2:                       #위치 + 이름 기반 검색
       SearchInfoAddrAndName()
   elif SearchIndex == 3:
       MakeImage(InputLabel.get())


   RenderText.configure(state='disabled')

def SearchInfoAddrAndName():
    import http.client
    from xml.dom.minidom import parse, parseString
    global server, regKey
    conn = http.client.HTTPConnection(server)

    temp = str(InputLabel.get()).split()

    address = temp[0]
    name = temp[len(temp) - 1]

    encText = urllib.parse.quote(address)
    encText2 = urllib.parse.quote(name)

    uri = userURIBuilder(server, servicekey=regKey, Q0=encText, QN = encText2, numOfRows="100")
    conn.request("GET", uri)

    req = conn.getresponse()
    if int(req.status) == 200:  # okay
        return ExtractDataFromURI(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None

def SearchInfoName():
    import http.client
    from xml.dom.minidom import parse, parseString

    global server, regKey
    conn = http.client.HTTPConnection(server)
    address = InputLabel.get()
    encText = urllib.parse.quote(address)

    uri = userURIBuilder(server, servicekey=regKey, Q0=encText, numOfRows="100")
    conn.request("GET", uri)

    req = conn.getresponse()
    if int(req.status) == 200:  # okay
        return ExtractDataFromURI(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None

def SearchInfoAddr():
    import http.client
    from xml.dom.minidom import parse, parseString

    global server,regKey
    conn = http.client.HTTPConnection(server)
    name = InputLabel.get()
    encText2 = urllib.parse.quote(name)

    uri = userURIBuilder(server, servicekey=regKey, QN = encText2, numOfRows="100")
    conn.request("GET",uri )

    req = conn.getresponse()
    if int(req.status) == 200:  # okay
        return ExtractDataFromURI(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None

def ExtractDataFromURI(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    # print("디버그")
    # Book 엘리먼트를 가져옵니다.
    global itemElements
    #global SList

    itemElements = tree.getiterator("item")  # return list type
    strXml.decode('utf-8')
    #print(itemElements)
    cnt = 0
    # 데이터 69000개까지 rum = 69까지 존재
    #SList = []
    for item in itemElements:
        BigAdress = item.find("dutyAddr")  # 도
        # SmallAdress = item.find("Q1")  # 구
        QZ = item.find("dutyName")  # B : 병원 C : 의원
        Emergency = item.find("dutyEryn")  # 모르겠음ㅎ
        Tel = item.find("dutyTel1")  # 일하는날
        JobDef = item.find("dutyInf")
        # HospitalName = item.find("QN")  # 병원이름

        weekdaySTime = item.find("dutyTime1s")  # 평일 시작시간
        weekdayETime = item.find("dutyTime1c")  # 평일 끝나는시간

        weekendSTime = item.find("dutyTime6s")  # 토요일 진료 시작시간
        weekendETime = item.find("dutyTime6c")  # 토요일 진료 끝나는시간

        weekendSTimeH = item.find("dutyTime7s")  # 일요일 진료 시작시간
        weekendETimeH = item.find("dutyTime7c")  # 일요일 진료 끝나는시간

        HolidaySTime = item.find("dutyTime8s")  # 공휴일 진료 시작시간
        HolidayETime = item.find("dutyTime8c")  # 공휴일 진료 끝나는시간

        # Num = item.find("rnum")

        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, cnt + 1)
        RenderText.insert(INSERT, "]")
        RenderText.insert(INSERT, "병원이름: ")
        RenderText.insert(INSERT, QZ.text)
        RenderText.insert(INSERT, "굈")
        RenderText.insert(INSERT, "주소: ")
        RenderText.insert(INSERT, BigAdress.text)
        RenderText.insert(INSERT, "굈")
        RenderText.insert(INSERT, "전화번호: ")
        RenderText.insert(INSERT, Tel.text)
        RenderText.insert(INSERT, "굈")
        RenderText.insert(INSERT,  "응급실 운영여부: ")

        if Emergency.text == 1:
            RenderText.insert(INSERT, "응급실 운영")
        else:
            RenderText.insert(INSERT, "응급실 운영 안함")
        RenderText.insert(INSERT, "굈")

        if JobDef != None:
            RenderText.insert(INSERT, "기관 설명 상세내용:")
            RenderText.insert(INSERT, JobDef.text)
            RenderText.insert(INSERT, "굈")
        else:
            RenderText.insert(INSERT, "기관 설명 상세내용 없음")
            RenderText.insert(INSERT, "굈")

        if weekdaySTime == None or weekdayETime == None:
            pass
        else:
            RenderText.insert(INSERT, "평일 진료 시작시간:")
            RenderText.insert(INSERT, weekdaySTime.text)
            RenderText.insert(INSERT, "평일 진료 종료시간:")
            RenderText.insert(INSERT, weekdayETime.text)
            RenderText.insert(INSERT, "굈")

        if weekendSTime == None or weekendETime == None:
            pass
        else:
            RenderText.insert(INSERT, "토요일 진료 시작시간:")
            RenderText.insert(INSERT, weekendSTime.text)
            RenderText.insert(INSERT, "토요일 진료 종료시간:")
            RenderText.insert(INSERT, weekendETime.text)
            RenderText.insert(INSERT, "굈")

        if weekendSTimeH == None or weekendETimeH == None:
            pass
        else:
            RenderText.insert(INSERT, "일요일 진료 시작시간:")
            RenderText.insert(INSERT, weekendSTimeH.text)
            RenderText.insert(INSERT, "일요일 진료 종료시간:")
            RenderText.insert(INSERT, weekendETimeH.text)
            RenderText.insert(INSERT, "굈")

        if HolidaySTime == None or HolidayETime == None:
            pass
        else:
            RenderText.insert(INSERT, "공휴일 진료 시작시간:")
            RenderText.insert(INSERT,  HolidaySTime.text)
            RenderText.insert(INSERT, "공휴일 진료 종료시간:")
            RenderText.insert(INSERT,  HolidayETime.text)
            RenderText.insert(INSERT, "굈")

        RenderText.insert(INSERT, "굈굈")
        #print("이름:", QZ.text)
        #print("주소:", BigAdress.text)
        #print("전화번호:", Tel.text)

        #if weekdaySTime == None or weekdayETime == None:
        #    pass
        #else:
        #    print("평일 진료 시작시간:", weekdaySTime.text, "평일 진료 종료 시간 ", weekdayETime.text)

        #if weekendSTime == None or weekendETime == None:
        #    pass
        #else:
        #    print("토요일 진료 시작시간:", weekendSTime.text, "토요일 진료 종료 시간 ", weekendETime.text)
        #if weekendSTimeH == None or weekendETimeH == None:
        #    pass
        #else:
        #    print("일요일 진료 시작시간:", weekendSTimeH.text, "일요일 진료 종료 시간 ", weekendETimeH.text)
        #if HolidaySTime == None or HolidayETime == None:
        #    pass
        #else:
        #    print("공휴일 진료 시작시간:", HolidaySTime.text, "공휴일 진료 종료 시간 ", HolidayETime.text)
        cnt = cnt + 1
        if cnt >= 10:
            break
        #print(cnt)
        # 여기에 정보 추가
        #SList += []
        #print(" ")

    RenderText.insert(INSERT, "총 병원 갯수:")
    RenderText.insert(INSERT,cnt)

#### Menu  implementation
def printMenu():
    print("\nWelcome! Book Manager Program (xml version)")
    print("========Menu==========")
    print("주소로 병원 찾기!! : g")
    print("이름으로 병원 찾기!! : k")
    print("지역 + 이름으로 병원 찾기!! : s")
    print("========Menu==========")

    
def launcherFunction(menu):
    if menu ==  'l':
       pass
    elif menu == 'g': 
        address = str(input ('찾을 병원 위치를 입력해주세요:'))
        ret = getBookDataFromISBN1(address)
    elif menu == 'k':
        name = str(input ('찾을 병원의 이름을 입력해주세요:'))
        ret = getBookDataFromName(name)
    elif menu == 's':
        address = str(input('찾을 병원 위치를 입력해주세요:'))
        name = str(input('찾을 병원의 이름을 입력해주세요:'))
        ret = getBookDataFromISBN(address,name)
    else:
        print ("error : unknow menu key")


g_Tk = Tk()
g_Tk.geometry("450x600+750+200")
DataList = []
InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
g_Tk.mainloop()


def QuitBookMgr():

    global loopFlag
    loopFlag = 0
    BooksFree()
    
##### run #####
while(loopFlag > 0):

    printMenu()


    menuKey = str(input('select menu :'))
    launcherFunction(menuKey)





else:
    print ("Thank you! Good Bye")



