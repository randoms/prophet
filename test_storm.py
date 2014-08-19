import requests
import json
    
def send_server(mnews):
    params = {'title':mnews['title'],
              'content':mnews['content'],
              'link':mnews['link'],
              'time':mnews['time'],
              'keywords':json.dumps(mnews['keywords'],indent=4),
              'refers':json.dumps(mnews['refers'],indent=4)}
    r = requests.post("http://api.randoms.me/news/add", data=params)
    f = open('res.html','w')
    f.write(r.text)
    f.close()
    
mitem = {
        'title':"this is a title",
        'content':'this is content',
        'time':321421,
        'keywords':['dsad','dsaf','fdaf'],
        'refers':['dsadf','fasfedas','dsafads'],
        'link':'dsadfsafsa'
    }
send_server(mitem)

