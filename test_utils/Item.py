class Item:
    attributes = {
        'item': {
            'skuId': '91186',
            'description': 'pytest sample',
            'discountable': True,
            'notForSale': False,
            "taxable": True,
            'uom': 'EACH'
        },
        'itemPrice': {
            'price': {
                'value': .50,
                'currency': 'USD'
            },
            'pricingTierType': 'THRESHOLD',
            'pricingTierMethod': 'TOTAL',
            'tiers': None,
            'uom': 'EACH'
        }
    }

    def set_id(self, id):
        self.attributes['item']['skuId'] = id

    def set_attributes(self, item_dict):
        self.attributes = item_dict
