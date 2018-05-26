#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wx
import wx.grid
import math


# MainFrame class is the main window of the application. Inside it there are 4 different panels aimed to show a CAD file,
# edit it, put some additional parameters to the geometry and future robot's movement, and finally create and save fully
# compatible AS language file.


class MainFrame(wx.Frame):
    def __init__(self, parent):
        style = wx.DEFAULT_FRAME_STYLE #^ wx.RESIZE_BORDER #^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, parent, title=".asCAD", size=(977, 728), style=style)
        icon = wx.Icon('ascad.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # MyData list consist of all the trajectories from the CAD file
        # myPoints list consist of all the reference points
        self.myData = []
        self.myPoints = []

        self.programName = ""
        self.choice = -1

        self.sizer = wx.GridBagSizer(1, 1)
        wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)

        self.createDrawPanel()
        self.createListPanel()
        self.createEditPanel()
        self.createASPanel(self.programName)
        self.SetSizer(self.sizer)

        openIcon = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        saveIcon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16, 16))
        exitIcon = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16, 16))

        # self.statusBar = self.CreateStatusBar()
        self.toolBar = self.CreateToolBar()
        openTool = self.toolBar.AddSimpleTool(1, openIcon, "New", "Open new DXF file")
        saveTool = self.toolBar.AddSimpleTool(2, saveIcon, "Save", "Save the `file into AS code")
        exitIcon = self.toolBar.AddSimpleTool(3, exitIcon, "Exit", "Exit program")
        self.toolBar.Realize()

        self.toolBar.EnableTool(2, False)

        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "Open a CAD file", "Utworz nowy plik")
        self.menuSave = filemenu.Append(wx.ID_SAVE, "Save a AS file", "Zapisuje plik w formacie AS")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "About the program","Informacje o programie")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"Exit","Wyjscie z programu")

        self.menuSave.Enable(False)

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        self.Center()
        self.Show()

        #Setting event handlers
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuNew)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.ASPanel.btnRefresh)
        self.Bind(wx.EVT_BUTTON, self.printMyData, self.ASPanel.btnPrintData)
        self.Bind(wx.EVT_MENU, self.OnOpen, openTool)
        self.Bind(wx.EVT_MENU, self.OnExit, exitIcon)

        self.Bind(wx.EVT_MENU, self.OnSave, self.menuSave)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.ASPanel.btnSaveAS)
        self.Bind(wx.EVT_MENU, self.OnSave, saveTool)

        self.Bind(wx.EVT_BUTTON, self.OnApplyParam, self.EditPanel.btnApplyParam)
        self.Bind(wx.EVT_BUTTON, self.OnApplyBase, self.EditPanel.btnApplyBase)
        self.Bind(wx.EVT_BUTTON, self.OnApplyOrient, self.EditPanel.btnApplyOrient)
        
        self.Bind(wx.EVT_BUTTON, self.EditPanel.OnHelp, self.EditPanel.btnHelp)
        self.Bind(wx.EVT_LISTBOX, self.OnEdit, self.ListPanel.listbox)

        self.Bind(wx.EVT_BUTTON, self.OnUp, self.ListPanel.btnUp)
        self.Bind(wx.EVT_BUTTON, self.OnDown, self.ListPanel.btnDown)
        self.Bind(wx.EVT_BUTTON, self.OnInvert, self.ListPanel.btnInvert)

    def printMyData(self, e):
        # for i in range(self.myData.__len__()):
        #     print self.myData[i].type, self.myData[i].id
        #     print 'Start point:'
        #     self.myData[i].startPoint.printPoint()
        #     if self.myData[i].type == 'ARC' or self.myData[i].type == 'CIRCLE':
        #         print 'Between point:'
        #         self.myData[i].betweenPoint.printPoint()
        #     print 'Finish point:'
        #     self.myData[i].finishPoint.printPoint()
        #     print '\n'
        #
        # for i in range(self.myPoints.__len__()):
        #     self.myPoints[i].printPoint()

        DataFrame(self, self.myData)


    def createDrawPanel(self):
        self.DrawPanel = DrawPanel(self, myData=[], myPoints=[], choice=-1)
        self.sizer.Add(self.DrawPanel, pos=(0, 0), flag=wx.TOP, border=0)
        self.sizer.FitInside(self)

    def createEditPanel(self):
        self.EditPanel = EditPanel(self)
        self.sizer.Add(self.EditPanel, pos=(1, 0), flag=wx.TOP, border=0)

    def createASPanel(self, programName):
        self.ASPanel = ASPanel(self, programName)
        self.sizer.Add(self.ASPanel, pos=(0, 1), flag=wx.TOP, border=0)

    def createListPanel(self):
        self.ListPanel = ListPanel(self)
        self.sizer.Add(self.ListPanel, (1, 1), flag=wx.TOP, border=0)

    def OnApplyParam(self, e):
        done = False
        if self.ListPanel.btnCheckAll.GetValue():
            for i in range(self.myData.__len__()):
                if self.EditPanel.checkHeight.GetValue():
                    self.myData[i].height = self.EditPanel.height.GetValue()
                if self.EditPanel.checkAccuracy.GetValue():
                    self.myData[i].accuracy = self.EditPanel.accuracy.GetValue()
                if self.EditPanel.checkAccel.GetValue():
                    self.myData[i].accel = self.EditPanel.accel.GetValue()
                if self.EditPanel.checkSpeed.GetValue():
                    self.myData[i].speed = self.EditPanel.speed.GetValue()
                    self.myData[i].speedUnit = self.EditPanel.speedUnit.GetSelection()
                self.myData[i].work = self.EditPanel.work.GetValue()
                done = True
        else:
            if self.choice != -1:
                if self.EditPanel.checkHeight.GetValue():
                    self.myData[self.choice].height = self.EditPanel.height.GetValue()
                if self.EditPanel.checkAccuracy.GetValue():
                    self.myData[self.choice].accuracy = self.EditPanel.accuracy.GetValue()
                if self.EditPanel.checkAccel.GetValue():
                    self.myData[self.choice].accel = self.EditPanel.accel.GetValue()
                if self.EditPanel.checkSpeed.GetValue():
                    self.myData[self.choice].speed = self.EditPanel.speed.GetValue()
                self.myData[self.choice].work = self.EditPanel.work.GetValue()
                self.myData[self.choice].speedUnit = self.EditPanel.speedUnit.GetSelection()

        if done:
            self.ASPanel.writeAS(self.myData, self.myPoints, self.EditPanel.returnBaseParameters(), self.programName)
        else:
            info = wx.MessageDialog(self, "Please choose a trajectory to edit parameters.", "Information", wx.OK)
            info.ShowModal()
            info.Destroy()

    def OnApplyBase(self, e):
        tempX = self.EditPanel.xBasePoint.GetValue()
        tempY = self.EditPanel.yBasePoint.GetValue()
        if self.overRangeP(self.DrawPanel.findMax()[0], self.DrawPanel.findMax()[1], tempX, tempY):
            dialog = wx.MessageDialog(self, "The point over working range!", "Warning", wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            self.EditPanel.baseX = tempX
            self.EditPanel.baseY = tempY
            self.EditPanel.baseZ = self.EditPanel.zBasePoint.GetValue()
            self.ASPanel.writeAS(self.myData, self.myPoints, self.EditPanel.returnBaseParameters(), self.programName)
            
    def OnApplyOrient(self, e):
        if self.ListPanel.btnCheckAll.GetValue():
            for i in range(self.myData.__len__()):
                temp = self.myData[i]
                o = self.EditPanel.xBaseAngle.GetValue()
                a = self.EditPanel.yBaseAngle.GetValue()
                t = self.EditPanel.zBaseAngle.GetValue()
                if i == 0:
                    self.setOrientation(temp.startPoint, o, a, t)
                self.setOrientation(temp.finishPoint, o, a, t)
                self.setOrientation(self.myPoints[temp.finishPoint.id-1], o, a, t)

                if temp.type == 'ARC':
                    self.setOrientation(temp.betweenPoint, o, a, t)

        elif self.choice != -1:
            temp = self.myData[self.choice]
            o = self.EditPanel.xBaseAngle.GetValue()
            a = self.EditPanel.yBaseAngle.GetValue()
            t = self.EditPanel.zBaseAngle.GetValue()

            if self.choice == 0:
                    self.setOrientation(temp.startPoint, o, a, t)
            self.setOrientation(temp.finishPoint, o, a, t)
            self.setOrientation(self.myPoints[temp.finishPoint.id-1], o, a, t)

            if temp.type == 'ARC':
                self.setOrientation(temp.betweenPoint, o, a, t)

        else:
            info = wx.MessageDialog(self, "Please choose a trajectory to edit parameters.", "Information", wx.OK)
            info.ShowModal()
            info.Destroy()
        self.ASPanel.writeAS(self.myData, self.myPoints, self.EditPanel.returnBaseParameters(), self.programName)

    def setOrientation(self, point, o, a, t):
        point.O = o
        point.A = a
        point.T = t

    def OnEdit(self, e):
        self.choice = self.ListPanel.listbox.GetSelection()
        self.DrawPanel.choice = self.choice
        self.EditPanel.height.SetValue(self.myData[self.choice].height)
        self.EditPanel.accuracy.SetValue(self.myData[self.choice].accuracy)
        self.EditPanel.accel.SetValue(self.myData[self.choice].accel)
        self.EditPanel.work.SetValue(self.myData[self.choice].work)
        self.EditPanel.speed.SetValue(self.myData[self.choice].speed)
        self.DrawPanel.Refresh()

    def OnAbout(self, e):
       dialog = wx.MessageDialog(self, "Created by Michal Kozminski", "ver 1.0", wx.OK)
       dialog.ShowModal()
       dialog.Destroy()

    def OnExit(self, e):
        if self.toolBar.GetToolEnabled(2):
            dlg = wx.MessageDialog(None, "Would you like to save the AS file?", 'A Message Box', wx.YES_NO |
                                       wx.ICON_QUESTION)
            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                self.OnSave(self)
            else:
                dlg.Destroy()
                self.Close(True)
        else:
            self.Close(True)

    def OnOpen(self, file):
        self.dirname = ''
        dialog = wx.FileDialog(self, "Choose a DXF file", self.dirname, "", "*.dxf*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            try:
                file = open(os.path.join(self.dirname, self.filename), 'r')
                dlg = wx.TextEntryDialog(None, "Write a name of a AS program.", defaultValue="",
                                     style=wx.TextEntryDialogStyle ^ wx.CANCEL)
                dlg.ShowModal()
                self.programName = dlg.GetValue()
                if self.programName != '':
                    if self.myData.__sizeof__() != 0:
                        self.myData = []
                        self.ListPanel.listbox.Clear()
                        self.myPoints = []

                    if self.readDXF(file):
                        self.createmyPoints()
                        self.DrawPanel.dane = self.myData
                        self.DrawPanel.points = self.myPoints
                        self.DrawPanel.Refresh()
                        self.ListPanel.addOnListbox(self.myData)
                        self.showFunctions()
                        self.ASPanel.writeAS(self.myData, self.myPoints, self.EditPanel.returnBaseParameters(),
                                         self.programName)
                    else:
                        dialog = wx.MessageDialog(self, "Trajectory over working range.",
                                                  "Warning", wx.OK)
                        dialog.ShowModal()
                        dialog.Destroy()
                file.close()
                dialog.Destroy()
            except IOError, e:
                dialog2 = wx.MessageDialog(self, "No such file or directory. Try again.", "Warning", wx.OK)
                dialog2.ShowModal()
                dialog2.Destroy()
        else:
            dialog2 = wx.MessageDialog(self, "No file chosen.", "Warning", wx.OK)
            dialog2.ShowModal()
            dialog2.Destroy()

    def OnRefresh(self, e):
        self.ASPanel.writeAS(self.myData, self.myPoints, self.EditPanel.returnBaseParameters(), self.programName)
        self.DrawPanel.Refresh()

    def OnSave(self, e):
        self.dirname = ''
        dialog = wx.DirDialog(self, "Choose a directory", self.dirname, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
            f = open(os.path.join(self.path, self.programName + '.as'), 'w')
            f.write(self.ASPanel.AS.GetValue())
            f.close()
            dialog2 = wx.MessageDialog(self, "File %s.as was sucessfully saved." % self.programName, "File was sucessfully saved.", wx.OK)
            dialog2.ShowModal()
            dialog2.Destroy()
        dialog.Destroy()

    def OnUp(self, e):
        myData = self.myData
        self.choice = self.ListPanel.listbox.GetSelection()
        if self.choice > 0:
            temp = myData.pop(self.choice)
            myData.insert(self.choice-1, temp)
            self.DrawPanel.dane = myData
            self.ListPanel.listbox.Clear()
            self.ListPanel.addOnListbox(self.myData)
            self.ListPanel.listbox.SetSelection(self.choice-1)

    def OnDown(self, e):
        myData = self.myData
        self.choice = self.ListPanel.listbox.GetSelection()
        if self.choice < (myData.__len__()-1):
            temp = myData.pop(self.choice)
            myData.insert(self.choice+1, temp)
            self.DrawPanel.dane = myData
            self.ListPanel.listbox.Clear()
            self.ListPanel.addOnListbox(self.myData)
            self.ListPanel.listbox.SetSelection(self.choice+1)

    def OnInvert(self, e):
        if self.choice != -1:
            temp = self.myData[self.choice]
            tempSP = temp.startPoint
            temp.startPoint = temp.finishPoint
            temp.finishPoint = tempSP

            if temp.type == "ARC":
                if not temp.inverted:
                    temp.inverted = True
                else:
                    temp.inverted = False
        self.OnRefresh(self)

    def readDXF(self, f):
        s = ' '
        i = 1
        while s != 'ENTITIES\n':
            s = f.readline()
        while s != 'ENDSEC\n':
            s = f.readline()
            if s == 'LINE\n':
                while s != 'AcDbEntity\n':
                    s = f.readline()
                f.readline()
                s = f.readline()
                if s != 'Border\n':
                    while s != ' 10\n':
                        s = f.readline()
                    s = f.readline()
                    xs = float(s)
                    f.readline()
                    s = f.readline()
                    ys = float(s)
                    f.readline()
                    f.readline()
                    f.readline()
                    s = f.readline()
                    xf = float(s)
                    f.readline()
                    s = f.readline()
                    yf = float(s)

                    sPoint = MyPoint(x=round(xs, 2), y=round(ys, 2))
                    fPoint = MyPoint(x=round(xf, 2), y=round(yf, 2))

                    if self.overRange(sPoint) or self.overRange(fPoint):
                        return False

                    line = MyLine(type="LINE", startPoint=sPoint, finishPoint=fPoint, id=i)
                    self.myData.append(line)
                    i += 1

            if s == 'ARC\n':
                while s != 'AcDbEntity\n':
                    s = f.readline()
                f.readline()
                s = f.readline()
                if s != 'Border\n':
                    while s != ' 10\n':
                        s = f.readline()
                    s = f.readline()
                    xc = float(s)
                    f.readline()
                    s = f.readline()
                    yc = float(s)
                    f.readline()
                    f.readline()
                    f.readline()
                    s = f.readline()
                    r = float(s)
                    f.readline()
                    f.readline()
                    f.readline()
                    s = f.readline()
                    alpha1 = float(s)
                    f.readline()
                    s = f.readline()
                    alpha2 = float(s)
                    alpha = (alpha1 + alpha2)/2
                    if alpha1 > alpha2:
                        alpha -= 180

                    xb = xc+(r*math.cos(math.radians(alpha)))
                    yb = yc+(r*math.sin(math.radians(alpha)))

                    x1 = xc+(r*math.cos(math.radians(alpha1)))
                    y1 = yc+(r*math.sin(math.radians(alpha1)))
                    x2 = xc+(r*math.cos(math.radians(alpha2)))
                    y2 = yc+(r*math.sin(math.radians(alpha2)))

                    sPoint = MyPoint(x=round(x1, 2), y=round(y1, 2))
                    fPoint = MyPoint(x=round(x2, 2), y=round(y2, 2))
                    cPoint = MyPoint(x=round(xc, 2), y=round(yc, 2))
                    bPoint = MyPoint(x=round(xb, 2), y=round(yb, 2))

                    if self.overRange(sPoint) or self.overRange(fPoint) or self.overRange(bPoint):
                        return False

                    arc = MyArc(type="ARC", startPoint=sPoint, finishPoint=fPoint, centerPoint=cPoint, betweenPoint=bPoint,
                                id=i, alpha1=math.radians(alpha1), alpha2=math.radians(alpha2))
                    self.myData.append(arc)
                    i += 1

            if s == 'CIRCLE\n':
                while s != 'AcDbEntity\n':
                    s = f.readline()
                f.readline()
                s = f.readline()
                if s != 'Border\n':
                    while s != ' 10\n':
                        s = f.readline()
                    s = f.readline()

                    xc = float(s)
                    f.readline()
                    s = f.readline()
                    yc = float(s)
                    f.readline()
                    f.readline()
                    f.readline()
                    s = f.readline()
                    r = float(s)

                    cPoint = MyPoint(round(xc, 2), round(yc, 2))
                    sPoint1 = MyPoint(round(xc-r, 2), round(yc, 2))
                    bPoint1 = MyPoint(round(xc, 2), round(yc+r, 2))
                    fPoint1 = MyPoint(round(xc+r, 2), round(yc, 2))
                    bPoint2 = MyPoint(round(xc, 2), round(yc-r, 2))
                    sPoint2 = fPoint1
                    fPoint2 = sPoint1

                    if self.overRange(sPoint1) or self.overRange(fPoint1) or self.overRange(bPoint1) or self.overRange(bPoint2):
                        return False

                    # centerPoint domyslnie, alpha1 i alpha2
                    arc1 = MyArc(type="ARC", startPoint=sPoint1, finishPoint=fPoint1, betweenPoint=bPoint1,
                                 centerPoint=cPoint, id=i)
                    self.myData.append(arc1)
                    i += 1
                    arc2 = MyArc(type="ARC", startPoint=sPoint2, finishPoint=fPoint2, betweenPoint=bPoint2,
                                 centerPoint=cPoint, id=i)
                    self.myData.append(arc2)
                    i += 1

            if s == 'LWPOLYLINE\n':
                tempPoint = MyPoint(x=0, y=0)
                while s != '  0\n':
                    s = f.readline()
                    if s == ' 10\n':
                        if tempPoint.id != '0':
                            sPoint = tempPoint
                        else:
                            s = f.readline()
                            xs = float(s)
                            f.readline()
                            s = f.readline()
                            ys = float(s)
                            sPoint = MyPoint(x=round(xs, 2), y=round(ys, 2))
                            f.readline()

                        s = f.readline()
                        xf = float(s)
                        f.readline()
                        s = f.readline()
                        yf = float(s)

                        fPoint = MyPoint(x=round(xf, 2), y=round(yf, 2))
                        tempPoint = fPoint

                        if self.overRange(sPoint) or self.overRange(fPoint):
                            return False

                        line = MyLine(type="LINE", startPoint=sPoint, finishPoint=fPoint, id=i)
                        self.myData.append(line)
                        i += 1

        if i == 1:
            return False
        else:
            return True

    def createmyPoints(self):
        self.myPoints.append(self.myData[0].startPoint)
        # self.myData[0].startPoint.strID = 'p' + repr(1)
        self.myData[0].startPoint.id = 1

        if self.myData[0].type == 'ARC':
            self.myPoints.append(self.myData[0].betweenPoint)
            # self.myData[0].betweenPoint.strID = 'p' + repr(2)
            self.myData[0].betweenPoint.id = 2

        self.myPoints.append(self.myData[0].finishPoint)
        # self.myData[0].finishPoint.strID = 'p' + repr(3)
        self.myData[0].finishPoint.id = 2

        for i in range(self.myData.__len__()):
            self.compare(self.myData[i].startPoint)
            if self.myData[i].type == "ARC":
                self.compare(self.myData[i].betweenPoint)
            self.compare(self.myData[i].finishPoint)

    def showFunctions(self):
        self.ASPanel.btnSaveAS.Enable()
        self.ASPanel.btnRefresh.Enable()
        self.ASPanel.btnPrintData.Enable()
        self.EditPanel.btnApplyParam.Enable()
        self.EditPanel.btnApplyBase.Enable()
        self.EditPanel.btnApplyOrient.Enable()

        self.menuSave.Enable()
        self.toolBar.EnableTool(2, True)
        self.EditPanel.btnHelp.Enable()
        # self.EditPanel.btnOrientOpen.Enable()
        # self.EditPanel.btnBaseOpen.Enable()

    def compare(self, point):
        found = False
        for j in range(self.myPoints.__len__()):
            if (point.x == self.myPoints[j].x) and (point.y == self.myPoints[j].y):
                found = True
                # temp = 'p' + repr(j+1)
                # point.strID = temp
                point.id = j+1
                break
            else:
                k = j+1
                pass
        if not found:
            self.myPoints.append(point)
            # temp = 'p' + repr(k+1)
            # point.strID = temp
            point.id = k+1

    def overRange(self, point):
        answer = False
        r = math.sqrt(math.pow(point.x + self.EditPanel.baseX, 2) + math.pow(point.y + self.EditPanel.baseX, 2))
        if r > 2100:
            answer = True
        return answer

    def overRangeP(self, x, y, xBase, yBase):
        answer = False
        r = math.sqrt(math.pow(x + xBase, 2) + math.pow(y + yBase, 2))
        if r > 2100:
            answer = True
        return answer


class HelpFrame(wx.Frame):
    def __init__(self, parent):
        style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        wx.Frame.__init__(self, parent, title="Help", size=(380, 370), style=style)
        panel = wx.Panel(self, -1, size=(380, 370), style=wx.BORDER_SUNKEN)
        wx.StaticBitmap(panel, -1, wx.Bitmap('oat.bmp'), pos=(0, 0), name='OAT')

        self.Show()


class DrawPanel(wx.Panel):
    def __init__(self, parent, myData, myPoints, choice):
        wx.Panel.__init__(self, parent, size=(650, 400), style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour('#4f5049')
        self.dane = myData
        self.points = myPoints
        self.choice = choice
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e):
        length = self.dane.__len__()
        self.dc = wx.PaintDC(self)
        self.dc.Clear()
        self.dc.SetTextForeground((255, 255, 255))
        self.dc.SetPen(wx.Pen(wx.WHITE, 1))
        s = self.autoScale()
        corX = self.findMin()[0] - 60*s
        corY = self.findMin()[1] - 60*s

        if s != 0:
            self.dc.SetPen(wx.Pen(wx.YELLOW, 1, wx.DOT))
            self.dc.DrawArc((-932.74 - corX)/s, (-1708.79 - corY)/s, (963.11 - corX)/s, (-1689.62 - corY)/s, (-1.51 - corX)/s, (-47.97 - corY)/s)
            self.dc.DrawArc((963.11 - corX)/s, (-1689.62 - corY)/s, (493.18 - corX)/s, (-1768.99 - corY)/s, (613.45 - corX)/s, (-1050.19 - corY)/s)
            self.dc.DrawArc((-498.38 - corX)/s, (-1782.37 - corY)/s, (-932.74 - corX)/s, (-1708.79 - corY)/s, (-602.25 - corX)/s, (-1076.69 - corY)/s)
            self.dc.DrawArc((500.0 - corX)/s, -corY/s, (-500.0 - corX)/s, -corY/s, -corX/s, - corY/s)
            self.dc.DrawArc((-500.0 - corX)/s, -corY/s, (500.0 - corX)/s, -corY/s, -corX/s, - corY/s)
            self.dc.DrawLine(-corX/s, (-500.0 - corY)/s, (493.18 - corX)/s, (-1768.99 - corY)/s)
            self.dc.DrawLine(-corX/s, (-500.0 - corY)/s, (-498.38 - corX)/s, (-1782.37 - corY)/s)

            self.dc.DrawLine((- corX)/s, (- corY)/s, (150- corX)/s, (- corY)/s)
            self.dc.DrawLine((- corX)/s, (- corY)/s, (-corX)/s, (150- corY)/s)
            self.dc.DrawText("x", (160 - corX)/s, (- corY)/s)
            self.dc.DrawText("y", (-corX)/s, (160-corY)/s)
            self.dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))

            self.dc.DrawLine((- corX)/s, (- corY)/s, (150- corX)/s, (- corY)/s)
            self.dc.DrawLine((- corX)/s, (- corY)/s, (-corX)/s, (150- corY)/s)


            for i in range(self.points.__len__()):
                txt = 'p' + repr(i+1)
                self.dc.DrawText(txt, (self.points[i].x - corX)/s, (self.points[i].y - corY)/s)

            for i in range(length):
                temp = self.dane[i]
                spx = temp.startPoint.x
                spy = temp.startPoint.y
                fpx = temp.finishPoint.x
                fpy = temp.finishPoint.y

                if self.choice == i:
                    self.dc.SetPen(wx.Pen(wx.RED, 1))

                if temp.type == "LINE":
                    self.dc.DrawLine((spx - corX)/s, (spy - corY)/s, (fpx - corX)/s, (fpy - corY)/s)

                    # print 'points', (spx - corX)/s, (spy - corY)/s, (fpx - corX)/s, (fpy - corY)/s
                if temp.type == 'ARC':
                    cpx = temp.centerPoint.x
                    cpy = temp.centerPoint.y

                    # print 'self.dc.DrawArc((',fpx,' - corX)/s, (',fpy, '- corY)/s, (',spx, '- corX)/s, (',spy,' - corY)/s)', cpx, '- corX)/s, (',cpy,' - corY)/s)'
                    if not temp.inverted:
                        self.dc.DrawArc((fpx - corX)/s, (fpy - corY)/s, (spx - corX)/s, (spy - corY)/s, (cpx - corX)/s,
                                                (cpy - corY)/s)
                    else:
                        self.dc.DrawArc((spx - corX)/s, (spy - corY)/s, (fpx - corX)/s, (fpy - corY)/s, (cpx - corX)/s,
                                                (cpy - corY)/s)
                self.dc.SetPen(wx.Pen(wx.WHITE, 1))

            for i in range(length):
                self.drawArrows(self.dane[i], corX, corY, s)

    def findMax(self):
        maxX = 0
        maxY = 0
        for i in range(len(self.dane)):
            temp = self.dane[i]
            if temp.startPoint.x > maxX:
                maxX = temp.startPoint.x
            if temp.finishPoint.x > maxX:
                maxX = temp.finishPoint.x
            if temp.startPoint.y > maxY:
                maxY = temp.startPoint.y
            if temp.finishPoint.y > maxY:
                maxY = temp.finishPoint.y
            if temp.type == 'ARC':
                if temp.betweenPoint.x > maxX:
                    maxX = temp.betweenPoint.x
                if temp.betweenPoint.y > maxY:
                    maxY = temp.betweenPoint.y
        max = [maxX, maxY]
        return max

    def findMin(self):
        minX = self.findMax()[0]
        minY = self.findMax()[1]

        for i in range(self.dane.__len__()):
            temp = self.dane[i]
            if temp.startPoint.x < minX:
                minX = temp.startPoint.x
            if temp.finishPoint.x < minX:
                minX = temp.finishPoint.x
            if temp.startPoint.y < minY:
                minY = temp.startPoint.y
            if temp.finishPoint.y < minY:
                minY = temp.finishPoint.y
            if temp.type == 'ARC':
                if temp.betweenPoint.x < minX:
                    minX = temp.betweenPoint.x
                if temp.betweenPoint.y < minY:
                    minY = temp.betweenPoint.y

        min = [minX, minY]
        return min

    def findDifference(self):
        differenceX = self.findMax()[0] - self.findMin()[0]
        differenceY = self.findMax()[1] - self.findMin()[1]
        max = [differenceX, differenceY]
        return max

    def autoScale(self):
        [maxX, maxY] = self.findDifference()
        max = maxX
        if maxX < 11*maxY/7:
            max = 11*maxY/7
        scale = round(0.002*max, 2)  #0,0025
        return scale

    def drawArrows(self, trajectory, corX, corY, s):
        r = 10*s
        const1 = math.radians(135)
        const2 = math.radians(225)
        xDif = trajectory.startPoint.x - trajectory.finishPoint.x
        yDif = trajectory.startPoint.y - trajectory.finishPoint.y

        if trajectory.type == 'LINE':
            x = (trajectory.startPoint.x + trajectory.finishPoint.x)/2
            y = (trajectory.startPoint.y + trajectory.finishPoint.y)/2
        else:
            x = trajectory.betweenPoint.x
            y = trajectory.betweenPoint.y

        if xDif != 0 and yDif != 0:
            if trajectory.startPoint.x < trajectory.finishPoint.x:
                    phase = 0
            else:
                    phase = math.pi

            angle = math.atan(yDif/xDif)
            xArr1 = x+r*math.cos(const1-angle+phase)
            yArr1 = y-r*math.sin(const1-angle+phase)
            xArr2 = x+r*math.cos(const2-angle+phase)
            yArr2 = y-r*math.sin(const2-angle+phase)

        else:
            # vertical
            if not xDif:
                if trajectory.finishPoint.y > trajectory.startPoint.y:
                        angle = math.pi/2
                else:
                        angle = -math.pi/2
            # horizontal
            elif not yDif:
                if trajectory.finishPoint.x > trajectory.startPoint.x:
                        angle = 0
                else:
                        angle = math.pi

            xArr1 = x+r*math.cos(const1+angle)
            yArr1 = y+r*math.cos(const1+angle)
            xArr2 = x+r*math.cos(const2+angle)
            yArr2 = y-r*math.cos(const2+angle)

        self.dc.DrawLine((x-corX)/s, (y-corY)/s, (xArr1-corX)/s, (yArr1-corY)/s)
        self.dc.DrawLine((x-corX)/s, (y-corY)/s, (xArr2-corX)/s, (yArr2-corY)/s)

    def getScale(self):
        return self.slider.GetValue()


class EditPanel(wx.Panel):
    def __init__(self, parent):
        self.baseX = 0
        self.baseY = 0
        self.baseZ = 0

        wx.Panel.__init__(self, parent, size=(650, 250), style=wx.BORDER_SUNKEN)

        mp = wx.StaticBox(self, label="Movement parameters", size=(205, 230), pos=(5, 5))
        bp = wx.StaticBox(self, label="Base point", size=(140, 230), pos=(225, 5))
        eo = wx.StaticBox(self, label='Orientation', size=(140, 230), pos=(380, 5))
        pt = wx.StaticBox(self, label="Process type", size=(110, 140), pos=(530, 5))
        wx.StaticBoxSizer(pt, wx.VERTICAL)
        wx.StaticBoxSizer(mp, wx.VERTICAL)
        wx.StaticBoxSizer(bp, wx.VERTICAL)

        self.work = wx.CheckBox(self, -1, 'Work ON', pos=(10, 205))
        self.checkHeight = wx.CheckBox(self, -1, "Height:", pos=(10, 45))
        self.checkAccuracy = wx.CheckBox(self, -1, "Accuracy:", pos=(10, 85))
        self.checkSpeed = wx.CheckBox(self, -1, "Speed:", pos=(10, 125))
        self.checkAccel = wx.CheckBox(self, -1, "Accel.:", pos=(10, 165))
        wx.StaticText(self, -1, "mm", pos=(140, 45))
        wx.StaticText(self, -1, "mm", pos=(140, 85))
        wx.StaticText(self, -1, "%", pos=(140, 165))
        wx.StaticText(self, -1, "X:", pos=(240, 50))
        wx.StaticText(self, -1, "Y:", pos=(240, 90))
        wx.StaticText(self, -1, "Z:", pos=(240, 130))
        wx.StaticText(self, -1, "O:", pos=(395, 50))
        wx.StaticText(self, -1, "A:", pos=(395, 90))
        wx.StaticText(self, -1, "T:", pos=(395, 130))

        units = ["%", "mm/s", 'mm/min', 's']
        self.speedUnit = wx.Choice(self, -1, size=(60, 20), pos=(140, 125), choices=units)
        self.speedUnit.SetSelection(0)

        self.processType = wx.ListBox(self, -1, style=wx.LB_ALWAYS_SB and wx.LB_SINGLE, size=(80, 80),
                                  pos=(550, 45))
        self.processType.Append("Gripping")
        self.processType.Append("Welding")

        self.xBasePoint = wx.SpinCtrl(self, 1, pos=(260, 45), size=(60, 20), min=-1000, max=1000)
        self.yBasePoint = wx.SpinCtrl(self, 1, pos=(260, 85), size=(60, 20), min=-1000, max=1000)
        self.zBasePoint = wx.SpinCtrl(self, 1, pos=(260, 125), size=(60, 20), min=-1000, max=1000)
        self.xBaseAngle = wx.SpinCtrl(self, 1, pos=(415, 45), size=(60, 20), min=-1000, max=1000)
        self.yBaseAngle = wx.SpinCtrl(self, 1, pos=(415, 85), size=(60, 20), min=-1000, max=1000)
        self.zBaseAngle = wx.SpinCtrl(self, 1, pos=(415, 125), size=(60, 20), min=-1000, max=1000)
        self.height = wx.SpinCtrl(self, 1, pos=(80, 45), size=(50, 20), min=0, max=1000)
        self.accuracy = wx.SpinCtrl(self, -1, pos=(80, 85), size=(50, 20), min=2, max=30)
        self.speed = wx.SpinCtrl(self, -1, pos=(80, 125), size=(50, 20), min=10, max=100)
        self.accel = wx.SpinCtrlDouble(self, 1, pos=(80, 165), size=(50, 20), min=0.1, max=100)
        self.accel.SetValue(0)

        self.btnApplyParam = wx.Button(self, label="Apply", pos=(140, 190), size=(50, 30))
        self.btnApplyBase = wx.Button(self, label="Apply", pos=(270, 190), size=(50, 30))
        self.btnApplyOrient = wx.Button(self, label="Apply", pos=(400, 190), size=(50, 30))

        bmpHelp = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_BUTTON, (16, 16))
        self.btnHelp = wx.BitmapButton(self, -1, bmpHelp, pos=(470, 190), size=(30, 30))

        # bmpOpen = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_BUTTON, (16, 16))
        # self.btnBaseOpen = wx.BitmapButton(self, -1, bmpOpen, pos=(300, 190), size=(50, 30))
        # self.btnOrientOpen = wx.BitmapButton(self, -1, bmpOpen, pos=(460, 190), size=(50, 30))

        self.addLogos()
        self.hideFunctions()

    def hideFunctions(self):
        self.btnApplyParam.Disable()
        self.btnApplyBase.Disable()
        self.btnApplyOrient.Disable()
        self.btnHelp.Disable()
        # self.btnBaseOpen.Disable()
        # self.btnOrientOpen.Disable()

    def addLogos(self):
        wx.StaticBitmap(self, -1, wx.Bitmap('pwr.bmp'), pos=(600, 190), name='Wroclaw University of Technology')
        wx.StaticBitmap(self, -1, wx.Bitmap('astor.bmp'), pos=(550, 190), name='ASTOR Sp. z o.o.')

    def returnBaseParameters(self):
        return [self.baseX, self.baseY, self.baseZ]

    def OnHelp(self, e):
        HelpFrame(None)
        pass


