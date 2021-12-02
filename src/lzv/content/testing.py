# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import lzv.content


class LzvContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=lzv.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'lzv.content:default')


LZV_CONTENT_FIXTURE = LzvContentLayer()


LZV_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LZV_CONTENT_FIXTURE,),
    name='LzvContentLayer:IntegrationTesting',
)


LZV_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LZV_CONTENT_FIXTURE,),
    name='LzvContentLayer:FunctionalTesting',
)


LZV_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LZV_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='LzvContentLayer:AcceptanceTesting',
)
