# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .product import *

def register():
    Pool.register(
        PriceListCategory,
        Template,
        PriceList,
        PriceListLine,
        module='product_price_list_price_category', type_='model')
