from util.emplacement import Emplacement
from util.inventaire import Inventaire
from util.oeuvre import Oeuvre
#emplacement 
def test_type_attributs(self):
        emplacement = emplacement(2, "Zone B")
        self.assertIsInstance(emplacement.numeroEmplacement, int)
        self.assertIsInstance(emplacement.nom, str)

#inventaire
class TestInventaire(test.TestCase):
    def setUp(self):
        self.inventaire = Inventaire()
        self.oeuvre1 = Oeuvre(1, "Mona Lisa", "Léonard de Vinci")
        self.oeuvre2 = Oeuvre(2, "La Nuit étoilée", "Vincent van Gogh")
        
    def test_ajout_oeuvre(self):
        self.assertTrue(self.inventaire.ajouterOeuvre(self.oeuvre1))
        self.assertIn(self.oeuvre1, self.inventaire.listeOeuvres)

    def test_recuperer_oeuvre(self):
        self.inventaire.ajouterOeuvre(self.oeuvre1)
        self.assertEqual(self.inventaire.recupererOeuvre(1), self.oeuvre1)
        self.assertIsNone(self.inventaire.recupererOeuvre(99))

    def test_supprimer_oeuvre(self):
        self.inventaire.ajouterOeuvre(self.oeuvre1)
        self.assertTrue(self.inventaire.supprimerOeuvre(1))
        self.assertFalse(self.inventaire.supprimerOeuvre(1))
#oeuvre
class TestOeuvre(test.TestCase):
    def setUp(self):
        self.oeuvre = Oeuvre(1, "La Joconde", "Léonard de Vinci", date(1503, 1, 1), 850000000, ETATS[1])
    
    def test_initialisation(self):
        self.assertEqual(self.oeuvre.numeroOeuvre, 1)
        self.assertEqual(self.oeuvre.nom, "La Joconde")
        self.assertEqual(self.oeuvre.createur, "Léonard de Vinci")
        self.assertEqual(self.oeuvre.valeur, 850000000)
        self.assertEqual(self.oeuvre.etat, ETATS[1])
    
    def test_modification_createur(self):
        self.oeuvre.modifierCreateur("Anonyme")
        self.assertEqual(self.oeuvre.createur, "Anonyme")
    
    def test_modification_valeur(self):
        self.assertTrue(self.oeuvre.modifierValeur(900000000))
        self.assertEqual(self.oeuvre.valeur, 900000000)
        self.assertFalse(self.oeuvre.modifierValeur(-100))
    
    def test_modification_etat(self):
        self.oeuvre.modifierEtat(ETATS[2])
        self.assertEqual(self.oeuvre.etat, ETATS[2])
    
    def test_conversion_json(self):
        json_data = self.oeuvre.JSON()
        oeuvre_from_json = Oeuvre.depuisJSON(json_data)
        self.assertEqual(oeuvre_from_json.nom, "La Joconde")
        self.assertEqual(oeuvre_from_json.createur, "Léonard de Vinci")
        self.assertEqual(oeuvre_from_json.valeur, 850000000)
        self.assertEqual(oeuvre_from_json.etat, ETATS[1])
