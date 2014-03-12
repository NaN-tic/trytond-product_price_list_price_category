# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__all__ = ['PriceListCategory', 'Template', 'PriceList', 'PriceListLine']
__metaclass__ = PoolMeta

from trytond.modules.product.product import STATES, DEPENDS


class PriceListCategory(ModelSQL, ModelView):
    '''Price List Category'''
    __name__ = 'product.price_list.category'
    _order = [('name', 'ASC')]
    name = fields.Char('Name', translate=True, required=True)


class Template:
    __name__ = 'product.template'

    price_list_category = fields.Many2One('product.price_list.category',
        'Price List Category', states=STATES, depends=DEPENDS)


class PriceList:
    __name__ = 'product.price_list'

    def compute(self, party, product, unit_price, quantity, uom,
            pattern=None):
        """
        Add the product's price list category in pattern.
        """
        if pattern is None:
            pattern = {}

        pattern = pattern.copy()
        if product:
            pattern['price_list_category'] = (product.price_list_category and
                product.price_list_category.id or None)
        return super(PriceList, self).compute(party, product, unit_price,
            quantity, uom, pattern)


class PriceListLine:
    __name__ = 'product.price_list.line'

    price_list_category = fields.Many2One('product.price_list.category',
        'Price List Category')
