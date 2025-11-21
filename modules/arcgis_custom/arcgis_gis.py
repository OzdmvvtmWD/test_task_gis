import datetime as dt
import pandas as pd
from arcgis.gis import GIS

from modules.utils.utils import get_mapping, get_n_mapping

class GISDriver:
    def __init__(self,
                 username: str,
                 password: str,
                 portal: str = "https://www.arcgis.com"):

        self._gis = GIS(portal, username, password)

    @property
    def gis(self):
        return self._gis
    
    @gis.setter
    def gis(self, value):
        self._gis = value

    def ensure_folder(self, name_folder):
        try:
            self.gis.content.folders.create(name_folder)
        except Exception:
            pass 


    def get_item(self, item_id: str):
        return self.gis.content.get(item_id)
    

    def search_by_title(self, title: str, owner: str = None):
        if owner is None:
            owner = self.gis.users.me.username

        items = self.gis.content.search(f'title:"{title}" owner:{owner}')
        return items[0] if items else None
    

    
    def get_item_in_folder(self, title: str, name_folder:str, type_r:str = None):
        
        user = self.gis.users.get(self.gis.users.me.username)

        for item in user.items(folder=name_folder):
            if item.title == title:
                if type_r:
                    if item.type.lower() == type_r.lower():
                        return item
                    
                else:
                    return item
            
        return None
    

    def clone_item_to_folder(self, item_id: str, name_folder:str):
        item = self.gis.content.get(item_id)

        result = self.gis.content.clone_items(
            items=[item],
            folder=name_folder
        )
        return self.get_item_in_folder(item.title, name_folder)
    
    
    def get_source_info(self, item_id):
        return self.gis.content.analyze(item=item_id, file_type='csv', location_type='none')
    

    def upload_csv_to(self, csv_path: str, title: str, name_folder:str = None):
        now_ts = str(int(dt.datetime.now().timestamp()))

        item_prop = {
            'title': f'{title}',
            'type': 'CSV'
        }
        root_folder = None
        if name_folder:
            self.ensure_folder(name_folder)
            root_folder = self.gis.content.folders.get(name_folder)

        else:
            root_folder = self.gis.content.folders.get()

        item_exist = self.get_item_in_folder(title, name_folder)

        if item_exist:
            return item_exist

        item = root_folder.add(item_properties=item_prop, file=csv_path).result()

        return item
    
    
    def add_csv(self, layer, csv_path, limit: int = None):
        df = pd.read_csv(csv_path)

        adding_list = []

        for item, row in df.iterrows():
            feat = get_n_mapping(self.gis, row)
            print(item, feat)
            adding_list.append(feat)

            if limit:
                if item >= limit:
                    break

        add_result = layer.edit_features(adds = adding_list)
        print(add_result)


    def get_layer_fields(self, layer):
        for f in layer.properties.fields:
            print(f["name"], "|", f.get("alias"))
        
        return layer.properties.fields


    def delete_garbage_field(self, layer, field_name):

        all_fields = [f["name"] for f in layer.properties.fields]
        fields_to_delete = [f for f in all_fields if f == field_name]

        print("Fields to delete:", fields_to_delete)

        if not fields_to_delete:
            print("No fields to delete.")
            return

        payload = {"fields": [{"name": fld} for fld in fields_to_delete]}
        result = layer.manager.delete_from_definition(payload)
        print(result)

    # def delete_feature(self, layer):

    def delete_all_features(self, layer):
        all_features = layer.query(where="1=1").features
        all_object_ids = [str(f.attributes['OBJECTID']) for f in all_features]
        delete_string = ",".join(all_object_ids)

        delete_result = layer.edit_features(deletes=delete_string)
        print(delete_result)
