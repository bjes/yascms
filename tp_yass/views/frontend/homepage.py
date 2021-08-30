import json
import logging
from pyramid.view import view_config

from tp_yass.enum import NavbarType, HomepageOrderType, HomepageOrderParamsSubType
from tp_yass.helpers.navbar import generate_navbar_trees
from tp_yass.dal import DAL


logger = logging.getLogger(__name__)


@view_config(route_name='homepage', renderer='')
def homepage_view(request):
    request.override_renderer = f'themes/{request.current_theme_name}/frontend/homepage.jinja2'

    homepage_content_list = []
    for each_item in DAL.get_homepage_order():
        params = json.loads(each_item.params)
        new_item = dict(name=each_item.name, type=each_item.type, params=params, description=each_item.description)
        if each_item.type == HomepageOrderType.NEWS:
            if params['sub_type'] == HomepageOrderParamsSubType.UNSPECIFIED:
                new_item['entities'] = DAL.get_news_list(quantity_per_page=params['quantity'])
            else:
                new_item['entities'] = DAL.get_news_list(quantity_per_page=params['quantity'],
                                                         category_id=params['sub_type'])
        elif each_item.type == HomepageOrderType.PAGE:
            new_item['entities'] = DAL.get_page(params['id'])
        elif each_item.type == HomepageOrderType.TELEXT:
            new_item['entities'] = DAL.get_pinned_telext_list()
        elif each_item.type == HomepageOrderType.LINKS:
            if params['sub_type'] == HomepageOrderParamsSubType.UNSPECIFIED:
                new_item['entities'] = DAL.get_link_list(quantity_per_page=params['quantity'])
            else:
                new_item['entities'] = DAL.get_link_list(quantity_per_page=params['quantity'],
                                                         category_id=params['sub_type'])
        else:
            logger.critical('homepage_order 資料表出現不合法的資料： %s', each_item)
            continue
        homepage_content_list.append(new_item)
    return {'navbar_trees': generate_navbar_trees(request, visible_only=True),
            'homepage_content_list': homepage_content_list,
            'NavbarType': NavbarType,
            'HomepageOrderType': HomepageOrderType,
            'HomepageOrderParamsSubType': HomepageOrderParamsSubType}
