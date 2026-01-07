import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Calculatrice extends JFrame implements ActionListener {
    
    // Composants
    private JTextField affichage;
    private JButton[] boutons_chiffres;
    private JButton[] boutons_operations;
    private JButton bouton_egal, bouton_effacer, bouton_supprimer, bouton_virgule;
    private JPanel panneau;
    
    // Variables de calcul
    private double nombre1 = 0, nombre2 = 0, resultat = 0;
    private char operateur;
    
    public Calculatrice() {
        // Configuration de la fenêtre
        setTitle("Calculatrice");
        setSize(400, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);
        setResizable(false);
        getContentPane().setBackground(new Color(50, 50, 50));
        
        // Affichage
        affichage = new JTextField();
        affichage.setBounds(30, 30, 340, 80);
        affichage.setFont(new Font("Arial", Font.BOLD, 32));
        affichage.setEditable(false);
        affichage.setHorizontalAlignment(JTextField.RIGHT);
        affichage.setBackground(new Color(230, 230, 230));
        affichage.setBorder(BorderFactory.createLineBorder(Color.BLACK, 2));
        add(affichage);
        
        // Initialiser les boutons
        boutons_chiffres = new JButton[10];
        for (int i = 0; i < 10; i++) {
            boutons_chiffres[i] = new JButton(String.valueOf(i));
            boutons_chiffres[i].addActionListener(this);
            boutons_chiffres[i].setFont(new Font("Arial", Font.BOLD, 28));
            boutons_chiffres[i].setFocusable(false);
            boutons_chiffres[i].setBackground(new Color(255, 255, 255));
            boutons_chiffres[i].setForeground(new Color(30, 30, 30));
            boutons_chiffres[i].setBorder(BorderFactory.createLineBorder(new Color(150, 150, 150), 3));
        }
        
        // Boutons d'opérations
        boutons_operations = new JButton[4];
        boutons_operations[0] = new JButton("+");
        boutons_operations[1] = new JButton("-");
        boutons_operations[2] = new JButton("×");
        boutons_operations[3] = new JButton("÷");
        
        for (int i = 0; i < 4; i++) {
            boutons_operations[i].addActionListener(this);
            boutons_operations[i].setFont(new Font("Arial", Font.BOLD, 32));
            boutons_operations[i].setFocusable(false);
            boutons_operations[i].setBackground(new Color(100, 150, 255));
            boutons_operations[i].setForeground(Color.BLACK);
            boutons_operations[i].setBorder(BorderFactory.createLineBorder(new Color(70, 120, 220), 3));
        }
        
        // Boutons spéciaux
        bouton_egal = new JButton("=");
        bouton_egal.addActionListener(this);
        bouton_egal.setFont(new Font("Arial", Font.BOLD, 32));
        bouton_egal.setFocusable(false);
        bouton_egal.setBackground(new Color(76, 175, 80));
        bouton_egal.setForeground(Color.BLACK);
        bouton_egal.setBorder(BorderFactory.createLineBorder(new Color(50, 140, 50), 3));
        
        bouton_effacer = new JButton("C");
        bouton_effacer.addActionListener(this);
        bouton_effacer.setFont(new Font("Arial", Font.BOLD, 28));
        bouton_effacer.setFocusable(false);
        bouton_effacer.setBackground(new Color(255, 90, 90));
        bouton_effacer.setForeground(Color.BLACK);
        bouton_effacer.setBorder(BorderFactory.createLineBorder(new Color(220, 50, 50), 3));
        
        bouton_supprimer = new JButton("DEL");
        bouton_supprimer.addActionListener(this);
        bouton_supprimer.setFont(new Font("Arial", Font.BOLD, 28));
        bouton_supprimer.setFocusable(false);
        bouton_supprimer.setBackground(new Color(255, 90, 90));
        bouton_supprimer.setForeground(Color.BLACK);
        bouton_supprimer.setBorder(BorderFactory.createLineBorder(new Color(220, 50, 50), 3));
        
        bouton_virgule = new JButton(".");
        bouton_virgule.addActionListener(this);
        bouton_virgule.setFont(new Font("Arial", Font.BOLD, 32));
        bouton_virgule.setFocusable(false);
        bouton_virgule.setBackground(new Color(255, 255, 255));
        bouton_virgule.setForeground(new Color(30, 30, 30));
        bouton_virgule.setBorder(BorderFactory.createLineBorder(new Color(150, 150, 150), 3));
        
        // Panneau pour disposer les boutons
        panneau = new JPanel();
        panneau.setBounds(30, 140, 340, 400);
        panneau.setLayout(new GridLayout(5, 4, 10, 10));
        panneau.setBackground(new Color(50, 50, 50));
        
        // Disposition des boutons (comme une vraie calculatrice)
        // Ligne 1: C, DEL, ÷
        panneau.add(bouton_effacer);
        panneau.add(bouton_supprimer);
        panneau.add(new JLabel()); // Espace vide
        panneau.add(boutons_operations[3]); // ÷
        
        // Ligne 2: 7, 8, 9, ×
        panneau.add(boutons_chiffres[7]);
        panneau.add(boutons_chiffres[8]);
        panneau.add(boutons_chiffres[9]);
        panneau.add(boutons_operations[2]); // ×
        
        // Ligne 3: 4, 5, 6, -
        panneau.add(boutons_chiffres[4]);
        panneau.add(boutons_chiffres[5]);
        panneau.add(boutons_chiffres[6]);
        panneau.add(boutons_operations[1]); // -
        
        // Ligne 4: 1, 2, 3, +
        panneau.add(boutons_chiffres[1]);
        panneau.add(boutons_chiffres[2]);
        panneau.add(boutons_chiffres[3]);
        panneau.add(boutons_operations[0]); // +
        
        // Ligne 5: 0, ., =
        panneau.add(new JLabel()); // Espace vide
        panneau.add(boutons_chiffres[0]);
        panneau.add(bouton_virgule);
        panneau.add(bouton_egal);
        
        add(panneau);
        
        // Centrer la fenêtre
        setLocationRelativeTo(null);
        setVisible(true);
    }
    
    @Override
    public void actionPerformed(ActionEvent e) {
        String texte = affichage.getText();
        
        // Gestion des chiffres
        for (int i = 0; i < 10; i++) {
            if (e.getSource() == boutons_chiffres[i]) {
                affichage.setText(texte + String.valueOf(i));
            }
        }
        
        // Gestion de la virgule
        if (e.getSource() == bouton_virgule) {
            // Vérifier qu'il n'y a pas déjà de virgule dans le nombre actuel
            String[] parties = texte.split("[+\\-×÷]");
            if (parties.length > 0) {
                String dernierNombre = parties[parties.length - 1];
                if (!dernierNombre.contains(".")) {
                    affichage.setText(texte + ".");
                }
            }
        }
        
        // Gestion des opérations - afficher sur l'écran
        if (e.getSource() == boutons_operations[0]) { // +
            if (!texte.isEmpty() && !texte.endsWith("+") && !texte.endsWith("-") && 
                !texte.endsWith("×") && !texte.endsWith("÷")) {
                affichage.setText(texte + " + ");
            }
        }
        if (e.getSource() == boutons_operations[1]) { // -
            if (!texte.isEmpty() && !texte.endsWith("+") && !texte.endsWith("-") && 
                !texte.endsWith("×") && !texte.endsWith("÷")) {
                affichage.setText(texte + " - ");
            }
        }
        if (e.getSource() == boutons_operations[2]) { // ×
            if (!texte.isEmpty() && !texte.endsWith("+") && !texte.endsWith("-") && 
                !texte.endsWith("×") && !texte.endsWith("÷")) {
                affichage.setText(texte + " × ");
            }
        }
        if (e.getSource() == boutons_operations[3]) { // ÷
            if (!texte.isEmpty() && !texte.endsWith("+") && !texte.endsWith("-") && 
                !texte.endsWith("×") && !texte.endsWith("÷")) {
                affichage.setText(texte + " ÷ ");
            }
        }
        
        // Gestion du bouton égal - évaluer l'expression complète
        if (e.getSource() == bouton_egal) {
            try {
                double resultatFinal = evaluerExpression(texte);
                
                // Afficher le résultat (sans décimales inutiles)
                if (resultatFinal == (long) resultatFinal) {
                    affichage.setText(String.valueOf((long)resultatFinal));
                } else {
                    affichage.setText(String.format("%.4f", resultatFinal).replaceAll("0*$", "").replaceAll("\\.$", ""));
                }
            } catch (Exception ex) {
                affichage.setText("Erreur");
            }
        }
        
        // Gestion du bouton effacer
        if (e.getSource() == bouton_effacer) {
            affichage.setText("");
        }
        
        // Gestion du bouton supprimer
        if (e.getSource() == bouton_supprimer) {
            String texteActuel = affichage.getText();
            if (texteActuel.length() > 0) {
                affichage.setText(texteActuel.substring(0, texteActuel.length() - 1));
            }
        }
    }
    
    // Méthode pour évaluer une expression mathématique
    private double evaluerExpression(String expression) {
        // Remplacer les symboles par des opérateurs standards
        expression = expression.replace("×", "*").replace("÷", "/").replace(" ", "");
        
        // Évaluer l'expression avec priorité des opérations
        return evaluer(expression);
    }
    
    private double evaluer(String expr) {
        // D'abord traiter les multiplications et divisions
        while (expr.contains("*") || expr.contains("/")) {
            // Trouver la première multiplication ou division
            int posM = expr.indexOf("*");
            int posD = expr.indexOf("/");
            int pos;
            char op;
            
            if (posM == -1) {
                pos = posD;
                op = '/';
            } else if (posD == -1) {
                pos = posM;
                op = '*';
            } else {
                if (posM < posD) {
                    pos = posM;
                    op = '*';
                } else {
                    pos = posD;
                    op = '/';
                }
            }
            
            // Extraire les nombres avant et après l'opérateur
            int debut = pos - 1;
            while (debut > 0 && (Character.isDigit(expr.charAt(debut - 1)) || expr.charAt(debut - 1) == '.')) {
                debut--;
            }
            
            int fin = pos + 1;
            while (fin < expr.length() && (Character.isDigit(expr.charAt(fin)) || expr.charAt(fin) == '.')) {
                fin++;
            }
            
            double a = Double.parseDouble(expr.substring(debut, pos));
            double b = Double.parseDouble(expr.substring(pos + 1, fin));
            double resultat = (op == '*') ? a * b : a / b;
            
            expr = expr.substring(0, debut) + resultat + expr.substring(fin);
        }
        
        // Ensuite traiter les additions et soustractions
        double total = 0;
        int i = 0;
        boolean addition = true;
        StringBuilder nombre = new StringBuilder();
        
        while (i < expr.length()) {
            char c = expr.charAt(i);
            
            if (c == '+' || c == '-') {
                if (nombre.length() > 0) {
                    if (addition) {
                        total += Double.parseDouble(nombre.toString());
                    } else {
                        total -= Double.parseDouble(nombre.toString());
                    }
                    nombre = new StringBuilder();
                }
                addition = (c == '+');
            } else {
                nombre.append(c);
            }
            i++;
        }
        
        // Ajouter le dernier nombre
        if (nombre.length() > 0) {
            if (addition) {
                total += Double.parseDouble(nombre.toString());
            } else {
                total -= Double.parseDouble(nombre.toString());
            }
        }
        
        return total;
    }
    
    public static void main(String[] args) {
        // Utiliser le look and feel du système
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        new Calculatrice();
    }
}
