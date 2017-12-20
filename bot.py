import requests
import threading
import json
from datetime import datetime
import values

migrations = []
auth = ('ant6190', values.KEY)
GIT_URL = 'https://api.github.com/repos'

COMMENT_INFO = {
  "body": "Hey, your Migration is out of date! You should fix that.\n "
          "Fix it with Tyler's Script: "
          "https://gist.github.com/CNBorn/7c312744b34c9b6e9b853382fe93385f\n"
          "The last migration to integration happened at {0}",
  "event": "COMMENT",
}


def check_review_status(migration, time):
    COMMENT_INFO['body'] = COMMENT_INFO['body'].format(time)
    requests.post(
        '{0}/ant6190/BotTest/pulls/{1}/reviews'.format(GIT_URL, migration),
        auth=auth, data=json.dumps(COMMENT_INFO))


def send_comments(merged_migrations):
    print('Merged Migrations')
    print(merged_migrations)
    for merged_migration in merged_migrations:
        migrations.remove(merged_migration)
        for migration in migrations:
            check_review_status(migration, str(datetime.now().time()))


def main():
    threading.Timer(5.0, main).start()
    r = requests.get('{0}/ant6190/BotTest/pulls'.format(GIT_URL),
                     auth=auth)
    if r.json():
        for pr in r.json():
            if '[Migration]' in pr['title'] \
                    and pr['number'] not in migrations \
                    and pr['state'] == 'open':
                migrations.append(pr['number'])

    else:
        print("No PRs to Check")

    print(migrations)

    merged_migrations = []
    for migration in migrations:
        request = requests.get(
            '{0}/ant6190/BotTest/pulls/{1}/merge'.format(GIT_URL, migration),
            auth=auth)
        if request.status_code == 204:
            merged_migrations.append(migration)
    if merged_migrations:
        send_comments(merged_migrations)


main()


