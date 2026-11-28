import requests

def main():

    token = "0b19751f2403d86bdc20ceb8716648b91090c0db216bacb9f17c7e4965b8fc82"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.tiny.com.br/public-api/v3/contatos",headers=headers)

    print(response.status_code)
    print(response.text)

if __name__ == '__main__':
    main()