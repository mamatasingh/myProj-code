# Imports
import os
import shutil
import fileinput
import subprocess
import filecmp
import sys
import re
import subprocess
import subprocess, platform
import time
import tkinter as tk
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
import webbrowser
import difflib
import socket
import zipfile
from zipfile import ZipFile
from difflib import ndiff
from tkinter import *
#from socket import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from xml.dom import minidom
from xml.dom.minidom import Node
from tkinter.ttk import Separator, Style

# Global Declaration
szTkExecution=Tk()
szTkExecution.geometry("550x300+60+60")
szTkExecution.title("CFD Automation Tool")
dialog_window = None
szDialogEindowForRunTestcase = None
szPortNumber= ""
txtPortNumber= ""
txtEntryCfdExePath= ""
szEnteredTestCaseName= ""
szTargetFolderPath = ""
RootLibraryFolderPath = ""
szCopiedModelFolder= ""
CfdExePath = ""
szBaseLineFolder = ""
szModelFolder = ""
szPythonFilePath= ""
txtEntryRootFolderPath= ""
lstBoxListAllClients= ""
Settingsicon=PhotoImage(file="Settings.png")
# XML elements declaration
ParentNode = ET.Element("ParentNode")
ChildNode = ET.SubElement(ParentNode, "ChildNode")
ResultNode= ET.SubElement(ChildNode, "ResultNode")
# Creating the Frame for CFD automation tool application
szMainFrame = Frame()
szMainFrame.grid()

# Function to select Root folder path
def SelectMainPath():
    global RootLibraryFolderPath
    RootLibraryFolderPath=filedialog.askdirectory(title="Select Root Folder Path")
    txtEntryRootFolderPath.insert(0,RootLibraryFolderPath)
    txtEntryRootFolderPath.config(state=DISABLED)
# Function to select CFD exe path
def SelectCfdExePath():
    global CfdExePath
    CfdExePath=filedialog.askopenfilename(title="SelectCFDSolverPath",filetypes = (("python files","*.exe"),("all files","*.*")))
    if len(CfdExePath)==0:
        messagebox.showerror("Error","You have to select the CFD solver path")
    else:
        txtEntryCfdExePath.insert(0,CfdExePath)
        txtEntryCfdExePath.config(state=DISABLED)
def EnterPortNumber():
    global szPortNumber
    szPortNumber=txtPortNumber.get()
    if len(szPortNumber)==0:
        szPortNumber=9999
        messagebox.showinfo("Info","Default value '9999' is the port number")
        return
    else:
        szPortNumber=szPortNumber
def CloseSettingsWindow():
    global RootLibraryFolderPath
    if len(RootLibraryFolderPath)== 0:
        RootLibraryFolderPath = os.getcwd()
        dialog_window.destroy()
    else:
        dialog_window.destroy()
        
# Creating Settings dialog dialog
def CreateSettingsdialog():
    global dialog_window
    global txtPortNumber
    global CfdExePath
    global txtEntryRootFolderPath
    global txtEntryCfdExePath
    dialog_window = Toplevel()
    dialog_window.geometry("330x180+300+200")
    dialog_window.grab_set()
    dialog_window.title("Settings")
    # Label to display Select path
    lblSelectMainStoragePath=Label(dialog_window,text="Select a path for Storage:")
    lblSelectMainStoragePath.grid(row=0,column=0,sticky=W)
    # Button to browse Root folder path
    btnBrowseMainPath = Button(dialog_window, text='Browse...', bg="Light Blue",command=SelectMainPath,width=7, height=1)
    btnBrowseMainPath.grid(row=1,column=1,padx=10)
    # Text entry to display selected root folder path
    txtEntryRootFolderPath = Entry(dialog_window,width=40,bg="azure")
    txtEntryRootFolderPath.grid(row=1,column=0,sticky=W,padx=5,ipady=4)
    # Label to display Select CFD exe
    lblSelectCfdExePath=Label(dialog_window,text="Select a path for CFD.exe(Mandatory):")
    lblSelectCfdExePath.grid(row=2,column=0,sticky=W)
    # Button to browse CFD exe path
    btnBrowseCfdExePath = Button(dialog_window, text='Browse...',bg="Light Blue",command=SelectCfdExePath,width=7, height=1)
    btnBrowseCfdExePath.grid(row=3,column=1,padx=10)
    # Text entry to display selected CFD exe path
    txtEntryCfdExePath = Entry(dialog_window,width=40,bg="azure")
    txtEntryCfdExePath.grid(row=3,column=0,sticky=W,padx=5,ipady=4)
    # Label for port number
    lblSelectPortNumber=Label(dialog_window,text="Port number:")
    lblSelectPortNumber.grid(row=4,column=0,sticky=W)
    # Text entry take port number
    txtPortNumber = Entry(dialog_window,width=40,bg="azure")
    txtPortNumber.grid(row=5,column=0,sticky=W,padx=5,ipady=4)
    # Button to Select the port number
    btnPortNumber = Button(dialog_window, text='Click',bg="Light Blue",command=EnterPortNumber,width=7, height=1)
    btnPortNumber.grid(row=5,column=1,padx=10)
    # Button ok
    btnOk = Button(dialog_window, text='Ok',bg="Light Blue",width=7, height=1,command=CloseSettingsWindow)
    btnOk.grid(row=6,column=0,pady=5)
    
    dialog_window.lift()
