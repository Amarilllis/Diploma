import requests
import ssl
import certifi
import pickle
import json

ya = {
      "Host": "api.content.market.yandex.ru",
      "Accept": "*/*",
      "Authorization": "Cuga2L5umu3IskxHfsN6xqUZMfNuv8"
    };

def get_models(cat):
    url = "https://api.content.market.yandex.ru/v1/category/" + str(cat) + "/models.json?geo_id=213";

    r = requests.get(url, headers = ya)
    data = r.json()

    model_ids = []
    print(type(data))
    print(data)
    try:
        models = data["models"]["items"] #["id"]
    except Exception:
        return []
    for model in models:
        model_ids.append(model["id"])

    print(model_ids)
    return model_ids

def get_reviews(model, grade, page):
    url = "https://api.content.market.yandex.ru/v1/model/" + str(model) + "/opinion.json"

    my_params = {
      "grade": grade,
      "count": 30,
      "page": page
    };

    r = requests.get(url, headers = ya, params = my_params)
    data = r.json()

    reviews = []
    try:
        opinions = data["modelOpinions"]["opinion"]
    except Exception:
        return []
    for opinion in opinions:
        try:
            reviews.append(opinion["text"])
        except Exception:
            continue

    #print(reviews)
    return reviews

def get_all_reviews(model, grade):
    res = []
    page = 1
    revs = get_reviews(model, grade, page)
    res.extend(revs)
    print(len(res))

    while revs != []:
        page += 1
        revs = get_reviews(model, grade, page)
        res.extend(revs)

    return res

positive_reviews = []
neutral_reviews = []
negative_reviews = []
cat_list = [90568]
for cat in cat_list:
    model_ids = get_models(cat)
    print("models:")
    print(len(model_ids))
    for model in model_ids:
        positive_reviews.extend(get_all_reviews(model, 2))

        positive_reviews.extend(get_all_reviews(model, 1))

        neutral_reviews.extend(get_all_reviews(model, 0))
        negative_reviews.extend(get_all_reviews(model, -2))

        negative_reviews.extend(get_all_reviews(model, -1))


print(positive_reviews[0])
print(len(positive_reviews))
pickle.dump(positive_reviews, open("many_pos.pkl", "wb"))
pickle.dump(negative_reviews, open("many_neg.pkl", "wb"))
pickle.dump(neutral_reviews, open("many_neut.pkl", "wb"))