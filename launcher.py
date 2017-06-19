# -*- coding: cp949 -*-
loopFlag = 1
from tkinter import font
from internetbook import*

#�̹��� ���---------------------------------------
from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from Pw import *
#--------------------------------------------------

server = "apis.data.go.kr"
regKey = 'XhKqnYiL44B3YdVVzKn2K2HUJ0tJJMUAAveunEp5YXfcfJhkpnUmo98E%2FlRE1X5CjqWTRCstJYzKwAHNCZ8lVQ%3D%3D'

import tkinter.messagebox

RenderText = None
DepRenderText = None
g_Tk = None
showList = []


def InitTopText():
    TempFont = font.Font(g_Tk, size =20, weight = 'bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text = "[���� ���� ã�� ����]")
    MainText.pack()
    MainText.place(x=350)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)

    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=163, y=58)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=12, height=1, borderwidth=12, relief='ridge'
                            ,yscrollcommand = ListBoxScrollbar.set)
    ListBoxScrollbar.config(command=SearchListBox.yview)

    SearchListBox.insert(1, "��ġ��ݰ˻�")
    SearchListBox.insert(2, "�̸���ݰ˻�")
    SearchListBox.insert(3, "��ġ+�̸���ݰ˻�")
    #�ӽ�
    SearchListBox.insert(4, "�̹����˻�")



    SearchListBox.pack()
    SearchListBox.place(x=10, y=60)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font=TempFont, width=45, borderwidth=12, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=200, y=60)

def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=70, height=40, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=130)

    RenderTextScrollbar.config(command=RenderText.yview)

    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

def InitDepInfoRenderText():
    global DepRenderText
    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    DepRenderText = Text(g_Tk, width=50, height=40, borderwidth=12, relief='ridge')
    DepRenderText.pack()
    DepRenderText.place(x=600, y=130)

    DepRenderText.configure(state='disabled')

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=16, weight='bold', family='Consolas')

    SearchButton = Button(g_Tk, font=TempFont, text="�˻�", command=SearchButtonAction)
    #gmailButton = Button(g_Tk,font= TempFont, text="�̸��� ������", command = OpenMailWindow)
    #gmailButton = Button(g_Tk, font=TempFont, text="�ù� ������", command=SearchshowBoxAction)

    shootMailButton = Button(g_Tk, font=TempFont, text="�̸��� ������", command=SendGmail)

    #gmailButton.pack()
    SearchButton.pack()
    shootMailButton.pack()

    SearchButton.place(x=730, y = 65)
    #gmailButton.place(x=810, y = 45)
    shootMailButton.place(x = 810, y = 90)

#-----------------------------------------------------------------------------------------------------------
#�̹���
def MakeImage(ImageName):
     getDaumImageData(ImageName)
     #root = Tk()
     #root.geometry("1024x1024+500+200")

     url = str(ImageItemList[2][3])

     with urllib.request.urlopen(url) as u:
         raw_data = u.read()

     im = Image.open(BytesIO(raw_data))
     image = ImageTk.PhotoImage(im)

     label = Label(g_Tk, image = image, height=400, width=400)
     label.pack()
     label.place(x=300, y=0)

#-----------------------------------------------------------------------------------------------------------

def SendGmail():
    global showBox, showList
    # 0 / 3 / 6 / 9 / 12
    SearchIndex = showBox.curselection()[0]
    Label = SearchIndex // 3

    MailList = []
    for i in range(len(showList)):
        if showList[i][0] == Label:
            tempList = [showList[i][0], showList[i][1], showList[i][2], showList[i][3], showList[i][4], showList[i][5],
                        showList[i][6],
                        showList[i][7], showList[i][8]]
            MailList.append(tempList)

    sendMain(MailList)


#-----------------------------------------------------------------------------------------------------------
def InitMailTkSendButton(Tk_Label):
    TempFont = font.Font(Tk_Label, size=12, weight='bold', family='Consolas')
    gmailButton = Button(Tk_Label, font=TempFont, text="�̸��� ������", command=SendGmail)
    gmailButton.pack()
    gmailButton.place(x=300, y=500)

def InputMailTkLabel(Tk_Label, height):
    global InputLabel
    TempFont = font.Font(Tk_Label, size=15, weight='bold', family= '����ü')
    InputLabel = Entry(Tk_Label, font=TempFont, width=26, borderwidth=12, relief="ridge")
    InputLabel.pack()
    InputLabel.place(x=10, y=height)

