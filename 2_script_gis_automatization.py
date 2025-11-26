
from modules.arcgis_custom.arcgis_gis import GISDriver
from dotenv import load_dotenv
from CONFIG import *

load_dotenv()

USERNAME = os.environ.get('USERNAME_GIS') 
PASSWORD = os.environ.get('PASSWORD_GIS')

gis_custom = GISDriver(
    USERNAME, 
    PASSWORD, 
    PORTAL_URL
)

test_item = gis_custom.get_item(TEST_ITEM_ID)
test_layer = test_item.layers[0]

print(test_layer.properties['capabilities'])

# gis_custom.ensure_folder(WORK_FOLDER_NAME)
# test_item_copy = gis_custom.clone_item_to_folder(TEST_ITEM_ID, WORK_FOLDER_NAME)
# test_layer_copy  = test_item_copy.layers[0]
# print(test_layer_copy.properties['capabilities'])

print(test_item.id)
gis_custom.get_layer_fields(test_layer)

gis_custom.delete_all_features(test_layer)
gis_custom.add_csv(test_layer, CSV_PATH)


"""
for deleting garbage_field, if i try it calls 
Exception: User does not have permissions to access this service
User does not have permissions to access this service
(Error Code: 403)
"""
# gis_custom.delete_garbage_field(test_layer,'Область')
# gis_custom.delete_garbage_field(test_layer,'date_1')
# gis_custom.delete_garbage_field(test_layer,'date__')
# gis_custom.delete_garbage_field(test_layer,'GlobalID')
