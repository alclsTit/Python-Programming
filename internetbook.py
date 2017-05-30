# -*- coding: cp949 -*-
#OpenAPI 와 관련된 것들
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

##global
conn = None
#다음api
regKey = 'XhKqnYiL44B3YdVVzKn2K2HUJ0tJJMUAAveunEp5YXfcfJhkpnUmo98E%2FlRE1X5CjqWTRCstJYzKwAHNCZ8lVQ%3D%3D'

# 네이버 OpenAPI 접속 정보 information
#server = "openapi.naver.com"

# 다음 OpenAPI 접속 정보 information
server = "apis.data.go.kr"


# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server,**user):
    #네이버 검색URL
    # str = "http://" + server + "/search" + "?"

    #다음 검색 URL
    #" " 은 갯수가 정해지지 않은 사전형 문자열을 받는다
    str = "https://" + server + "/B552657/HsptlAsembySearchService/getHsptlMdcncFullDown" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

#여기부분 수정
def getBookDataFromISBN(pageNumber):
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    #uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, servicekey=regKey, pageNo=pageNumber, numOfRows = "1000")
    conn.request("GET", uri)
    
    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 : #okay
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def SearchData(Addr):
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()

    for i in range(69):
        #for j in range(1000):
        uri = userURIBuilder(server, servicekey = regKey, pageNo = str(i + 1), numOfRows = "1000")
        conn.request("GET", uri)
        req = conn.getresponse()

        if int(req.status) == 200:  # okay
            print("Book data downloading complete!")
            return  extractHospitalData(req.read(), Addr)
        else:
            print("OpenAPI request has been failed!! please retry")
            return None


def extractHospitalData(strXml,Addr):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")

    for item in itemElements:
        ItemAddr = item.find("dutyAddr")
        str(ItemAddr).split()
    print(Addr)

    #for item in itemElements:
    #    if

def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Book 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)

    #데이터 69000개까지 rum = 69까지 존재
    for item in itemElements:
        name = item.find("dutyName")  # 병원이름
        phone = item.find("dutyTel1")  # 병원전화번호
        ErynPhone = item.find("dutyTel3")  # 응급실 전화번호
        addr = item.find("dutyAddr")  # 병원주소
        Eryn = item.find("dutyEryn")  # 응급실운영여부
        etc = item.find("dutyEtc")  # 비고
        DespInfo = item.find("dutyInf")  # 상세내용

        weekdaySTime = item.find("dutyTime1s")    # 평일 시작시간
        weekdayETime = item.find("dutyTime1c")    # 평일 끝나는시간

        weekendSTime = item.find("dutyTime6s")     # 토요일 진료 시작시간
        weekendETime = item.find("dutyTime6c")     # 토요일 진료 끝나는시간

        weekendSTimeH = item.find("dutyTime7s")    # 일요일 진료 시작시간
        weekendETimeH = item.find("dutyTime7c")    # 일요일 진료 끝나는시간

        HolidaySTime = item.find("dutyTime8s")    #공휴일 진료 시작시간
        HolidayETime = item.find("dutyTime8c")    #공휴일 진료 끝나는시간

        Num = item.find("rnum")

        print(name.text)
        print(addr.text)
        print(phone.text)
        #print(DespInfo.text)
        #print(etc.text)
        print(Num.text)
        #rnum = 항목번호

        #print(ErynPhone)
        #print(Eryn)

        if len(name.text) > 0:
            return {"병원이름" : name.text, "대표전화": phone.text}

        #print (strTitle)
        #if len(strTitle.text) > 0 :
        #   return {"ISBN":isbn.text,"title":strTitle.text}

def sendMain():
    global host, port
    html = ""
    title = str(input ('Title :'))
    senderAddr = str(input ('sender email address :'))
    recipientAddr = str(input ('recipient email address :'))
    msgtext = str(input ('write message :'))
    passwd = str(input (' input your password of gmail account :'))
    msgtext = str(input ('Do you want to include book data (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('input keyword to search:'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
    
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
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