def MailTk():
    mail_Tk = Tk()
    mail_Tk.geometry("450x600+750+200")

    #�̸�
    TempFont = font.Font(mail_Tk, size=20, weight='bold', family='a����')
    MainText = Label(mail_Tk, font=TempFont, text="���� ������")
    MainText.pack()
    MainText.place(x=20)

    for i in range(4):
        InputMailTkLabel(mail_Tk,100 + i * 80)

    InitMailTkSendButton(mail_Tk)

    url = "http://cfile10.uf.tistory.com/image/2710E53756D6D0601C650D"
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    label = Label(mail_Tk, image=image, height=400, width=400)
    label.pack()
    label.place(x=0, y=0)

    mail_Tk.mainloop()

def OpenMailWindow():
    MailTk()
    #sendMain()



#-----------------------------------------------------------------------------------------------------------
#����

def SearchButtonAction():
   global SearchListBox

   RenderText.configure(state = 'normal')
   RenderText.delete(0.0, END)
   SearchIndex = SearchListBox.curselection()[0]
   if SearchIndex == 0:                         #��ġ ��� �˻�
       SearchInfoAddr()
   elif SearchIndex == 1:                       #�̸� ��� �˻�
       SearchInfoName();
   elif SearchIndex == 2:                       #��ġ + �̸� ��� �˻�
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
        return temp(req.read())
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
        return temp(req.read())
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
        return temp(req.read())
        #return ExtractDataFromURI(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None


def temp(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    global itemElements , showBox , showList
    # global SList

    itemElements = tree.getiterator("item")  # return list type
    strXml.decode('utf-8')
    # print(itemElements)
    cnt = 0
    # ������ 69000������ rum = 69���� ����
    # SList = []
    ListBoxScrollbar = Scrollbar(g_Tk)

    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=163, y=58)

    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    showBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=0, height=27, borderwidth=12, relief='ridge'
                            , yscrollcommand=ListBoxScrollbar.set)
    index = 0
    #tempList = []
    #if len(tempList) > 0:
    #    tempList.clear()

    for item in itemElements:
        tempList = []

        #if len(tempList) > 0:
        #    tempList.clear()

        BigAdress = item.find("dutyAddr")  # ��
        # SmallAdress = item.find("Q1")  # ��
        QZ = item.find("dutyName")  # B : ���� C : �ǿ�
        Emergency = item.find("dutyEryn")  # �𸣰�����
        Tel = item.find("dutyTel1")  # ���ϴ³�
        JobDef = item.find("dutyInf")

        tempList += [cnt,QZ.text,BigAdress.text,Tel.text,Emergency.text]

        weekdaySTime = item.find("dutyTime1s")  # ���� ���۽ð�
        weekdayETime = item.find("dutyTime1c")  # ���� �����½ð�

        weekendSTime = item.find("dutyTime6s")  # ����� ���� ���۽ð�
        weekendETime = item.find("dutyTime6c")  # ����� ���� �����½ð�

        weekendSTimeH = item.find("dutyTime7s")  # �Ͽ��� ���� ���۽ð�
        weekendETimeH = item.find("dutyTime7c")  # �Ͽ��� ���� �����½ð�

        HolidaySTime = item.find("dutyTime8s")  # ������ ���� ���۽ð�
        HolidayETime = item.find("dutyTime8c")  # ������ ���� �����½ð�

        if weekdaySTime == None or weekdayETime == None:
            pass
        else:
            tempList += [weekdaySTime.text,weekdayETime.text]

        if weekendSTime == None or weekendETime == None:
            pass
        else:
            tempList += [weekendSTime.text,weekendETime.text]

        if weekendSTimeH == None or weekendETimeH == None:
            pass
        else:
            tempList += [weekendSTimeH.text, weekendETimeH.text]

        if HolidaySTime == None or HolidayETime == None:
            pass
        else:
            tempList += [HolidaySTime.text, HolidayETime.text]

        if JobDef != None:
            tempList += [JobDef.text]
        else:
            pass

        showList.append(tempList)

        showBox.insert(index, "�ּ�: " + BigAdress.text)
        showBox.insert(index, "��ȭ��ȣ: " + Tel.text)
        showBox.insert(index,"[" + str(cnt + 1) + "]" + "�����̸�: " + QZ.text)

        cnt  = cnt + 1

        if cnt >= 10:
            break

    showBox.pack()
    showBox.place(x = 10,y = 130)
    SearchshowBoxAction()

