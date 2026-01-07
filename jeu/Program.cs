using System;
using System.Collections.Generic;
using System.Linq;

namespace Morpion
{
    class Program
    {
        static void Main(string[] args)
        {
            JeuMorpion jeu = new JeuMorpion();
            jeu.Demarrer();
        }
    }

    class JeuMorpion
    {
        private char[] grille;
        private char joueur;
        private char ordinateur;
        private Random random;

        public JeuMorpion()
        {
            grille = new char[9];
            joueur = 'X';
            ordinateur = 'O';
            random = new Random();
        }

        public void Demarrer()
        {
            bool continuer = true;

            while (continuer)
            {
                InitialiserGrille();
                Jouer();
                continuer = DemanderRejouer();
            }

            Console.WriteLine("\n========================================");
            Console.WriteLine("   Merci d'avoir joué ! À bientôt !");
            Console.WriteLine("========================================\n");
        }

        private void InitialiserGrille()
        {
            for (int i = 0; i < 9; i++)
            {
                grille[i] = (char)('1' + i);
            }
        }

        private void Jouer()
        {
            AfficherBanniere();
            bool jeuTermine = false;
            bool tourJoueur = true;

            while (!jeuTermine)
            {
                AfficherGrille();

                if (tourJoueur)
                {
                    Console.WriteLine("\n>>> C'est votre tour (X)");
                    int position = DemanderPosition();
                    grille[position - 1] = joueur;
                }
                else
                {
                    Console.WriteLine("\n>>> L'ordinateur joue (O)...");
                    System.Threading.Thread.Sleep(1000);
                    int position = CoupOrdinateur();
                    grille[position] = ordinateur;
                    Console.WriteLine($">>> L'ordinateur joue en position {position + 1}");
                    System.Threading.Thread.Sleep(1000);
                }

                if (VerifierVictoire(tourJoueur ? joueur : ordinateur))
                {
                    AfficherGrille();
                    if (tourJoueur)
                    {
                        AfficherVictoire();
                    }
                    else
                    {
                        AfficherDefaite();
                    }
                    jeuTermine = true;
                }
                else if (GrilleRemplie())
                {
                    AfficherGrille();
                    AfficherMatchNul();
                    jeuTermine = true;
                }

                tourJoueur = !tourJoueur;
            }
        }

        private void AfficherBanniere()
        {
            Console.Clear();
            Console.WriteLine("\n========================================");
            Console.WriteLine("          MORPION (TIC-TAC-TOE)");
            Console.WriteLine("            Joueur vs IA");
            Console.WriteLine("========================================\n");
        }

        private void AfficherGrille()
        {
            Console.Clear();
            Console.WriteLine("\n========================================");
            Console.WriteLine("          MORPION (TIC-TAC-TOE)");
            Console.WriteLine("========================================\n");

            Console.WriteLine("     |     |     ");
            Console.WriteLine($"  {grille[0]}  |  {grille[1]}  |  {grille[2]}  ");
            Console.WriteLine("_____|_____|_____");
            Console.WriteLine("     |     |     ");
            Console.WriteLine($"  {grille[3]}  |  {grille[4]}  |  {grille[5]}  ");
            Console.WriteLine("_____|_____|_____");
            Console.WriteLine("     |     |     ");
            Console.WriteLine($"  {grille[6]}  |  {grille[7]}  |  {grille[8]}  ");
            Console.WriteLine("     |     |     \n");
        }

        private int DemanderPosition()
        {
            while (true)
            {
                Console.Write("Choisissez une case (1-9) : ");
                string? input = Console.ReadLine();

                if (int.TryParse(input, out int position) && position >= 1 && position <= 9)
                {
                    if (grille[position - 1] != joueur && grille[position - 1] != ordinateur)
                    {
                        return position;
                    }
                    else
                    {
                        Console.WriteLine(">>> Cette case est déjà occupée !");
                    }
                }
                else
                {
                    Console.WriteLine(">>> Veuillez entrer un nombre entre 1 et 9 !");
                }
            }
        }