# Lifting Settings dialog window
def ShowSettingsdialog():
    if dialog_window is None:
        CreateSettingsdialog()
        return
    try:
        dialog_window.lift()
    except TclError:
        CreateSettingsdialog()

def OnClickCreateNewTestCaseWindow():
    global dialog_window
    global szEnteredTestCaseName
    global RootLibraryFolderPath
    dialog_window = Toplevel()
    dialog_window.geometry("518x250+250+160")
    dialog_window.grab_set()
    dialog_window.title("New Testcase")
    # Label frame for all the buttons and entries
    lblfCreateNewTestcase = LabelFrame(dialog_window,font=('arial',10))
    lblfCreateNewTestcase.grid(pady=5,ipady=10)
    # Label for the name
    lblEnterTestcaseName = Label(lblfCreateNewTestcase, font=('arial',10),text="Name :")
    lblEnterTestcaseName.grid(row=0,column=0,pady=5,sticky=W)
    # Text entry for printing the name of the test case
    txtEntryEnterTestcase = Entry(lblfCreateNewTestcase,width=50,bg="azure")
    txtEntryEnterTestcase.grid(row=0,column=1,pady=5,ipady=3)
    # Label for the moedl filder
    lblModelFolder = Label(lblfCreateNewTestcase, font=('arial',10),text="Model folder :")
    lblModelFolder.grid(row=1,column=0,pady=2,sticky=W)
    # Text entry for priniting the name of the Model folder
    txtEntryBrowseModelFolder = Entry(lblfCreateNewTestcase,width=50,bg="azure")
    txtEntryBrowseModelFolder.grid(row=1,column=1,pady=2,padx=20,ipady=3)

    # Function On clck creat new testcase
    def OnClickCreateNewTestCase():
        global szModelFolder
        global szBaseLineFolder
        global szCopiedModelFolder
        global szTargetFolderPath
        szStatusbar['text']="Enter a testcase name of your choice"
        # Text box input 
        szEnteredTestCaseName=txtEntryEnterTestcase.get()
	# Checking if the text box is empty
        if len(szEnteredTestCaseName) == 0:
            # Displaying the error message
            messagebox.showerror("Error","Please enter a valid testcase name")
            return
        if os.path.isdir(os.path.join(RootLibraryFolderPath,szEnteredTestCaseName)):
            messagebox.showerror("Error", "Testcase alredy exists")
        else:
	    # Printing which testcase name user has entered 
            szStatusbar['text']="Testcase Name :"+" "+szEnteredTestCaseName
            txtEntryEnterTestcase.config(state=DISABLED)
            szStatusbar['text']="Select a Model Folder"
	    # UI dialog for selecting the folder 
            szModelFolder = filedialog.askdirectory(title="Select Model Folder")
	    # Checking if the selection is done 
            if len(szModelFolder) == 0:
		# Displaying the error message
                messagebox.showerror("Error","Please select a valid folder, Selection process terninated")
            else:
                txtEntryBrowseModelFolder.insert(0,szModelFolder)
                txtEntryBrowseModelFolder.config(state=DISABLED)
		# Obtaining the path of the user selected folder
                szTargetFolderPath = os.path.join(RootLibraryFolderPath,szEnteredTestCaseName)           

                if not os.path.exists(szTargetFolderPath):
                    os.makedirs(szTargetFolderPath)
		    # Copping the user selected folder to model folder location
                    szCopiedModelFolder = os.path.join(szTargetFolderPath, os.path.basename(szModelFolder))  
                    shutil.copytree(szModelFolder, szCopiedModelFolder)
                    szBaseLineFolder = os.path.join(szTargetFolderPath,"BaseLineFiles")                 
                    os.makedirs(szBaseLineFolder)
                    btnBrowseModelFolder.config(state=DISABLED)
                    
    # Button to browse the model folder
    btnBrowseModelFolder=Button(lblfCreateNewTestcase,text="Browse...",
                                bg="Light Blue",command=OnClickCreateNewTestCase,width=7)
    btnBrowseModelFolder.grid(row=1,column=2,pady=2,padx=10)

    # Label for the Python script
    lblPythonScript = Label(lblfCreateNewTestcase, font=('arial',10),text="Python script :")
    lblPythonScript.grid(row=2,column=0,pady=2,sticky=W)
    # Text entry for printing the name of the Python script
    txtEntryPythonScript = Entry(lblfCreateNewTestcase,width=50,bg="azure")
    txtEntryPythonScript.grid(row=2,column=1,pady=2,padx=20,ipady=3)
    # Nested Function on click select select python file
    def OnClickSelectPythonFile():
        global szPythonFilePath
        if len(szModelFolder)== 0:
               szStatusbar['text']="Select Model folder in order to browse the python file"
               return 
        print("CDF EXE Path :"+" "+CfdExePath)
        print("Root path:"+" "+RootLibraryFolderPath)
        szStatusbar['text']="Select Python Script"
        
        szPythonFilePath = filedialog.askopenfilename(initialdir=szCopiedModelFolder,title="Select Python File",
                                                      filetypes = (("python files","*.py"),("all files","*.*"))) 
	# Checking if the selection is done 
        if len(szPythonFilePath) == 0:
            messagebox.showerror("Error","Please select a valid python file, Selection process terninated")
        else:
            txtEntryPythonScript.insert(0,szPythonFilePath)
            txtEntryPythonScript.config(state=DISABLED)
            
            szStatusbar['text']="Click yes to execute python file,CFD will run in background  "
            szMsgBoxYesNo=messagebox.askyesno("Message", "Do you want to run the current \nPython script on CFD ?")
            if szMsgBoxYesNo == True:
                #subprocess.call([CfdExePath,'-script',szPythonFilePath])
                szStatusbar['text']="CFD Finished execution"
                return
            szStatusbar['text']="Select the Files to copy into the baseline"
            btnBrowsePythonScript.config(state=DISABLED)
            return
    # Button to browse the Python script
    btnBrowsePythonScript=Button(lblfCreateNewTestcase,text="Browse...",
                                bg="Light Blue",command=OnClickSelectPythonFile,width=7, height=1)
    btnBrowsePythonScript.grid(row=2,column=2,pady=2,padx=10,)
    # Label for the Baseline files
    lblBaselineFiles = Label(lblfCreateNewTestcase, font=('arial',10),text="Baseline files :")
    lblBaselineFiles.grid(row=4,column=0,sticky=W)
    # Lis box to show all the files 
    lstBoxListAllBaseLineFiles = Listbox(lblfCreateNewTestcase,selectmode=EXTENDED,width=50,height=6,bg="azure")
    lstBoxListAllBaseLineFiles.grid(row=3,column=1,rowspan=3)
    def OnClickAddBaselineFilesList():
        if len(szModelFolder) == 0:
            szStatusbar['text']="Please create testcase,select modelfolder for Adding the baseline files"
            return
        if len(szPythonFilePath)== 0:
            szStatusbar['text']="Please create testcase,python file for Adding the baseline files"
            return
        szSelectedUserFilesForBaseline=filedialog.askopenfilename(initialdir=szCopiedModelFolder,title="Select Files for Baseline",multiple=1)
        for i in szSelectedUserFilesForBaseline:
            lstBoxListAllBaseLineFiles.insert(END, i)
            
    # Button to Add theBaseline files
    btnBrowseBaselineFiles=Button(lblfCreateNewTestcase,text="Add",bg="Light Blue",width=7, height=1,command=OnClickAddBaselineFilesList)
    btnBrowseBaselineFiles.grid(row=3,column=2)
    #button to delete the baseline files
    def OnClickDeleteBaselineFileList():
        if len(lstBoxListAllBaseLineFiles.get(0,END)) == 0:
            szStatusbar['text']="Listbox is empty, Cannot remove an entry"
        else:
            selection =lstBoxListAllBaseLineFiles.curselection()
            lstBoxListAllBaseLineFiles.delete(selection)
        
    btnBrowseDeleteFiles=Button(lblfCreateNewTestcase,text="Delete",bg="Light Blue",width=7, height=1,command=OnClickDeleteBaselineFileList)
    btnBrowseDeleteFiles.grid(row=4,column=2)
    # Button to Copy the files into baseline files
    def OnClickCopyTheFilesTOBaseline():
        if len(lstBoxListAllBaseLineFiles.get(0,END)) == 0:
            szStatusbar['text']="Listbox is empty, Add Files to Copy to Baseline"
        else:
            szGetAllListItems=lstBoxListAllBaseLineFiles.get(0,END)
            for i in range(0,len(szGetAllListItems)):
                shutil.copy2(os.path.join(szCopiedModelFolder,os.path.basename(szGetAllListItems[i])),szBaseLineFolder)
                szStatusbar['text']="The selected files have been copied into the baseline"
                
            ET.SubElement(ChildNode, "ModelFolder").text = szCopiedModelFolder
            ET.SubElement(ChildNode, "PythonFilePath").text =szPythonFilePath
            for i in range(0,len(szGetAllListItems)):
                szStrConvertions=str(i)
                ET.SubElement(ResultNode, "UserSelectedResult-"+szStrConvertions).text=szGetAllListItems[i]
            tree = ET.ElementTree(ParentNode)
            tree.write(szTargetFolderPath+"\\"+"allpaths.xml")
            messagebox.showinfo("Success", "Testcase has been created ")
            dialog_window.destroy()
    btnAllDone=Button(lblfCreateNewTestcase,text="Ok",bg="Light Blue",width=7, height=1,command=OnClickCopyTheFilesTOBaseline)
    btnAllDone.grid(row=5,column=2)

    # Label for the Status bar
    szStatusbar= Label(dialog_window,text=" ",anchor=W)
    szStatusbar.grid(sticky=W+E+N+S)
    szStatusbar['text']="Enter a testcase name of your choice"
    
    dialog_window.lift()
    
