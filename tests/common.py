from odoo.tests import common

class BaseWarehouseConfig(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(BaseWarehouseConfig, cls).setUpClass()
        Warehouse = cls.env['stock.warehouse']

        # Create new company so there is more than one warehouse
        cls.test_company = cls.create_company('test_company')
        cls.test_warehouse = Warehouse.search([('company_id', '=', cls.test_company.id)])
        cls.test_user = cls.create_user('test_user',
                                        'test_user_login',
                                        company_id=cls.test_company.id,
                                        company_ids=[(6, 0, cls.test_company.ids)])

    @classmethod
    def create_user(cls, name, login, **kwargs):
        """ Create and return a user"""
        User = cls.env['res.users']
        # Creating user without company 
        # takes company from current user
        vals = {
            'name': name,
            'login': login,
        }
        vals.update(kwargs)
        return User.create(vals)
    
    @classmethod
    def create_company(cls, name, **kwargs):
        """Create and return a company"""
        Company = cls.env['res.company']
        vals = {
            'name': name
        }
        vals.update(kwargs)
        return Company.create(vals)

    @classmethod
    def do_as_user(cls, user):
        """Returns User under the context of
           the supplied user
        """
        User = cls.env['res.users']
        return User.sudo(user)
