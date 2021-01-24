import requests,time,random
from lxml import etree
import pymysql
from fake_useragent import UserAgent

def get_url_name(url,dt):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    header = {'user-agent':ua}
    response = requests.get(url,headers=header)
    selector = etree.HTML(response.text)
    # 电影名称列表
    film_name = selector.xpath('//div[@class="hd"]/a/span[1]/text()')
    # 电影链接列表
    film_link = selector.xpath('//div[@class="hd"]/a/@href')

    for i in range(len(film_name)):
        dt[film_name[i]] = film_link[i]

    
def get_comment(moviedict,result):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    header = {'user-agent':ua}
       
    for name in moviedict.keys():
        link = moviedict[name] + 'comments?sort=new_score&status=P'
        response = requests.get(link,headers=header)       
        selector = etree.HTML(response.text)
        star = selector.xpath('//div[@class="comment"]/h3/span[2]/span[2]/@class')
        remark = selector.xpath('//div[@class="comment"]/p/span/text()')
        datime = selector.xpath('//div[@class="comment"]/h3/span[2]/span[@class="comment-time "]/text()')

        for i in range(len(star)):
            if star[i][7] == '-':
                result.append((name,0,remark[i],datime[i].strip()))
                continue
            result.append((name,star[i][7],remark[i],datime[i].strip()))
        time.sleep(5)


if __name__ == '__main__':
    urls = tuple(f'https://movie.douban.com/top250?start={ page * 25}&fliter=' for page in range(2))
    dt = {}
    result = []
    for page in urls:
        get_url_name(page,dt)
        time.sleep(5)

    get_comment(dt,result)
       
    conn = pymysql.connect(host='192.168.20.62',
                           user='testuser',
                           password='testpass',
                           database='testdb')
    try:
        with conn.cursor() as cursor:
            sql = 'insert into movie_test (name,stars,remark,date) values (%s,%s,%s,%s)'
            values = tuple(result)
            cursor.executemany(sql,values)
            print(tuple(result))
            print('executed')
            
        conn.commit()
    except Exception as e:
        print(f'insert error {e}')
    finally:
        conn.close()
