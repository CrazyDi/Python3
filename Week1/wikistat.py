from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    parents = [start]
    next_parents = []

    while files[end] is None:
        for parent in parents:
            with open(path + parent, encoding='utf-8') as f:
                html = f.read()
                links = re.findall(link_re, html)
                for link in links:
                    if link in files and link != parent:
                        if files[link] is None:
                            files[link] = parent
                            next_parents.append(link)
        parents = next_parents
        next_parents = []

    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []

    file = end
    while start not in bridge:
        bridge.append(file)
        file = files[file]

    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file), encoding='utf-8') as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        # TODO посчитать реальные значения
        # imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        imgs = 0
        tags = body.select('img[width]')
        for tag in tags:
            if int(tag["width"]) > 199:
                imgs += 1

        # headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        headers = 0
        tags = body.select('h1,h2,h3,h4,h5,h6')
        for tag in tags:
            res = re.search(r'(\>[A-Z]{1})', str(tag)).group(0)
            if len(re.findall(r'\>[ETC]', res)) == 1:
                headers += 1

        # linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        linkslen = 0
        linkslen_tmp = 0
        tags = body.select('a')
        for tag in tags:
            link = tag
            while link is not None:
                if link.name == 'a':
                    link = link.find_next_sibling()
                    linkslen_tmp += 1
                else:
                    link = None

            if linkslen_tmp > linkslen:
                linkslen = linkslen_tmp
            linkslen_tmp = 0



        lists = 20  # Количество списков, не вложенных в другие списки
        lists = 0
        tags = body.select('ul,ol')
        for tag in tags:
            if tag.find_parent("ul") is None and tag.find_parent('ol') is None:
                lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out
