# -*- coding: cp949 -*-
#OpenAPI 와 관련된 것들
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

#################추가
import os
import sys
import urllib.request

##global
conn = None
itemElements = None
ImageItemList = []

#다음api
regKey = 'XhKqnYiL44B3YdVVzKn2K2HUJ0tJJMUAAveunEp5YXfcfJhkpnUmo98E%2FlRE1X5CjqWTRCstJYzKwAHNCZ8lVQ%3D%3D'

DaumRegKey = '1efb37404806e2bdc4373a41da338841'

# 네이버 OpenAPI 접속 정보 information
#server = "openapi.naver.com"

# 다음 OpenAPI 접속 정보 information
server = "apis.data.go.kr"
DaumServer = "apis.daum.net"

# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server,**user):
    str = "https://" + server + "/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def DaumUserURIBuilder(DaumServer,**user):
    str = "https://" + DaumServer + "/search/image" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def getDaumImageData(imageName):
    global DaumServer, DaumRegKey, conn, xml, ImageItemList

    Name = urllib.parse.quote(imageName)

    if conn == None:
        connectDaumPIServer()

    uri = DaumUserURIBuilder(DaumServer, apikey=DaumRegKey, q = Name, output = "xml")
    conn.request("GET", uri)
    req = conn.getresponse()

    if int(req.status) == 200:  # okay
        return extractImageData(req.read()) ,  ImageItemList
    else:
        print("OpenAPI request has been failed!! please retry")
        return None




def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def connectDaumPIServer():
    global conn, DaumServer
    conn = HTTPConnection(DaumServer)

#여기부분 수정
def getBookDataFromName(name):

    global server, regKey, conn
    encText = urllib.parse.quote(name)
    if conn == None:
        connectOpenAPIServer()
    # uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, servicekey=regKey, QN=encText, numOfRows="1000")
    conn.request("GET", uri)

    # 파싱 추가코드
    # request = urllib.request.Request(uri)
    # response = urllib.request.urlopen(request)
    # rescode = response.getcode()

    req = conn.getresponse()

    print(req.status)
    if int(req.status) == 200:  # okay
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None

def getBookDataFromISBN1(address):
    global server, regKey, conn

    encText = urllib.parse.quote(address)

    if conn == None :
        connectOpenAPIServer()
    #uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, servicekey=regKey, Q0 =  encText, numOfRows = "1000")
    conn.request("GET", uri)

    #파싱 추가코드
    #request = urllib.request.Request(uri)
    #response = urllib.request.urlopen(request)
    #rescode = response.getcode()

    req = conn.getresponse()


    print (req.status)
    if int(req.status) == 200 : #okay
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def getBookDataFromISBN(address,name):
    global server, regKey, conn

    encText = urllib.parse.quote(address)
    encText2 = urllib.parse.quote(name)

    if conn == None :
        connectOpenAPIServer()
    #uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, servicekey=regKey, Q0 =  encText, QN = encText2, numOfRows = "1000")
    conn.request("GET", uri)

    #파싱 추가코드
    #request = urllib.request.Request(uri)
    #response = urllib.request.urlopen(request)
    #rescode = response.getcode()

    req = conn.getresponse()


    print (req.status)
    if int(req.status) == 200 : #okay
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def extractImageData(strXml):
    global channelElements , itemListElements
    global ImageChannelList , ImageItemList

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    channelElements = tree.getiterator("channel")
    itemListElements = tree.getiterator("item")

    strXml.decode('utf-8')

    ImageChannelList = []

    if len(ImageItemList) > 0:
        ImageItemList.clear()

    showCnt = 0
    #한번만 받아옴
    for channel in channelElements:
        title = channel.find("title")
        dep = channel.find("description")
        link = channel.find("link")

        ImageChannelList += [title, dep, link]

    for item in itemListElements:
        width = item.find("width")
        height = item.find("height")
        cpn = item.find("cpname")
        url = item.find("image")

        ImageItemList.append([width.text, height.text, cpn.text, url.text])

        showCnt += 1
        if(showCnt >= 3):
            break



