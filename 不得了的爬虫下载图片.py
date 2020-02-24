#!/usr/bin/python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2018.02.05
"""Capture pictures from sina-weibo with user_id."""
import re
import os
import platform,requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

def _get_path(uid):
    path = {
        'Windows': 'D:/乃木坂46/Pictures' + uid,

    }.get(platform.system())
    if not os.path.isdir(path):
        os.makedirs(path)
    return path
# 获取安装路径
def _get_html(url, headers):
    try:

        req = urllib.request.Request(url, headers = headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')  # 使用UTF-8解码解决中文乱码
        '''
        req = requests.get(url,headers = headers)
        req.encoding = req.apparent_encoding
        html = req.text '''
    except Exception as e:
        print("get %s failed" % url)
        return None
    return html
# 通过urllib库打开每个要爬虫的网页
def _capture_images(uid, headers, path):
    filter_mode = 0      # 0-all 1-original 2-pictures
    num_pages = 1
    num_blogs = 0
    num_imgs = 0
    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'   # 这个东西不变存储所有的照片
    imglist_pattern = re.compile(imglist_reg)  # 转换为正则对象
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)
    print('start capture picture of uid:' + uid)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (uid, filter_mode, num_pages)
        # 1. get html of each page url
        html = _get_html(url, headers)
        # 2. parse（解析） the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "lxml")
        # <div class="c" id="M_G4gb5pY8t"><div>
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False) # 通过attrs寻找tag（标签） 且查找的均为直接字节点
        num_blogs += len(blogs)
        imgurls = []
        for blog in blogs:
            blog = str(blog)  # 按页查找
            imglist_url = imglist_pattern.findall(blog)
            if not imglist_url:
                # 2.1 get img-url from blog that have only one pic
                imgurls += img_pattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = _get_html(imglist_url[0], headers)   #先获取组图页面的链接
                imgurls += img_pattern.findall(html)
        if not imgurls:
            print('capture complete!')
            print('captured pages:%d, blogs:%d, imgs:%d' % (num_pages, num_blogs, num_imgs))
            print('directory:' + path)
            break
        # 3. download all the imgs from each imgList
        print('PAGE %d with %d images' % (num_pages, len(imgurls)))
        for img in imgurls:
            '''
            print(img[0])
            print(img[1])
            print(img[2])
            '''
            imgurl = img[0].replace(img[1], 'large')
            num_imgs += 1
            try:
                urllib.request.urlretrieve(imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
                # display the raw url of images
                print('\t%d\t%s' % (num_imgs, imgurl))
            except Exception as e:
                print(str(e))
                print('\t%d\t%s failed' % (num_imgs, imgurl))
        num_pages += 1
        print('')
def main():
    # uids = ['2657006573','2173752092','3261134763','2174219060']
    uid = '5746077676'
    path = _get_path(uid)
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.chrome(chromedriver)
    urll = "https://m.weibo.cn/profile/"+uid
    driver.get(urll)
    ck = driver.get_cookies()
    print(ck)
    # cookie is form the above url->network->request headers
    # '_T_WM=77123558928; MLOGIN=1; XSRF-TOKEN=eb07cc; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302832811699412; ALF=1565834638; SCF=AiDQHZorXq6HZSpAzVCEN9WnnMQ7HUl7dGXLYcTBd7yE-CKiCoLoUgYaQ_KLGAhQexNJ8qzDr4uHGlQSixjjc4g.; SUB=_2A25wKUFDDeRhGeRO71sS8CjMwj2IHXVT0m8LrDV6PUJbktAKLWXfkW1NUGWfrHbWVKNYMWcUwTqv-1akS2n-1i5Z; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeGF9QKK0j8MSn3Vc-1dYW5JpX5K-hUgL.Foz7Sh.0ehq71K22dJLoI7_2MJHyd-9DMcyNU7tt; SUHB=0Lcjb2OkLfAhIs; SSOLoginState=1563242772'
    #cookies = ' _T_WM=77123558928; MLOGIN=1; ALF=1565834638; SCF=AiDQHZorXq6HZSpAzVCEN9WnnMQ7HUl7dGXLYcTBd7yE-CKiCoLoUgYaQ_KLGAhQexNJ8qzDr4uHGlQSixjjc4g.; SUB=_2A25wKUFDDeRhGeRO71sS8CjMwj2IHXVT0m8LrDV6PUJbktAKLWXfkW1NUGWfrHbWVKNYMWcUwTqv-1akS2n-1i5Z; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeGF9QKK0j8MSn3Vc-1dYW5JpX5K-hUgL.Foz7Sh.0ehq71K22dJLoI7_2MJHyd-9DMcyNU7tt; SUHB=0Lcjb2OkLfAhIs; SSOLoginState=1563242772; XSRF-TOKEN=ac4a16; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076035546145590%26fid%3D1076032811699412%26uicode%3D10000011'
    cookies = '_ga=GA1.2.165447574.1563351865; _gid=GA1.2.587732577.1563351865; ALF=1566003542; _T_WM=54994403779; WEIBOCN_FROM=1110006030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeGF9QKK0j8MSn3Vc-1dYW5JpX5K-hUgL.Foz7Sh.0ehq71K22dJLoI7_2MJHyd-9DMcyNU7tt; MLOGIN=1; XSRF-TOKEN=b083f6; SCF=AiDQHZorXq6HZSpAzVCEN9WnnMQ7HUl7dGXLYcTBd7yEAr-k61B9Gqo9ZbnVGwBE3Mdu8GmUUD0A9azutXyQ1xQ.; SUB=_2A25wNGclDeRhGeRO71sS8CjMwj2IHXVT1wltrDV6PUJbktAKLXf2kW1NUGWfrDTHuGXs3ke0tPnoyxqb73zuHcsf; SUHB=0k1z3A6rxfyAWa; SSOLoginState=1563432821; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231093_-_selffollowed%26uicode%3D10000011%26fid%3D1076035746077676'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}


    # capture imgs from sina
    #_capture_images(uid, headers, path)
if __name__ == '__main__':
    main()