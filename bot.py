import requests
import threading


def main():
    threading.Timer(5.0, main).start()
    migrations = []
    auth = ('ant6190', 'temp')
    r = requests.get('https://api.github.com/repos/ant6190/BotTest/pulls', auth=auth)
    if r.json():
        for item in r.json():
            pr = requests.get(item['url'], auth=auth).json()
            if '[Migration]' in pr['title'] and pr['number'] not in migrations and pr['state'] == 'open':
                migrations.append(pr['number'])
    else:
        print("No PRs to Check")

    print(migrations)

    for migration in migrations:
        request = requests.get('https://api.github.com/repos/ant6190/pulls/{0}/merge'.format(migration), auth=auth)
        print(request.status_code)

main()


