from problem import Problem
import requests
import json
import utils
import mayi_utils

url = 'http://zujuan.21cnjy.com/question/list?grade_id%5B%5D=0&grade_id%5B%5D=10&grade_id%5B%5D=11&grade_id%5B%5D=12&grade_id%5B%5D=13'

def get_new_cookie():
    url = 'http://zujuan.21cnjy.com/question?chid=3&xd=3&tree_type=knowledge'
    before_cookie = utils.download(url)
    if before_cookie == None:
        exit(0)
    before_cookie = before_cookie.cookies
    rebuilt_cookie = {'chid': before_cookie['chid']}

    after_cookie = utils.download(url, cookies=before_cookie)
    if after_cookie == None:
        exit(0)
    after_cookie = after_cookie.cookies
    rebuilt_cookie['xd'] = after_cookie['xd']

    return rebuilt_cookie

def get_page_num(problem_num):
    lower_limit = problem_num // 10

    if lower_limit * 10 < problem_num:
        return lower_limit + 1

    return lower_limit

def main():
    find_target = False
    target = "极差、方差与标准差"

    rfile = open('merge_point.txt', 'r')
    point_json = json.loads(rfile.read())
    rfile.close();

    for sub_part in point_json:
        category = sub_part[len(sub_part) - 1]['point']
        for point in sub_part:
            if 'point' in point:
                continue

            if not find_target:
                if point['title'] == target:
                    find_target = True
                else:
                    continue
            question_category = category + [point['title']]

            params = {
                'knowledges': point['id'],
                'question_channel_type': 6,
                'sortField': 'time',
                'page': 1
            }

            cookie = get_new_cookie()
            
            r = utils.download(url, params=params, cookies=cookie)
            if r == None:
                continue

            question_json = json.loads(r.text)

            question_num = question_json.get('total')
            if question_num == None:
                continue

            page_num = get_page_num(question_num)
            count = 0
            for x in range(1, page_num + 1):
                count += 1

                params['page'] = x
                r = utils.download(url, params=params, cookies=cookie)
                if r == None:
                    continue

                question_json = json.loads(r.text)

                question_ids = question_json.get('ids')
                if question_ids == None:
                    continue
                
                for question_id in question_ids:
                    problem = Problem(question_id, question_category)
                    problem.download_problem()

                if count == 5:
                    count = 0
                    cookie = get_new_cookie()

if __name__ == "__main__":
    main()