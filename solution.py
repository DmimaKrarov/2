from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": """https://market.yandex.ru/product--figura-slon-bronza-17kh9kh19sm-3928142/1755785740?cpc=H0DoTS7hx
            SZcuvnTxQMcsUK4BDljM1v1bFK17biqo_jKNQ5Su9qBdmp09lCBXBcD8lSbU_my8WYBFaqBBaqP1AZswWtyI5tbLqrpQx3RBox0goDMz3Br
            947bWzuaBZ6Ufoelp7TXwbA_4Xzv_mqf4YBOSIfLOeT2FYwOi7HI6E7tj6Q1j1xqLUnV6MlmoTlXQO7ldLlcHRZGTev1fxC6uUWVunp4iJh
            RU-CXUhK5boaiqV-PkiMfgQ%2C%2C&sku=101764079677&offerid=7VQzefDe-xc4Bu0FHtpY1Q&cpa=1""",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
