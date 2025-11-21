
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

gis_custom.ensure_folder(WORK_FOLDER_NAME)
test_item_copy = gis_custom.clone_item_to_folder(TEST_ITEM_ID, WORK_FOLDER_NAME)
test_layer_copy  = test_item_copy.layers[0]

gis_custom.get_layer_fields(test_layer_copy)

gis_custom.delete_all_features(test_layer_copy)
gis_custom.add_csv(test_layer_copy, CSV_PATH)

gis_custom.delete_garbage_field(test_layer_copy,'Область')
gis_custom.delete_garbage_field(test_layer_copy,'date_1')
gis_custom.delete_garbage_field(test_layer_copy,'date__')
gis_custom.delete_garbage_field(test_layer_copy,'GlobalID')
