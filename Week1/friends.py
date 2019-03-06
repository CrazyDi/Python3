import requests


def calc_age(uid):
    # получаем user_id
    token = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
    url = f"https://api.vk.com/method/users.get?v=5.71&access_token={token}&user_ids={uid}"
    r = requests.get(url).json()
    uid = r['response'][0]['id']

    # получаем список друзей
    url = f'https://api.vk.com/method/friends.get?v=5.71&access_token={token}&user_id={uid}&fields=bdate'
    r = requests.get(url).json()

    res = {}

    for friend in r['response']['items']:
        if 'bdate' in friend:
            l = friend['bdate'].split('.')
            if len(l) == 3:
                age = 2019  - int(l[2])
                if age in res:
                    res[age] += 1
                else:
                    res[age] = 1

    res = res.items()
    res = sorted(res, key=lambda age: (-age[1], age[0]))

    return res


if __name__ == '__main__':
    res = calc_age('reigning')
    print(type(res), res)
