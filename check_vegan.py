import requests

def check_vegan(food_items):
    print("foods not categorized yet, "
          "program is checking what is vegan")

    url = "https://doublecheckvegan.com/wp-admin/admin-ajax.php"

    try:

        with open("lists.txt", "r") as f:
            content = f.read().replace("'", "")
            vegan_l = content.split("\n")[0].split("=")[1].strip().strip("[]").split(", ")
            non_vegan_l = content.split("\n")[1].split("=")[1].strip().strip("[]").split(", ")

    except Exception as e:
        print(e)
        vegan_l = []
        non_vegan_l = []
        pass

    for item in food_items:
        if item in vegan_l or item in non_vegan_l:
            continue

        payload = {
            "action": "search_ingredients",
            "data": f"{item}"
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            if "0 flagged" in response.text:
                print(f"{item} is vegan")
                vegan_l.append(item)
            else:
                print(f"{item} is not vegan")
                non_vegan_l.append(item)
        else:
            print(f"Request for {item} failed with status code: {response.status_code}")

    with open("lists.txt", "w") as f:
        f.write(f"cert_vegan_l = {vegan_l}\n")
        f.write(f"non_vegan_l = {non_vegan_l}\n")

