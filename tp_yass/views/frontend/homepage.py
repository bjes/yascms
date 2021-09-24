import copy
import json
import logging
from pyramid.view import view_config

from tp_yass.enum import NavbarType, HomepageItemType, HomepageItemParamsSubType
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_config(route_name='homepage', renderer='')
def homepage_view(request):
    request.override_renderer = f'themes/{request.current_theme_name}/frontend/homepage.jinja2'

    homepage_items = []
    for each_item in DAL.get_theme_config(request.current_theme_name)['settings']['homepage_items_order']['value']:
        new_item = copy.deepcopy(each_item)
        if new_item['type'] == HomepageItemType.NEWS:
            if new_item['params']['sub_type'] == HomepageItemParamsSubType.UNSPECIFIED:
                new_item['entities'] = DAL.get_news_list(quantity_per_page=new_item['params']['quantity'])
            else:
                new_item['entities'] = DAL.get_news_list(quantity_per_page=new_item['params']['quantity'],
                                                         category_id=new_item['params']['sub_type'])
        elif new_item['type'] == HomepageItemType.PAGE:
            new_item['entities'] = DAL.get_page(new_item['params']['id'])
        elif new_item['type'] == HomepageItemType.TELEXT:
            new_item['entities'] = DAL.get_pinned_telext_list()
        elif new_item['type'] == HomepageItemType.LINKS:
            if new_item['params']['sub_type'] == HomepageItemParamsSubType.UNSPECIFIED:
                new_item['entities'] = DAL.get_pinned_link_list()
            else:
                new_item['entities'] = DAL.get_link_list(quantity_per_page=new_item['params']['quantity'],
                                                         category_id=new_item['params']['sub_type'])
        else:
            logger.critical('homepage_items_order 設定出現不合法的資料： %s', new_item)
            continue
        homepage_items.append(new_item)
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'homepage_items': homepage_items,
            'NavbarType': NavbarType,
            'HomepageItemType': HomepageItemType,
            'HomepageItemParamsSubType': HomepageItemParamsSubType}
