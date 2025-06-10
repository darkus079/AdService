import os
import json
from datetime import datetime
from Manager import Manager
from typing import List, Dict


class AdManager(Manager):
    def __init__(self):
        self.ads_file = "ads.json"
        self.ads = self._load(self.ads_file)

    def save(self):
        with open(self.ads_file, 'w') as f:
            json.dump(self.ads, f, indent=4)

    def _load(self, filename: str):
        if os.path.exists(self.ads_file):
            with open(self.ads_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def add_ad(self, current_user: str, ad_data: Dict):
        if not self.ads:
            ad_id = "1"
        else:
            max_id = max(int(k) for k in self.ads.keys())
            ad_id = str(max_id + 1)

        ad_data['id'] = ad_id
        ad_data['owner'] = current_user
        ad_data['popularity'] = 0
        ad_data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ads[ad_id] = ad_data
        self.save()

    def update_ad(self, ad_id: str, ad_data: Dict):
        if ad_id in self.ads:
            self.ads[ad_id].update(ad_data)
            self.save()

    def delete_ad(self, ad_id: str):
        if ad_id in self.ads:
            del self.ads[ad_id]
            self.save()

    def increment_popularity(self, ad_id: str):
        if ad_id in self.ads:
            self.ads[ad_id]['popularity'] += 1
            self.save()

    def get_user_ads(self, current_user: str) -> List[Dict]:
        return [ad for ad in self.ads.values() if ad['owner'] == current_user]

    def get_all_ads(self) -> List[Dict]:
        return list(self.ads.values())