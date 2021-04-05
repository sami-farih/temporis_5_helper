from card import Card
from cardlist import CardList
from craftlist import CraftList
from imports import *
from globalvars import card_list


class TemporisHelper:
    """
    Cet outil a pour but de référencer les crafts et les cartes de Temporis V.
    
    
    Utilisation:
    
        th.help()                            Aide
        
    
        th.cards.list()                      Liste des cartes Temporis V
        
        th.cards.show(id)                    Cherche une carte ainsi que les crafts où elle intervient
            ex: th.cards.search(37)          Carte no 37
                th.cards.search('cochon')    Cartes dont le nom ressemble ou contient 'cochon'
            
        th.cards.add(id)                     Ajoute une méthode de drop à la carte
        
        th.cards.remove(id)                  Retire une méthode de drop à la carte
        
        th.cards.check_recipe(ids)           Cherche la recette correspondant à la combinaison de cartes
        
        
        th.craft.list()                      Liste des objets craftables (à éviter si possible)
        
        th.craft.recipes(id)                 Cherche les recettes du craft
            ex: th.cards.recipes(1)          Recettes de l'item no 1
                th.cards.recipes('pain')     Recettes des items dont le nom ressemble ou contient 'pain'
                
        th.craft.search(id)                  Cherche un item
        
        th.craft.add(id)                     Ajoute une recette à l'item
        
        th.craft.remove(id)                  Retire une recette à l'item
    """
    def __init__(self, new=False, backup_id=''):
        if not new:
            try:
                self.load(backup_id)
            except:
                print("Sauvegarde non trouvée. Création d'un nouvel outil.")
                self.cards = CardList([
                    Card(*i)
                    for i in list(zip(card_list.keys(), card_list.values()))
                ])
                self.craft = CraftList(self.cards)

                self.cpt = 0
                self.cur_time = time()
                self.cards.crafts = self.craft

    def save(self):
        id_ = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

        with open(f'saves/temporis_helper_save.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print(
            f'Sauvegarde: temporis_helper_save.pkl')

        if self.cpt >= 20 or self.cur_time - time() >= 7200:
            with open(f'saves/temporis_helper_save_{id_}.pkl', 'wb') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
            print(
                f'Sauvegarde: temporis_helper_save{id_}.pkl')
            self.cpt = 0
            self.cur_time = time()

    def load(self, id_=''):
        with open(f'saves/temporis_helper_save{"_" + id_ if id_ != "" else ""}.pkl',
                  'rb') as f:
            tmp_dict = pickle.load(f)
        self.__dict__.update(tmp_dict.__dict__)

    def help(self):
        print(self.__doc__)
