import pyqtgraph as pg
from PyQt5.QtCore import QPointF,pyqtSlot,pyqtSignal,Qt
from PyQt5.QtWidgets import QMenu,QAction,QMessageBox,QTableWidgetItem,QTableWidget,QDialog,QHBoxLayout,QMainWindow
import numpy as np
from PyQt5 import QtGui,QtCore
def tanToColor(s:str):
    if len(s) == 7:
        a1 = s[1:3]
        a2 = s[3:5]
        a3 = s[5:]
    else:
        a1 = s[:2]
        a2 = s[2:4]
        a3 = s[4:]
    def func(string:str):
        d = {"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
        r = int(d.get(string[0],string[0]))*16+int(d.get(string[1],string[1]))
        return r
    return func(a1),func(a2),func(a3)


# 可以作分层标识的二维窗口
class graphView(pg.ImageView):
    def __init__(self,*args,**kwargs):
        super(graphView, self).__init__(*args,**kwargs,imageItem=myImageItem())
        ## Set a custom color map
        colors = [
                "#FFF9B2","#FFFF00","#FEE440","#DCEDC8","#42B3D5","1A237E","#150050"
        ]
        colors = list(map(tanToColor,colors))
        cmap = pg.ColorMap(pos=np.array([0,0.1,0.3,0.5,0.65,0.85,1.0]), color=colors)
        self.setColorMap(cmap)
        self.setEvent()
        # 内部的标识线（见myROI）
        self.ROI = set()


    def setImage(self, img, autoRange=True, autoLevels=True, levels=None, axes=None, xvals=None, pos=None, scale=None, transform=None, autoHistogramRange=True, levelMode=None,rawdata=None, depth =None):
        super(graphView, self).setImage(img, autoRange, autoLevels, levels, axes, xvals, pos, scale, transform, autoHistogramRange, levelMode)
        self.depth = depth
        if rawdata is None:
            self.data = img
        else:
            self.data = rawdata

    def setEvent(self):
        # 设置menu
        view: pg.ViewBox = self.getView()
        menu: QMenu = view.menu
        subMenu = QMenu(menu)
        subMenu.setTitle("Choose Select R")
        menu.addMenu(subMenu)
        self.addNoneROI = QAction("add none ROI", menu)
        self.addNoneROI.setCheckable(True)
        self.addNoneROI.setChecked(True)
        subMenu.addAction(self.addNoneROI)
        self.addNoneROI.triggered.connect(self.triggered_addNoneROI_event)

        self.addSelectROI = QAction("add Select ROI", menu)
        self.addSelectROI.setCheckable(True)
        subMenu.addAction(self.addSelectROI)
        self.addSelectROI.triggered.connect(self.triggered_addSelectROI_event)

        self.addAngleROI = QAction("add Angle ROI",menu)
        subMenu.addAction(self.addAngleROI)
        self.addAngleROI.setCheckable(True)
        self.addAngleROI.triggered.connect(self.triggered_addAngleROI_event)
        self.imageItem.clicked.connect(self.click_event)

    @pyqtSlot(bool)
    def triggered_addNoneROI_event(self, checked: bool):
        self.addSelectROI.setChecked(not checked)
        self.addAngleROI.setChecked(not checked)

    @pyqtSlot(bool)
    def triggered_addSelectROI_event(self,checked:bool):
        self.addNoneROI.setChecked(not checked)
        self.addAngleROI.setChecked(not checked)

    @pyqtSlot(bool)
    def triggered_addAngleROI_event(self, checked: bool):
        self.addNoneROI.setChecked(not checked)
        self.addSelectROI.setChecked(not checked)

    @pyqtSlot(QPointF)
    # 双击事件：添加分层点
    def click_event(self,pos:QPointF):
        if len(self.ROI) > 0:
            if QMessageBox.information(self, "提示", "是否添加新的标记", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                if self.addNoneROI.isChecked():
                    return None
                elif self.addSelectROI.isChecked():
                    _roi = selectROI([[0, pos.y()], [720, pos.y()]],imageView=self)
                elif self.addAngleROI.isChecked():
                    _roi = angleROI([[0, pos.y()], [360, pos.y()],[720, pos.y()]],pen=(0,255,0,0),imageView=self)
                self.ROI.add(_roi)
                self.getView().addItem(_roi)
                _roi.sigRemoveRequested.connect(self.deleteROI_event)
                _roi.sigRemoveAllRequested.connect(self.deleteAllROI_event)
        else:
            if self.addNoneROI.isChecked():
                return None
            elif self.addSelectROI.isChecked():
                _roi = selectROI([[0,pos.y()],[720,pos.y()]],imageView=self)
            elif self.addAngleROI.isChecked():
                _roi = angleROI([[0, pos.y()], [360, pos.y()],[720, pos.y()]],pen=(0,255,0,0),imageView=self)
            self.ROI.add(_roi)
            self.getView().addItem(_roi)
            _roi.sigRemoveRequested.connect(self.deleteROI_event)
            _roi.sigRemoveAllRequested.connect(self.deleteAllROI_event)



    @pyqtSlot(object)
    # 移除分层点
    def deleteROI_event(self,roi):
        print("only one")
        try:
            curve = roi.curveItem
            self.getView().removeItem(curve)
        except:
            pass
        self.ROI.remove(roi)
        self.removeItem(roi)

    @pyqtSlot()
    # 移除所有分层点
    def deleteAllROI_event(self):
        _rois = list(self.ROI)
        for roi in _rois:
            self.deleteROI_event(roi)

    # 获取点数据
    def getHandlPosValues(self):
        result = []
        for roi in self.ROI:
            posValue = roi.getHandlePosValue(self.data)
            # 排序:按每个roi中第一个点，由上到下排列
            if len(result) == 0:
                result.append(posValue)
            else:
                for i in range(len(result) + 1):
                    if i == len(result):
                        result.append(posValue)
                    else:
                        if result[i][0,1] > posValue[0,1]:
                            result.insert(i,posValue)
                            continue
        return result

class myImageItem(pg.ImageItem):
    clicked = pyqtSignal(QPointF)
    def __init__(self, image=None, **kargs):
        super(myImageItem, self).__init__(image=image,**kargs)

    def mouseDoubleClickEvent(self,a0):
        self.clicked.emit(a0.pos())

class myROI(pg.PolyLineROI):
    '''
    注意两个信号量：
        sigRemoveRequested:删除当前roi(ROI 已经定义）
        sigRemoveAllRequested:删除全部roi
    '''
    sigRemoveAllRequested = pyqtSignal() #close all rois

    def getMenu(self):
        # 重写菜单栏
        if self.menu is None:
            self.menu = QMenu()
            self.menu.setTitle("ROI")
            remAct = QAction("Remove ROI", self.menu)
            remAllAct = QAction("Remove All ROI",self.menu)
            remAct.triggered.connect(self.removeClicked)
            remAllAct.triggered.connect(self.sigRemoveAllRequested.emit)
            self.menu.addAction(remAct)
            self.menu.addAction(remAllAct)
            self.menu.remAct = remAct
            self.menu.remAllAct = remAllAct
        return self.menu

    def getHandlePosValue(self, data,depth) -> np.array:
        tmpReuslt = []
        for h in self.getHandles():
            x = int(h.pos().x() / 10)
            print("x:",x)
            if x == 720:
                x = 0
            y = int(h.pos().y())
            print(y)
            rgn = data[x, y]
            dp = depth[y]
            tmpReuslt.append((x, dp, rgn))
        return np.array(tmpReuslt)
    ###################

class selectROI(myROI):
    # 调用返回标识线各个点的数据，返回数据结构
    # np.array,shape:(None,3)--(角度下标*72,深度下标*100,数据值)
    def __init__(self,*arg, imageView, **kwargs):
        super(selectROI, self).__init__(*arg,**kwargs)
        menu = self.getMenu()
        action_showInfo = QAction("show Info",menu)
        menu.addAction(action_showInfo)
        action_showInfo.triggered.connect(self.showInfo_event)
        self.data = imageView.data
        self.depth = imageView.depth

    def movePoint(self, handle, pos:QPointF, modifiers=Qt.KeyboardModifier(), finish=True, coords='parent'):
        index = -1
        length = len(self.handles)
        for i in range(length):
            c = self.handles[i]["item"]==handle
            if c:
                index = i
        if index == 0 or index == length-1:
            pos.setX(handle.scenePos().x())
            super(myROI, self).movePoint(handle, pos, modifiers, finish, coords)
        else:
            super(myROI, self).movePoint(handle, pos, modifiers, finish, coords)

    @pyqtSlot()
    def showInfo_event(self):
        dailog = QDialog()
        tableW = QTableWidget()
        tableW.setColumnCount(len(self.getHandles()))
        tableW.setRowCount(3)
        tableW.setVerticalHeaderItem(0,QTableWidgetItem("x"))
        tableW.setVerticalHeaderItem(1, QTableWidgetItem("y"))
        tableW.setVerticalHeaderItem(2, QTableWidgetItem("value"))
        point = self.getHandlePosValue(self.data, self.depth)
        for i in range(point.shape[0]):
            tableW.setItem(0,i, QTableWidgetItem("{:.2f}°".format(point[i,0]*5)))
            tableW.setItem(1, i, QTableWidgetItem("{:.2f}m".format(point[i, 1])))
            tableW.setItem(2, i, QTableWidgetItem("{}".format(point[i, 2])))

        layout = QHBoxLayout()
        dailog.setLayout(layout)
        layout.addWidget(tableW)
        dailog.exec_()

class angleROI(myROI):
    def __init__(self,*arg,imageView,**kwargs):
        super(angleROI, self).__init__(*arg,**kwargs)
        self.curveItem = pg.PlotCurveItem(pen=(255, 255, 255, 200), antialias=True)
        view = imageView.getView()
        view.addItem(self.curveItem)
        self.sigRegionChanged.connect(self.curveUpdate)
        self.curveUpdate()
        self.moveFLag = True
        menu = self.getMenu()
        action_showInfo = QAction("show Info", menu)
        menu.addAction(action_showInfo)
        action_showInfo.triggered.connect(self.showInfo_event)
        self.data = imageView.data
        self.depth = imageView.depth

    def movePoint(self, handle, pos:QPointF, modifiers=Qt.KeyboardModifier(), finish=True, coords='parent'):
        index = -1
        length = len(self.handles)
        for i in range(length):
            c = self.handles[i]["item"]==handle
            if c:
                index = i
        if index == 0 or index == length-1:
            pos.setX(handle.scenePos().x())
            super(myROI, self).movePoint(handle, pos, modifiers, finish, coords)
            firstHandle = self.handles[0]["item"]
            endHandle = self.handles[-1]["item"]
            if firstHandle.scenePos().y() != endHandle.scenePos().y() and self.moveFLag:
                self.moveFLag = False
                if index == 0:
                    p = QPointF(endHandle.scenePos().x(),firstHandle.scenePos().y())
                    endHandle.movePoint(p)
                else:
                    p = QPointF(firstHandle.scenePos().x(), endHandle.scenePos().y())
                    firstHandle.movePoint(p)
                self.moveFLag = True
        else:
            super(myROI, self).movePoint(handle, pos, modifiers, finish, coords)

    def segmentClicked(self, segment, ev=None, pos=None):
        number = len(self.handles)
        if number >= 3:
            pass
        else:
            super(angleROI, self).segmentClicked(segment,ev,pos)

    def removeHandle(self, handle, updateSegments=True):
        pass

    @pyqtSlot()
    def curveUpdate(self):
        pts = self.getState()['points']
        width = pts[-1].x() - pts[0].x()
        A2 = (pts[1].y() - pts[0].y())/2
        A1 = pts[0].y() + A2
        A3 = (pts[1].x() - pts[0].x())
        x,y = F_plotPoint(A1,A2,A3,width)
        self.curveItem.setData(x, y)
        self.curveItem.setPen(pg.mkPen("#B61919",width=2))

    @pyqtSlot()
    def showInfo_event(self):
        dailog = angleTableDailog()
        point = self.getHandlePosValue(self.data,self.depth)
        D = 0.18
        DI = 0.12
        H = (point[1,1] - point[0,1])
        dailog.setInfo(D,DI,H)
        dailog.exec_()
#
def F_theta(A1,A2,A3,theta):
    c = np.cos((theta-A3)*np.pi/180)
    r = A1+A2*c
    return r

def F_plotPoint(A1,A2,A3,width):
    x = np.arange(0,360,1)
    y = F_theta(A1,A2,A3*360/width,x)
    return x /360 * width,y

class angleTableDailog(QDialog):
    def __init__(self,*args, **kwargs):
        super(angleTableDailog, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.tableW = QTableWidget()
        layout.addWidget(self.tableW)
        self.tableW.setRowCount(4)
        self.tableW.setColumnCount(1)
        self.tableW.setHorizontalHeaderItem(0,QTableWidgetItem("value"))
        txt = ["D","DI","H","a"]
        for i in range(4):
            self.tableW.setVerticalHeaderItem(i, QTableWidgetItem(txt[i]))

        self.D_Item = QTableWidgetItem()
        self.tableW.setItem(0, 0, self.D_Item)
        self.DI_Item = QTableWidgetItem()
        self.tableW.setItem(1, 0, self.DI_Item)
        self.H_Item = QTableWidgetItem()
        self.tableW.setItem(2, 0, self.H_Item)
        self.a_Item = QTableWidgetItem()
        self.tableW.setItem(3, 0, self.a_Item)

    def setInfo(self,D, DI, H):
        a = np.arctan(H/(D+DI*2))
        angle = a/np.pi * 180
        # if angle < 0:
        #     angle += 90
        self.D_Item.setText("{}m".format(D))
        self.DI_Item.setText("{}m".format(DI))
        self.H_Item.setText("{:.2f}m".format(H))
        self.a_Item.setText("{:.5f}°".format(angle))


if __name__ == '__main__':
    # from pyqtgraph.examples import run
    # run()
    import sys
    from tmp_interpolation import *
    app = QtGui.QApplication([])
    win = QMainWindow()
    img = graphView(parent=win)
    #rawData = azidendf[2200:2670]
    #data_after = dynamicOperation(rawData, testFunction)
    #dO2 = functools.partial(testFunction,dealStep=2)
    #data_raw = dynamicOperation(rawData,dO2)
    from pastCode.measureData import measureData
    nowData = measureData
    img.setImage(nowData.values.T, rawdata=nowData.values.T,depth=nowData.index.values)
    win.setCentralWidget(img)
    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()