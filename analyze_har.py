import json
from urllib.parse import parse_qs

with open('www.threads.com.har - posting.har', 'r', encoding='utf-8') as f:
    har = json.load(f)

entries = har['log']['entries']

# Print ALL POST requests to any threads URL with their full body
for i, entry in enumerate(entries):
    req = entry['request']
    if req['method'] != 'POST':
        continue

    url = req['url']
    body = ''
    if req.get('postData'):
        body = req['postData'].get('text', '')

    resp_status = entry['response']['status']
    resp_body = entry.get('response', {}).get('content', {}).get('text', '')

    print(f'[{i}] POST {url[:60]}')
    print(f'     Status: {resp_status}')
    if 'doc_id' in body:
        params = parse_qs(body)
        print(f'     doc_id: {params.get("doc_id", ["?"])[0]}')
        print(f'     variables: {params.get("variables", ["{}"])[0][:200]}')
    else:
        print(f'     body: {body[:200]}')
    print(f'     resp: {resp_body[:150]}')
    print()
