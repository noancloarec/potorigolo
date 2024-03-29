#! python3

"""
Grammar checker tests for French language
"""

import unittest
import os
import re
import time

from ..graphspell.ibdawg import IBDAWG
from ..graphspell.echo import echo
from . import conj
from . import phonet
from . import mfsp


class TestDictionary (unittest.TestCase):
    "Test du correcteur orthographique"

    @classmethod
    def setUpClass (cls):
        cls.oDic = IBDAWG("fr-allvars.bdic")

    def test_lookup (self):
        for sWord in ["branche", "Émilie"]:
            self.assertTrue(self.oDic.lookup(sWord), sWord)

    def test_lookup_failed (self):
        for sWord in ["Branche", "BRANCHE", "BranchE", "BRanche", "BRAnCHE", "émilie"]:
            self.assertFalse(self.oDic.lookup(sWord), sWord)

    def test_isvalid (self):
        for sWord in ["Branche", "branche", "BRANCHE", "Émilie", "ÉMILIE", "aujourd'hui", "aujourd’hui", "Aujourd'hui", "Aujourd’hui"]:
            self.assertTrue(self.oDic.isValid(sWord), sWord)

    def test_isvalid_failed (self):
        for sWord in ["BranchE", "BRanche", "BRAnCHE", "émilie", "éMILIE", "émiLie"]:
            self.assertFalse(self.oDic.isValid(sWord), sWord)


class TestConjugation (unittest.TestCase):
    "Tests des conjugaisons"

    @classmethod
    def setUpClass (cls):
        pass

    def test_isverb (self):
        for sVerb in ["avoir", "être", "aller", "manger", "courir", "venir", "faire", "finir"]:
            self.assertTrue(conj.isVerb(sVerb), sVerb)
        for sVerb in ["berk", "a", "va", "contre", "super", "", "à"]:
            self.assertFalse(conj.isVerb(sVerb), sVerb)

    def test_hasconj (self):
        for sVerb, sTense, sWho in [("aller", ":E", ":2s"), ("avoir", ":Is", ":1s"), ("être", ":Ip", ":2p"),
                                    ("manger", ":Sp", ":3s"), ("finir", ":K", ":3p"), ("prendre", ":If", ":1p")]:
            self.assertTrue(conj.hasConj(sVerb, sTense, sWho), sVerb)

    def test_getconj (self):
        for sVerb, sTense, sWho, sConj in [("aller", ":E", ":2s", "va"), ("avoir", ":Iq", ":1s", "avais"), ("être", ":Ip", ":2p", "êtes"),
                                           ("manger", ":Sp", ":3s", "mange"), ("finir", ":K", ":3p", "finiraient"), ("prendre", ":If", ":1p", "prendrons")]:
            self.assertEqual(conj.getConj(sVerb, sTense, sWho), sConj, sVerb)


class TestPhonet (unittest.TestCase):
    "Tests des équivalences phonétiques"

    @classmethod
    def setUpClass (cls):
        cls.lSet = [
            ["ce", "se"],
            ["ces", "saie", "saies", "ses", "sais", "sait"],
            ["cet", "cette", "sept", "set", "sets"],
            ["dé", "dés", "dès", "dais", "des"],
            ["don", "dons", "dont"],
            ["été", "étaie", "étaies", "étais", "était", "étai", "étés", "étaient"],
            ["faire", "fer", "fers", "ferre", "ferres", "ferrent"],
            ["fois", "foi", "foie", "foies"],
            ["la", "là", "las"],
            ["mes", "mets", "met", "mai", "mais"],
            ["mon", "mont", "monts"],
            ["mot", "mots", "maux"],
            ["moi", "mois"],
            ["notre", "nôtre", "nôtres"],
            ["or", "ors", "hors"],
            ["hou", "houe", "houes", "ou", "où", "houx"],
            ["peu", "peux", "peut"],
            ["son", "sons", "sont"],
            ["tes", "tais", "tait", "taie", "taies", "thé", "thés"],
            ["toi", "toit", "toits"],
            ["ton", "tons", "thon", "thons", "tond", "tonds"],
            ["voir", "voire"]
        ]

    def test_getsimil (self):
        for aSet in self.lSet:
            for sWord in aSet:
                self.assertListEqual(phonet.getSimil(sWord), sorted(aSet))


class TestMasFemSingPlur (unittest.TestCase):
    "Tests des masculins, féminins, singuliers et pluriels"

    @classmethod
    def setUpClass (cls):
        cls.lPlural = [
            ("travail", ["travaux"]),
            ("vœu", ["vœux"]),
            ("gentleman", ["gentlemans", "gentlemen"])
        ]

    def test_getplural (self):
        for sSing, lPlur in self.lPlural:
            self.assertListEqual(mfsp.getMiscPlural(sSing), lPlur)


def main():
    "start function"
    unittest.main()


if __name__ == '__main__':
    main()
