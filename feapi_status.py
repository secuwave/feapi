import requests


def analysis_status(analysis_id, token):
    headers = {'X-FeApi-Token': token}
    url = 'https://192.168.5.240:443/wsapis/v2.0.0/submissions/status/{}'.format(analysis_id)
    res = requests.get(url, headers=headers, verify=False)
    if res.status_code == 200:
        status = res.json().get('submissionStatus')
        message = 'analysis status: id #{}: status: {}.'.format(analysis_id, status)
        return res.status_code, message
    elif res.status_code == 401:
        message = 'analysis status: id #{}: token error: {}, (resp code={})'.format(analysis_id, res.text, res.status_code)
        return res.status_code, message
    elif res.status_code == 404:  # id 오류는 retry에서도 계속 실패일 것이므로 fail로 옮긴다.
        message = 'analysis status: id #{}: incorrect id. (resp code={})'.format(analysis_id, res.status_code)
        return res.status_code, message
    else:  # 502: timeout
        message = 'analysis status: id #{}: error: {}, (resp code={})'.format(analysis_id, res.text, res.status_code)
        return res.status_code, message