# -*- coding: utf-8 -*-

from plone import api
from cs.publiccontracts import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from Acquisition import aq_parent


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class ContractBodiesVocabulary(object):
    """ """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        putils = api.portal.get_tool("plone_utils")
        try:
            contracts_folder = aq_parent(context)
            contracts_bodies = contracts_folder.bodies
            items = [
                VocabItem(putils.normalizeString(i["value"]), i["name"])
                for i in contracts_bodies
            ]
        except:
            items = []

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


ContractBodiesVocabularyFactory = ContractBodiesVocabulary()
