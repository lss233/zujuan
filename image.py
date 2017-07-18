import utils
import re
import os

def download_img(url, num_retries=3, params=None, headers={'user-agent': 'Mozilla/5.0'}, cookies=None, proxy=None):
    r = utils.download(url, num_retries, params, headers, cookies=cookies, proxy=proxy)
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
        return img_tag[beg_pos+1: end_pos]

def download_all_img(id, img_count, img_path):
    count = 1
    for img in img_count:
        src = get_img_src(img)

        if src == None:
            return False

        value = download_img(src)
        if value == None:
            return False

        with open(img_path + str(id) + '_' + str(count) + '.png', 'wb') as wfile:
            wfile.write(value)
            count += 1

    return True

def make_img_dir(img_path):
    if not os.path.exists(img_path):
        os.mkdir(img_path)