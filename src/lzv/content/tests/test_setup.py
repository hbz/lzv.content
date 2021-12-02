# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from lzv.content.testing import LZV_CONTENT_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that lzv.content is properly installed."""

    layer = LZV_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lzv.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'lzv.content'))

    def test_browserlayer(self):
        """Test that ILzvContentLayer is registered."""
        from lzv.content.interfaces import (
            ILzvContentLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ILzvContentLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LZV_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['lzv.content'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if lzv.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'lzv.content'))

    def test_browserlayer_removed(self):
        """Test that ILzvContentLayer is removed."""
        from lzv.content.interfaces import \
            ILzvContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ILzvContentLayer,
            utils.registered_layers())
