# -*- coding: utf-8 -*-


default_data = {
    'imp_date_start': '',
    'imp_target': '0',
    'imp_target_note': '',
    'account_type': '1',
    'imp_mode': ['api', 'web'],
    'multi_apply': '0',
    'required_key': 'id,cell,name,商户',
    'pgbg_product': {
        'test': {
            'api_count': 50,
            'web_count': 1000,
            'email_pic': '',
        },
        'product_selected': {
            0: {'name': '', 'code': '', 'price': 0},
        }
    },
    'HNApi_selected': {
        0: {'name': '', 'code': '', 'test_nums': 50, 'note': ''}
    },
    'cus_config': {
        'cus_pf': '',
        'cus_data': '',
        'rule_blk_sheet': '',
        'rule_multi_apply': '',
    },
    'radar_permission': '',
}

key = 'imp_target'

if key in default_data.keys():
