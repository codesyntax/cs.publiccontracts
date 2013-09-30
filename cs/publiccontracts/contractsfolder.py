from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope import schema
from cs.publiccontracts import MessageFactory as _
from five import grok
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from zope.interface import Interface
from plone.namedfile.field import NamedBlobFile
from cs.publiccontracts.contract import IContract

class IContractTypesRowSchema(Interface):

    value = schema.TextLine(title=_(u'Contract type value'))
    name = schema.TextLine(title=_(u'Contract type name'))


class IContractStatesRowSchema(Interface):

    value = schema.TextLine(title=_(u'Contract state value'))
    name = schema.TextLine(title=_(u'Contract state name'))


class IContractProceduresRowSchema(Interface):

    value = schema.TextLine(title=_(u'Contract procedure value'))
    name = schema.TextLine(title=_(u'Contract procedure name'))


class IContractProcessingsRowSchema(Interface):

    value = schema.TextLine(title=_(u'Contract processing value'))
    name = schema.TextLine(title=_(u'Contract processing name'))


# Interface class; used to define content-type schema.
class IContractsFolder(form.Schema, IImageScaleTraversable):
    """
    Contracts Folder
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/contractsfolder.xml to define the content type
    # and add directives here as necessary.
    form.widget(types=DataGridFieldFactory)
    types = schema.List(title=_(u'Contract Types'),
        description=_(u'Enter here the contract types'),
        required=False,
        value_type=DictRow(title=_(u'Contract Types'),
                          schema=IContractTypesRowSchema,
                          required=False)
        )

    form.widget(states=DataGridFieldFactory)
    states = schema.List(title=_(u'Contract States'),
        description=_(u'Enter here the contract states'),
        required=False,
        value_type=DictRow(title=_(u'Contract States'),
                          schema=IContractStatesRowSchema,
                          required=False)
        )

    form.widget(procedures=DataGridFieldFactory)
    procedures = schema.List(title=_(u'Contract Procedures'),
        description=_(u'Enter here the contract Procedures'),
        required=False,
        value_type=DictRow(title=_(u'Contract Procedures'),
                          schema=IContractProceduresRowSchema,
                          required=False)
        )

    form.widget(processings=DataGridFieldFactory)
    processings = schema.List(title=_(u'Contract Processings'),
        description=_(u'Enter here the contract Processings'),
        required=False,
        value_type=DictRow(title=_(u'Contract Processings'),
                          schema=IContractProcessingsRowSchema,
                          required=False)
        )

    generic_file = NamedBlobFile(title=_(u'Generic File'),
                           required=False,
     )




# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class ContractsFolder(dexterity.Container):
    grok.implements(IContractsFolder)
    # Add your class methods and properties here



# View class
# The view will automatically use a similarly named template in
# templates called contractsfolderview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type

grok.templatedir('templates')


class ContractsFolderView(grok.View):
    grok.context(IContractsFolder)
    grok.require('zope2.View')
    grok.name('view')

    def contracts_dict(self):

        context = aq_inner(self.context)
        states_dict = context.states
        catalog = getToolByName(context, 'portal_catalog')
        states_list = []
        contracts_path = '/'.join(context.getPhysicalPath())
        if not states_dict:
            state_dict = {}
            contracts = catalog(object_provides=IContract.__identifier__,
                                review_state="published",
                                path=contracts_path)
            state_dict['contracts'] = contracts
            state_dict['title'] = ''
            state_dict['value'] = ''
            states_list.append(state_dict)
            return states_list

        for state in states_dict:
            state_dict = {}
            state_value = state['value']
            contracts = catalog(object_provides=IContract.__identifier__,
                                review_state="published",
                                contract_state=state_value,
                                path=contracts_path)
            state_dict['title'] = state['name']
            state_dict['value'] = state['value']
            state_dict['contracts'] = contracts

            states_list.append(state_dict)
        return states_list

    def has_states(self):
        context = aq_inner(self.context)
        states_dict = context.states
        if states_dict:
            return True
        else:
            return False

    def has_procedures(self):
        context = aq_inner(self.context)
        procedures_dict = context.procedures
        if procedures_dict:
            return True
        else:
            return False

    def has_processings(self):
        context = aq_inner(self.context)
        processings_dict = context.processings
        if processings_dict:
            return True
        else:
            return False

    def has_types(self):
        context = aq_inner(self.context)
        types_dict = context.types
        if types_dict:
            return True
        else:
            return False


class ContractTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ Vocabularu factory for all contract types"""
        contracts_folder = context
        contracts_types = contracts_folder.types
        items = [(i['name'], i['value']) for i in contracts_types]
        return SimpleVocabulary.fromItems(items)

grok.global_utility(ContractTypesVocabulary, name=u'contract_types')


class ContractProceduresVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ Vocabularu factory for all contract types"""
        contracts_folder = context
        contracts_procedures = contracts_folder.procedures
        items = [(i['name'], i['value']) for i in contracts_procedures]
        return SimpleVocabulary.fromItems(items)

grok.global_utility(ContractProceduresVocabulary, name=u'contract_procedures')


class ContractProcessingsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ Vocabularu factory for all contract types"""
        contracts_folder = context
        contracts_processings = contracts_folder.processings
        items = [(i['name'], i['value']) for i in contracts_processings]
        return SimpleVocabulary.fromItems(items)

grok.global_utility(ContractProcessingsVocabulary, name=u'contract_processings')


class ContractStatesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ Vocabularu factory for all contract types"""
        contracts_folder = context
        contracts_states = contracts_folder.states
        items = [(i['name'], i['value']) for i in contracts_states]
        return SimpleVocabulary.fromItems(items)

grok.global_utility(ContractStatesVocabulary, name=u'contract_states')