def ShowCreateNewTestCasedialog():
    global RootLibraryFolderPath
    if len(RootLibraryFolderPath) == 0:
        RootLibraryFolderPath = os.getcwd()
        return
    if dialog_window is None:
        OnClickCreateNewTestCaseWindow()
        return
    try:
        dialog_window.lift()
    except TclError:
        if len(RootLibraryFolderPath) == 0:
            RootLibraryFolderPath = os.getcwd()
            return
        OnClickCreateNewTestCaseWindow()
    

lblAppname = Label(szMainFrame,font=('arial',30, 'bold'),text="CFD AUTOMATION TOOL",fg="Steel Blue")
lblAppname.grid(row=0,column=0)

btnSettings = Button(szMainFrame,bg="Light Blue",command=ShowSettingsdialog,height=20,width=20)
Settingsicon = Settingsicon.subsample(6)
btnSettings.config(image=Settingsicon)
btnSettings.grid(row=0,column=1,padx=20)

btnCreateNewTestCase = Button(szMainFrame, text='Create new test case', bg="Light Blue",width=30, height=5,command=ShowCreateNewTestCasedialog)
btnCreateNewTestCase.grid(row=1,column=0,pady=10)
def EnterClientIp():
    szEnterClientIpWindow=Toplevel()
    szEnterClientIpWindow.geometry("170x70+400+400")
    szEnterClientIpWindow.grab_set()
    szEnterClientIpWindow.title("Enter IP Of Client")
    txtEnteyClientName=Entry(szEnterClientIpWindow)
    txtEnteyClientName.grid(row=0,padx=10,pady=10,ipadx=10)
    def SelectIP():
        szIpAddress=txtEnteyClientName.get()
        szPingStr = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
        szPingClient = "ping " + " " + szPingStr + " " + szIpAddress
        szPingReturnVal = False if  platform.system().lower()=="windows" else True
        szPingRes=subprocess.call(szPingClient, shell=szPingReturnVal) == 0
        if szPingRes == True:
            lstBoxListAllClients.insert(END,szIpAddress)
        else:
            messagebox.showerror("Error","Requested Client is inactive")
        szEnterClientIpWindow.destroy()
    btnAddClintName=Button(szEnterClientIpWindow, text='Ok', bg="Light Blue",width=7, height=1,command=SelectIP)
    btnAddClintName.grid(row=1)
