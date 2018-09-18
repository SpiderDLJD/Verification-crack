# coding=utf-8

import os

import re

import time

import math

import urllib

import random

import shutil

from PIL import Image

from lxml import etree

from PIL import ImageChops

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver import ActionChains





# 设置用户名和密码

username = '188****3930'

password = '*************'





# 提示信息及路径输入

print(u'请预先以字符串形式输入验证码图片存储路径！')

print(u'注意！部分字符可能需要进行转移字符处理！')





try:

    path = input()

except:

    print(u'路径格式应为字符串格式')

    print(u'请重新输入路径！')





print(u'路径录入正确！')

print(u'正在打开Firefox浏览器...')

time.sleep(2)





# 获取浏览器驱动

driver = webdriver.Firefox()





# 窗口最大化

driver.maximize_window()





# 打开登录界面

request_url = 'https://passport.bilibili.com/login'

driver.get(request_url)

time.sleep(2)





# 设置用户名密码

driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)

driver.find_element_by_xpath('//*[@id="login-passwd"]').send_keys(password)





# 获取验证码图片链接

soup = BeautifulSoup(driver.page_source, 'lxml')

pattern_fig = re.compile(r'http.*?jpg')



# 无缺口突脸链接

link_data_ori_fig = soup.find_all('div', class_= 'gt_cut_fullbg_slice')[0]

selector_ori = etree.HTML(str(link_data_ori_fig))

str_url_ori = selector_ori.xpath('//*[@class ="gt_cut_fullbg_slice"]/@style')[0]

url_ori_fig = re.findall(pattern_fig, str_url_ori)[0]



# 有缺口图片链接

link_data_cut_fig = soup.find_all('div', class_= 'gt_cut_bg_slice')[0]

selector_cut = etree.HTML(str(link_data_cut_fig))

str_url_cut = selector_cut.xpath('//*[@class ="gt_cut_bg_slice"]/@style')[0]

url_cut_fig = re.findall(pattern_fig, str_url_cut)[0]





# 获取验证码图片像素点

pattern_pix_loca = re.compile(r'background-position.*?px.*?px')

pattern_pix = re.compile(r'-[1-9]\d*|0')

pix_ori = []

pix_cut = []



# 下载验证码图片

name_ori = 'fig_ori.jpg'

name_cut = 'fig_cut.jpg'

path_ori = path + '\\' + name_ori

path_cut = path + '\\' + name_cut

res1 = urllib.urlretrieve(url_ori_fig, path_ori)

res2 = urllib.urlretrieve(url_cut_fig, path_cut)

print(u'验证码对应图片下载成功！')





# 无缺口图片像素坐标

list_pix_data_ori_fig = soup.find_all('div', class_ = 'gt_cut_fullbg_slice')

for pix_data_ori_fig in list_pix_data_ori_fig:

    str_middle = re.findall(pattern_pix_loca, str(pix_data_ori_fig))

    pix_ori.append(map(int, re.findall(pattern_pix, str(str_middle))))



# 有缺口图片像素坐标

list_pix_data_cut_fig = soup.find_all('div', class_ = 'gt_cut_bg_slice')

for pix_data_cut_fig in list_pix_data_cut_fig:

    str_middle = re.findall(pattern_pix_loca, str(pix_data_cut_fig))

    pix_cut.append(map(int, re.findall(pattern_pix, str(str_middle))))



# 预处理像素坐标

for i in range(len(pix_ori)):

    pix_ori[i][0] = abs((pix_ori[i][0] + 1)/12)

    if pix_ori[i][1] == -58:

        pix_ori[i][1] = 1

for i in range(len(pix_cut)):

    pix_cut[i][0] = abs((pix_cut[i][0] + 1)/12)

    if pix_cut[i][1] == -58:

        pix_cut[i][1] = 1





# 构建文件夹存储剪切图片

path_ori = path + '/figs_ori'

os.mkdir(path_ori, 0755)

path_cut = path + '/figs_cut'

os.mkdir(path_cut, 0755)





# 将两张图片还原

# 首先将图片按顺序拆解

im_ori = Image.open(name_ori)

img_ori_size = im_ori.size

