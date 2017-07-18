import utils
import os
import json
import image
import mayi_utils

class Problem:
    base_url = "http://zujuan.21cnjy.com/question/detail/"
    def __init__(self, question_id, category):
        self.question = ""
        self.answer = ""
        self.explanation = ""
        self.img_count = []
        self.question_path = os.getcwd() + "\\question\\"
        self.img_path = os.getcwd() + "\\img\\"

        self.question_id = question_id
        self.category = category

        self.valid = True


    def download_problem(self):
        text = mayi_utils.download(self.base_url+str(self.question_id))
        if text == None:
            return
        text = text.text
        test_count = 0

        if text == None:
            return
        beg_location = self.find_json_beg(text)
        end_location = self.find_json_end(text, beg_location)

        if not self.valid:
            return

        question_json = text[beg_location: end_location].strip(' \n\t;')
        question_json = json.loads(question_json)

        question_json[0]['point'] = self.category
        self.answer = question_json[0]['questions'][0]['answer']
        self.question = question_json[0]['questions'][0]['question_text']
        self.explanation = question_json[0]['questions'][0]['explanation']

        if self.answer == '':
            return

        self.get_img_count()

        image.make_img_dir(self.img_path)
        valid = image.download_all_img(self.question_id, self.img_count, self.img_path)

        if not valid:
            return
        else:
            self.test_question_path();
            with open(self.question_path + str(self.question_id) + '.txt', 'w') as wfile:
                wfile.write(json.dumps(question_json))
                
    def test_question_path(self):
        if not os.path.exists(self.question_path):
            os.mkdir(self.question_path)

    def find_json_beg(self, text):
        beg = text.find('MockDataTestPaper')
        
        beg_location = text.find('[', beg)

        if beg == -1:
            self.valid = False
        return beg_location

    def find_json_end(self, text, beg):
        end = text.find('OT2.renderQList', beg)

        if end == -1:
            self.valid = False
        return end

    def get_img_count(self):
        image.get_img_tags(self.question, self.img_count)
        image.get_img_tags(self.answer, self.img_count)
        image.get_img_tags(self.explanation, self.img_count)