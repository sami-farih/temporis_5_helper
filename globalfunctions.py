def pprint(d):
    if d == '-':
        return d
    res = ''
    for k in d.keys():
        if len(d[k]) > 0:
            res += f'{k}<br/><br/>{"<br/>".join(d[k])}<br/><br/><br/>'
    return res


def pprint_craft(d):
    if len(d) == 0:
        return '-'
    res = ''
    for k in d:
        res += f'''<br/><br/>{' '.join(list(map(lambda p: '<div id="card_pics" style="display:inline-block;"><img src="' + p.img_path + '" width="120" ></div>', k)))}'''
    return res


def pprint_craft_bis(d):
    if len(d) == 0:
        return '-'
    res = ''
    for k in d:
        res += f'''{''.join(list(map(lambda p: '<div>#' + str(p.id) + ' • ' + p.name + '</div>', k)))}'''
    return res


def format_name(x):
    name, url = x
    return f'<a href="{url}" target="_blank">{name}</a>'


def format_image(x, w=50):
    return (
        '<img src="' + x +
        f'" width="{w}" style="display: block; margin-left: auto; margin-right: auto;">'
    )


def format_recipe(x, card_set_, titles=True):
    if len(x) == 0:
        return '-'
    card_set_ = {c.id: [c.name, c.img_path] for c in card_set_}

    res = f'<table width=100%>'
    for i in range(len(x)):
        if titles:
            res += f'<tr><td></td><td></td><td style="text-align: center; padding-top: 4%">Recette {i + 1}</td><td></td><td></td></tr>'
        res += '<tr>'
        for c in x[i]:
            res += f'<td width=100% style="padding-bottom: 2%"><img src="{card_set_[c][1]}">'
            res += f'<figcaption style="text-align: center; padding-top: 2%">{card_set_[c][0]}</figcaption></td>'
        res += '</tr>'
    res += '</table>'
    return res
