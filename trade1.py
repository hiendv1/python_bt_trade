
import sys
from PySide import QtCore, QtGui
from gui import Ui_MainWindow
import time
from threading import Timer
import buy_sell

class MyMainWindow(QtGui.QMainWindow):
    count=0
    stragery_status={'trend':False,'bollingerband':False,'cci':False,'rsi':False,'volume':False,'volume_value':0}
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #count=1234
        #self.ui.txt_volume.setText('dv')
        #self.ui.radio_bollinger.changeEvent(self.updateGui)
        #self.ui.radio_bollinger.toggled.connect(self.updateGui)
        #list_dv=['dv','ok','hien']
        #self.ui.list_top_five.addItems(list_dv)
        #self.ui.list_top_five.itemClicked.connect(self.updateGui)
        #self.ui.checkbox_volume.setChecked(False)
        #check=self.ui.checkbox_volume.isChecked()
        #self.ui.txt_buy_1_profit.setText(str(check))
        #self.ui.txt_volume.setDisabled(True)
        #self.ui.btn_sell_imi.clicked.connect(self.btn_event_test)
        self.ui.btn_update_balance.clicked.connect(self.update_balance)
    def update_balance(self):
        total_btc,df=buy_sell.totalBitcoin()
        df=df.reset_index()
        total_usd=total_btc*buy_sell.bit_to_usd()
        self.ui.label_balance_btc.setText('%.4f'%total_btc)
        self.ui.label_balance_usd.setText('%.4f'%total_usd)
        list_balance=[]
        for i in range(len(df)):
            #balance_str=df.loc[i]['Currency']+' '+str(df.loc[i]['Balance'])+' '+str(df.loc[i]['BTC_VALUE'])+' '+str(df.loc[i]['percent'])
            balance_str=df.loc[i]['Currency']+'     %.4f     %.6fBtc    %.2f %%'%(df.loc[i]['Balance'],df.loc[i]['BTC_VALUE'],df.loc[i]['percent'])
            list_balance.append(balance_str)
        self.ui.list_balance.clear()   
        self.ui.list_balance.addItems(list_balance)   
    def btn_event_test(self):   
        #self.onShowWarning()
        self.get_stragery()
    def updateGui(self):
        #self.ui.txt_volume.setText('ok')
        at=self.ui.list_top_five.currentRow()
        et=self.ui.list_top_five.currentItem().text()
        self.ui.txt_volume.setText(et)
        check1=self.ui.radio_bollinger.isChecked()
        self.ui.txt_buy_2_profit.setText(str(check1))
        self.ui.label_balance_btc.setText('500do')
    def onShowWarning(self):
        flags=QtGui.QMessageBox.StandardButton.Ok        
        msg = "TEXTBOX NOT HAVE CHARACTOR !! ONLY NUMBER"
        QtGui.QMessageBox.warning(self, "Warning!",
                                         msg, flags)
        
    def get_stragery(self):
        stragery_status={'trend':False,'bollingerband':False,'cci':False,'rsi':False,'volume':False,'volume_value':0.0}
        if self.ui.radio_trend.isChecked()==True:
            stragery_status['trend']=True
        else:
            stragery_status['trend']=False
        if self.ui.radio_bollinger.isChecked()==True:
            stragery_status['bollingerband']=True
        else:
            stragery_status['bollingerband']=False
        if self.ui.radio_cci.isChecked()==True:
            stragery_status['cci']=True
        else:
            stragery_status['cci']=False
        if self.ui.radio_rsi.isChecked()==True:
            stragery_status['cci']=True
        else:
            stragery_status['cci']=False
        if self.ui.checkbox_volume.isChecked()==True:
            stragery_status['volume']=True
            self.ui.txt_volume.setEnabled(True)
        else:
            stragery_status['volume']=False
            self.ui.txt_volume.setDisabled(True)
        if self.ui.txt_volume.isEnabled()==True:
            try:
               stragery_status['volume_value']=float(self.ui.txt_volume.text())
            except:
               self.onShowWarning()               
        else:
            stragery_status['volume_value']=0.0
        print stragery_status
        return stragery_status
             
           
            
        
        
        """
        self.ui.listTopCoin.addItems(MyMainWindow.listName)
        self.ui.listTopCoin.item(0).setForeground(QtGui.QColor('red'))
        self.ui.btnBuy.clicked.connect(self.updateGui)
    def updateGui(self):
        self.ui.txtProfit.setText(str(MyMainWindow.count))
        MyMainWindow.count=MyMainWindow.count+1
        """
          
        
if __name__ == "__main__":     
    app=QtGui.QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
       app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    myapp = MyMainWindow()
     #t=Timer(20,MyMainWindow.updateGui())
    myapp.show()
    sys.exit(app.exec_())
    