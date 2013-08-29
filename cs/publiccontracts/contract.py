from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary
from Acquisition import aq_parent
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from five import grok
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from cs.publiccontracts import MessageFactory as _
from plone.app.textfield import RichText
from zope.interface import implements
# Interface class; used to define content-type schema.
class IContract(form.Schema, IImageScaleTraversable):
    """
    Public Contract
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/contract.xml to define the content type
    # and add directives here as necessary.
    file_number = schema.TextLine(
        title=_(u'File Number'),
        description=_(u'Contract file number'),
        required=True,
        )

    file_type = schema.Choice(title=_(u'File Type'),
                          description=_(u'Contract Type'),
                          vocabulary=u'contract_types',
                          required=True,
                          )
    """
    file_procedure = schema.Choice(title=_(u'File Procedure'),
                          description=_(u'Contract Procedure'),
                          vocabulary=u'contract_procedures',
                          required=True,
                          )

    file_processing = schema.Choice(title=_(u'File Processing'),
                          description=_(u'Contract Processing'),
                          vocabulary=u'contract_processings',
                          required=True,
                          )

    file_state = schema.Choice(title=_(u'File State'),
                          description=_(u'Contract State'),
                          vocabulary=u'contract_states',
                          required=True,
                          )
    """
    last_date = schema.Datetime(
            title=_(u"Last Date"),
            description=_(u'Last date for the submission of tenders'),
            required=True,
        )

    info = RichText(title=_(u'info'),
        description=_(u'Contract information'),
        required=False,
        )




# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class Contract(dexterity.Container):
    grok.implements(IContract)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called contractview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type

grok.templatedir('templates')


class ContractView(grok.View):
    grok.context(IContract)
    grok.require('zope2.View')
    grok.name('view')

def ContractTypesVocabulary(context):
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ Vocabularu factory for all contract types"""
        contracts_folder = aq_parent(context)
        contracts_types = contracts_folder.types
        items = []

        for value, name in contracts_types:
            items.append(SimpleTerm(value, value, name))

        return SimpleVocabulary(items)

grok.global_utility(ContractTypesVocabulary, name=u'Lista-de-pilotos')