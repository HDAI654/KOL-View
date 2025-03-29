from PublicRep import PR
from PyQt5.QtCore import QRegularExpression, QDate
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QDateEdit, QLabel, QDateEdit, QScrollArea, QVBoxLayout, QWidget
import datetime


class ASE_win(QMainWindow):
    
    def __init__(self, db, table, add_edit_sts, back_func, custom_data, TTS_mdl, page_title=None, df="yyyy/MM/dd", row_data=None, TTS_sts=False, custom_field_name=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.table = table
        self.add_edit_sts = "Add"
        if self.add_edit_sts in ["Add", "Edit"]:
            self.add_edit_sts = add_edit_sts
        self.back_func = back_func
        self.custom_data = custom_data
        self.page_title = f"Add New  {self.custom_data["Table_name"]}"
        if page_title:
            self.page_title = page_title
        self.df = df  
        self.row_data = row_data
        self.TTS_sts = TTS_sts
        
        self.custom_field_name = [cf[0] for cf in self.custom_data["Columns"]]
        if custom_field_name and len(custom_field_name) == len(self.custom_data["Columns"]):
            self.custom_field_name = [str(cfn) for cfn in custom_field_name]
        
        
        self.validators = {"INTEGER":QIntValidator(), "STRING":None, "FREE":None, "EMAIL":QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"))}
        self.TTS_mdl = TTS_mdl
        
        self.FormUI()
        
    def FormUI(self):
        # the main scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)
        
        
        # the main widget
        self.form_widget = QWidget()
        self.scroll_area.setWidget(self.form_widget)
        
        # layout
        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)
        
        # title button
        self.PageTitle = QPushButton(self.page_title)
        self.form_layout.addWidget(self.PageTitle)
        
        # back button
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.back_func)
        self.form_layout.addWidget(self.back_btn)
        
        self.form_layout.addSpacing(50)
        
        # Create Fields
        self.fields = {}
        self.src_edit = {}
        for i, f in enumerate(self.custom_data['Columns']):
            lbl = QLabel(str(f"{self.custom_field_name[i]} :"))
            input = QLineEdit()
            input.setPlaceholderText(f"Enter {f[0]}")
            
            if self.add_edit_sts == "Edit":
                input.setText(self.row_data[i])
            
            # set validators
            if str(f[1]) == "PRIMARY":
                continue
            
            elif str(f[1]) == "DATE":
                input = QDateEdit()
                if self.add_edit_sts == "Add":
                    t = str(datetime.date.today()).split("-")
                    input.setDate(QDate(int(t[0]), int(t[1]), int(t[2])))
                    input.setDisplayFormat(self.df)
                    
                if self.add_edit_sts == "Edit":
                    t = str(datetime.date.today()).split("-")
                    input.setDate(QDate().fromString(self.row_data[i], self.df))
                    input.setDisplayFormat(self.df)
            
            else:
                input.setValidator(self.validators[f[1]])
            
            # add to page and fields array
            self.fields[str(f[0])] = input
            self.src_edit[str(f[0])] = input.text()
            self.form_layout.addWidget(lbl)
            self.form_layout.addWidget(input)
            

        # Submit Button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.SubmitClick)
        self.form_layout.addWidget(self.submit_btn)
   
    def SubmitClick(self):
        data = {}
        for k, v in self.fields.items():
            data[str(k)] = str(v.text()) 
             
        if self.add_edit_sts == "Add":
            FLAG = True
            for i, f in enumerate(self.custom_data['Columns']):
                if f[2] == 0: # if field can be null
                    pass
                elif f[2] == 1:# if field can not be null
                    if str(f[0]) in data.keys(): # if field be in data (some field are not   like primaty keys that we didn't make Line edit for primaries)
                        if str(data[str(f[0])]).strip() != "": # if field is not null
                            pass
                        else: # if field is null
                            FLAG = False
                    else:
                        pass
                else:
                    pass
              
            if FLAG:
                PR.Insert(db=self.db, table=self.table, fields=", ".join(data.keys()), values=", ".join([f"'{x}'" for x in data.values()]))
                self.back_func()
                self.TTS_mdl.text_to_speech("Add successful", self.TTS_sts)
            else:
                self.TTS_mdl.text_to_speech("You have to fill all fields", self.TTS_sts)
                return
        elif self.add_edit_sts == "Edit":
            FLAG = True
            for i, f in enumerate(self.custom_data['Columns']):
                if f[2] == 0: # if field can be null
                    pass
                elif f[2] == 1:# if field can not be null
                    if str(f[0]) in data.keys(): # if field be in data (some field are not   like primaty keys that we didn't make Line edit for primaries)
                        if str(data[str(f[0])]).strip() != "": # if field is not null
                            pass
                        else: # if field is null
                            FLAG = False
                    else:
                        pass
                else:
                    pass
            
            if FLAG:
                sf = str(", ".join([f"{d[0]}='{d[1]}'" for d in data.items()]))
                whr = str(" AND ".join([f"{dd[0]}='{dd[1]}'" for dd in self.src_edit.items()]))
                PR.Update(db=self.db, table=self.table, set_fields=sf, where=whr)
                self.back_func()
                self.TTS_mdl.text_to_speech("Edit successful", self.TTS_sts)
                    
            else:
                self.TTS_mdl.text_to_speech("You have to fill all fields", self.TTS_sts)
                return
        else:
            return
        
                