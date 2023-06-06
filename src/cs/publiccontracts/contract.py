# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from cs.publiccontracts import _
from plone.app.event.base import date_speller
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.textfield import RichText
from plone.autoform.directives import widget
from plone.dexterity.content import Container
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class IDatesRowSchema(Interface):
    title = schema.TextLine(
        title=_(u"Date title"),
        description=_(u"Date title"),
        required=False,
        default=''
    )
    description = schema.TextLine(
        title=_(u"Date description"),
        description=_(u"Date description"),
        required=False,
        default=''
    )
    day = schema.Datetime(
        title=_(u"Day"),
        required=False,
    )
    link = schema.TextLine(
        title=_(u"Date link"),
        description=_(u"Date link"),
        required=False,
        default=''
    )


class IContract(Interface):
    """
    Public Contract
    """

    dexteritytextindexer.searchable("file_number")
    file_number = schema.TextLine(
        title=_(u"File Number"),
        description=_(u"Contract file number"),
        required=True,
    )

    file_type = schema.Choice(
        title=_(u"File Type"),
        description=_(u"Contract Type"),
        vocabulary=u"cs.publiccontracts.ContractTypesVocabulary",
        required=False,
    )

    file_procedure = schema.Choice(
        title=_(u"File Procedure"),
        description=_(u"Contract Procedure"),
        vocabulary=u"cs.publiccontracts.ContractProceduresVocabulary",
        required=False,
    )

    file_processing = schema.Choice(
        title=_(u"File Processing"),
        description=_(u"Contract Processing"),
        vocabulary=u"cs.publiccontracts.ContractProcessingsVocabulary",
        required=False,
    )

    file_organization = schema.Choice(
        title=_(u"File organization"),
        description=_(u"Contract organization"),
        vocabulary=u"cs.publiccontracts.ContractOrganizationsVocabulary",
        required=False,
    )

    file_body = schema.Choice(
        title=_(u"File body"),
        description=_(u"Contract body"),
        vocabulary=u"cs.publiccontracts.ContractBodiesVocabulary",
        required=False,
    )

    file_state = schema.Choice(
        title=_(u"File State"),
        description=_(u"Contract State"),
        vocabulary=u"cs.publiccontracts.ContractStatesVocabulary",
        required=False,
    )

    last_date = schema.Datetime(
        title=_(u"Last Date"),
        description=_(u"Last date for the submission of tenders"),
        required=False,
    )

    dexteritytextindexer.searchable("file_number")
    info = RichText(
        title=_(u"info"),
        description=_(u"Contract information"),
        required=False,
    )

    widget(dates=DataGridFieldFactory)
    dates = schema.List(
        title=u"Dates",
        required=False,
        value_type=DictRow(title=u"Dates", schema=IDatesRowSchema),
        default=[],
    )


alsoProvides(IContract["file_number"], ILanguageIndependentField)
alsoProvides(IContract["file_type"], ILanguageIndependentField)
alsoProvides(IContract["file_procedure"], ILanguageIndependentField)
alsoProvides(IContract["file_processing"], ILanguageIndependentField)
alsoProvides(IContract["file_state"], ILanguageIndependentField)
alsoProvides(IContract["last_date"], ILanguageIndependentField)


def get_vocabulary(name, context):
    factory = getUtility(IVocabularyFactory, name)
    return factory(context)


@implementer(IContract)
class Contract(Container):
    def file_type_string(self):
        vocabulary = get_vocabulary("cs.publiccontracts.ContractTypesVocabulary", self)
        try:
            term = vocabulary.getTerm(self.file_type)
            return term and term.title or None
        except LookupError:
            return None

    def file_procedure_string(self):
        vocabulary = get_vocabulary(
            "cs.publiccontracts.ContractProceduresVocabulary", self
        )
        try:
            term = vocabulary.getTerm(self.file_procedure)
            return term and term.title or None
        except LookupError:
            return None

    def file_processing_string(self):
        vocabulary = get_vocabulary(
            "cs.publiccontracts.ContractProcessingsVocabulary", self
        )
        try:
            term = vocabulary.getTerm(self.file_processing)
            return term and term.title or None
        except LookupError:
            return None

    def file_body_string(self):
        vocabulary = get_vocabulary("cs.publiccontracts.ContractBodiesVocabulary", self)
        try:
            term = vocabulary.getTerm(self.file_body)
            return term and term.title or None
        except LookupError:
            return None

    def file_organization_string(self):
        vocabulary = get_vocabulary(
            "cs.publiccontracts.ContractOrganizationsVocabulary", self
        )
        try:
            term = vocabulary.getTerm(self.file_organization)
            return term and term.title or None
        except LookupError:
            return None

    def file_state_string(self):
        vocabulary = get_vocabulary("cs.publiccontracts.ContractStatesVocabulary", self)
        try:
            term = vocabulary.getTerm(self.file_state)
            return term and term.title or None
        except LookupError:
            return None

    def files(self):
        return self.getFolderContents({"portal_type": ["File", "Link"]}, full_objects=1)

    def contract_state_index(self):
        return self.file_state

    def has_hour(self, date):
        return date_speller(self, date)["hour"] or date_speller(self, date)["minute"]