        private int CoupOrdinateur()
        {
            // Essayer de gagner
            int coupGagnant = TrouverCoupGagnant(ordinateur);
            if (coupGagnant != -1) return coupGagnant;

            // Bloquer le joueur
            int coupBloquant = TrouverCoupGagnant(joueur);
            if (coupBloquant != -1) return coupBloquant;

            // Prendre le centre si disponible
            if (grille[4] != joueur && grille[4] != ordinateur)
                return 4;

            // Prendre un coin
            int[] coins = { 0, 2, 6, 8 };
            List<int> coinsDisponibles = coins.Where(c => grille[c] != joueur && grille[c] != ordinateur).ToList();
            if (coinsDisponibles.Count > 0)
                return coinsDisponibles[random.Next(coinsDisponibles.Count)];

            // Prendre n'importe quelle case
            List<int> casesDisponibles = new List<int>();
            for (int i = 0; i < 9; i++)
            {
                if (grille[i] != joueur && grille[i] != ordinateur)
                    casesDisponibles.Add(i);
            }

            return casesDisponibles[random.Next(casesDisponibles.Count)];
        }

        private int TrouverCoupGagnant(char symbole)
        {
            // Toutes les combinaisons gagnantes
            int[][] lignesGagnantes = new int[][]
            {
                new int[] { 0, 1, 2 }, new int[] { 3, 4, 5 }, new int[] { 6, 7, 8 }, // Lignes
                new int[] { 0, 3, 6 }, new int[] { 1, 4, 7 }, new int[] { 2, 5, 8 }, // Colonnes
                new int[] { 0, 4, 8 }, new int[] { 2, 4, 6 }                          // Diagonales
            };

            foreach (var ligne in lignesGagnantes)
            {
                int compteur = 0;
                int caseVide = -1;

                for (int i = 0; i < 3; i++)
                {
                    int pos = ligne[i];
                    if (grille[pos] == symbole)
                        compteur++;
                    else if (grille[pos] != joueur && grille[pos] != ordinateur)
                        caseVide = pos;
                }

                if (compteur == 2 && caseVide != -1)
                    return caseVide;
            }

            return -1;
        }

        private bool VerifierVictoire(char symbole)
        {
            // Lignes
            for (int i = 0; i < 9; i += 3)
            {
                if (grille[i] == symbole && grille[i + 1] == symbole && grille[i + 2] == symbole)
                    return true;
            }

            // Colonnes
            for (int i = 0; i < 3; i++)
            {
                if (grille[i] == symbole && grille[i + 3] == symbole && grille[i + 6] == symbole)
                    return true;
            }

            // Diagonales
            if (grille[0] == symbole && grille[4] == symbole && grille[8] == symbole)
                return true;
            if (grille[2] == symbole && grille[4] == symbole && grille[6] == symbole)
                return true;

            return false;
        }

        private bool GrilleRemplie()
        {
            for (int i = 0; i < 9; i++)
            {
                if (grille[i] != joueur && grille[i] != ordinateur)
                    return false;
            }
            return true;
        }

        private void AfficherVictoire()
        {
            Console.WriteLine("\n========================================");
            Console.WriteLine("          🎉 FÉLICITATIONS ! 🎉");
            Console.WriteLine("========================================");
            Console.WriteLine("\n   Vous avez gagné contre l'IA !");
            Console.WriteLine("\n   \\O/  VICTOIRE !  \\O/");
            Console.WriteLine("    |              |");
            Console.WriteLine("   / \\            / \\\n");
        }

        private void AfficherDefaite()
        {
            Console.WriteLine("\n========================================");
            Console.WriteLine("            GAME OVER !");
            Console.WriteLine("========================================");
            Console.WriteLine("\n   L'ordinateur a gagné !");
            Console.WriteLine("\n   Réessayez pour votre revanche !\n");
        }

        private void AfficherMatchNul()
        {
            Console.WriteLine("\n========================================");
            Console.WriteLine("            MATCH NUL !");
            Console.WriteLine("========================================");
            Console.WriteLine("\n   Égalité parfaite !");
            Console.WriteLine("\n   Personne ne gagne cette fois !\n");
        }

        private bool DemanderRejouer()
        {
            Console.Write("\nVoulez-vous rejouer ? (o/n) : ");
            string? reponse = Console.ReadLine()?.ToLower();
            return reponse == "o" || reponse == "oui";
        }
    }
}