def ShowEnerClientdialog():
    if dialog_window is None:
        EnterClientIp()
        return
    try:
        dialog_window.lift()
    except TclError:
        EnterClientIp()
# Function to create run testcase
def CreateRunTestWindow():
    global szDialogEindowForRunTestcase
    global lstBoxListAllClients
    szDialogEindowForRunTestcase = Toplevel()
    szDialogEindowForRunTestcase.geometry("405x366+250+160")
    szDialogEindowForRunTestcase.grab_set()
    szDialogEindowForRunTestcase.title("Run Testcase")
    # Label frame for Run testcase
    lblfRunTestcase = LabelFrame(szDialogEindowForRunTestcase,font=('arial',10))
    lblfRunTestcase.grid(ipady=5,pady=5,padx=2,ipadx=40)
    # Label test case name
    lblAppname = Label(lblfRunTestcase,text="Test Cases :")
    lblAppname.grid(row=0,column=0,sticky=W,padx=5)
    # Label test status
    lblAppname = Label(lblfRunTestcase,text="Status :")
    lblAppname.grid(row=0,column=1,sticky=W)
    # List box to display all the testcases
    lstBoxListAllTestCases = Listbox(lblfRunTestcase,selectmode=EXTENDED,width=30,height=6,bg="azure",exportselection=0)
    lstBoxListAllTestCases.grid(row=1,column=0,padx=5,ipady=40,sticky=W)
    
    szAllDirectories=os.listdir(RootLibraryFolderPath)
    for i in szAllDirectories:
            lstBoxListAllTestCases.insert(END, i)

    def OnSelectRunTestCase():
        global szPortNumber
        szBrowserNewTab = 2
        szListBoxSelectedValue=lstBoxListAllTestCases.curselection()
        szListBoxSelectedClient=lstBoxListAllClients.curselection()
        if len(szListBoxSelectedValue)==0:
            messagebox.showerror("Error","Please select a testcase")
            return
        if len(szListBoxSelectedClient)== 0:
            messagebox.showerror("Error","Select Client machine to run on,\nYou can even select LocalRun")
            return
        #szStatusbarRunTestcase['text']="You have selected LocalRun CDF will run in the background"
        szLocalClientSelected=lstBoxListAllClients.get(szListBoxSelectedClient)
        if szLocalClientSelected == "LocalRun":
            for j in szListBoxSelectedValue:
                szSelectedFolderName=os.path.join(RootLibraryFolderPath, lstBoxListAllTestCases.get(j))
                szEmptyFolder=os.listdir(szSelectedFolderName)
                if len(szEmptyFolder) == 0:
                    szStatusbarRunTestcase['text']="Selected testcase folder is empty please select a valid folder"
                else:
                    szTestCaseInput = szSelectedFolderName
                    #print(szTestCaseInput)
        
            szReadXml=minidom.parse(szTestCaseInput+"\\"+"allpaths.xml")
            szListForHoldingResultFiles=[]
            szXmlModelFolder=szReadXml.getElementsByTagName('ModelFolder')
            szXmlPythonFile=szReadXml.getElementsByTagName('PythonFilePath')
            szModelFolder=(szXmlModelFolder[0].firstChild.data)
            szPythonFile=(szXmlPythonFile[0].childNodes[0].data)
        
            #subprocess.call([CfdExePath,'-script',szPythonFile])

            # Selecting the baseline files
            szBaseLineFolderName="BaseLineFiles"
            szBaselineFolderLocation=os.path.join(szTestCaseInput,szBaseLineFolderName)
            # Variable to select the Date and time
            szDateAndTime=time.strftime("%d%m%Y-%H%M%S")
            # Creating a new directory base on the date and time
            
            szCoppyBeforeRun = os.path.join(szTestCaseInput,"Run_"+szDateAndTime)
            os.makedirs(szCoppyBeforeRun)
            
            szLocalFolder=os.path.join(szCoppyBeforeRun,"LocalRun")
            os.makedirs(szLocalFolder)
            
            # Loop to select the Result file from the xml
            for elem in szReadXml.getElementsByTagName('ResultNode'):
                for x in elem.childNodes:
                    if x.nodeType == Node.ELEMENT_NODE:
                        szListForHoldingResultFiles.append(x.childNodes[0].data)
            # Loop to select the Basename of the files from xml and copying it to the dedicated run folder 
            for i in range(0,len(szListForHoldingResultFiles)):
                szResulfFileBasename=os.path.basename(szListForHoldingResultFiles[i])
                szAllResultFileModelFolderPath=os.path.join(szModelFolder,szResulfFileBasename)
                shutil.copy2(szAllResultFileModelFolderPath,szLocalFolder)
                
            szCommonFilesInLocalRun=filecmp.dircmp(szBaselineFolderLocation,szLocalFolder)
            for j in szCommonFilesInLocalRun.common_files:
                szCommonFilesInBaselineForRun=os.path.join(szBaselineFolderLocation, j)
                szCommonFilesInCoppyBeforeRun=os.path.join(szLocalFolder, j)
                context  = True
                context_number = 0
                szFirstFileOpenToreadFronRun=open(szCommonFilesInBaselineForRun,"r")
                szSecondFileOpenToreadFronRun=open(szCommonFilesInCoppyBeforeRun,"r")
                szDifferenceInRun=difflib.HtmlDiff().make_file(
                    szFirstFileOpenToreadFronRun.readlines(),szSecondFileOpenToreadFronRun.readlines(),
                    szCommonFilesInBaselineForRun,szCommonFilesInCoppyBeforeRun, context, context_number)
                szLocalOutputResult=open(os.path.join(szLocalFolder, "report.html"), "a")
                szLocalOutputResult.write(szDifferenceInRun)
                szLocalOutputResult.close()
                url=os.path.join(szLocalFolder, "report.html")
            webbrowser.open(url,new=szBrowserNewTab)
        else:
            if len(szPortNumber)==0:
                 szPortNumber=9999

            szSelectedClientTestCase=lstBoxListAllTestCases.get(szListBoxSelectedValue)
            
            szSelectedClientTestCasePath=os.path.join(RootLibraryFolderPath,szSelectedClientTestCase)
            print(szSelectedClientTestCasePath)
            
            szZipFolderLocation=os.path.join(RootLibraryFolderPath,szSelectedClientTestCase+".zip")
            print(szZipFolderLocation)
            szBaseName=os.path.basename(szZipFolderLocation)
            print(szBaseName)
            
    # List box to display Status
    lstBoxListAllStatus = Listbox(lblfRunTestcase,selectmode=EXTENDED,width=20,height=6,bg="azure",exportselection=0)
    lstBoxListAllStatus.config(state=DISABLED)
    lstBoxListAllStatus.grid(row=1,column=1,ipady=40)
    # Label for Client list
    lblClientList = Label(lblfRunTestcase,text="Client List :")
    lblClientList.grid(row=2,column=0,sticky=W,padx=5)
    # List box to display the client list
    lstBoxListAllClients = Listbox(lblfRunTestcase,selectmode=EXTENDED,width=30,height=6,bg="azure")
    lstBoxListAllClients.grid(row=3,column=0,padx=5,sticky=W,rowspan=2)
    # Fixed list box value for Local machine 
    lstBoxListAllClients.insert(0,"LocalRun")
    # Button to add client
    btnAddClient = Button(lblfRunTestcase, text='AddClient', bg="Light Blue",width=7, height=1,command=ShowEnerClientdialog)
    btnAddClient.grid(row=3,column=1)
    # Button to run the Testcase
    btnRun = Button(lblfRunTestcase, text='Run', bg="Light Blue",width=7, height=1,command=OnSelectRunTestCase)
    btnRun.grid(row=4,column=1)
    # Status bar
    szStatusbarRunTestcase= Label(szDialogEindowForRunTestcase,text="Status Bar",anchor=W)
    szStatusbarRunTestcase.grid(sticky=N+S+W+E)
    szStatusbarRunTestcase['text']="Select the Testcase of your choice from the list and also select the Client"
    
def ShowRunTestCasedialog():
    global RootLibraryFolderPath
    if len(RootLibraryFolderPath) == 0:
        RootLibraryFolderPath = os.getcwd()
        return
    if dialog_window is None:
        CreateRunTestWindow()
        return
    try:
        dialog_window.lift()
    except TclError:
        if len(RootLibraryFolderPath) == 0:
            RootLibraryFolderPath = os.getcwd()
            return
        CreateRunTestWindow()
btnCompareResults = Button(szMainFrame, text="Run Testcase", bg="Light Blue",width=30, height=5,command=ShowRunTestCasedialog)
btnCompareResults.grid(row=2,column=0,pady=10) 

szTkExecution.mainloop()
