# -*- coding: utf-8 -*-
from lzv.content import _
from plone.supermodel.directives import fieldset
from plone.app.textfield import RichText
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five import BrowserView
from lzv.content.config import SERVICESTATUS, BASEFUNCTIONS, EXTRAFUNCTIONS, INGESTS, STORAGES

items = [SimpleTerm(value=key, title=value) for (key, value) in SERVICESTATUS]
choice_servicesstatus = SimpleVocabulary(items)

items = [SimpleTerm(value=key, title=value) for (key, value) in BASEFUNCTIONS]
choice_basefunctions = SimpleVocabulary(items)

items = [SimpleTerm(value=key, title=value) for (key, value) in EXTRAFUNCTIONS]
choice_extrafunctions = SimpleVocabulary(items)

items = [SimpleTerm(value=key, title=value) for (key, value) in INGESTS]
choice_ingests = SimpleVocabulary(items)

items = [SimpleTerm(value=key, title=value) for (key, value) in STORAGES]
choice_storages = SimpleVocabulary(items)


class IService(model.Schema):
    """An lzv service"""

    # Servicebeschreibung

    fieldset('description',
        label=u'Servicebeschreibung',
        fields=['serviceid', 'servicename', 'details', 'servicefamily', 'servicestatus']
    )

    serviceid = schema.Int(
        title=_(u"Service ID"),
        description=_("Eindeutige numerische ID des Services.")
    )

    servicename = schema.TextLine(
        title=_(u"Servicebezeichnung"),
        description=_("Kürzel des Services.")
    )

    details = RichText(
        title=_(u"Detailbeschreibung"),
        description=_("Detailierte Beschreibung des Services.")
    )

    servicefamily = schema.TextLine(
        title=_(u"Servicefamilie"),
        description=_("Servicefamilie."),
        required=False
    )

    servicestatus = schema.Choice(
        title=_(u"Servicestatus"),
        description=_(u"Status des Service"),
        vocabulary=choice_servicesstatus
    )

    # Serviceumfang und Optionen

    fieldset('options',
        label=u'Serviceumfang und Optionen',
        fields=['basefunctions', 'extrafunctions', 'ingests', 'serviceoptions', 'storageoptions']
    )

    basefunctions = schema.List(
        title=_(u"Basisfunktionen"),
        description=_("Grundlegende Funktionen des Services."),
        value_type=schema.Choice(vocabulary=choice_basefunctions)
    )

    extrafunctions = schema.List(
        title=_(u"Zusatzfunktionen"),
        description=_("Weitergehende Funktionen des Services."),
        value_type=schema.Choice(vocabulary=choice_extrafunctions),
        required=False
    )

    ingests = schema.List(
        title=_(u"Einlieferung"),
        description=_("Mögliche Methoden zur Einlieferung."),
        value_type=schema.Choice(vocabulary=choice_ingests)
    )

    serviceoptions = RichText(
        title=_(u"Service-Optionen"),
        description=_("Mögliche Optionen des Services.")
    )

    storageoptions = schema.List(
        title=_(u"Speicher-Optionen"),
        description=_("Mögliche Speicheroptionen."),
        value_type=schema.Choice(vocabulary=choice_storages)
    )

    # Nutzungsvoraussetzungen

    fieldset('terms',
        label=u'Nutzungsvoraussetzungen',
        fields=['staff', 'terms']
    )

    staff = schema.List(
        title=_(u"Personal"),
        description=_("Notwendiges Personal, eine Stellenbeschreibung pro Zeile."),
        value_type=schema.TextLine(required=True)
    )

    terms = RichText(
        title=_(u"Nutzungsregelungen"),
        description=_("Nutzungsregelungen")
    )

    # Portlet

    fieldset('portlet',
        label=u'Portlet',
        fields=['specs', 'process', 'workflow', 'lop']
    )

    specs = schema.URI(
        title=_(u"Technische Spezifikation"),
        required=False
    )

    process = schema.URI(
        title=_(u"Prozessbeschreibung"),
        required=False
    )

    workflow = schema.URI(
        title=_(u"Workflow"),
        required=False
    )

    lop = schema.URI(
        title=_(u"Levels of Preservation"),
        required=False
    )


@indexer(IService)
def serviceDetailsIndexer(obj):
    return obj.details.raw


class ServiceView(BrowserView):
    """A lzv service"""

    def get_servicestatus_names(self):
        return  {k:v for k,v in SERVICESTATUS}
    
    def get_basefunctions_names(self):
        return  {k:v for k,v in BASEFUNCTIONS}
    
    def get_extrafunctions_names(self):
        return  {k:v for k,v in EXTRAFUNCTIONS}

    def get_ingests_names(self):
        return  {k:v for k,v in INGESTS}
    
    def get_storages_names(self):
        return  {k:v for k,v in STORAGES}


