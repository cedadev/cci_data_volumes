# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '26 Mar 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


from elasticsearch import Elasticsearch

es = Elasticsearch(['https://jasmin-es1.ceda.ac.uk'])

UNITS = ('B','KB','MB','GB','TB','PB','EB')


def get_units(size_in_bytes):
    """
    Convert and get Units describing conversion
    :param size_in_bytes:
    :return: Converted value, unit string
    """

    # Magnitude
    magnitude = len(str(int(size_in_bytes)))//3

    if magnitude:
        # Convert bytes
        value = size_in_bytes/(1000**magnitude)
    else:
        value = size_in_bytes

    return value, UNITS[magnitude]


def get_dir_query(path):
    return {
        'sort': {
            'dir.keyword': {
                'order': 'asc'
            }
        },
        'query': {
            'bool': {
                'must': [{
                    'prefix': {
                        'path.keyword': path + '/'
                    }
                }],
                'filter': {
                    'term': {
                        'depth': len(path.split('/'))
                    }
                }
            }
        },
        'size': 1000
    }


def get_file_query(path):
    return {
        'query': {
            'match_phrase_prefix': {
                'info.directory.analyzed': path
            }
        },
        'aggs': {
            'data_volume': {
                'sum': {
                    'field': 'info.size'
                }
            }
        },
        'size': 0
    }


directories = es.search(index='ceda-dirs', body=get_dir_query('/neodc/esacci'))

for hit in directories['hits']['hits']:
    path = hit['_source']['path']
    results = es.search(index='ceda-fbi', body=get_file_query(path))
    volume = results['aggregations']['data_volume']['value']

    converted_vol, units = get_units(volume)

    print(f'{path} {converted_vol:.2f} {units}\n')

