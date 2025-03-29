from PyQt5.QtWidgets import QMainWindow, QHeaderView
from TblView import Viewer
    
class Main_(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Viewer(db='Assets/DataBases/test_data.db', table="Products", custom_name="Product", icon_address="Assets/Images/Products.png", tbl_SectionResizeMode=QHeaderView.Stretch, toolbar_movable=False, toolbar_floatable=False, bottom_toolbar=True, bottom_toolbar_movable=False, bottom_toolbar_floatable=False, TTS_sts=True, custom_field_name=["ID", "Name", "Supplier Name", "Price", "Date"]))
             
