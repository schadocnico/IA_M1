import sys

class Morpion:
    """Un etat est un tableau qui represente le jeu en cours."""
    # 1 est l'ordi et -1 le joueur
    def __init__(self):
        self.commence = -1

    def gagnant(self, jeu):
        """Test si il y'a un gagant et retourne le gagnant. Sinon retourne 0"""
        res = 0
        if jeu[0]!=0 and jeu[0]==jeu[3]==jeu[6]:
            res = jeu[0]
        if jeu[1]!=0 and jeu[1]==jeu[4]==jeu[7]:
            res = jeu[1]
        if jeu[2]!=0 and jeu[2]==jeu[5]==jeu[8]:
            res = jeu[2]
        if jeu[0]!=0 and jeu[0]==jeu[1]==jeu[2]:
            res = jeu[0]
        if jeu[4]!=0 and jeu[4]==jeu[5]==jeu[3]:
            res = jeu[4]
        if jeu[7]!=0 and jeu[7]==jeu[8]==jeu[6]:
            res = jeu[7]
        if jeu[0]!=0 and jeu[0]==jeu[4]==jeu[8]:
            res = jeu[0]
        if jeu[2]!=0 and jeu[2]==jeu[4]==jeu[6]:
            res = jeu[2]
        return res

    def joueur(self, etat):
        """Retourne si c'est le joueur 1 ou -1 qui doit jouer en fonction d'un etat"""
        nb_x = 0
        nb_o = 0
        for case in etat:
            if case == -1:
                nb_x += 1
            if case == 1:
                nb_o += 1
        if nb_x == nb_o:
            return self.commence
        else:
            return self.commence * -1
    
    def coups_possible(self, etat):
        """Retourne un tableau avec les index des coups possible"""
        coups = []
        for i in range(etat.__len__()):
            if etat[i] == 0:
                coups.append(i)
        return coups
            
    def test_terminal(self, etat):
        """Test si c'est un etat terminal -> Si il y a un gagnant ou match nul"""
        if 0 in etat:        
            return self.gagnant(etat)!=0
        else:
            return True
        
    def utilite(self, etat):
        """Associe un score en tant que etat terminal, -1 si le joueur gagne sinon 1 et 0 match nul"""
        return self.gagnant(etat)

    def successeurs_etat(self, etat):
        """retourne tous les successeurs sous la forme d'un tableau de couple (coup joué, etat apres coup)"""
        coups_possible = self.coups_possible(etat)
        joueur = self.joueur(etat)
        successeurs = []
        for coup in coups_possible:
            etat_tmp = etat.copy()
            etat_tmp[coup] = joueur
            successeurs.append((coup, etat_tmp))
        return successeurs

    # algorithme min-max

    def valeur_max(self, etat):
        if self.test_terminal(etat):
            return self.utilite(etat)

        v = -10000
        for a,s in self.successeurs_etat(etat):
            v = max(v, self.valeur_min(s))
        return v

    def valeur_min(self, etat):
        if self.test_terminal(etat):
            return self.utilite(etat)

        v = 10000
        for a,s in self.successeurs_etat(etat):
            v = min(v, self.valeur_max(s))
        return v

    def decision_minimax(self, etat):
        successeurs_vals = []
        for a,s in self.successeurs_etat(etat):
            # Applique l'algo min aux successeurs de l'etat actuel sous forme de couple (valeur, action(0-9))
            successeurs_vals.append((self.valeur_min(s), a))
        # Retourne la meilleur action
        return max(successeurs_vals, key=lambda x: x[0])[1]
    
    # algorithme alpha-beta

    def valeur_max_ab(self, etat, alpha, beta):
        if self.test_terminal(etat):
            return self.utilite(etat)

        v = -10000
        for a,s in self.successeurs_etat(etat):
            v = max(v, self.valeur_min_ab(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def valeur_min_ab(self, etat, alpha, beta):
        if self.test_terminal(etat):
            return self.utilite(etat)

        v = 10000
        for a,s in self.successeurs_etat(etat):
            v = min(v, self.valeur_max_ab(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def recherche_alpha_beta(self, etat):
        successeurs_vals = []
        alpha = -1000
        beta = 1000
        for a,s in self.successeurs_etat(etat):
            # Applique l'algo min aux successeurs de l'etat actuel sous forme de couple (valeur, action(0-9))
            v = self.valeur_min_ab(s, alpha, beta)
            successeurs_vals.append((v, a))
        # Retourne la meilleur action
        return max(successeurs_vals, key=lambda x: x[0])[1]

    # fonction demarre

    def demarre(self, commence=1, algo=2):
        """Demarre avec l'algo algo=1(minmax) ou algo=2(alpha-beta) et commence=1 si le l'ordi commence et -1 pour le joueur"""
        self.commence = commence # -1 si le joueur commence 1 sinon
        if algo == 1 :
            algo = self.decision_minimax
        else:
            algo = self.recherche_alpha_beta
        plateau = [0]*9
        while(not self.test_terminal(plateau)):
            self.afficher_etat(plateau)
            if(self.joueur(plateau) == -1):
                self.afficher_joueur("Au joueur de jouer :\n")
                inp = -1
                while(not inp in self.coups_possible(plateau)):
                    inp = self.selectionner_case()
                plateau[inp] = -1
            else:
                self.afficher_joueur("L'ordi joue :\n")
                plateau[algo(plateau)] = 1

        self.afficher_etat(plateau)

    # Methodes d'affichage

    def afficher_joueur(self, text):
        print(text)

    def selectionner_case(self):
        try:
            inp = int(input())
        except ValueError:
            inp = -1
        return inp

    def afficher_etat(self, etat):
        aff = ""
        for i in range(9):
            if i%3 == 0 and i != 0:
                aff += '\n'
            if etat[i] == 0:
                aff += str(i)
            else:
                if etat[i] == 1:
                    if self.commence == -1:
                        aff += 'O'
                    else:
                        aff += 'X'
                else:
                    if self.commence == -1:
                        aff += 'X'
                    else:
                        aff += 'O'
        print(aff)

    def __str__(self):
        return plateau.__str__()

try:
    if __name__ == "__main__":
        BOLD = '\033[1m'
        END = "\033[0;0m"

        morpion = Morpion()

        print("Choisissez l'algo: minmax[" + BOLD + "0" + END + "] alpha-beta[1]")
        try:
            algo_inp = int(input())
        except ValueError:
            algo_inp = 0

        print("Choisissez qui commence: Joueur[" + BOLD + "-1" + END + "] Ordi[1]")
        try:
            choix_inp = int(input())
        except ValueError:
            choix_inp = -1

        morpion.demarre(algo=algo_inp, commence=choix_inp)
        
except KeyboardInterrupt:
    print('')


