
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool
from trytond.modules.company.tests import (
    CompanyTestMixin, create_company, set_company)
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class ProductPriceListPriceCategoryTestCase(CompanyTestMixin, ModuleTestCase):
    'Test ProductPriceListPriceCategory module'
    module = 'product_price_list_price_category'

    @with_transaction()
    def test_price_list(self):
        'Test price_list'
        pool = Pool()
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Uom = pool.get('product.uom')
        PriceList = pool.get('product.price_list')
        PriceListCategory = pool.get('product.price_list.category')

        company = create_company()
        with set_company(company):
            unit, = Uom.search([
                    ('name', '=', 'Unit'),
                    ])

            price_list_category = PriceListCategory()
            price_list_category.name = 'Price List Category'
            price_list_category.save()

            template = Template(
                name='Template1',
                list_price=Decimal(10),
                default_uom=unit,
                price_list_category=price_list_category,
                )
            template.save()
            product = Product(template=template)
            product.save()
            variant = Product(template=template)
            variant.save()

            template2 = Template(
                name='Template2',
                list_price=Decimal(20),
                default_uom=unit,
                )
            template2.save()
            product2 = Product(template=template2)
            product2.save()

            price_list, = PriceList.create([{
                        'name': 'Default Price List',
                        'price': 'list_price',
                        'lines': [('create', [{
                                        'quantity': 10.0,
                                        'product': variant.id,
                                        'formula': 'unit_price * 0.8',
                                        'price_list_category': price_list_category.id,
                                        }, {
                                        'quantity': 10.0,
                                        'formula': 'unit_price * 0.9',
                                        }, {
                                        'product': variant.id,
                                        'formula': 'unit_price * 1.1',
                                        }, {
                                        'formula': 'unit_price',
                                        }])],
                        }])
            tests = [
                (product, 1.0, Decimal(10.0)),
                (product, 1000.0, Decimal(9.0)),
                (variant, 1.0, Decimal(11.0)),
                (product2, 1.0, Decimal(20.0)),
                (product2, 1000.0, Decimal(18.0)),
                ]
            for product, quantity, result in tests:
                self.assertEqual(
                    price_list.compute(product, quantity, uom=unit), result)

del ModuleTestCase
