# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from .common import BaseWarehouseConfig

class TestGetUserWarehouse(BaseWarehouseConfig):

    def test01_get_user_warehouse_no_user(self):
        """Checking that when a user no user is found
           the correct error is raised
        """
        # Make it so user isn't found in search
        self.test_user.active = False
        with self.assertRaises(ValidationError) as e:
             self.do_as_user(self.test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Cannot find user to get warehouse.')

    def test02_get_user_warehouse_no_warehouse(self):
        """Checking that when a user has no warehouse 
           the correct error is raised
        """
        # Make it so warehouse isn't found in search
        self.test_company_warehouse.active = False

        with self.assertRaises(ValidationError) as e:
             self.do_as_user(self.test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Cannot find a warehouse for user')

    def test03_get_user_warehouse_multiple_warehouses(self):
        """Checking that when a user has mutiple warehouses 
           the correct error is raised
        """
        Settings = self.env['res.config.settings']
        test_settings = Settings.create({'group_stock_multi_warehouses': True,
                                         'group_stock_multi_locations': True})
        test_settings.execute()

        # Create new warehouse by copying current one and changing
        # the required feilds
        warehouse2 = self.test_company_warehouse.copy({'name': '123',
                                      'code': '123'})

        with self.assertRaises(ValidationError) as e:
            self.do_as_user(self.test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Found multiple warehouses for user')

    def test04_get_user_warehouse_success(self):
        """Checks that the correct warehouse is returned
        """
        # Create new company so there is more than one warehouse
        returned_warehouse = self.do_as_user(self.test_user).get_user_warehouse()
        self.assertEqual(returned_warehouse.id, self.test_company_warehouse.id)
