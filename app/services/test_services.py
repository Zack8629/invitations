from app.services import generate_qr


def test_short_link():
    from app.services import crypto, link_shortener_local

    events_id = 0
    for event in range(1):
        events_id += 1
        users_id = 0
        for user in range(40):
            users_id += 1
            print(f'{events_id=}')
            print(f'{users_id=}')

            crypt_event_id = crypto.encrypt_data(events_id)
            crypt_user_id = crypto.encrypt_data(users_id)

            decrypt_event_id = crypto.decrypt_data(crypt_event_id)
            decrypt_user_id = crypto.decrypt_data(crypt_user_id)
            print(f'{decrypt_event_id=}')
            print(f'{decrypt_user_id=}')

            orig_url = link_shortener_local.get_orig_url(crypt_event_id, crypt_user_id)
            print(f'{event + 1}_{user + 1} => {orig_url}')

            short_url = link_shortener_local.generate_short_url(orig_url)
            print(f'SHORT {event + 1}_{user + 1} => {short_url}')
            print()


my_short_link = 'http://127.0.0.1:5000/asd'

if __name__ == '__main__':
    generate_qr.gen_text(my_short_link)
