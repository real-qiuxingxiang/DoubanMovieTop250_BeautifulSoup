import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_html(url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    timeout = random.choice(range(80, 100))
    while True:
        try:
            response = requests.get(url, headers = header, timeout = timeout)
            response.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
        except socket.error as e:
            print(e)
            time.sleep(random.choice(range(0, 60)))
        except http.client.BadStatusLine as e:
            print(e)
            time.sleep(random.choice(range(30, 60)))
        except http.client.IncompleteRead as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
    return response.text
    
def get_data(html_text, rank):
    result = []
    bs = BeautifulSoup(html_text, "html.parser")
    content = bs.find_all('div', {'class': 'info'})
    for movie in content:
        temp = []
        temp.append(rank)
        rank += 1
        for span in movie.find_all('span','title'):
            temp.append(span.text.replace('/', ''))
            if len(movie.find_all('span','title')) == 1:
                temp.append(movie.find('span','other').text.replace('/', ''))
        for span in movie.find_all('span','rating_num'):
            temp.append(span.text)
        temp.append(movie.find('p').text)
        a_tag = movie.find('a')
        temp.append(a_tag['href'])
        result.append(temp)
    return result
    
def data_output(data, filename):
    with open(filename, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)
        
if __name__ == '__main__':
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(i)
        html = get_html(url)
        result = get_data(html, i+1)
        data_output(result, 'Top250.csv')
        