def SearchshowBoxAction():
    global showBox , showList , MailList ,DepRenderText
    #0 / 3 / 6 / 9 / 12
    SearchIndex = showBox.curselection()[0]
    Label = SearchIndex // 3

    MailList = []
    for i in range(len(showList)):
        if showList[i][0] == Label:
            tempList = [showList[i][0],showList[i][1],showList[i][2],showList[i][3],showList[i][4],showList[i][5],showList[i][6],
                        showList[i][7],showList[i][8]]
            MailList.append(tempList)

    #MakeImage(MailList[0][1])

    DepRenderText.insert(INSERT, "�����̸�: ")
    DepRenderText.insert(INSERT, MailList[0][1])
    DepRenderText.insert(INSERT, "�n")
    DepRenderText.insert(INSERT, "�ּ�: ")
    DepRenderText.insert(INSERT, MailList[0][2])
    DepRenderText.insert(INSERT, "�n")
    DepRenderText.insert(INSERT, "��ȭ��ȣ: ")
    DepRenderText.insert(INSERT, MailList[0][3])
    DepRenderText.insert(INSERT, "�n")

    if (MailList[0][4] == "1"):
        RenderText.insert(INSERT, "���޽� �")
    else:
        RenderText.insert(INSERT, "���޽� � ����")
        RenderText.insert(INSERT, "�n")

    RenderText.insert(INSERT, "���� ���� ���۽ð�:")
    RenderText.insert(INSERT, MailList[0][5])
    RenderText.insert(INSERT, "���� ���� ����ð�:")
    RenderText.insert(INSERT, MailList[0][5])
    RenderText.insert(INSERT, "�n")

    RenderText.insert(INSERT, "����� ���� ���۽ð�:")
    RenderText.insert(INSERT, MailList[0][6])
    RenderText.insert(INSERT, "����� ���� ����ð�:")
    RenderText.insert(INSERT, MailList[0][6])
    RenderText.insert(INSERT, "�n")

    RenderText.insert(INSERT, "�Ͽ��� ���� ���۽ð�:")
    RenderText.insert(INSERT, MailList[0][7])
    RenderText.insert(INSERT, "�Ͽ��� ���� ����ð�:")
    RenderText.insert(INSERT, MailList[0][7])
    RenderText.insert(INSERT, "�n")

    RenderText.insert(INSERT, "������ ���� ���۽ð�:")
    RenderText.insert(INSERT, MailList[0][8])
    RenderText.insert(INSERT, "������ ���� ����ð�:")
    RenderText.insert(INSERT, MailList[0][8])
    RenderText.insert(INSERT, "�n")


