from globalvars import *
from globalfunctions import *


class CraftList:
    def __init__(self, card_set_):
        def remove_url(text):
            res = re.sub(r'^https?:\/\/.*[\r\n]*/', '', text)
            return int(res.split('-')[0])

        self.card_set = card_set_
        all_items = list(craft_list.keys())
        self.crafts = {
            remove_url(craft_list[all_items[i]]['url']):
            dict({
                'name': all_items[i],
                'recipes': []
            }, **craft_list[all_items[i]])
            for i in range(len(all_items))
        }

    def display(self, ids_=None):
        df = pd.DataFrame.from_dict(self.crafts).T.reset_index()
        df.rename(columns={
            'name': 'Nom',
            'recipes': 'Recettes',
            'img_url': 'Image',
            'index': 'id'
        },
                  inplace=True)
        df['Nom'] = list(map(format_name, list(zip(df['Nom'], df['url']))))
        df['Image'] = list(map(format_image, df['Image']))
        df['Recettes'] = list(map(len, df['Recettes']))

        if ids_ is None:
            show(df[['id', 'Nom', 'Recettes', 'Image']].set_index('id'))
        else:
            show(df[df['id'].isin(ids_)][['id', 'Nom', 'Recettes',
                                          'Image']].set_index('id'),
                 columnDefs=[{
                     "width": "200px",
                     "targets": "_all"
                 }])

    def recipes(self, x):
        if type(x) == str:
            self.search(x)
            id_ = int(
                input(
                    "Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                ))
            obj = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (obj is None or obj not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                obj = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x

        clear_output(wait=True)
        df = pd.DataFrame.from_dict(self.crafts).T.reset_index()
        df.rename(columns={
            'name': 'Nom',
            'recipes': 'Recettes',
            'img_url': 'Image',
            'index': 'id'
        },
                  inplace=True)
        df = df[df['id'] == id_]
        df['Nom'] = list(map(format_name, list(zip(df['Nom'], df['url']))))
        df['Image'] = list(map(format_image, df['Image']))
        df['Recettes'] = list(
            map(lambda c: format_recipe(c, self.card_set.cards),
                df['Recettes']))

        display(
            HTML('<div style="text-align: center">' + df['Nom'].values[0] +
                 '</div>'))
        display(
            HTML('<div style="text-align: center">' + df['Image'].values[0] +
                 '</div>'))

        show(df[['Recettes']].set_index('Recettes'), index=False)

    def list(self):
        return self.display()

    def fetch_by_id(self, id_):
        if id_ in self.crafts.keys():
            self.display([id_])
        else:
            display("id non reconnu.")

    def fetch_by_id_aux(self, id_):
        if id_ in self.crafts.keys():
            return id_
        else:
            display("id non reconnu.")

    def fetch_by_name(self, name_):
        def match_seq(a, b):
            return SequenceMatcher(lambda x: x == " ", unidecode(a.lower()),
                                   unidecode(b.lower()))

        craft_names = {
            k: unidecode(self.crafts[k]['name'].lower())
            for k in self.crafts.keys()
        }
        search_res = [
            k for k in craft_names.keys()
            if craft_names[k].lower() == name_.lower()
        ]

        if len(search_res) == 0:
            adv_search_res = [
                (k, match_seq(name_, craft_names[k]).ratio())
                for k in craft_names.keys()
                if unidecode(name_.lower()) in unidecode(craft_names[k].lower(
                )) or match_seq(name_, craft_names[k]).ratio() > .58
            ]

            adv_search_res.sort(key=lambda x: 1 - x[1])
            adv_search_res = list(map(lambda x: x[0], adv_search_res))

            nb_res = len(adv_search_res)
            if nb_res == 0:
                display("id non reconnu.")
            else:
                s = '' if nb_res == 1 else 's'
                display(
                    HTML(
                        f'<p style="text-align:center">{nb_res} résultat{s} possible{s}.</p>'
                    ))
                self.display(adv_search_res)
        else:
            display("1 résultat trouvé.")
            self.dicsplay(search_res)

    def fetch_by_name_aux(self, name_):
        def match_seq(a, b):
            return SequenceMatcher(lambda x: x == " ", unidecode(a.lower()),
                                   unidecode(b.lower()))

        craft_names = {
            k: unidecode(self.crafts[k]['name'].lower())
            for k in self.crafts.keys()
        }
        search_res = [
            k for k in craft_names.keys()
            if craft_names[k].lower() == name_.lower()
        ]

        if len(search_res) == 0:
            adv_search_res = [
                (k, match_seq(name_, craft_names[k]).ratio())
                for k in craft_names.keys()
                if unidecode(name_.lower()) in unidecode(craft_names[k].lower(
                )) or match_seq(name_, craft_names[k]).ratio() > .58
            ]

            adv_search_res.sort(key=lambda x: 1 - x[1])
            adv_search_res = list(map(lambda x: x[0], adv_search_res))

            nb_res = len(adv_search_res)
            if nb_res == 0:
                return None
            else:
                return adv_search_res
        else:
            return search_res

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
            obj = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (obj is None or obj not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                obj = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x
            obj = self.fetch_by_id_aux(id_)

        clear_output(wait=True)
        display(f'Ajout de recette pour la carte ({self.crafts[obj]["name"]})')
        if len(self.crafts[obj]['recipes']) > 0:
            display(
                HTML(f"Carte: (#{obj}: {self.crafts[obj]['name']})<br/>" +
                     f"<br/>Actuellement"))
            self.recipes(id_)

            if input(
                    "Une méthode de drop est déjà renseignée, voulez-vous la remplacer ? (y/[n]) "
            ).lower() == 'y':
                self.crafts[obj]['recipes'] = []
            else:
                if input(
                        "Voulez-vous ajouter une nouvelle méthode de drop ? (y/[n]) "
                ).lower() != 'y':
                    clear_output(wait=True)
                    display("Requête annulée.")
                    return None

        dropdown_cards = [
            widgets.Dropdown(
                options=["-"] + self.card_set.card_names(),
                value="-",
                description=f"Carte {i+1}",
                disabled=False,
            ) for i in range(5)
        ]

        info_dup = widgets.Box(
            [widgets.Label('Certaines cartes sont en double !')])
        info_dup.layout.visibility = 'hidden'

        def update_duplicates(*args):
            vals = [
                dropdown_cards[j].value for j in range(5)
                if dropdown_cards[j].value != '-'
            ]
            if len(vals) != len(set(vals)):
                info_dup.layout.visibility = 'visible'
            else:
                info_dup.layout.visibility = 'hidden'

        for i in range(5):
            dropdown_cards[i].observe(update_duplicates, 'value')

        selector = widgets.HBox(dropdown_cards)
        output = widgets.Output()
        run_button = widgets.Button(description='Valider')
        cancel_button = widgets.Button(description='Annuler')

        def validate(b):
            res = [d.value for d in dropdown_cards]
            if "-" in res:
                clear_output(wait=True)
                display(selector)
                display(run_button)
                display(cancel_button)
                display("Veuillez remplir tous les champs.")
                return None

            if len(set(res)) != 5:
                clear_output(wait=True)
                display(selector)
                display(info_dup)
                display(run_button)
                display(cancel_button)
                display("Certaines cartes sont en double.")
                return None

            cards_reversed = {c.name: c.id for c in self.card_set.cards}
            recipe = {cards_reversed[r] for r in res}

            if recipe not in self.crafts[obj]['recipes']:
                self.crafts[obj]['recipes'].append(recipe)
            else:
                clear_output(wait=True)
                display("Recette déjà renseignée.")
                return None

            clear_output(wait=True)
            display(
                f"Recette ajoutée. (#{obj}: {self.crafts[obj]['name']}) mis à jour."
            )
            
            global th
            th.save()

        def cancel(b):
            clear_output(wait=True)
            display(f"Requête annulée.")

        run_button.on_click(validate)
        cancel_button.on_click(cancel)
        display(selector)
        display(info_dup)
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
            obj = self.fetch_by_id_aux(id_)
            max_try = 0
            fetcher = self.fetch_by_name_aux(x)

            while (obj is None or obj not in fetcher) and max_try < 5:
                id_ = int(
                    input(
                        "id non reconnu. Entrez l'id de l'objet si vous le voyez dans la liste ci-dessus: "
                        + f'({5 - max_try} tentatives restantes)'))
                obj = self.fetch_by_id_aux(id_)
                max_try += 1

            if max_try >= 5:
                clear_output(wait=True)
                display("Maximum de tentatives dépassé. Requête annulée.")
                return None

        elif type(x) == int:
            id_ = x
            obj = self.fetch_by_id_aux(id_)

        clear_output(wait=True)
        display(
            f'Suppression de recette pour la carte ({self.crafts[obj]["name"]})'
        )

        if len(self.crafts[obj]['recipes']) > 0:
            display(
                HTML(f"Carte: (#{obj}: {self.crafts[obj]['name']})<br/>" +
                     f"<br/>Actuellement"))
            self.recipes(id_)

        else:
            clear_output(wait=True)
            display("Aucune recette à supprimer. Requête annulée.")
            return None

        dropdown_recipes = widgets.Dropdown(
            options=["-"] +
            [i + 1 for i in range(len(self.crafts[obj]['recipes']))],
            value="-",
            description="Recette",
            disabled=False)

        output = widgets.Output()
        run_button = widgets.Button(description='Valider')
        cancel_button = widgets.Button(description='Annuler')

        def validate(b):
            res = dropdown_recipes.value
            if res == "-":
                clear_output(wait=True)
                display(dropdown_recipes)
                display(run_button)
                display(cancel_button)
                display(
                    "Veuillez remplir tous les champs ou annuler la requête.")
                return None

            self.crafts[obj]['recipes'].remove(
                self.crafts[obj]['recipes'][res - 1])

            clear_output(wait=True)
            display(
                f"Recette supprimée. (#{obj}: {self.crafts[obj]['name']}) mis à jour.")
            
            global th
            th.save()

        def cancel(b):
            clear_output(wait=True)
            display(f"Requête annulée.")

        run_button.on_click(validate)
        cancel_button.on_click(cancel)
        display(dropdown_recipes)
        display(run_button)
        display(cancel_button)
        output
