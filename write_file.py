import json
with open('progress.log', 'w') as wfile:
    content = {
        'target': "集合的含义",
        'target_page': 1
    }
    
    wfile.writelines(json.dumps(content))
    