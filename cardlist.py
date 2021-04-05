from globalvars import *
from globalfunctions import *


class CardList:
    def __init__(self, cards_):
        cards = set(cards_)
        assert len(set([c.id for c in cards])) == len(cards), "ids en double."
        self.cards = cards
        self.crafts = None
        self.th = None

    def display(self, sort_index_=None):
        df = pd.DataFrame([[c.id, c.name, c.drop, c.img_path]
                           for c in self.cards],
                          columns=["id", "Nom", "Obtention", "Image"])

        if not sort_index_ is None:
            df['Rang'] = sort_index_
            df.set_index('Rang', inplace=True)

        df['Image'] = list(map(lambda i: format_image(i, w=200), df['Image']))
        df['Obtention'] = list(map(pprint, df['Obtention']))

        show(df)

    def show(self, x):
        if type(x) == str:
            self.search(x)
            id_ = int(
                input(
                    "Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                ))
            card = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (card is None or card not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                card = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x
            card = self.fetch_by_id_aux(id_)

        clear_output(wait=True)
        CardList([card]).display()
        display(
            HTML('<div style="text-align: center">Recettes contenant (' +
                 card.name + ')</div>'))
        self.crafts.display([
            k for k in self.crafts.crafts.keys()
            if any([card.id in r for r in self.crafts.crafts[k]['recipes']])
        ])

    def check_recipe(self, xs):
        ids = []
        cards = []
        for x in xs:
            if type(x) == str:
                display(HTML('<div style="text-align: center">Recherche de ('+ x +')</div>'))
                self.search(x)
                id_ = int(
                    input(
                        "Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                    ))
                card = self.fetch_by_id_aux(id_)
                max_try = 0
                fetcher = self.fetch_by_name_aux(x)

                while (card is None or card not in fetcher) and max_try < 5:
                    id_ = int(
                        input(
                            "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                            + f'({5 - max_try} tentatives restantes)'))
                    card = self.fetch_by_id_aux(id_)
                    max_try += 1

                if max_try >= 5:
                    clear_output(wait=True)
                    display("Maximum de tentatives dépassé. Requête annulée.")
                    return None

            elif type(x) == int:
                id_ = x
                card = self.fetch_by_id_aux(id_)

            ids.append(id_)
            cards.append(card)

            clear_output(wait=True)

        clear_output(wait=True)

        display(HTML('<div style="text-align: center">Résultat</div>'))

        res = {'Recette': {'idx': format_recipe([ids], self.cards, titles=False)}}
        show(pd.DataFrame.from_dict(res).reset_index()[['Recette']].set_index('Recette'))

        self.crafts.display([
            k for k in self.crafts.crafts.keys()
            if any([set(ids) == r for r in self.crafts.crafts[k]['recipes']])
        ])

    def list(self):
        self.display()

    def card_names(self):
        return [c.name for c in self.cards]

    def fetch_by_id(self, id_):
        search_res = [c for c in self.cards if c.id == id_]
        if len(search_res) == 0:
            display("id non reconnu.")
        else:
            CardList(search_res).display()

    def fetch_by_id_aux(self, id_):
        search_res = [c for c in self.cards if c.id == id_]
        if len(search_res) == 0:
            display("id non reconnu.")
        else:
            return search_res[0]

    def fetch_by_name(self, name_):
        def match_seq(a, b):
            return SequenceMatcher(lambda x: x == " ", unidecode(a.lower()),
                                   unidecode(b.lower()))

        search_res = [c for c in self.cards if c.name.lower() == name_.lower()]

        if len(search_res) == 0:
            adv_search_res = [
                (c, match_seq(name_, c.name).ratio()) for c in self.cards
                if unidecode(name_.lower()) in unidecode(c.name.lower())
                or match_seq(name_, c.name).ratio() > .58
            ]

            adv_search_res.sort(key=lambda x: 1 - x[1])
            adv_search_res = list(map(lambda x: x[0], adv_search_res))

            nb_res = len(adv_search_res)
            if nb_res == 0:
                display("id non reconnu.")
            else:
                s = '' if nb_res == 1 else 's'
                display(f"{nb_res} résultat{s} possible{s}.")
                sort_index_ = list(range(1, len(adv_search_res) + 1))
                CardList(adv_search_res).display(sort_index_=sort_index_)
        else:
            display("1 résultat trouvé.")
            CardList(search_res).display()

    def fetch_by_name_aux(self, name_):
        def match_seq(a, b):
            return SequenceMatcher(lambda x: x == " ", unidecode(a.lower()),
                                   unidecode(b.lower()))

        search_res = [c for c in self.cards if c.name.lower() == name_.lower()]

        if len(search_res) == 0:
            adv_search_res = [(c, match_seq(name_, c.name).ratio())
                              for c in self.cards
                              if name_.lower() in c.name.lower()
                              or match_seq(name_, c.name).ratio() > .58]

            adv_search_res.sort(key=lambda x: x[1])
            adv_search_res = list(map(lambda x: x[0], adv_search_res))

            nb_res = len(adv_search_res)
            if nb_res == 0:
                return None
            else:
                sort_index_ = list(range(1, len(adv_search_res) + 1))
                return CardList(adv_search_res).cards
        else:
            return CardList(search_res).cards

    def search(self, x):
        if type(x) == int:
            return self.fetch_by_id(x)
        elif type(x) == str:
            return self.fetch_by_name(x)
        else:
            display("Erreur dans la requête.")

    def add(self, x):
        if type(x) == str:
            self.search(x)
            id_ = int(
                input(
                    "Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                ))
            card = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (card is None or card not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                card = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x
            card = self.fetch_by_id_aux(id_)

        if card.drop != "-":
            display(
                f'Ajout de méthode de drop pour la carte (#{card.id}: {card.name})'
            )
            display(HTML(f"Actuellement:<br/>{pprint(card.drop)}"))

            if input(
                    "Une méthode de drop est déjà renseignée, voulez-vous la remplacer ? (y/[n]) "
            ).lower() == 'y':
                card.drop = {
                    "Craft métier": [],
                    "Drop donjon": [],
                    "Drop mobs": []
                }
            else:
                if input(
                        "Voulez-vous ajouter une nouvelle méthode de drop ? (y/[n]) "
                ).lower() != 'y':
                    clear_output(wait=True)
                    display("Requête annulée.")
                    return None

        else:
            display(
                f'Ajout de méthode de drop pour la carte (#{card.id}: {card.name})'
            )
            card.drop = {
                "Craft métier": [],
                "Drop donjon": [],
                "Drop mobs": []
            }

        dropdown_type = widgets.Dropdown(
            options=["-", "Craft métier", "Drop donjon", "Drop mobs"],
            value="-",
            description="Méthode d'obtention",
            disabled=False,
        )

        dropdown_craft = widgets.Dropdown(
            options=job_list,
            value="-",
            description="Métier",
            disabled=False,
        )

        dropdown_dungeon = widgets.Dropdown(
            options=sorted(dungeon_list.keys()),
            value="-",
            description="Donjon",
            disabled=False,
        )

        dropdown_mob = widgets.Dropdown(
            options=sorted(monster_list.keys()),
            value="-",
            description="Mob",
            disabled=False,
        )

        slider_level = widgets.IntSlider(value=1,
                                         min=1,
                                         max=200,
                                         step=1,
                                         description='Level',
                                         disabled=False,
                                         continuous_update=True,
                                         orientation='horizontal',
                                         readout=True,
                                         readout_format='d')

        empty_widget = widgets.FloatText()
        empty_widget.layout.display = 'none'

        stacked = widgets.Stacked(
            [empty_widget, dropdown_craft, dropdown_dungeon, dropdown_mob])
        stacked_bis = widgets.Stacked(
            [empty_widget, slider_level, empty_widget, empty_widget])

        widgets.jslink((dropdown_type, 'index'), (stacked, 'selected_index'))
        widgets.jslink((dropdown_type, 'index'),
                       (stacked_bis, 'selected_index'))

        selector = widgets.VBox([dropdown_type, stacked, stacked_bis])
        output = widgets.Output()
        run_button = widgets.Button(description='Valider')
        cancel_button = widgets.Button(description='Annuler')

        def validate(b):
            res = [
                dropdown_type.value,
                stacked.children[dropdown_type.index].value
            ]
            if "-" in res:
                clear_output(wait=True)
                display(selector)
                display(run_button)
                display(cancel_button)
                display("Veuillez remplir tous les champs.")
                return None
            if res[0] == "Drop donjon":
                drop_ = f"{dungeon_list[res[1]]}"

            elif res[0] == "Craft métier":
                drop_ = f"{res[1]} lv. {slider_level.value}"

            elif res[0] == "Drop mobs":
                drop_ = f"<a href='{monster_list[res[1]]['url']}' target='_blank'>\
                {res[1]}</a><br/>[{', '.join(monster_list[res[1]]['areas'])}]"

            if drop_ not in card.drop[res[0]]:
                card.drop[res[0]].append(drop_)
            else:
                clear_output(wait=True)
                display("Méthode déjà renseignée.")
                return None

            clear_output(wait=True)
            display(
                f"Méthode de drop pour (#{card.id}: {card.name}) mise à jour.")
            self.th.save()

        def cancel(b):
            clear_output(wait=True)
            display(f"Requête annulée.")

        run_button.on_click(validate)
        cancel_button.on_click(cancel)
        display(selector)
        display(run_button)
        display(cancel_button)
        output

    def remove(self, x):
        if type(x) == str:
            self.search(x)
            id_ = int(
                input(
                    "Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                ))
            card = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (card is None or card not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                card = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x
            card = self.fetch_by_id_aux(id_)

        if card.drop == "-" or (all(
            [len(card.drop[k]) == 0 for k in card.drop.keys()])):
            clear_output(wait=True)
            display("Case vide. Requête annulée.")
            return None

        opt_dropdown = ['-']

        for i in ["Craft métier", "Drop donjon", "Drop mobs"]:
            if len(card.drop[i]) > 0:
                opt_dropdown.append(i)

        dropdown_craft = widgets.Dropdown(
            options=['-'] +
            [c.split(' ')[0] for c in card.drop['Craft métier']],
            value="-",
            description="Métier",
            disabled=False,
        )

        dropdown_dungeon = widgets.Dropdown(
            options=sorted(['-'] + [
                k for k in dungeon_list.keys()
                if dungeon_list[k] in card.drop['Drop donjon']
            ]),
            value="-",
            description="Donjon",
            disabled=False,
        )

        dropdown_mob = widgets.Dropdown(
            options=sorted(['-'] + [
                k for k in monster_list.keys()
                if f"<a href='{monster_list[k]['url']}' target='_blank'>\
                {k}</a><br/>[{', '.join(monster_list[k]['areas'])}]" in
                card.drop['Drop mobs']
            ]),
            value="-",
            description="Mob",
            disabled=False,
        )

        dropdown_type = widgets.Dropdown(
            options=opt_dropdown,
            value="-",
            description="Méthode d'obtention",
            disabled=False,
        )

        empty_widget = widgets.FloatText()
        empty_widget.layout.display = 'none'

        stacked = widgets.Stacked([empty_widget] + [
            d for d in [dropdown_craft, dropdown_dungeon, dropdown_mob]
            if len(d.options) > 1
        ])
        widgets.jslink((dropdown_type, 'index'), (stacked, 'selected_index'))

        selector = widgets.VBox([dropdown_type, stacked])
        output = widgets.Output()
        run_button = widgets.Button(description='Valider')
        cancel_button = widgets.Button(description='Annuler')

        def validate(b):
            res = [
                dropdown_type.value,
                stacked.children[dropdown_type.index].value
            ]
            if "-" in res:
                clear_output(wait=True)
                display(selector)
                display(run_button)
                display(cancel_button)
                display(
                    "Veuillez remplir tous les champs ou annuler la requête.")
                return None

            if res[0] == "Drop donjon":
                drop_ = f"{dungeon_list[res[1]]}"

            elif res[0] == "Craft métier":
                drop_ = [c for c in card.drop['Craft métier']
                         if res[1] in c][0]

            elif res[0] == "Drop mobs":
                drop_ = f"<a href='{monster_list[res[1]]['url']}' target='_blank'>\
                {res[1]}</a><br/>[{', '.join(monster_list[res[1]]['areas'])}]"

            card.drop[res[0]].remove(drop_)

            if all([len(card.drop[k]) == 0 for k in card.drop.keys()]):
                card.drop = '-'

            clear_output(wait=True)
            display(
                f"Méthode de drop pour (#{card.id}: {card.name}) mise à jour.")

            self.th.save()

        def cancel(b):
            clear_output(wait=True)
            display(f"Requête annulée.")

        run_button.on_click(validate)
        cancel_button.on_click(cancel)
        display(
            f'Suppression de méthode de drop pour la carte (#{card.id}: {card.name})'
        )
        display(selector)
        display(run_button)
        display(cancel_button)
        output