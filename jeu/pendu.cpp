#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <algorithm>
#include <cctype>

using namespace std;

class JeuDuPendu {
private:
    vector<string> mots;
    string motSecret;
    string motCache;
    int viesRestantes;
    vector<char> lettresUtilisees;
    const int MAX_VIES = 7;

public:
    JeuDuPendu() {
        // Liste de mots pour le jeu
        mots = {
            "ordinateur", "programmation", "clavier", "souris", "ecran",
            "internet", "telephone", "musique", "cinema", "voiture",
            "avion", "bateau", "montagne", "ocean", "foret",
            "soleil", "planete", "etoile", "galaxie", "univers",
            "livre", "cahier", "stylo", "tableau", "chaise",
            "python", "javascript", "developpeur", "algorithme", "fonction"
        };
        
        // Initialiser le générateur de nombres aléatoires
        srand(time(0));
    }
    
    void demarrer() {
        bool continuer = true;
        
        while (continuer) {
            initialiserJeu();
            jouer();
            continuer = demanderRejouer();
        }
        
        cout << "\n========================================" << endl;
        cout << "   Merci d'avoir joue ! A bientot !" << endl;
        cout << "========================================\n" << endl;
    }

private:
    void initialiserJeu() {
        // Choisir un mot aléatoire
        motSecret = mots[rand() % mots.size()];
        
        // Initialiser le mot caché avec des tirets
        motCache = string(motSecret.length(), '_');
        
        viesRestantes = MAX_VIES;
        lettresUtilisees.clear();
    }
    
    void jouer() {
        afficherBanniere();
        
        while (viesRestantes > 0 && motCache != motSecret) {
            afficherEtat();
            char lettre = demanderLettre();
            
            if (lettreDejaUtilisee(lettre)) {
                cout << "\n>>> Vous avez deja propose cette lettre !" << endl;
                pause();
                continue;
            }
            
            lettresUtilisees.push_back(lettre);
            
            if (verifierLettre(lettre)) {
                cout << "\n>>> Bravo ! La lettre '" << lettre << "' est dans le mot !" << endl;
            } else {
                viesRestantes--;
                cout << "\n>>> Dommage ! La lettre '" << lettre << "' n'est pas dans le mot." << endl;
                cout << ">>> Il vous reste " << viesRestantes << " vie(s)." << endl;
            }
            
            pause();
        }
        
        afficherResultat();
    }
    
    void afficherBanniere() {
        system("cls");
        cout << "\n========================================" << endl;
        cout << "          JEU DU PENDU - C++" << endl;
        cout << "========================================\n" << endl;
    }
    
    void afficherEtat() {
        system("cls");
        afficherPendu();
        
        cout << "\n----------------------------------------" << endl;
        cout << "  Mot a deviner : ";
        for (char c : motCache) {
            cout << c << " ";
        }
        cout << "\n----------------------------------------" << endl;
        
        cout << "\nVies restantes : " << viesRestantes << " / " << MAX_VIES << endl;
        
        if (!lettresUtilisees.empty()) {
            cout << "Lettres utilisees : ";
            for (char c : lettresUtilisees) {
                cout << c << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
    
    void afficherPendu() {
        cout << "\n";
        switch (viesRestantes) {
            case 7:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 6:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 5:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << "  |   |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 4:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << " /|   |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 3:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << " /|\\  |\n";
                cout << "      |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 2:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << " /|\\  |\n";
                cout << " /    |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 1:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  O   |\n";
                cout << " /|\\  |\n";
                cout << " / \\  |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
            case 0:
                cout << "  +---+\n";
                cout << "  |   |\n";
                cout << "  X   |\n";
                cout << " /|\\  |\n";
                cout << " / \\  |\n";
                cout << "      |\n";
                cout << "=========\n";
                break;
        }
    }
    
    char demanderLettre() {
        string input;
        char lettre;
        
        while (true) {
            cout << "Proposez une lettre : ";
            cin >> input;
            
            if (input.length() == 1 && isalpha(input[0])) {
                lettre = tolower(input[0]);
                return lettre;
            } else {
                cout << ">>> Veuillez entrer une seule lettre !" << endl;
            }
        }
    }
    
    bool lettreDejaUtilisee(char lettre) {
        return find(lettresUtilisees.begin(), lettresUtilisees.end(), lettre) != lettresUtilisees.end();
    }
    
    bool verifierLettre(char lettre) {
        bool trouve = false;
        
        for (size_t i = 0; i < motSecret.length(); i++) {
            if (motSecret[i] == lettre) {
                motCache[i] = lettre;
                trouve = true;
            }
        }
        
        return trouve;
    }
    
    void afficherResultat() {
        system("cls");
        
        if (motCache == motSecret) {
            cout << "\n========================================" << endl;
            cout << "          FELICITATIONS !" << endl;
            cout << "========================================" << endl;
            cout << "\nVous avez trouve le mot : " << motSecret << endl;
            cout << "Vies restantes : " << viesRestantes << " / " << MAX_VIES << endl;
            cout << "\n   \\O/  VICTOIRE !  \\O/" << endl;
            cout << "    |              |" << endl;
            cout << "   / \\            / \\" << endl;
        } else {
            afficherPendu();
            cout << "\n========================================" << endl;
            cout << "            GAME OVER !" << endl;
            cout << "========================================" << endl;
            cout << "\nLe mot etait : " << motSecret << endl;
            cout << "\nDommage ! Reessayez !" << endl;
        }
        cout << "\n" << endl;
    }
    
    bool demanderRejouer() {
        string reponse;
        cout << "Voulez-vous rejouer ? (o/n) : ";
        cin >> reponse;
        
        return (reponse == "o" || reponse == "O" || reponse == "oui" || reponse == "OUI");
    }
    
    void pause() {
        cout << "\nAppuyez sur Entree pour continuer...";
        cin.ignore(1000, '\n');
        cin.get();
    }
};

int main() {
    JeuDuPendu jeu;
    jeu.demarrer();
    
    return 0;
}
