import copy
import datetime
from tastypie.resources import ModelResource
from tastypie.constants import ALL
from main.models import AddrObj, House


class AddrResource(ModelResource):
    class Meta:
        queryset = AddrObj.objects.filter(livestatus=True, enddate__gte=datetime.date.today())
        allowed_methods = ['get', ]
        filtering = {
            u'formalname': ALL,
            u'aolevel': [u'exact', u'in'],
            u'parentguid': [u'exact'],
            u'aoguid': [u'exact'],
            u'centstatus': [u'exact'],
            u'postalcode': [u'exact'],
        }
        resource_name = u'addresses'

    def dehydrate(self, bundle):
        addrs = AddrObj.objects.filter(parentguid=bundle.data['aoguid'], aolevel__in=[3, 4, 5, 6])
        bundle.data['places_count'] = addrs.count()
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del data_dict['meta']
                data_dict['addresses'] = copy.copy(data_dict['objects'])
                del data_dict['objects']

        return data_dict


class HouseResource(ModelResource):
    class Meta:
        queryset = House.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            u'formalname': ALL,
            u'aolevel': [u'exact'],
            u'aoguid': [u'exact'],
            u'postalcode': [u'exact'],
        }
        resource_name = u'houses'

