# -*- coding: utf-8 -*-
from cs.publiccontracts import _
from cs.publiccontracts.testing import CS_PUBLICCONTRACTS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class ContractStatesVocabularyIntegrationTest(unittest.TestCase):

    layer = CS_PUBLICCONTRACTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_contract_states_vocabulary(self):
        vocab_name = "cs.publiccontracts.ContractStatesVocabulary"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(
            vocabulary.getTerm("sony-a7r-iii").title, _(u"Sony Aplha 7R III"),
        )
