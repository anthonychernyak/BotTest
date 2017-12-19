import requests

auth = ('ant6190', 'temp')
r = requests.get('https://api.github.com/repos/ant6190/BotTest/pulls', auth=auth)
if r.json():
    print(r.json())
else:
    print("No PRs to Check")
