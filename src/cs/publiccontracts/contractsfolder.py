# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from cs.publiccontracts import _
from plone.autoform.directives import widget
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobFile
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IContractTypesRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract type value"))
    name = schema.TextLine(title=_(u"Contract type name"))


class IContractStatesRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract state value"))
    name = schema.TextLine(title=_(u"Contract state name"))


class IContractProceduresRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract procedure value"))
    name = schema.TextLine(title=_(u"Contract procedure name"))


class IContractProcessingsRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract processing value"))
    name = schema.TextLine(title=_(u"Contract processing name"))


class IContractOrganizationsRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract organization value"))
    name = schema.TextLine(title=_(u"Contract organization name"))


class IContractBodiesRowSchema(Interface):

    value = schema.TextLine(title=_(u"Contract body value"))
    name = schema.TextLine(title=_(u"Contract body name"))


# Interface class; used to define content-type schema.
class IContractsFolder(Interface):
    """
    Contracts Folder
    """

    widget(types=DataGridFieldFactory)
    types = schema.List(
        title=_(u"Contract Types"),
        description=_(u"Enter here the contract types"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract Types"), schema=IContractTypesRowSchema, required=False
        ),
    )

    widget(states=DataGridFieldFactory)
    states = schema.List(
        title=_(u"Contract States"),
        description=_(u"Enter here the contract states"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract States"), schema=IContractStatesRowSchema, required=False
        ),
    )

    widget(procedures=DataGridFieldFactory)
    procedures = schema.List(
        title=_(u"Contract Procedures"),
        description=_(u"Enter here the contract Procedures"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract Procedures"),
            schema=IContractProceduresRowSchema,
            required=False,
        ),
    )

    widget(processings=DataGridFieldFactory)
    processings = schema.List(
        title=_(u"Contract Processings"),
        description=_(u"Enter here the contract Processings"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract Processings"),
            schema=IContractProcessingsRowSchema,
            required=False,
        ),
    )

    widget(organizations=DataGridFieldFactory)
    organizations = schema.List(
        title=_(u"Contract organizations"),
        description=_(u"Enter here the contract organizations"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract organizations"),
            schema=IContractOrganizationsRowSchema,
            required=False,
        ),
    )

    widget(bodies=DataGridFieldFactory)
    bodies = schema.List(
        title=_(u"Contract bodies"),
        description=_(u"Enter here the contract bodies"),
        required=False,
        value_type=DictRow(
            title=_(u"Contract bodys"), schema=IContractBodiesRowSchema, required=False
        ),
    )

    generic_file = NamedBlobFile(
        title=_(u"Generic File"),
        required=False,
    )


@implementer(IContractsFolder)
class ContractsFolder(Container):
    pass
