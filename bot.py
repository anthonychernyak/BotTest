import requests


def parse_content(info):
    rev_start_pos = info.find('revision')
    rev = ''
    if rev_start_pos != -1:
        while rev_start_pos < len(info) and info[rev_start_pos] != "\'":
            rev_start_pos += 1
        while rev_start_pos < len(info) and info[rev_start_pos] != "\'":
            rev += info[rev_start_pos]
            rev_start_pos += 1

    down_rev_start_pos = info.find('down_revision')
    down_rev = ''
    if down_rev_start_pos != -1:
        while down_rev_start_pos < len(info) and info[down_rev_start_pos] != "\'":
            down_rev_start_pos += 1
        while down_rev_start_pos < len(info) and info[down_rev_start_pos] != "\'":
            rev += info[down_rev_start_pos]
            down_rev_start_pos += 1

    return {'rev': rev, 'down_rev': down_rev}


def main():
    auth = ('ant6190', 'temp')
    r = requests.get('https://api.github.com/repos/ant6190/BotTest/pulls', auth=auth)
    if r.json():
        for item in r.json():
            pr = requests.get(item['url'], auth=auth)
            commits = requests.get(pr.json()['commits_url'], auth=auth).json()
            for commit in commits:
                r_commit = requests.get(commit['url'], auth=auth).json()
                for content_url in r_commit['files']:
                    print(content_url['patch'])
    else:
        print("No PRs to Check")


main()