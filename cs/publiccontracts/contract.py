from Acquisition import aq_parent
from five import grok
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from cs.publiccontracts import MessageFactory as _
from plone.app.textfield import RichText
from zope.interface import alsoProvides
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

    file_type = schema.Choice(
        title=_(u'File Type'),
        description=_(u'Contract Type'),
        vocabulary=u'contract_types',
        required=False,
        )

    file_procedure = schema.Choice(
        title=_(u'File Procedure'),
        description=_(u'Contract Procedure'),
        vocabulary=u'contract_procedures',
        required=False,
        )

    file_processing = schema.Choice(
        title=_(u'File Processing'),
        description=_(u'Contract Processing'),
        vocabulary=u'contract_processings',
        required=False,
        )

    file_state = schema.Choice(
        title=_(u'File State'),
        description=_(u'Contract State'),
        vocabulary=u'contract_states',
        required=False,
        )

    last_date = schema.Datetime(
        title=_(u"Last Date"),
        description=_(u'Last date for the submission of tenders'),
        required=False,
        )

    info = RichText(
        title=_(u'info'),
        description=_(u'Contract information'),
        required=False,
        )

try:
    from plone.multilingualbehavior.interfaces import ILanguageIndependentField
    alsoProvides(IContract['file_number'], ILanguageIndependentField)
    alsoProvides(IContract['file_type'], ILanguageIndependentField)
    alsoProvides(IContract['file_procedure'], ILanguageIndependentField)
    alsoProvides(IContract['file_processing'], ILanguageIndependentField)
    alsoProvides(IContract['file_state'], ILanguageIndependentField)
    alsoProvides(IContract['last_date'], ILanguageIndependentField)
except:
    pass


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class Contract(dexterity.Container):
    grok.implements(IContract)
    # Add your class methods and properties here

    def file_type_string(self):

        file_type_value = self.file_type
        contracts_folder = aq_parent(self)
        contracts_folder_types = contracts_folder.types

        for i in contracts_folder_types:
            if i['value'] == file_type_value:
                return i['name']
        return None

    def file_procedure_string(self):

        file_procedure_value = self.file_procedure
        contracts_folder = aq_parent(self)
        contracts_folder_procedures = contracts_folder.procedures

        for i in contracts_folder_procedures:
            if i['value'] == file_procedure_value:
                return i['name']
        return None

    def file_processing_string(self):

        file_processing_value = self.file_processing
        contracts_folder = aq_parent(self)
        contracts_folder_processings = contracts_folder.processings

        for i in contracts_folder_processings:
            if i['value'] == file_processing_value:
                return i['name']
        return None

    def file_state_string(self):

        file_state_value = self.file_state
        contracts_folder = aq_parent(self)
        contracts_folder_states = contracts_folder.states

        for i in contracts_folder_states:
            if i['value'] == file_state_value:
                return i['name']
        return None

    def files(self):
        return self.getFolderContents({'portal_type': 'File'}, full_objects=1)

    def contract_state_index(self):
        return self.file_state

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
