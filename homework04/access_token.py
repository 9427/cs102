import webbrowser
import argparse

#access_token=f70d16eb903423b39265b537cefbb202cd4d08b9194cd122b60ac00461586bcc2df31562626aba1ac1682&expires_in=86400&user_id=65000344


def get_access_token(client_id, scope):
    assert isinstance(client_id, int), 'clinet_id must be positive integer'
    assert isinstance(scope, str), 'scope must be string'
    assert client_id > 0, 'clinet_id must be positive integer'
    url = """\
    https://oauth.vk.com/authorize?client_id={client_id}&\
    redirect_uri=https://oauth.vk.com/blank.hmtl&\
    scope={scope}&\
    &response_type=token&\
    display=page\
    """.replace(" ", "").format(client_id=client_id, scope=scope)
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="Application Id", type=int)
    parser.add_argument("-s",
                        dest="scope",
                        help="Permissions bit mask",
                        type=str,
                        default="",
                        required=False)
    args = parser.parse_args()
    get_access_token(args.client_id, args.scope)
