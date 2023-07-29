from bs4 import BeautifulSoup
import requests
import json

ful = "https://stackoverflow.com/questions/tagged/{tag}?tab={filter}&pagesize=15"
filters = [
    "1. Newest",
    "2. Active",
    "3. Bounties",
    "4. Unanswered",
    "5. Frequent",
    "6. Votes",
]

tag = input("enter any question tag (python, java)\n")
print("\n".join(filters))
filter = int(input("enter the filter number (1, 3, 5)\n"))

try:
    filter = filters[filter].split(" ")[-1]
except:
    filter = "Votes"

#генерация url по входным данным
URL = ful.format(tag=tag, filter=filter)

print("generated URL ", URL)
content = requests.get(URL).content

soup = BeautifulSoup(content, "lxml")

def is_question(tag):
    try:
        return tag.get("id").startswith("question-summary-")
    except:
        return False


questions = soup.find_all(is_question)
question_data = []
if questions:
    for question in questions:
        question_dict = {}
        question_dict["votes"] = (
            question.find(class_="s-post-summary--stats-item-number").get_text().strip()
        )
        h3 = question.find(class_="s-post-summary--content-title")
        question_dict["title"] = h3.get_text().strip()
        question_dict["link"] = "https://stackoverflow.com" + h3.find("a").get("href")
        question_dict["date"] = (
            question.find(class_="s-user-card--time").span.get_text().strip()
        )
        question_data.append(question_dict)

    with open(f"questions-{tag}.json", "w") as f:
        json.dump(question_data, f)

    print("file exported")

else:
    print(URL)
    print("looks like there are no questions matching your tag ", tag)