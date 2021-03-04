import requests
import os

ANALYSIS_OPTIONS = '{"application": "0", "timeout": "240", "priority": "0", "profiles": ["win7-sp1m"], "analysistype": "1", "force": "true", "prefetch": "1"}'


sample = os.path.join(os.path.dirname(__file__), 'LineUpdater.exe')
# host = '192.168.5.240'
# port = 443
# api_version = 'v2.0.0'
api_account = 'xxxx'
api_password = 'xxxx'
file_name = 'sss.exe'


url_login = 'https://192.168.5.240:443/wsapis/v2.0.0/auth/login'
# url_login = 'https://{}:{}/wsapis/{}/auth/login'.format(host, port, api_version)

url_submit = 'https://192.168.5.240:443/wsapis/v2.0.0/submissions/file'
# url_submit = 'https://{}:{}/wsapis/{}/submissions/file'.format(host, port, api_version)

res = requests.post(url_login, auth=(api_account, api_password), verify=False)  # http post, tuple, ssl verify false
if res.status_code == 200:
    token = res.headers.get('X-FeApi-Token')
    # print('FireEye 로그인에 성공했습니다: device: {}, token: {}'.format(host, token))
else:
    # print('FireEye 로그인에 실패했습니다: device: {}, account: {}, response code: {}, error: {}'.format(host, api_account, res.status_code, res.text))
    token = None

data = {'filename': file_name, 'options': ANALYSIS_OPTIONS}
headers = {'X-FeApi-Token': token}

with open(sample, 'rb') as file_payload:
    files = {'file': file_payload}
    res = requests.post(url_submit, data=data, files=files, headers=headers, verify=False)

if res.status_code == 200:
    d_res = res.json()  # 리턴된 json 데이터를 dict로 변환
    analysis_id = d_res[0].get('ID')
    message = 'analysis submit done. file: {}, analysis id #{}'.format(sample, analysis_id)
    print(message)
    if analysis_id:
        message, success = analysis_status(analysis_id, token)
        print('analysis id: {}, status check: {}, status message: {}'.format(analysis_id, success, message))
elif res.status_code == 401:
    message = 'analysis submit failed. file: {}, invalid token. (resp code={}) Stop & try next time'.format(sample, res.status_code)
    print(message)
else:
    message = 'analysis submit failed. file: {}, message: {} (resp code={})'.format(sample, res.text, res.status_code)
    print(message)





"""
# API URLs
BASE: 'https://{ip}:{port}/wsapis/{api_version}'
LOGIN:           + '/auth/login'
SUBMIT_URL:      + '/submissions/url'
SUBMIT_FILE:     + '/submissions/file'
ANALYSIS_STATUS: + '/submissions/status/{analysis_id}'
LOGOUT:          + '/auth/logout'


# file submit header 구성 주의사항
  1. 아래와 같은 헤더를 넣으면 안된다.
    {'Content-Type': 'application/json'}
    {'Content-Type': 'multipart/form-data'}
  2. 옵션은 형태는 json이지만, load하지 않고 문자열로 전달한다.
   숫자를 문자열로 처리하든 아니든 상관없다. 아래 두 개가 같다.
    '{"application": "0", "timeout": "240", "priority": "0", "profiles": ["win7-sp1m"], "analysistype": "1", "force": "true", "prefetch": "1"}'
    '{"application": 0, "timeout": 240, "priority": 0, "profiles": ["win7-sp1m"], "analysistype": 1, "force": "true", "prefetch": 1}'
"""