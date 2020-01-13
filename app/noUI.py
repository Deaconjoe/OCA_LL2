import string
import random
import re
import mysql.connector


def dbConnect():
    con = mysql.connector.connect(
        host="db_1",
        user="user",
        passwd="password",
        database="CCLoanLaptops")

    return con
    

def GetCustomerName(CustomerName):
        storage1 = CustomerName
        storage = storage1.upper()
        return storage

def GetLendingStaffName(StaffName):
    storage1 = StaffName
    storage = storage1.upper()
    return storage

def SQLSave(RoB, CCassetTag, assetTag, DateBorrowed, TimeBorrowed, BorrowedBy, LentBy, ReturnedBy, ReceivedBy, DateReturned, TimeReturned):
    import mysql.connector
    if RoB == True:
        mydb = dbConnect()
        
        mycursor = mydb.cursor()
        fotmat = "INSERT INTO LoanedLaptops (CCassetTag,assetTag, DateBorrowed,BorrowedBy, LentBy,ReturnedBy, ReceivedBy,DateReturned, TimeReturned,TimeBorrowed) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        sql = fotmat
        val = (str(CCassetTag), assetTag, str(DateBorrowed), BorrowedBy, LentBy,
               ReturnedBy, ReceivedBy, DateReturned, str(TimeReturned), str(TimeBorrowed))
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()    
        
    if RoB == False:
        mydb = dbConnect()
        mycursor = mydb.cursor()
        sql = """select * from LoanedLaptops where assetTag = '{}' AND ReturnedBy = '{}'""".format(
            assetTag, 'Null')
        mycursor.execute(sql)
        allrecs = mycursor.fetchall()
        print(allrecs)
        try:
            idToUpd = allrecs[0][10]
            with open('out.txt', 'w') as f:
                print('Filename:', idToUpd, file=f)
                mycursor.execute("UPDATE LoanedLaptops SET ReturnedBy = '%s' WHERE id = '%s'" % (
                ReturnedBy,   idToUpd))
                mycursor.execute("UPDATE LoanedLaptops SET ReceivedBy = '%s' WHERE id = '%s'" % (
                ReceivedBy,   idToUpd))
                mycursor.execute("UPDATE LoanedLaptops SET DateReturned = '%s' WHERE id = '%s'" % (
                DateReturned,   idToUpd))
                mycursor.execute("UPDATE LoanedLaptops SET TimeReturned = '%s' WHERE id = '%s'" % (
                TimeReturned,   idToUpd))
                mydb.commit()
                mydb.close()
        except:
            print('No Existing Ticket Found')
        
        
def GetDateTime():
    import os
    import time
    from time import gmtime, strftime, localtime
    os.environ['TZ'] = 'Europe/London'
    time.tzset()
    dateToday = (strftime("%Y-%m-%d", localtime()))
    timeNow = (strftime("%H:%M:%S", localtime()))

    return timeNow, dateToday
