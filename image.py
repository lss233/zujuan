import utils
import re
import os
import mayi_utils

import threading

def download_img(url, num_retries=3, params=None, headers={'user-agent': 'Mozilla/5.0'}, cookies=None, proxy=None):
    r = utils.download(url, num_retries, params, headers=headers, cookies=cookies, proxy=proxy)
    if r == None:
        return None

    return r.content

def get_img_tags(text, img_count):
    img_collect = re.findall(r'<img.*?/?>', text)
    for img in img_collect:
        img_count.append(img)

def decide_location(beg_pos_tmp, beg_pos_tmp2):
    if beg_pos_tmp == -1 and beg_pos_tmp2 == -1:
        return None
    elif beg_pos_tmp > 0 and beg_pos_tmp2 > 0:
        if beg_pos_tmp > beg_pos_tmp2:
            return beg_pos_tmp2
        else:
            return beg_pos_tmp
    elif beg_pos_tmp == -1 and beg_pos_tmp2 != -1:
        return beg_pos_tmp2
    elif beg_pos_tmp2 == -1 and beg_pos_tmp != -1:
        return beg_pos_tmp

def get_img_src(img_tag):
    beg_pos = img_tag.find('src')
    beg_pos_tmp = img_tag.find('"', beg_pos)
    beg_pos_tmp2 = img_tag.find("'", beg_pos)
    beg_pos = decide_location(beg_pos_tmp, beg_pos_tmp2)

    end_pos_tmp = img_tag.find('"', beg_pos + 1)
    end_pos_tmp2 = img_tag.find("'", beg_pos + 1)
    end_pos = decide_location(end_pos_tmp, end_pos_tmp2)

    if beg_pos == None or end_pos == None:
        return None
    else:
        return img_tag[beg_pos+1: end_pos].strip(' \n\t;')

        
def download_single_image(img, filename):

    global ALL_IMAGE_SUCCESS
    
    try:
        src = get_img_src(img)
        
        if not src.startswith('http'):
            raise AssertionError
        if src == None:
            raise AssertionError

        for i in range(0, 5):
            value = download_img(src)
            if value is not None:
                break
            
        if value == None:
            raise AssertionError

        with open(filename, 'wb') as wfile:
            wfile.write(value)
            
    except AssertionError:
        print("Failed download:" + src)
        ALL_IMAGE_SUCCESS = False
        
def download_all_img(id, img_count, img_path):

    global ALL_IMAGE_SUCCESS
    ALL_IMAGE_SUCCESS = True

    count = 1
    
    thread_list = []
    
    for img in img_count:
    
        filename = img_path + str(id) + '_' + str(count) + '.png'
        count += 1
        
        t = threading.Thread(target=download_single_image,args=(img, filename, ))
        t.start()
        thread_list.append(t)
        
    for t in thread_list:
        t.join()
    
    if not ALL_IMAGE_SUCCESS:
        print('Problem '+str(id)+'failed: cannot download all images.')
        return False
    
    return True

def make_img_dir(img_path):
    if not os.path.exists(img_path):
        os.mkdir(img_path)