def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    global SList, itemElements
    itemElements = tree.getiterator("item")  # return list type
    strXml.decode('utf-8')

    cnt =0
    #데이터 69000개까지 rum = 69까지 존재
    for item in itemElements:
        BigAdress = item.find("dutyAddr")  # 도
        #SmallAdress = item.find("Q1")  # 구
        QZ = item.find("dutyName")  #  B : 병원 C : 의원
        QD = item.find("QD")  #  모르겠음ㅎ
        Tel = item.find("dutyTel1")  # 일하는날
        #HospitalName = item.find("QN")  # 병원이름


        weekdaySTime = item.find("dutyTime1s")    # 평일 시작시간
        weekdayETime = item.find("dutyTime1c")    # 평일 끝나는시간

        weekendSTime = item.find("dutyTime6s")     # 토요일 진료 시작시간
        weekendETime = item.find("dutyTime6c")     # 토요일 진료 끝나는시간

        weekendSTimeH = item.find("dutyTime7s")    # 일요일 진료 시작시간
        weekendETimeH = item.find("dutyTime7c")    # 일요일 진료 끝나는시간

        HolidaySTime = item.find("dutyTime8s")    #공휴일 진료 시작시간
        HolidayETime = item.find("dutyTime8c")    #공휴일 진료 끝나는시간

        #Num = item.find("rnum")

        print("이름:",QZ.text)
        print("주소:",BigAdress.text)
        print("전화번호:",Tel.text)
        if weekdaySTime ==None or weekdayETime == None :
            pass
        else:
            print("평일 진료 시작시간:",weekdaySTime.text, "평일 진료 종료 시간 ",weekdayETime.text)

        if weekendSTime == None or weekendETime == None :
            pass
        else:
            print("토요일 진료 시작시간:",weekendSTime.text, "토요일 진료 종료 시간 ",weekendETime.text)
        if weekendSTimeH == None or weekendETimeH == None:
            pass
        else:
            print("일요일 진료 시작시간:", weekendSTimeH.text, "일요일 진료 종료 시간 ", weekendETimeH.text)
        if HolidaySTime==None or HolidayETime == None:
           pass
        else:
            print("일요일 진료 시작시간:", HolidaySTime.text, "일요일 진료 종료 시간 ", HolidayETime.text)
        cnt = cnt +1
        print(cnt)
        #여기에 정보 추가
        SList += []
        print(" ")


def sendMain(List):
    global host, port
    html = ""
    #title = str(input ('Title :'))
    senderAddr = "c936891@gmail.com"
    recipientAddr = "gusdl576@naver.com"
    temp_str = " "
    temp_str3 = " "

    if(List[0][4] == "1"):
        temp_str2 = "응급실 운영함"
    else:
        temp_str2 = "응급실 운영안함"

    temp_str3 += "평일 진료시간: " + List[0][5] + "토요일 진료시간:" + List[0][6] + "일요일 진료시간: " + List[0][7] + "공휴일 진료시간" + List[0][8]
    temp_str += "병원이름: " +  List[0][1] + "    " +  "주소: " + List[0][2] + "    " + "전화번호: " + List[0][3] + "    " + temp_str2 + temp_str3

    msgtext = str(temp_str)
    passwd = "choi975813"
    #html = MakeHtmlDoc(msgtext)
    #msgtext = str(input ('Do you want to include book data (y/n):'))
    #if msgtext == 'y' :
    #    keyword = str(input ('input keyword to search:'))
    #    html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = "병원 정보"
    msg['From'] = "c936891@gmail.com"
    msg['To'] = "gusdl576@naver.com"
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    #msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400,' bad requst : please check the your url') # 잘 못된 요청라는 에러를 응답한다.
        
def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server 종료합니다.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
