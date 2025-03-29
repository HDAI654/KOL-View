from PublicRep import PR
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TextToSpeech import TTS
from Add_Edit import ASE_win
import pandas as pd
import os
import sqlite3

class Viewer(QMainWindow):
    
    def __init__(self, db, table, custom_name, icon_address, tbl_SectionResizeMode, toolbar_movable, toolbar_floatable, bottom_toolbar=True, bottom_toolbar_movable=False, bottom_toolbar_floatable=False, style_sheet=PR.Style(), exp_sts=True, DF_SAVE_METHODS={"csv":pd.DataFrame.to_csv, "json":pd.DataFrame.to_json, "html":pd.DataFrame.to_html, "db":pd.DataFrame.to_sql, "md":pd.DataFrame.to_markdown}, DEFAULT_SAVE_PATH=str(os.path.expanduser("~")), row_tools_sts=True, df="yyyy/MM/dd", TTS_sts=False, custom_field_name=None, **kwargs):
        super().__init__(**kwargs)
        self.db = str(db)
        self.table = str(table)
        self.custom_name = str(custom_name)
        self.icon_address = str(icon_address)
        self.tbl_SectionResizeMode = tbl_SectionResizeMode
        self.toolbar_movable = toolbar_movable
        self.toolbar_floatable = toolbar_floatable
        self.bottom_toolbar = bottom_toolbar
        self.bottom_toolbar_movable = bottom_toolbar_movable
        self.bottom_toolbar_floatable = bottom_toolbar_floatable
        self.style_sheet = style_sheet
        self.exp_sts = exp_sts
        self.row_tools_sts = row_tools_sts
        self.df = df
        
        self.setStyleSheet(self.style_sheet)
        
        self.custom_data = PR.SQL_Table_to_custom_data(self.db, self.table, "main")
        self.data = PR.Select(self.db, "*", self.table, "true")
        self.search_combo_index = 0
        self.search_input_text = ""
        self.HEADS = PR.Get_Fields_of_a_table(self.db, self.table)
        
        self.TOOLS_HEAD = []
        if self.row_tools_sts:
            self.TOOLS_HEAD = ["Delete Tool", "Show/Edit"]
        self.selected_row = None
        self.selected_column = None
        self.TTS_sts = TTS_sts
        self.TTS_mdl = TTS()
        self.DF_SAVE_METHODS = DF_SAVE_METHODS
        self.DEFAULT_SAVE_PATH = DEFAULT_SAVE_PATH
        
        self.custom_field_name = [cf[0] for cf in self.custom_data["Columns"]]
        if custom_field_name and len(custom_field_name) == len(self.custom_data["Columns"]):
            self.custom_field_name = [str(cfn) for cfn in custom_field_name]
        
        
        
        self.UI()
    
    def UI(self):
        self.StackUI()
        self.ToolbarUI()
        self.TableUI()
        if self.bottom_toolbar:
            self.BottomToolbarUI()
         
    def StackUI(self):
        # create main layers
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create Frames
        self.table_frame = QMainWindow()
        self.add_edit_frame = QMainWindow()

        # Add Frames to Stacked Widget
        self.stacked_widget.addWidget(self.table_frame)
        self.stacked_widget.addWidget(self.add_edit_frame)
        self.stacked_widget.setCurrentIndex(0)
    
    def TableUI(self):
        # create table of clients info
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.HEADS+self.TOOLS_HEAD))
        self.table_widget.setHorizontalHeaderLabels(self.custom_field_name+self.TOOLS_HEAD)
        self.table_widget.horizontalHeader().setSectionResizeMode(self.tbl_SectionResizeMode)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.horizontalHeader().sectionClicked.connect(self.ColClick)
        self.table_widget.verticalHeader().sectionClicked.connect(self.RowClick)
        self.table_widget.verticalHeader().sectionDoubleClicked.connect(lambda index: self.EditClick(row=index))
        self.table_widget.cellClicked.connect(self.CellClick)

        self.table_frame.setCentralWidget(self.table_widget)

        # Do search
        self.Search()
      
    def ToolbarUI(self):
        # Toolbar
        self.toolbar = QToolBar(f"{self.custom_name} Page Tools")
        self.toolbar.setMovable(self.toolbar_movable)
        self.toolbar.setFloatable(self.toolbar_floatable)
        self.toolbar.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.table_frame.addToolBar(self.toolbar)

        # Icon
        self.ClientIcon = QLabel()
        self.ClientIcon.setPixmap(QPixmap(self.icon_address))
        self.ClientIcon.setAlignment(Qt.AlignCenter)
        self.toolbar.addWidget(self.ClientIcon)
        self.toolbar.addSeparator()

        # Actions
        self.delete_all_action = QAction(QIcon(QPixmap("Assets/Images/Delete All.png")), "Delete All (Ctrl+Alt+D)", self)
        self.delete_all_action.setShortcut("Ctrl+Alt+D")
        self.delete_all_action.triggered.connect(lambda : self.DeleteAll(DO=None, Dialog=None))
        self.toolbar.addAction(self.delete_all_action)

        self.refresh_action = QAction(QIcon(QPixmap("Assets/Images/Refresh.png")), "Refresh (Ctrl+R)", self)
        self.refresh_action.setShortcut("Ctrl+R")
        self.refresh_action.triggered.connect(self.RefreshAll)
        self.toolbar.addAction(self.refresh_action)

        self.add_action = QAction(QIcon(QPixmap("Assets/Images/Add2.png")), "Add (Ctrl+N)", self)
        self.add_action.setShortcut("Ctrl+N")
        self.add_action.triggered.connect(self.AddClick)
        self.toolbar.addAction(self.add_action)
        
        
        self.del_action = QAction(QIcon(QPixmap("Assets/Images/Delete.png")), "Delete (Ctrl+D)", self)
        self.del_action.setShortcut("Ctrl+D")
        self.del_action.triggered.connect(lambda : self.DeleteClick(row=None, DFI=True))
        self.toolbar.addAction(self.del_action)
        
        self.edit_action = QAction(QIcon(QPixmap("Assets/Images/Edit.png")), "Edit (Ctrl+E)", self)
        self.edit_action.setShortcut("Ctrl+E")
        self.edit_action.triggered.connect(lambda : self.EditClick(row=None, DFI=True))
        self.toolbar.addAction(self.edit_action)
        
        self.exp_action = QAction(QIcon(QPixmap("Assets/Images/Export.png")), "Export Data (Ctrl+Shift+E) \n convert data to some types of file and save it", self)
        self.exp_action.setShortcut("Ctrl+Shift+E")
        self.exp_action.triggered.connect(self.ExportClick)
        if self.exp_sts :
            self.toolbar.addAction(self.exp_action)

        # Search Widget
        self.search_widget = QWidget()
        self.serach_layout = QHBoxLayout()
        self.search_widget.setLayout(self.serach_layout)
        self.toolbar.addWidget(self.search_widget)
        ## Search Input
        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setPlaceholderText("Search")
        self.search_input.setText(self.search_input_text)
        self.search_input.textChanged.connect(self.Search)
        self.serach_layout.addWidget(self.search_input)
        

        ## Search ComboBox
        self.search_combo = QComboBox()
        self.search_combo.addItems(["All"]+self.custom_field_name)
        self.search_combo.setCurrentIndex(self.search_combo_index)
        self.search_combo.currentIndexChanged.connect(self.ComboChange)
        self.serach_layout.addWidget(self.search_combo)
    
    def BottomToolbarUI(self):
        # Bottom Toolbar
        self.bottom_toolbar = QToolBar()
        self.bottom_toolbar.setMovable(self.bottom_toolbar_movable)
        self.bottom_toolbar.setFloatable(self.bottom_toolbar_floatable)
        self.bottom_toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.bottom_toolbar.setOrientation(Qt.Horizontal)
        self.table_frame.addToolBar(Qt.BottomToolBarArea, self.bottom_toolbar)
        
        # Labels
        self.row_and_col_selected_label = QLabel("selected row: None, selected column: None")
        self.row_and_col_selected_label.setAlignment(Qt.AlignCenter)
        self.row_and_col_selected_label.setStyleSheet("font-size: 15px;margin-top: 2px;color: #ffffff;font-weight: bold;")
        self.bottom_toolbar.addWidget(self.row_and_col_selected_label)
    
    def RefreshAll(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
        # Remake
        self.search_input_text = ""
        self.selected_row = None
        self.selected_column = None

        self.UI()
    
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                attr.deleteLater()
        # Remake
        self.selected_row = None
        self.selected_column = None
        self.UI()
    
    def Search(self):
        # set new data of input
        self.search_input_text = self.search_input.text()

        # Get Table Data
        table_data = list(PR.Select(self.db, '*', self.table, 'true'))
        
        # Input Text
        search_text = self.search_input.text()

        # End Data After Search
        filtered_data = []

        if table_data != None:

            # Search
            if search_text.strip() != "" :

                # Search By All Field
                if self.search_combo.currentIndex() == 0 :
                    for row in table_data :
                        for cell in row:
                            if PR.Filter(search_text, cell):
                                if row not in filtered_data:
                                    filtered_data.append(row)
                                    continue
                
                # Search By a Field
                else :
                    for row in table_data :
                        if PR.Filter(search_text, row[self.search_combo.currentIndex()-1]) :
                            if row not in filtered_data:
                                filtered_data.append(row)

                # Fill Table With Filtered Data
                self.FillTable(data=filtered_data)
            
            
            # if search input not filled
            if self.search_input.text().strip() == "" :
                self.FillTable(data=list(PR.Select(self.db, '*', self.table, 'true')))

    def FillTable(self, data):
        if data != None:
            # set row count
            self.table_widget.setRowCount(len(data))

            # Set Data
            for row in range(len(data)):
                for column in range(len(data[row])):
                    self.table_widget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

            if self.row_tools_sts:
                # Set Delete Buttons
                for row_index, row_data in enumerate(data):
                    button = QPushButton("Delete")
                    self.table_widget.setCellWidget(row_index, len(self.HEADS), button)
                    button.clicked.connect(lambda checked, row=row_index: self.DeleteClick(row))
                
                # Set Show/Edit Buttons
                for row_index, row_data in enumerate(data):
                    button = QPushButton("Show/Edit")
                    self.table_widget.setCellWidget(row_index, len(self.HEADS)+1, button)
                    button.clicked.connect(lambda checked, row=row_index: self.EditClick(row))
        return
    
    def ComboChange(self):
        self.search_combo_index = self.search_combo.currentIndex()
        if self.search_input.text().strip() != "" :
            self.Search()
    
    def ColClick(self, column):
        self.selected_row = None
        self.selected_column = column
        self.row_and_col_selected_label.setText(f"selected column: {column+1}")
        
    def RowClick(self, row):
        self.selected_column = None
        self.selected_row = row
        self.row_and_col_selected_label.setText(f"selected row: {row+1}")
        
    def CellClick(self, row, column):
        self.selected_row = row
        self.selected_column = column
        self.row_and_col_selected_label.setText(f"selected row: {row+1}, selected column: {column+1}")
        
    def DeleteAll(self, DO=None, Dialog=None):
        if DO == None :
            # Show Dialog
            dialog = QDialog(self)
            dialog.setWindowOpacity(1)
            dialog.setWindowTitle("Delete All")
            dialog.setWindowFlag(Qt.SubWindow)
            # Layout
            dialog_layout = QVBoxLayout()
            dialog.setLayout(dialog_layout)
            
            # Label
            label = QLabel("Are you sure you want to delete all data?")
            dialog_layout.addWidget(label)
            
            # Buttons
            button_layout = QHBoxLayout()
            dialog_layout.addLayout(button_layout)
            # OK Button
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(lambda : self.DeleteAll(DO=True, Dialog=dialog))
            button_layout.addWidget(ok_button)
            # Cancel Button
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(dialog.close)
            button_layout.addWidget(cancel_button)
            # Show Dialog
            dialog.exec_()
        
        if DO == True :
            if Dialog:
                Dialog.close()
            PR.Delete(self.db, self.table, 'true')
            self.RefreshAll()
            self.TTS_mdl.text_to_speech(f"All Data deleted successfully", self.TTS_sts)
    
            
        return
      
    def AddClick(self):
        self.add_edit_frame = ASE_win(db=self.db, table=self.table, add_edit_sts='Add', back_func=self.BackToViewFunc, TTS_mdl=self.TTS_mdl, custom_data=self.custom_data, page_title=f"Add New {self.custom_name}", df=self.df, TTS_sts=self.TTS_sts, custom_field_name=self.custom_field_name)
        self.stacked_widget.insertWidget(1, self.add_edit_frame)
        self.stacked_widget.setCurrentIndex(1)
        
    def DeleteClick(self, row, DFI=None):
        if DFI == None and row != None: # when the rows delete button is clicked
            row_dt = []
            for c in range(len(self.HEADS)):
                row_dt.append(self.table_widget.item(int(row), int(c)).text())
            whr = str(" AND ".join([f"{dd[0]}='{dd[1]}'" for dd in zip(self.HEADS, row_dt)]))
            PR.Delete(self.db, self.table, whr)
            self.Refresh()
            self.TTS_mdl.text_to_speech("Delete successful", self.TTS_sts)
        
        if DFI == True : # when the delete action in toolbar is clicked
            if self.selected_row != None and self.selected_column == None:
                row = self.selected_row
                row_dt = []
                for c in range(len(self.HEADS)):
                    row_dt.append(self.table_widget.item(int(row), int(c)).text())
                whr = str(" AND ".join([f"{dd[0]}='{dd[1]}'" for dd in zip(self.HEADS, row_dt)]))
                PR.Delete(self.db, self.table, whr)
                self.Refresh()
                self.TTS_mdl.text_to_speech("Delete successful", self.TTS_sts)
                
        return
        
    def EditClick(self, row, DFI=None):
        if DFI == None and row != None: # when the rows edit button is clicked
            row_dt = []
            for c in range(len(self.HEADS)):
                row_dt.append(self.table_widget.item(int(row), int(c)).text())
                
            self.add_edit_frame = ASE_win(db=self.db, table=self.table, add_edit_sts='Edit', back_func=self.BackToViewFunc, TTS_mdl=self.TTS_mdl, custom_data=self.custom_data, page_title=f"Show/Edit {self.custom_name}", df=self.df, row_data=row_dt, TTS_sts=self.TTS_sts, custom_field_name=self.custom_field_name)
            self.stacked_widget.insertWidget(1, self.add_edit_frame)
            self.stacked_widget.setCurrentIndex(1)
        
        if DFI == True : # when the edit action in toolbar is clicked
            if self.selected_row != None and self.selected_column == None:
                row = self.selected_row
                row_dt = []
                for c in range(len(self.HEADS)):
                    row_dt.append(self.table_widget.item(int(row), int(c)).text())
                    
                self.add_edit_frame = ASE_win(db=self.db, table=self.table, add_edit_sts='Edit', back_func=self.BackToViewFunc, TTS_mdl=self.TTS_mdl, custom_data=self.custom_data, page_title=f"Show/Edit {self.custom_name}", df=self.df, row_data=row_dt, TTS_sts=self.TTS_sts, custom_field_name=self.custom_field_name)
                self.stacked_widget.insertWidget(1, self.add_edit_frame)
                self.stacked_widget.setCurrentIndex(1)
        
        return
        
    def BackToViewFunc(self):
        self.RefreshAll()
      
    def ExportClick(self):
        # create a DataFrame from the data
        df = pd.DataFrame(self.data, columns=self.HEADS)
        
        # found the file formats that can be saved
        file_supports = []
        for ft in self.DF_SAVE_METHODS.keys():
            file_supports.append(f"{ft.upper()} File (*.{ft})")
        file_supports = ";;".join(file_supports)
            
        # open a file dialog to get file name and path
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", self.DEFAULT_SAVE_PATH, file_supports, options=options)
          
        # save the file
        if fileName:
            ft = str(fileName.rsplit(".", 1)[-1])
            if ft in self.DF_SAVE_METHODS.keys():
                if ft == "db":
                    self.DF_SAVE_METHODS[ft](df, self.table, con=sqlite3.connect(fileName), index=False, if_exists="replace")
                else:
                    self.DF_SAVE_METHODS[ft](df, str(fileName))
                """except:
                    self.TTS_mdl.text_to_speech("File saving faild", self.TTS_sts)
                else:
                    self.TTS_mdl.text_to_speech("File saved successfully", self.TTS_sts)"""
                
                return
            else:
                self.TTS_mdl.text_to_speech("File format not supported", self.TTS_sts)
                return
                
        else:
            return
              