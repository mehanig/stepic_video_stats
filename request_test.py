import requests
import random, string

url = 'http://127.0.0.1:5000/newVideo'
data = {'User': 'testUser', 'Name': ''.join(random.choice(string.ascii_letters) for i in range(10)), 'Duration': 'No data',
        'priority': 0, 'status': 0}


if __name__ == '__main__':
    r = requests.post(url, data=data)
    print(r.text)