import json
import os

if __name__ == "__main__":
	rfile = open('question\\2535937.txt', 'r')
	text = rfile.read()
	
	json_obj = json.loads(text)
	print(str(json_obj[0]['point']))
	print(str(json_obj[0]['questions'][0]['answer']))
	print(str(json_obj[0]['questions'][0]['question_text']))
	print(str(json_obj[0]['questions'][0]['explanation']))
	rfile.close()