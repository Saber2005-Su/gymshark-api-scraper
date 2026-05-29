import requests
import csv

url = "https://2deaes0cuo-dsn.algolia.net/1/indexes/*/recommendations"

params = {
    "x-algolia-api-key": "932fd4562e8443c09e3d14fd4ab94295",
    "x-algolia-application-id": "2DEAES0CUO"
}

headers = {
    "content-type": "application/json",
    "origin": "https://www.gymshark.com",
    "referer": "https://www.gymshark.com/",
    "user-agent": "Mozilla/5.0"
}

payload = {
    "requests": [
        {
            "indexName": "production_us_products_v2_recs_testing",
            "maxRecommendations": 10,

            "queryParameters": {
                "filters": '(inStock:"true") AND tier:3'
            },

            "threshold": 0,
            "facetName": "division",
            "facetValue": "accessories",
            "model": "trending-items"
        }
    ]
}

try:

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    products = data["results"][0]["hits"]

    with open("products.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "title",
            "price",
            "handle",
            "image"
        ])

        for product in products:

            title = product.get("title")

            handle = product.get("handle")

            sizes = product.get("availableSizes", [])

            if sizes:
                price = sizes[0].get("price")
            else:
                price = None

            image = None

            colors = product.get("availableColours", [])

            if colors:
                image = colors[0]["featuredImage"]["src"]

            writer.writerow([
                title,
                price,
                handle,
                image
            ])

            print("-" * 50)
            print("Title:", title)
            print("Price:", price)
            print("Handle:", handle)
            print("Image:", image)

    print("\nCSV file saved successfully.")

except requests.exceptions.RequestException as e:
    print("Request Error:", e)

except KeyError as e:
    print("JSON Key Error:", e)

except Exception as e:
    print("Unexpected Error:", e)