import requests
import json
# Request ee catalog
eeCatalog = requests.get('https://earthengine-stac.storage.googleapis.com/catalog/catalog.json').json()
# Get the datasets
datasets = []
# LEVEL 1
for level1catalog in eeCatalog["links"]:
    if level1catalog["rel"] == "child":
        response = requests.get(level1catalog["href"])
        if response.status_code == 200:
            catalogResponse = response.json()
            # LEVEL 2
            for level2catalog in catalogResponse["links"]:
                if level2catalog["rel"] == "child":
                    if not level2catalog["href"].endswith("catalog.json"):
                        datasets.append(level2catalog)
                    else:
                        response = requests.get(level2catalog["href"])
                        if response.status_code == 200:
                            catalogResponse = response.json()
                            # LEVEL 3
                            for level3catalog in catalogResponse["links"]:
                                if level3catalog["rel"] == "child":
                                    if not level3catalog["href"].endswith("catalog.json"):
                                        datasets.append(level3catalog)
# Save the list as a json file
with open('./list/ee-catalog-flatten.json','w') as fp:
    json.dump(datasets, fp, indent = 4, sort_keys = True)