class ASPanel(wx.Panel):
    def __init__(self, parent, programName):
        wx.Panel.__init__(self, parent, size=(310, 400), style=wx.BORDER_SUNKEN)
        wx.StaticBox(self, label="AS Code", size=(280, 340), pos=(5, 5))
        
        self.programName = programName
        self.AS = wx.TextCtrl(self, -1, pos=(15, 30), size=(250, 300), style=wx.TE_MULTILINE)

        self.btnRefresh = wx.Button(self, label="Refresh", pos=(100, 350), size=(50, 30))
        self.btnSaveAS = wx.Button(self, label="Save", pos=(20, 350), size=(50, 30))
        self.btnPrintData = wx.Button(self, label="Print Data", pos=(180, 350), size=(80, 30))

        self.AS.AlwaysShowScrollbars(-1)
        self.btnSaveAS.Disable()
        self.btnRefresh.Disable()
        self.btnPrintData.Disable()

    def alwaysSpeed(self, myData):
        speed = myData[0].speed
        theSame = True
        for i in range(1, myData.__len__()):
            if myData[i].speed != speed:
                theSame = False
        return theSame

    def alwaysAccuracy(self, myData):
        accur = myData[0].accuracy
        theSame = True
        for i in range(1, myData.__len__()):
            if myData[i].accuracy != accur:
                theSame = False
        return theSame

    def alwaysAccel(self, myData):
        accur = myData[0].accel
        theSame = True
        for i in range(1, myData.__len__()):
            if myData[i].accel != accur:
                theSame = False
        return theSame

    def whichUnit(self, input):
        if input == 0:
            return ""
        elif input == 1:
            return "mm/s"
        elif input == 2:
            return 'mm/min'
        elif input == 3:
            return 's'
        else:
            pass

    def writeAS(self, myData, myPoints, baseParameters, programName):
        #wyczyszczenie panelu
        self.AS.Clear()
        #wpisanie nazwy programu
        self.AS.write('.PROGRAM %s() #0\n BASE NULL\n' % programName)

        #sprawdzenie czy wszystkie trajektorie mają określone te same prędkości - wartość domyślna 10 ALWAYS
        if self.alwaysSpeed(myData):
            self.AS.write('  SPEED %d %s ALWAYS\n' % (myData[0].speed, self.whichUnit(myData[0].speedUnit)))
        #sprawdzenie czy wszystkie trajektorie mają określoną dokładność osiągania pozycji - wartość domyślna nieokreślona
        if self.alwaysAccuracy(myData) and myData[0].accuracy != 0:
            self.AS.write('  ACCURACY %d ALWAYS\n' % myData[0].accuracy)
        if self.alwaysAccel(myData) and myData[0].accel != 0:
            if myData[0].accel > 0:
                self.AS.write('  ACCEL %d ALWAYS\n' % myData[0].accel)
            else:
                self.AS.write('  DECEL %d ALWAYS\n' % myData[0].accel)

        #pętla - wszystkie geometrie
        for i in range(myData.__len__()):
            # sprawdzenie czy sPoint aktualnej geometrii jest taki sam jak fPoint poprzedniej - jeśli nie to LMOVE
            if (i > 0) and myData[i].startPoint.id != myData[i-1].finishPoint.id:
                    self.AS.write("  LMOVE p%s\n" % myData[i].startPoint.id)
            # w wypadku pierwszej geometrii zawsze dojście do jej sPoint
            elif i == 0:
                self.AS.write("  LMOVE p%s\n" % myData[i].startPoint.id)

            #jeśli prędkości nie są te same w każdej części trajektorii i nie ma zmiany wysokości
            if not self.alwaysSpeed(myData) and not myData[i].height:
                self.AS.write('  SPEED %d %s\n' % (myData[i].speed, self.whichUnit(myData[i].speedUnit)))

            #jeśli dokładność nie jest taka sama w każdej części trajektorii i nie ma zmiany wysokości
            if not self.alwaysAccuracy(myData) and not myData[i].height and myData[i].accuracy != 0:
                self.AS.write('  ACCURACY %d\n' % myData[i].accuracy)

            if not self.alwaysAccel(myData) and not myData[i].height and myData[i].accel != 0:
                if myData[i].accel > 0:
                    self.AS.write('  ACCEL %d\n' % myData[i].accel)
                else:
                    self.AS.write('  DECEL %d\n' % myData[i].accel)
            #komentuj
            if myData[i].work and (i == 0 or not myData[i-1].work or
                        (myData[i-1].work and myData[i].startPoint.id != myData[i-1].finishPoint.id)):
                # jesli na aktualnej trajektorii ma byc wykonana praca i wczesniej nie była wykonana
                self.AS.write("  CLOSEI\n")

            if myData[i].height != 0:
                # zmiana paramterów - podwyższenie 1st point o height w osi Z
                if i == 0 or (i > 0 and (myData[i].height != myData[i-1].height or myData[i].startPoint.id != myData[i-1].finishPoint.id)):
                    self.AS.write("  POINT p%s = SHIFT(%s BY 0,0,%d)\n" % (myData[i].startPoint.id,
                                                    myData[i].startPoint.id, myData[i].height))
                    self.AS.write("  LMOVE p%s\n" % myData[i].startPoint.id)

                #dojazd do punktu podwyższonego
                if not self.alwaysSpeed(myData) and myData[i].height != 0:
                    self.AS.write('  SPEED %d %s\n' % (myData[i].speed, self.whichUnit(myData[i].speedUnit)))
                if not self.alwaysAccuracy(myData) and myData[i].height != 0:
                    self.AS.write('  ACCURACY %d\n' % myData[i].speed)
                if not self.alwaysAccel(myData) and myData[i].height != 0:
                    if myData[i].accel > 0:
                        self.AS.write('  ACCEL %d\n' % myData[i].accel)
                    else:
                        self.AS.write('  DECEL %d\n' % myData[i].accel)

                # zmiana paramterów - obniżenie 1st point o height w osi Z
                self.AS.write("  POINT p%s = SHIFT(p%s BY 0,0,-%d)\n" % (myData[i].startPoint.id,
                                                    myData[i].startPoint.id, myData[i].height))

                #zmiana 2nd point - podwyzszenie o height
                if myData[i].type == "ARC":
                    self.AS.write("  POINT p%s = SHIFT(p%s BY 0,0,%d)\n" % (myData[i].betweenPoint.id,
                                                    myData[i].betweenPoint.id, myData[i].height))
                self.AS.write("  POINT p%s = SHIFT(p%s BY 0,0,%d)\n" % (myData[i].finishPoint.id,
                                                    myData[i].finishPoint.id, myData[i].height))

                # przejscie przez punkty trajektorii
                if myData[i].type == 'LINE':
                    self.AS.write("  LMOVE p%s\n" % myData[i].finishPoint.id)
                if myData[i].type == "ARC":
                    self.AS.write("  C1MOVE p%s\n" % myData[i].betweenPoint.id)
                    self.AS.write("  C2MOVE p%s\n" % myData[i].finishPoint.id)

                #zmiana 2nd point - obniżenie o height
                if i == myData.__len__()-1 or(i < myData.__len__()-1 and (myData[i].height != myData[i+1].height or myData[i].finishPoint.id != myData[i+1].startPoint.id)):
                    if myData[i].type == "ARC":
                        self.AS.write("  POINT p%s = SHIFT(p%s BY 0,0,-%d)\n" % (myData[i].betweenPoint.id,
                                                            myData[i].betweenPoint.id, myData[i].height))
                    self.AS.write("  POINT p%s = SHIFT(p%s BY 0,0,-%d)\n" % (myData[i].finishPoint.id,
                                                            myData[i].finishPoint.id, myData[i].height))

            if myData[i].type == "ARC" and myData[i].height == 0:
                # if not myData[i].work:
                self.AS.write("  C1MOVE p%s\n" % myData[i].betweenPoint.id)
                self.AS.write("  C2MOVE p%s\n" % myData[i].finishPoint.id)

            if myData[i].height == 0 or (i == myData.__len__()-1 or(i < myData.__len__()-1 and (myData[i].height != myData[i+1].height or myData[i].finishPoint.id != myData[i+1].startPoint.id))):
                    self.AS.write("  LMOVE p%s\n" % myData[i].finishPoint.id)

            # zamknięcie chwytaka gdy aktualnie pracuje i gdy jest ostatnią trajektorią lub w kolejnej nie ma pracy
            if myData[i].work and (i == myData.__len__()-1 or not myData[i+1].work or
                        (myData[i+1].work and myData[i].finishPoint.id != myData[i+1].startPoint.id)):
                self.AS.write("  OPENI\n")

        self.AS.write(".END\n.TRANS\n")

        for i in range(myPoints.__len__()):
            bP = baseParameters
            temp = myPoints[i]
            self.AS.write('  p%d %.1f %.1f %d %d %d %d\n' % (i+1, temp.x+bP[0], temp.y+bP[1], bP[2], temp.O, temp.A, temp.T))
        self.AS.write(".END")


