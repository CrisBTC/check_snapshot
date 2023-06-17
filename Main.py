import requests
import datetime
import time

url = "https://hub.snapshot.org/graphql"
headers = {"Content-Type": "application/json"}

# Чтение адресов из файла "wallet.txt"
with open("wallet.txt", "r") as file:
    voters = file.read().splitlines()

results = []
bad_addresses = []

for voter in voters:
    payload = {
        "operationName": "Votes",
        "variables": {
            "first": 20,
            "skip": 0,
            "voter": voter,
            "orderBy": "created",
            "orderDirection": "desc"
        },
        "query": "query Votes($voter: String!, $first: Int, $skip: Int, $orderBy: String, $orderDirection: OrderDirection) {\n votes(\n first: $first\n skip: $skip\n where: {voter: $voter}\n orderBy: $orderBy\n orderDirection: $orderDirection\n ) {\n id\n created\n choice\n proposal {\n id\n title\n choices\n type\n }\n space {\n id\n avatar\n }\n }\n}"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    votes = data["data"]["votes"]
    if len(votes) > 0:
        last_vote = votes[0]  # Берем первый голос, так как данные уже отсортированы по убыванию даты
        created_date = datetime.datetime.fromtimestamp(last_vote["created"]).strftime('%Y-%m-%d %H:%M:%S')
        choice_text = "YES" if last_vote["choice"] == 1 else "NO"
        title = last_vote["proposal"]["title"]

        result = f"Address: {voter} | Date: {created_date} | Choice: {choice_text} | Title: {title}"
        results.append(result)
        print(result)
    else:
        bad_addresses.append(voter)
        print("Bad:", voter)

    # Задержка в 2 секунды между запросами
    time.sleep(1)

# Запись результатов в файл "result.txt"
with open("result.txt", "w") as file:
    file.write("\n".join(results))

# Запись адресов без голосов в файл "BAD.txt"
with open("BAD.txt", "w") as file:
    file.write("\n".join(bad_addresses))