def ExtractDataFromURI(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    # print("�����")
    # Book ������Ʈ�� �����ɴϴ�.
    global itemElements
    #global SList

    itemElements = tree.getiterator("item")  # return list type
    strXml.decode('utf-8')
    #print(itemElements)
    cnt = 0
    # ������ 69000������ rum = 69���� ����
    #SList = []
    for item in itemElements:
        BigAdress = item.find("dutyAddr")  # ��
        # SmallAdress = item.find("Q1")  # ��
        QZ = item.find("dutyName")  # B : ���� C : �ǿ�
        Emergency = item.find("dutyEryn")  # �𸣰�����
        Tel = item.find("dutyTel1")  # ���ϴ³�
        JobDef = item.find("dutyInf")
        # HospitalName = item.find("QN")  # �����̸�

        weekdaySTime = item.find("dutyTime1s")  # ���� ���۽ð�
        weekdayETime = item.find("dutyTime1c")  # ���� �����½ð�

        weekendSTime = item.find("dutyTime6s")  # ����� ���� ���۽ð�
        weekendETime = item.find("dutyTime6c")  # ����� ���� �����½ð�

        weekendSTimeH = item.find("dutyTime7s")  # �Ͽ��� ���� ���۽ð�
        weekendETimeH = item.find("dutyTime7c")  # �Ͽ��� ���� �����½ð�

        HolidaySTime = item.find("dutyTime8s")  # ������ ���� ���۽ð�
        HolidayETime = item.find("dutyTime8c")  # ������ ���� �����½ð�

        # Num = item.find("rnum")

        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, cnt + 1)
        RenderText.insert(INSERT, "]")
        RenderText.insert(INSERT, "�����̸�: ")
        RenderText.insert(INSERT, QZ.text)
        RenderText.insert(INSERT, "�n")
        RenderText.insert(INSERT, "�ּ�: ")
        RenderText.insert(INSERT, BigAdress.text)
        RenderText.insert(INSERT, "�n")
        RenderText.insert(INSERT, "��ȭ��ȣ: ")
        RenderText.insert(INSERT, Tel.text)
        RenderText.insert(INSERT, "�n")
        RenderText.insert(INSERT,  "���޽� �����: ")

        if Emergency.text == 1:
            RenderText.insert(INSERT, "���޽� �")
        else:
            RenderText.insert(INSERT, "���޽� � ����")
        RenderText.insert(INSERT, "�n")

        if JobDef != None:
            RenderText.insert(INSERT, "��� ���� �󼼳���:")
            RenderText.insert(INSERT, JobDef.text)
            RenderText.insert(INSERT, "�n")
        else:
            RenderText.insert(INSERT, "��� ���� �󼼳��� ����")
            RenderText.insert(INSERT, "�n")

        if weekdaySTime == None or weekdayETime == None:
            pass
        else:
            RenderText.insert(INSERT, "���� ���� ���۽ð�:")
            RenderText.insert(INSERT, weekdaySTime.text)
            RenderText.insert(INSERT, "���� ���� ����ð�:")
            RenderText.insert(INSERT, weekdayETime.text)
            RenderText.insert(INSERT, "�n")

        if weekendSTime == None or weekendETime == None:
            pass
        else:
            RenderText.insert(INSERT, "����� ���� ���۽ð�:")
            RenderText.insert(INSERT, weekendSTime.text)
            RenderText.insert(INSERT, "����� ���� ����ð�:")
            RenderText.insert(INSERT, weekendETime.text)
            RenderText.insert(INSERT, "�n")

        if weekendSTimeH == None or weekendETimeH == None:
            pass
        else:
            RenderText.insert(INSERT, "�Ͽ��� ���� ���۽ð�:")
            RenderText.insert(INSERT, weekendSTimeH.text)
            RenderText.insert(INSERT, "�Ͽ��� ���� ����ð�:")
            RenderText.insert(INSERT, weekendETimeH.text)
            RenderText.insert(INSERT, "�n")

        if HolidaySTime == None or HolidayETime == None:
            pass
        else:
            RenderText.insert(INSERT, "������ ���� ���۽ð�:")
            RenderText.insert(INSERT,  HolidaySTime.text)
            RenderText.insert(INSERT, "������ ���� ����ð�:")
            RenderText.insert(INSERT,  HolidayETime.text)
            RenderText.insert(INSERT, "�n")

        RenderText.insert(INSERT, "�n�n")
        #print("�̸�:", QZ.text)
        #print("�ּ�:", BigAdress.text)
        #print("��ȭ��ȣ:", Tel.text)

        #if weekdaySTime == None or weekdayETime == None:
        #    pass
        #else:
        #    print("���� ���� ���۽ð�:", weekdaySTime.text, "���� ���� ���� �ð� ", weekdayETime.text)

        #if weekendSTime == None or weekendETime == None:
        #    pass
        #else:
        #    print("����� ���� ���۽ð�:", weekendSTime.text, "����� ���� ���� �ð� ", weekendETime.text)
        #if weekendSTimeH == None or weekendETimeH == None:
        #    pass
        #else:
        #    print("�Ͽ��� ���� ���۽ð�:", weekendSTimeH.text, "�Ͽ��� ���� ���� �ð� ", weekendETimeH.text)
        #if HolidaySTime == None or HolidayETime == None:
        #    pass
        #else:
        #    print("������ ���� ���۽ð�:", HolidaySTime.text, "������ ���� ���� �ð� ", HolidayETime.text)
        cnt = cnt + 1
        if cnt >= 10:
            break
        #print(cnt)
        # ���⿡ ���� �߰�
        #SList += []
        #print(" ")

    RenderText.insert(INSERT, "�� ���� ����:")
    RenderText.insert(INSERT,cnt)

#### Menu  implementation
def printMenu():
    print("\nWelcome! Book Manager Program (xml version)")
    print("========Menu==========")
    print("�ּҷ� ���� ã��!! : g")
    print("�̸����� ���� ã��!! : k")
    print("���� + �̸����� ���� ã��!! : s")
    print("========Menu==========")

    
def launcherFunction(menu):
    if menu ==  'l':
       pass
    elif menu == 'g': 
        address = str(input ('ã�� ���� ��ġ�� �Է����ּ���:'))
        ret = getBookDataFromISBN1(address)
    elif menu == 'k':
        name = str(input ('ã�� ������ �̸��� �Է����ּ���:'))
        ret = getBookDataFromName(name)
    elif menu == 's':
        address = str(input('ã�� ���� ��ġ�� �Է����ּ���:'))
        name = str(input('ã�� ������ �̸��� �Է����ּ���:'))
        ret = getBookDataFromISBN(address,name)
    else:
        print ("error : unknow menu key")

def Main():
    g_Tk = Tk()
    g_Tk.geometry("1000x700+750+200")
    InitTopText()
    InitSearchListBox()
    InitInputLabel()
    InitSearchButton()
    InitRenderText()
    #InitDepInfoRenderText()
    # DepRenderText()
    g_Tk.mainloop()


def ShowLoop():
    Title()
    Main()


ShowLoop()
#def QuitBookMgr():
#
#    global loopFlag
#    loopFlag = 0
#    BooksFree()
    
##### run #####
#while(loopFlag > 0):
##
#    printMenu()
#
#
#    menuKey = str(input('select menu :'))
#    launcherFunction(menuKey)
#
#
#
#
#
#else:
#    print ("Thank you! Good Bye")



