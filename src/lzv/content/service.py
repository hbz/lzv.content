# -*- coding: utf-8 -*-
from lzv.content import _
from plone.supermodel.directives import fieldset
from plone.app.textfield import RichText
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five import BrowserView
from lzv.content.config import SERVICESTATUS

items = [SimpleTerm(value=key, title=value) for (key, value) in SERVICESTATUS]
choice_servicesstatus = SimpleVocabulary(items)


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
        fields=['basefunctions']
    )

    basefunctions = schema.List(
        title=_(u"Basisfunktionen"),
        description=_("Grundlegende Funktionen des Services."),
        value_type=schema.Choice(
            [
            "Quellsystemanbindung",
            "Automatisierte Workflows",
            "Vorkonfigurierte Materialflows",
            "Individuelles Preservation Planning",
            "Reporting"
            ]
        )
    )
    # Nutzungsvoraussetzungen

    fieldset('terms',
        label=u'Nutzungsvoraussetzungen',
        fields=['staff']
    )

    staff = schema.List(
        title=_(u"Personal"),
        description=_("Notwendiges Personal, eine Stellenbeschreibung pro Zeile."),
        value_type=schema.TextLine(required=True)
    )
    # Portlet

    fieldset('portlet',
        label=u'Portlet',
        fields=['specs', 'process', 'workflow', 'lop']
    )

    specs = schema.URI(
        title=_(u"Technische Spezifikation")        
    )

    process = schema.URI(
        title=_(u"Prozessbeschreibung")        
    )

    workflow = schema.URI(
        title=_(u"Workflow")
    )

    lop = schema.URI(
        title=_(u"Levels of Preservation")        
    )


@indexer(IService)
def serviceDetailsIndexer(obj):
    return obj.details.raw


class ServiceView(BrowserView):
    """A lzv service"""

    def get_servicestatus_names(self):
        return  {k:v for k,v in SERVICESTATUS}



