import os
import yaml
import pprint
import json


config_file = os.path.join(os.path.normpath(os.path.dirname(__file__)), 'system.yml')
try:
    print('loading config from {}'.format(config_file))
    d = yaml.load(open(config_file, encoding='utf-8'), Loader=yaml.FullLoader)
    # pprint.pprint(d)
    # print(json.dumps(d, indent=4))
    # return d
except Exception as e:
    print('설정(file: {})에 오류가 있습니다: {}'.format(config_file, e))