# -*- coding: utf-8 -*-

from odoo.tests import common
from odoo.exceptions import ValidationError

class BaseBlocked(common.SavepointCase):

    def test_01_get_user_warehouse_no_user(self):
        """Checking that when a user no user is found
           the correct error is raised
        """
        User = self.env['res.users']
        # Creating user without company so takes company from current user
        test_user = User.create({'name': 'test_user',
                                 'login': '12345678910',
                                 'active': False})

        with self.assertRaises(ValidationError) as e:
            User.sudo(test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Cannot find user to get warehouse.')

    def test_02_get_user_warehouse_no_warehouse(self):
        """Checking that when a user has no warehouse 
           the correct error is raised
        """
        User = self.env['res.users']
        Warehouse = self.env['stock.warehouse']

        # Creating user without company so takes company from current user
        test_user = User.create({'name': 'test_user',
                                 'login': '12345678910'})
        
        # Find and deactivate warehouse so there is no warehouse to find
        warehouse = Warehouse.search([('company_id', '=', test_user.company_id.id)])
        warehouse.active = False

        with self.assertRaises(ValidationError) as e:
            User.sudo(test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Cannot find a warehouse for user')

    def test_03_get_user_warehouse_multiple_warehouses(self):
        """Checking that when a user has mutiple warehouses 
           the correct error is raised
        """
        Settings = self.env['res.config.settings']
        Warehouse = self.env['stock.warehouse']
        User = self.env['res.users']

        
        test_settings = Settings.create({'group_stock_multi_warehouses': True,
                                         'group_stock_multi_locations': True})
        test_settings.execute()


        # Creating user without company so takes company from current user
        test_user = User.create({'name': 'test_user',
                                 'login': '12345678910'})
        
        # Find and deactivate warehouse so there is no warehouse to find
        warehouse1 = Warehouse.search([('company_id', '=', test_user.company_id.id)])
        warehouse2 = warehouse1.copy({'name': '123',
                                      'code': '123'})

        with self.assertRaises(ValidationError) as e:
            User.sudo(test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Found multiple warehouses for user')

    def test_04_get_user_warehouse_success(self):
        """Checks to see that the returned warehouse is correct
           
           N.B. This would be better if there was more than one 
                warehouse but couldn't create a new user in 
                new company, revisit later.
        """
        User = self.env['res.users']
        Warehouse = self.env['stock.warehouse']

        # Creating user without company so takes company from current user
        test_user = User.create({'name': 'test_user',
                                 'login': '12345678910'})

        returned_warehouse = User.sudo(test_user).get_user_warehouse()
        user_warehouse = Warehouse.search([('company_id', '=', test_user.company_id.id)])

        self.assertEqual(returned_warehouse.id, user_warehouse.id)