for i in range(len(pix_ori)):

    region = im_ori.crop((pix_ori[i][0] * 2 * img_ori_size[0] / len(pix_ori),

                      pix_ori[i][1] * img_ori_size[1] / len(pix_ori[0]),

                      (pix_ori[i][0] + 1) * 2 * img_ori_size[0] / len(pix_ori),

                      (pix_ori[i][1] + 1) * img_ori_size[1] / len(pix_ori[0])))

    if i <= 25:

        region.save('./figs_ori/{}_{}.jpg'.format(0, i))

    else:

        region.save('./figs_ori/{}_{}.jpg'.format(1, i-26))

im_cut = Image.open(name_cut)

img_cut_size = im_cut.size

for i in range(len(pix_cut)):

    region = im_cut.crop((pix_cut[i][0] * 2 * img_cut_size[0] / len(pix_cut),

                      pix_cut[i][1] * img_cut_size[1] / len(pix_cut[0]),

                      (pix_cut[i][0] + 1) * 2 * img_cut_size[0] / len(pix_cut),

                      (pix_cut[i][1] + 1) * img_cut_size[1] / len(pix_cut[0])))

    if i <= 25:

        region.save('./figs_cut/{}_{}.jpg'.format(0, i))

    else:

        region.save('./figs_cut/{}_{}.jpg'.format(1, i-26))



# 将图片进行拼接

size_row = 12

size_col = 58

target = Image.new('RGB', (size_row * 26, size_col * 2))

for i in range(2):

    for j in range(26):

        target.paste(Image.open(path_ori + '/{}_{}.jpg'.format(i, j)), (j*size_row, i*size_col, (j+1)*size_row, (i+1)*size_col))

        target.save('Fig_ori_complete.jpg')

for i in range(2):

    for j in range(26):

        target.paste(Image.open(path_cut + '/{}_{}.jpg'.format(i, j)), (j*size_row, i*size_col, (j+1)*size_row, (i+1)*size_col))

        target.save('Fig_cut_complete.jpg')



# 删除存储图片的文件夹

shutil.rmtree(path_ori)

shutil.rmtree(path_cut)





# 像素值做差获取缺口

path_ori = path + '/Fig_ori_complete.jpg'

path_cut = path + '/Fig_cut_complete.jpg'

fig_ori = Image.open(path_ori)

fig_cut = Image.open(path_cut)

differ = ImageChops.difference(fig_ori, fig_cut)

differ.save(path + '/differ.jpg')

img_arr = differ.load()

difference = []

for i in range(size_row * 26):

    for j in range(size_col * 2):

        if img_arr[i, j] > (110, 110, 110):

            difference.append([i+j, i])



# 找在浏览器滑动的距离

left_edge = min(difference)[1]

right_edge = max(difference)[1]

middle_edge = float(0.5 * left_edge + 0.55 * right_edge)

track_s = int(middle_edge * 198 / 312)





# 构造滑动轨迹

distance = track_s

distance_speed_up = distance * 0.75

distance_speed_down = distance * 0.25

a_speed_up = random.uniform(30, 35)

t_speed_up = math.sqrt(2 * distance_speed_up / a_speed_up)

v_max = a_speed_up * t_speed_up

a_speed_down = (v_max*(3.13-t_speed_up) - distance_speed_down)*2/(3.13-t_speed_up)**2

t_speed_down = v_max / a_speed_down

trace_list_1 = []

trace_list_2 = []

trace_list = []

for i in range(int(t_speed_up * 3)):

    trace_list_1.append(0.5 * a_speed_up * (i/3.0)**2)

for i in range(int(t_speed_down * 5)):

    trace_list_2.append(v_max * (i/5.0) - 0.5 * a_speed_down * (i/5.0)**2 + trace_list_1[-1])

trace_list_ = trace_list_1 + trace_list_2

trace_list_[-1] = distance

for i in range(1, len(trace_list_)):

    trace_list.append(trace_list_[i] - trace_list_[i - 1])





# 控制浏览器滑块滑动

button = driver.find_element_by_class_name('gt_slider_knob.gt_show')

ActionChains(driver).click_and_hold(button).perform()

for trace in trace_list:

    ActionChains(driver).move_by_offset(xoffset=trace, yoffset=0).perform()

ActionChains(driver).release(button).perform()

time.sleep(3)

