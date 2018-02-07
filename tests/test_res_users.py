# -*- coding: utf-8 -*-

from odoo.tests import common
from odoo.exceptions import ValidationError

class BaseBlocked(common.SavepointCase):

    def test_01_get_user_warehouse_no_user(self):
        User = self.env['res.users']

        test_user = User.create({'name': 'test_user',
                                 'login': '12345678910',
                                 'active': False})

        with self.assertRaises(ValidationError) as e:
            User.sudo(test_user).get_user_warehouse()

        self.assertEqual(e.exception.name, 'Cannot find user to get warehouse.')