class MyGrid(wx.grid.Grid):
    def __init__(self, DataFrame, myData):
        wx.grid.Grid.__init__(self, DataFrame, -1)
        rows = myData.__len__()
        self.CreateGrid(rows, 7)
        self.SetColLabelValue(0, "Type")
        self.SetColLabelValue(1, "Start point")
        self.SetColLabelValue(3, "Between point")
        self.SetColLabelValue(2, "Finish point")
        self.SetColLabelValue(4, "Speed")
        self.SetColLabelValue(5, "Accuracy")
        self.SetColLabelValue(6, "Acceleration")
        self.SetColSize(3, 100)

        for i in range(rows):
            self.SetRowSize(i, 50)
            self.SetCellValue(i, 0, myData[i].type)
            str = "ID: " + repr(myData[i].startPoint.id) + "\nx: " + repr(myData[i].startPoint.x) + "\ny: " + repr(myData[i].startPoint.y)
            self.SetCellValue(i, 1, str)
            str = "ID: " + repr(myData[i].finishPoint.id) + "\nx: " + repr(myData[i].finishPoint.x) + "\ny: " + repr(myData[i].finishPoint.y)
            self.SetCellValue(i, 2, str)
            if myData[i].type == "ARC":
                str = "ID: " + repr(myData[i].betweenPoint.id) + "\nx: " + repr(myData[i].betweenPoint.x) + "\ny: " + repr(myData[i].betweenPoint.y)
                self.SetCellValue(i, 3, str)
            str = repr(myData[i].speed) + " " + self.whichUnit(myData[i].speedUnit)
            self.SetCellValue(i, 4, str)
            if myData[i].accuracy == 0:
                self.SetCellValue(i, 5, "Undefined")
            else:
                str = repr(myData[i].accuracy) + " %"
                self.SetCellValue(i, 5, str)
            if myData[i].accel == 0:
                self.SetCellValue(i, 6, "Undefined")
            else:
                str = repr(myData[i].accel) + " %"
                self.SetCellValue(i, 6, str)

    def whichUnit(self, input):
        if input == 0:
            return "%"
        elif input == 1:
            return "mm/s"
        elif input == 2:
            return 'mm/min'
        elif input == 3:
            return 's'
        else:
            pass


