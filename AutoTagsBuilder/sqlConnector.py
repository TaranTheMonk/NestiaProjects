import mysql.connector
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dataResult = ''

    def resetDataResult(self):
        self.dataResult = ''

    def handle_data(self, data):
        self.dataResult = self.dataResult + data + ' '

def getNewsContent():
    newsContent = dict()
    conn = mysql.connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com'
                                   , user='readonly', password='nestiareadonly', database='news')
    cursor = conn.cursor()
    cursor.execute('select title, content from news where language_id = 1')
    queryResult = cursor.fetchall()

    parser = MyHTMLParser()
    for titleContentPair in queryResult:
        parser.feed(titleContentPair[1])
        newsContent.update({titleContentPair[0]: parser.dataResult})
        parser.resetDataResult()
    print('Successfully get news content.')
    return newsContent