def GetCCNum(AssetTag):
    import csv
    data = []
    data2 = []
    FoundAsset = False
    AssetTag2 = re.sub("[^0-9^.]", "", AssetTag.upper())
    with open('AssetList.csv', mode='r', newline="") as f:
        reader = csv.reader(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in reader:
            if AssetTag2 in line:
                data.append(line)
                data2.append(data[0][0].split(','))
                FoundAsset = True
                data3 = data2[0]
                data4 = ', '.join(data3)

    if FoundAsset == True:
        return str(data4)
    else:
        print('Not an Existing Central Stores Asset, Added to database. ')
        return('Not in CC Inventory')

def CheckOpenTicket(AssetTag):
    import csv
    import re

    filename = 'TicketLog.csv'
    fields = ['CCassetTag', 'assetTag', 'TimeBorrowed', 'DateBorrowed', 'BorrowedBy', 'LentBy', 'ReturnedBy', 'ReceivedBy', 'DateReturned', 'TimeReturned']
    x=0
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        #row_count = sum(1 for row in reader)
        for row in reader:
            if AssetTag in row:
                #print('"'+AssetTag+'"') 
                if 'Null'in row:
                    x=1
                    break                  
                else:
                    x=0
            else:
               x=0              
    if x == 1:
        return True
    else: 
        return False



def OutWriteToExcel(AssetTag, CurrentDate, CurrentTime, BorrowingUserName, LendingUserName):
    import csv

    AssetTag1 = re.sub("[^0-9^.]", "", AssetTag.upper())
    AssetTag2 = '"'+str(AssetTag1)+'"'

    with open('TicketLog.csv', mode='r') as f:
            reader = csv.reader(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row_count = sum(1 for row in reader)
    new_row = row_count + 1

    CCNum = GetCCNum(AssetTag1)
    


    with open('TicketLog.csv', mode='a', newline="") as fd:
        writer = csv.writer(fd, delimiter=',',
                                quotechar="'", quoting=csv.QUOTE_MINIMAL)
            
        NewRow = [CCNum ,AssetTag2,CurrentDate ,CurrentTime , BorrowingUserName, LendingUserName,'Null','Null' ,'Null' ,'Null']
        writer.writerow(NewRow)

    SQLSave(True, CCNum, AssetTag1, CurrentTime, CurrentDate,
        BorrowingUserName, LendingUserName, "Null", "Null", "Null", "Null",)

    
def InWriteToExcel(AssetTag, CurrentDate, CurrentTime, ReturningUserName, ReceivingStaffName):
    import csv
    import re
    from tempfile import NamedTemporaryFile
    import shutil
    import csv

    AssetTag1 = re.sub("[^0-9^.]", "", AssetTag.upper())

    filename = 'TicketLog.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    fields = ['CCassetTag', 'assetTag', 'TimeBorrowed', 'DateBorrowed', 'BorrowedBy', 'LentBy', 'ReturnedBy', 'ReceivedBy', 'DateReturned', 'TimeReturned']
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['assetTag'] == str(AssetTag1) and row['ReturnedBy'] == 'Null':
                print('updating row', row['CCassetTag'])
                row2 = row
                row2['ReturnedBy'] = ReturningUserName
                row2['ReceivedBy'] = ReceivingStaffName
                row2['DateReturned'] = CurrentDate
                row2['TimeReturned'] = CurrentTime
                writer.writerow(row2)
                print(row2)
            else:
                writer.writerow(row)
    SQLSave(False, "Null", AssetTag1, "Null", "Null", "Null", "Null",
                        ReturningUserName, ReceivingStaffName, CurrentDate, CurrentTime)
   

    shutil.move(tempfile.name, filename)
  
  

def SaveOutgoing(CustName,StaffName, LaptopAsset):

    OutgoingLaptopAssetTagStorage = re.sub("[^0-9^.]", "", LaptopAsset.upper())

    def CheckDatabase(LaptopAsset): #AssetTags)
        import csv
        with open('AssetList.csv', mode='r', newline="") as f:
            reader = csv.reader(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in reader:
                if AssetTag in line:
                    return True
                    
    def AddToDatabase(AssetTag, NumLines):
        import csv
        with open('AssetList.csv', mode='a', newline="") as fd:
            writer = csv.writer(fd, delimiter=',',
                                quotechar="'", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(NewRow)
            return 'Done'
    def RowCount():
        import csv
        with open('AssetList.csv', mode='r') as f:
            reader = csv.reader(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row_count = sum(1 for row in reader)

            return row_count
    def GetDateTime():
       import os
       import time
       from time import gmtime, strftime, localtime
       os.environ['TZ'] = 'Europe/London'
       time.tzset()
       dateToday = (strftime("%Y-%m-%d", localtime()))
       timeNow = (strftime("%H:%M:%S", localtime()))


       return dateToday, timeNow

    CustomerName =  CustName.upper() #GetCustomerName()
    LendingStaffName = StaffName.upper() #GetLendingStaffName()
    dateTime = GetDateTime()
    Date = dateTime[1]
    Time = dateTime[0]
    AssetTag1 = OutgoingLaptopAssetTagStorage
    AssetTag = re.sub("[^0-9^.]", "", AssetTag1.upper())
    NumLines = RowCount()
    InDatabase = CheckDatabase(AssetTag)
    if InDatabase != True:
        RowNum = str(NumLines)
        NewRow = ['"' + str((int(RowNum))) + '"', '"' + AssetTag + '"']
        AddToDatabase(AssetTag, NumLines)
    if CheckOpenTicket(AssetTag) == False:
        OutWriteToExcel(AssetTag, Date, Time,
                        CustomerName, LendingStaffName)
    else:
        print("There is already an open ticket for this asset")

                
def SaveIncoming(CustomerName, StaffName, LaptopAsset):
    
    IncomingLaptopAssetStorage = re.sub("[^0-9^.]", "", LaptopAsset.upper())
    IncomingCustomerIDStorage = CustomerName.upper()
    ReceivingStaffName1 = StaffName.upper()


    CustomerName1 = IncomingCustomerIDStorage
    CustomerName = CustomerName1.upper()
    
    ReceivingStaffName = ReceivingStaffName1.upper()
    AssetTag1 = re.sub("[^0-9^.]", "", IncomingLaptopAssetStorage)
    AssetTag = AssetTag1

    dateTime = GetDateTime()
    Date = dateTime[1]
    Time = dateTime[0]

    InWriteToExcel(AssetTag, Date, Time, CustomerName, ReceivingStaffName)