class DataFrame(wx.Frame):
    def __init__(self, parent, myData):
        wx.Frame.__init__(self, parent, title="Data matrix", size=(720, 400))
        grid = MyGrid(self, myData)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(grid)
        # self.SetSizer(sizer)
        self.Show(True)


class ListPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(310, 250), style=wx.BORDER_SUNKEN)

        list = wx.StaticBox(self, label="Trajectory elements", size=(295, 235), pos=(5, 5))
        wx.StaticBoxSizer(list, wx.VERTICAL)
        self.listbox = wx.ListBox(self, -1, style=wx.LB_ALWAYS_SB and wx.LB_SINGLE, size=(190, 160),
                                  pos=(20, 30))

        bmpUp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        bmpDown = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        bmpInvert = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, (16, 16))

        self.btnUp = wx.BitmapButton(self, -1, bmpUp, pos=(220, 90), size=(20, 20))
        self.btnDown = wx.BitmapButton(self, -1, bmpDown, pos=(220, 120), size=(20, 20))
        self.btnInvert = wx.BitmapButton(self, -1, bmpInvert, pos=(250, 105), size=(20, 20))
        self.btnCheckAll = wx.CheckBox(self, -1, "Choose all", pos=(20, 200), size=(100, 20))
        self.btnMultiple = wx.CheckBox(self, -1, "Multiple choice", pos=(150, 200), size=(100, 20))

    def addOnListbox(self, myData):
        for i in range(myData.__len__()):
            temp = myData[i]
            self.listbox.Append("%s %d" % (temp.type, temp.id))


