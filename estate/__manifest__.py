{
    'name': 'Real Estate',
    'version': '0.1',
    'category': 'Tutorials',
    'depends': ['base'],
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/base_users_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application':True,
    'license':'LGPL-3',
    'author':'David Parlapiano',
}