class MyPoint:
    def __init__(self, x, y, id=-1):
        self.x = x
        self.y = y
        self.O = 0
        self.A = 0
        self.T = 0
        self.id = id

    def printPoint(self):
        print self.id, "x: ", self.x, " y: ", self.y, "o: ", self.O, "a: ", self.A, "t= ", self.T


class MyLine(MyPoint):
    def __init__(self, type='', startPoint=0, finishPoint=0, height=0, work=False, speed=10,
                 speedUnit=0, accel=0, accuracy=0, chosen=False, id=0):
        self.startPoint = startPoint
        self.finishPoint = finishPoint
        self.type = type
        self.height = height
        self.work = work
        self.speed = speed
        self.speedUnit = speedUnit
        self.accel = accel
        self.accuracy = accuracy
        self.chosen = chosen
        self.id = id


class MyArc(MyLine):
    def __init__(self, type='', startPoint=0, finishPoint=0, height=0, work=False, speed=10,
                 speedUnit=0, accel=0, accuracy=0, chosen=False, id=0, centerPoint=0, radius=0, betweenPoint=0, alpha1=0,
                 alpha2=0, inverted=False):
        MyLine.__init__(self, type, startPoint, finishPoint, height, work, speed, speedUnit, accel, accuracy,
                        chosen, id)

        self.centerPoint = centerPoint
        self.betweenPoint = betweenPoint
        self.radius = radius
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.inverted = inverted

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None)
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()