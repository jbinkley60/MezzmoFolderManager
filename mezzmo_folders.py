# -*- coding: utf-8 -*-
# #!/usr/bin/python
import os, fnmatch, sys, csv, json, glob
from datetime import datetime, timedelta
from pathlib import Path
import time
import subprocess
import string

folderdb = 'mezzmo_folders.db'
tr_config = {}

version = 'version 0.0.1'

sysarg1 = sysarg2 = ''

if len(sys.argv) == 2:
    sysarg1 = sys.argv[1].lower()
if len(sys.argv) == 3:
    sysarg1 = sys.argv[1].lower()   
    sysarg2 = sys.argv[2].lower()

print('The Number of arguments are: ' + str(len(sys.argv)) ) 


def getConfig():

    try: 

        global tr_config, version      
        fileh = open("config.txt")                                     # open the config file
        linecount = len(fileh.readlines())
        fileh.seek(0)                                                  # Move file pointer to the beginning            
        data = fileh.readline()                                        # Get Mezzmo database location
        dataa = data.split('#')                                        # Remove comments
        data = dataa[0].strip().rstrip("\n")                           # cleanup unwanted characters
        mezzmodbpath = data + "Mezzmo.db"

        data = fileh.readline()                                        # Logfile location
        if data != '':
            datab = data.split('#')                                    # Remove comments
            logoutfile = datab[0].strip().rstrip("\n")                 # cleanup unwanted characters         
        else:
            logoutfile = 'logfile.txt'                                 # Default to logfile.txt

        data = fileh.readline()                                        # Maximum number of folder backups to keep in database
        datac = data.split('#')                                        # Remove comments
        maxkeep = datac[0].strip().rstrip("\n")                        # cleanup unwanted characters
        if int(maxkeep) > 10:
            maxkeep = 10                                               # Max copies to keep 0 - 10
        elif int(maxkeep) < 0:
            maxkeep = 0

        data = fileh.readline()                                        # Enable automatic sync on Mezzmo update if changes
        datad = data.split('#')                                        # Remove comments
        autosync = datad[0].strip().rstrip("\n").lower()               # cleanup unwanted characters

        fileh.close()                                                  # close the file
        
        tr_config = {
                     'dbfile': mezzmodbpath,
                     'logoutfile': logoutfile,
                     'maxkeep': maxkeep,
                     'autosync': autosync
                    }

        configuration = [mezzmodbpath, logoutfile, maxkeep, autosync]
        mgenlog = ("Mezzmo Folder Manager started - " + version)
        print(mgenlog)
        genLog(mgenlog)
        mgenlog = 'Number of lines in the config file: ' + str(linecount)
        genLog(mgenlog)
        genLog(str(configuration))               # Record configuration to logfile    
        mgenlog = "Finished reading config file."
        genLog(mgenlog)       
        return 
 
    except Exception as e:
        print (e)
        mgenlog = 'There was a problem parsing the config file.'
        genLog(mgenlog)
        print(mgenlog)


def checkCommands(sysarg1, sysarg2):                                   # Check for valid commands
   
    if len(sysarg1) > 1 and sysarg1.lower() not in ['export', 'sync',  'help', 'backup']:
        displayHelp(sysarg1)
        sys.exit()
    elif sysarg1.lower().strip() in ['help', '?']:
        displayHelp(sysarg1)
        sys.exit()
    elif len(sysarg1) == 0:
        mainMenu()
    elif sysarg1 in ['sync']:                                          # Sync Mezzmo Folder to Mezzmo
        syncMezzmo()        
        sys.exit()
    elif sysarg1 in ['backup']:                                        # Mezzmo Folder Manager backup
        makeBackups()       
        sys.exit()
    elif sysarg1 in ['export']:                                        # Export Mezzmo Folder Manager data
        chooseData('export')       
        sys.exit()


def mainMenu():                                           # Main menu when no command line arg given


        while True:
            os.system('cls')
            print('\n\n\t          Choose Mezzmo Folder Manager Command \n')
            print('\t 1.  Sync    -  Sync Mezzmo Folder Manager to Mezzmo DB ')
            print('\t 2.  Update  -  Update Mezzmo DB from Mezzmo Folder Manager ')
            print('\t 3.  Export  -  Export Mezzmo F0lder Manager data to CSV file ')
            print('\t 4.  Import  -  Import Updated CSV file to Mezzmo Folder Manager ')
            print('\t 5.  Backup  -  Backup Mezzmo Folder Manager database ')
            print('\n\n\t 0.  Exit')
            choice = input('\n\n\tEnter selection 1-5 or 0 to exit ?   ')

            if choice == '0':
                sys.exit()
            elif choice == '1':
                syncMezzmo()
            elif choice == '2':
                chooseData('update')
            elif choice == '3':
                chooseData('export')
            elif choice == '4':
                checkImport()
            elif choice == '5':
                makeBackups()
                time.sleep(5)   
            else:
                print('\n\t Selected function not yet implemented.')
                time.sleep(3)
                #sys.exit()

       
def displayHelp(sysarg1):                                 #  Command line help menu display

        os.system('cls')
        print('\n=====================================================================================================')
        print('\nThe only valid commands are -  help, sync, backup, export ')
        print('\nExample:  mezzmo_folders.py sync')      
        print('\nhelp\t\t - Displays this help screen')
        print('sync\t\t - Syncs the Mezzmo Folder Manager to the Mezzmo database for folders and playlists')
        print('backup\t\t - Creates a time stamped backup of the Mezzmo Folder Manager database')
        print('export\t\t - Creates a time stamped CSV export of specificed Mezzmo Folder Manager data')
        print('\n\t\t - ENtering no command brings up a menu driven command structure for all features\n')       
        print('\n=====================================================================================================')
        print('\n\n ')         


def chooseData(userselect):                               #  Choose data to export or update    

        datachoice = []
        title = ''
        os.system('cls')
        if userselect == 'export':
            print('\n\n\t      Choose Mezzmo Folder Manager Data Export \n')
        elif userselect == 'update':
            print('\n\n\t      Choose Mezzmo Folder Manager Update Mezzmo \n')
        print('\t 1.  Sync - Folder      -  Mezzmo folder data added by Mezzmo Sync ')
        print('\t 2.  Sync - Playlist    -  Mezzmo playlist data added by Mezzmo Sync  ')
        print('\t 3.  Import - Folder    -  Mezzmo folder data added by User Import  ')
        print('\t 4.  Import - Playlist  -  Mezzmo playlist data added by User Import  ')
        choice = input('\n\n\tEnter selection 1-4 or 0 to return to main menu ?   ')

        if choice == '0':
            return
        elif choice == '1':
            datachoice = ['sync', 'subwatch']
            title = 'Mezzmo Sync Folder'        
        elif choice == '2':
            datachoice = ['sync', 'playlist']
            title = 'Mezzmo Sync Playlist'         
        elif choice == '3':
            datachoice = ['import', 'subwatch']
            title = 'User Import Folder'        
        elif choice == '4':
            datachoice = ['import', 'playlist']
            title = 'User Import Playlist'
        else:
            print('\n Invalid selection.')
            time.sleep(3)
            return

        #print(str(datachoice))
        #time.sleep(3)

        mgenlog = 'Choose data results: ' + userselect + '   ' + str(datachoice) + '   ' + title
        genLog(mgenlog)        
         

        dbf = openFolderDB()

        crecords = dbf.execute('select distinct dateAdded from mWatchFolders where           \
        source = ? and MezzTable = ? order by dateAdded desc, source, MezzTable LIMIT  10',  \
        (datachoice[0], datachoice[1],)) 
        ctuples = crecords.fetchall()                     #  Get list of dates
        dbf.close()

        #print('Number of records = ' + str(len(ctuples)))
        if len(ctuples) == 0:
            print('\n\t There were no records found yet for your selection.')
            time.sleep(4)
            return

        os.system('cls')
        if userselect == 'export':
            print('\n\n\t      Select ' + title + ' data to export  \n')
        elif userselect == 'update':
            print('\n\n\t      Select ' + title + ' data to update  \n') 
       
        for n in range(len(ctuples)):
            print('\t ' + str(n+1) + '.    ' + ctuples[n][0])

        choice = input('\n\n\t Enter selection 1-' + str(len(ctuples)) + ' or 0 to return to mainmenu ?   ')

        #if isinstance(choice, int) and int(choice) <= len(ctuples):
        if choice.isdigit() and int(choice) <= len(ctuples) and userselect == 'export':
            #print('\t Selection is: ' + ctuples[int(choice)-1][0])
            #time.sleep(4)
            checkCsv(datachoice[0], datachoice[1], ctuples[int(choice)-1][0])
        elif choice.isdigit() and int(choice) <= len(ctuples) and userselect == 'update':
            #print('\t Selection is: ' + ctuples[int(choice)-1][0])
            #time.sleep(4)
            mezzmoUpdate(datachoice[0], datachoice[1], ctuples[int(choice)-1][0])           
        else:
            return


def checkImport():                                             # Check for CSV file to import

        global importable

        filechoice = ''
        os.system('cls')
        print('\n\n\t      Choose Mezzmo Folder Manager CSV Import \n')
        print('\t 1.  Mezzmo Folder CSV file  ')
        print('\t 2.  Mezzmo Playlist CSV file  \n\n')
        choice = input('\n\n\tEnter selection 1-2 or 0 to return to main menu ?   ')

        if choice == '0':
            return
        elif choice == '1':
            filechoice = 'folder'
        elif choice == '2':
            filechoice = 'playlist'
        else:
            print('\n\t Invalid selection.')
            time.sleep(3)
            return

        paths = sorted(Path('import').glob('*' + filechoice + '*'), key=os.path.getmtime, reverse=True)
        found = 0
        if len(paths) > 0 :
            os.system('cls')
            print('\n\n      Select CSV file to import  \n')        
            for p in range(len(paths)):
                if filechoice in str(paths[p]):
                    print('\t ' + str(found+1) + '.    ' + str(paths[p]).split('\\')[1])
                    found += 1
        else:
            print('\n\tNo matching files found to import.\n')
            time.sleep(4)
            return

        choice = input('\n\n\tEnter selection or 0 to return to main menu ?   ')
        if choice == '0':
            return
        elif choice.isdigit() and int(choice) <= found:
            #print('Choice is: ' + str(paths[int(choice)-1]))
            #time.sleep(4)
            readFile(str(paths[int(choice)-1]))             # Import selected file
        else:
           print('\n\tNo matching files found to import.\n')
           time.sleep(4)
           return        


def genLog(mgenlog):                                        #  Write to logfile

        global tr_config
        logoutfile = tr_config['logoutfile']
        fileh = open(logoutfile, "a")                       #  open logf file
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        data = fileh.write(currTime + ' - ' + mgenlog + '\n')
        fileh.close()


def syncMezzmo():

        global tr_config

        mgenlog = 'Beginning Mezzmo sync'
        genLog(mgenlog)

        dbm = openMezDB()
        dbf = openFolderDB()

        """ Sync Mezzmo MGOSubWatchFolder table to Mezzmo Folder DB normalizing lookup values """

        mfolders = dbm.execute('select MGOSubWatchFolder.ID, SubWatchFolderPath,                  \
        MGOSubWatchFolder.Description,  MGOSubWatchFolder.ThumbnailID, MGOPoster.Path,            \
        MGOSubWatchFolder.BackdropArtworkID, MGOBackdrop.Path,  MGOPlaylist.name,                 \
        MGOSubWatchFolder.ContentRatingID, MGOFileContentRating.ContentRating,                    \
        MGOFileContentRating.Country FROM MGOSubWatchFolder                                       \
        INNER JOIN MGOPoster on MGOSubWatchFolder.ThumbnailID = MGOPoster.ID                      \
        INNER JOIN MGOBackdrop on MGOSubWatchFolder.BackdropArtworkID = MGOBackdrop.ID            \
        INNER JOIN MGOPlaylist on MGOSubWatchFolder.TopLevelWatchFolderID = MGOPlaylist.ID        \
        INNER JOIN MGOFileContentRating on MGOSubWatchFolder.ContentRatingID = MGOFileContentRating.ID')
        mftuples = mfolders.fetchall()
        
        mgenlog = 'Number of folder records found: ' + str(len(mftuples))
        print('\n\t' + mgenlog)
        genLog(mgenlog)

        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for f in range(len(mftuples)):
            dbf.execute('INSERT into mWatchFolders (dateAdded, ID, source, mezzTable,             \
            SubWatchFolderPath, Description, PosterFileID, PosterFile, BackdropFileID,            \
            BackdropFile, TopLevelWatchFolder, ContentRatingID, ContentRatingName, RatingCountry) \
            values (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?)',                                   \
            (currTime, mftuples[f][0], 'sync', 'subwatch',  mftuples[f][1], mftuples[f][2],       \
            mftuples[f][3], mftuples[f][4], mftuples[f][5], mftuples[f][6], mftuples[f][7],       \
            mftuples[f][8], mftuples[f][9], mftuples[f][10], ))  
        dbf.commit()

        mgenlog = 'MGOSubWatchFolder completed.  Records processed: ' + str(len(mftuples))
        print('\t ' + mgenlog)
        genLog(mgenlog)


        """ Sync Mezzmo MGOPlaylist table to Mezzmo Folder DB normalizing lookup values """

        mplaylists = dbm.execute('select ID, Name, Description, ThumbnailID, BackdropArtworkID, \
        ParentID, ContentRatingID from MGOPlaylist')
        mptuples = mplaylists.fetchall()
        
        mgenlog = 'Number of playlist records found: ' + str(len(mptuples))
        print('\n\t' + mgenlog)
        genLog(mgenlog)

        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for p in range(len(mptuples)):
            dbf.execute('INSERT into mWatchFolders (dateAdded, ID, source, mezzTable,          \
            SubWatchFolderPath, Description, PosterFileID,  BackdropFileID, ParentFolderID,    \
            ContentRatingID )                                                                  \
            values (?, ?, ?, ?, ?, ? ,?, ?, ?, ?)',                                            \
            (currTime, mptuples[p][0], 'sync', 'playlist',  mptuples[p][1], mptuples[p][2],    \
            mptuples[p][3], mptuples[p][4], mptuples[p][5], mptuples[p][6], ))  
        dbf.commit()


        mposters = dbm.execute('select ID, Path from MGOPoster')     # Get Mezzmo poster file table
        matuples = mposters.fetchall()

        if len(matuples) > 0:                                        # Create temporary artwork table
            dbf.execute('CREATE table IF NOT EXISTS artTemp (ID Integer, Path TEXT)')
            dbf.execute('CREATE INDEX IF NOT EXISTS artTemp_1 ON artTemp (ID)')
            dbf.commit()

            for a in range(len(matuples)):                           # Insert Mezzmo poster file table
                dbf.execute('INSERT into artTemp (ID, Path) values (?, ?)', (matuples[a][0],  \
                matuples[a][1],))
            dbf.commit()

        dbf.execute('update mWatchFolders set PosterFile = (select Path from artTemp where    \
        mWatchFolders.PosterFileID = artTemp.ID) where mezzTable = "playlist" and             \
        source = "sync" and dateAdded = ?', (currTime,))             # Update poster file names
        dbf.execute('DELETE from artTemp')                           # Clear artwork temporary table
        dbf.commit()

        mbdrops = dbm.execute('select ID, Path from MGOBackdrop')    # Get Mezzmo backdrop file table
        mbtuples = mbdrops.fetchall()

        if len(mbtuples) > 0:                                        # Update temporary artwork table
            for b in range(len(mbtuples)):                           # Insert Mezzmo backdrop file table
                dbf.execute('INSERT into artTemp (ID, Path) values (?, ?)', (mbtuples[b][0],  \
                mbtuples[b][1],))
            dbf.commit()

        dbf.execute('update mWatchFolders set BackdropFile = (select Path from artTemp where   \
        mWatchFolders.BackdropFileID = artTemp.ID) where mezzTable = "playlist" and            \
        source = "sync" and dateAdded = ?', (currTime,))             # Update backdrop file names
        dbf.execute('DELETE from artTemp')                           # Clear artwork temporary table
        dbf.commit()

        mparents = dbm.execute('select ID, Name from MGOPlaylist')   # Get parent info from Mezzmo
        mptuples = mparents.fetchall()

        if len(mptuples) > 0:                                        # Update temporary artwork table
            for p in range(len(mptuples)):                           # Insert parent records
                dbf.execute('INSERT into artTemp (ID, Path) values (?, ?)', (mptuples[p][0],  \
                mptuples[p][1],))
            dbf.commit()

        dbf.execute('update mWatchFolders set ParentFolder = (select Path from artTemp where  \
        mWatchFolders.ParentFolderID = artTemp.ID) where mezzTable = "playlist" and           \
        source = "sync" and dateAdded = ?', (currTime,))             # Update parent records    
        dbf.execute('DROP table IF EXISTS artTemp')
        dbf.commit()


        if len(mptuples) > 0:                                        # Create temporary lookup table
            dbf.execute('CREATE table IF NOT EXISTS contentTemp (ID Integer, ContentRating TEXT \
            COLLATE NOCASE, Country TEXT COLLATE NOCASE)')
            dbf.execute('CREATE INDEX IF NOT EXISTS contentTemp_1 ON contentTemp (ID)')
            dbf.commit()

        mcontent = dbm.execute('select ID, ContentRating, Country from MGOFileContentRating')
        mctuples = mcontent.fetchall()                               # Get Mezzmo content rating table
  
        if len(mctuples) > 0:
            for c in range(len(mctuples)):                           # Insert content ratings
                dbf.execute('INSERT into contentTemp (ID, ContentRating, Country)          \
                values (?, ?, ?)', (mctuples[c][0], mctuples[c][1], mctuples[c][2],))
            dbf.commit()

        dbf.execute('update mWatchFolders set ContentRatingName = (select ContentRating from \
        contentTemp where mWatchFolders.ContentRatingID = contentTemp.ID) where mezzTable    \
        = "playlist" and source = "sync" and dateAdded = ?', (currTime,))  # Update content rating    
        
        dbf.execute('update mWatchFolders set RatingCountry = (select Country from           \
        contentTemp where mWatchFolders.ContentRatingID = contentTemp.ID) where mezzTable    \
        = "playlist" and source = "sync" and dateAdded = ?', (currTime,))  # Update rating country         

        dbf.execute('DROP table IF EXISTS contentTemp')
        dbf.commit()
        
        dbm.close()
        dbf.close()

        mgenlog = 'MGOPlaylist completed.  Records processed: ' + str(len(mptuples))
        print('\t ' + mgenlog)
        genLog(mgenlog)


def mezzmoUpdate(source = '', mezztab = '', criteria = ''):        # Update Mezzmo from Mezzmo Folder Manager 

        choice = input('\n\n\t Have you stopped the Mezzmo server service and Mezzmo GUI (Y/Yes or N/No) ?   ')
        if choice.lower() not in  ['yes', 'y']:
            mgenlog = 'Mezzmo server service or Mezzmo GUI not stopped for update.'
            genLog(mgenlog)
            print('\t The Mezzmo server service and GUI must be stopped prior to updating Mezzmo.') 
            time.sleep(4)
            return
        else:
            mgenlog = 'Mezzmo update beginning   '
            print('\t ' + mgenlog)
            mgenlog = mgenlog + source + '  ' +  mezztab + '   ' + criteria 
            genLog(mgenlog)

        autosync = tr_config['autosync']
        db = openFolderDB()

        curm = db.execute('SELECT ID, Description FROM mWatchFolders where source = ?  \
        and mezzTable = ? and dateAdded = ? ORDER BY ID ASC', (source, mezztab, criteria,))
        recs = curm.fetchall()

        if len(recs) == 0:
            mgenlog = 'No matching records found to export.'
            print ('\t ' + mgenlog)
            genLog(mgenlog)            
            time.sleep(4)
            del curm
            db.close() 
            return   

        if mezztab == 'subwatch':
            utype = 'folder'
        else:
            utype = 'playlist'

        mgenlog = 'Number of ' + utype + 's found : ' + str(len(recs))
        genLog(mgenlog)
        print('\n\t ' + mgenlog)
        time.sleep(5)

        del curm
        db.close() 

        dbm = openMezDB()
        match = unmatch = checked = updated = notfound = 0
        for r in range(len(recs)): 
            if mezztab == 'subwatch':                        #  Update Mezzmo MGOSubWatchFolder table
                #print(str(recs[r][0]))
                murm = dbm.execute('SELECT ID, Description, SubWatchFolderPath FROM      \
                MGOSubWatchFolder WHERE ID = ?', (recs[r][0],))
                mtuple = murm.fetchone()
                checked += 1
                if mtuple:
                    #print('Match found: ' + mtuple[1] + '  ' + recs[r][1])
                    if mtuple[1] == recs[r][1]:              #  Mezzmo and Mezzmo Folder Manager match
                        match += 1                           #  Do nothing and increment match counter
                    elif mtuple[1] != recs[r][1]:            #  Update description if not match
                        unmatch += 1   
                        dbm.execute('Update MGOSubWatchFolder set Description = ? WHERE  \
                        ID = ?', (recs[r][1], recs[r][0],))
                        mgenlog = 'Mezzmo Folder ID updated:  ' +  str(recs[r][0]) + '\t' + mtuple[2][:48]
                        print ('\t ' + mgenlog)
                        mgenlog = 'Mezzmo Folder ID updated:  ' +  str(recs[r][0]) + '\t' + mtuple[2]
                        genLog(mgenlog) 
 
                else:
                    notfound += 1
                    mgenlog = 'MGOSubWatchFolder ID not found: ' +  str(recs[r][0])
                    print ('\t ' + mgenlog)
                    genLog(mgenlog) 

            elif mezztab == 'playlist':                       #  Update Mezzmo MGOPlaylist table
                #print(str(recs[r][0]))
                murm = dbm.execute('SELECT ID, Description, Name FROM MGOPlaylist WHERE  \
                ID = ?', (recs[r][0],))
                mtuple = murm.fetchone()
                checked += 1
                if mtuple:
                    if mtuple[1] == recs[r][1]:              #  Mezzmo and Mezzmo Folder Manager match
                        match += 1                           #  Do nothing and increment match counter
                    elif mtuple[1] != recs[r][1]:            #  Update description if not match
                        unmatch += 1   
                        dbm.execute('Update MGOPlaylist set Description = ? WHERE        \
                        ID = ?', (recs[r][1], recs[r][0],))
                        mgenlog = 'Mezzmo Playlist ID updated:  ' +  str(recs[r][0]) + '\t' + mtuple[2][:48]
                        print ('\t ' + mgenlog)
                        mgenlog = 'Mezzmo Playlist ID updated:  ' +  str(recs[r][0]) + '\t' + mtuple[2]
                        genLog(mgenlog)  
                else:
                    notfound += 1
                    mgenlog = 'MGOPlaylist ID not found: ' +  str(recs[r][0])
                    print ('\t ' + mgenlog)
                    genLog(mgenlog) 
  
        dbm.commit()
        dbm.close()
        mgenlog = 'Mezzmo update successfully completed'
        print('\n\t\t ' + mgenlog)
        genLog(mgenlog)
        mgenlog = 'Records checked:\t' + str(checked)
        print('\n\t ' + mgenlog)
        genLog(mgenlog)
        mgenlog = 'Records not updated:\t' + str(match)
        print('\t ' + mgenlog)
        genLog(mgenlog)
        mgenlog = 'Records updated:\t' + str(unmatch)
        print('\t ' + mgenlog)
        genLog(mgenlog)

        if unmatch > 0 and autosync in ['yes', 'y']:
            mgenlog = 'Automatic Mezzmo Sync enabled.  Sync beginning.'
            print('\t ' + mgenlog)
            genLog(mgenlog)
            syncMezzmo()
        choice = input('\n\n\tEnter to exit or 0 to return to main menu ?   ')
        if choice == '0':
            return 
        else:
            sys.exit()


def checkDatabase():

    try:
        global folderdb

        db = openFolderDB()

        db.execute('CREATE table IF NOT EXISTS mWatchFolders (dateAdded TEXT, ID INTEGER,        \
        source TEXT, mezzTable TEXT, SubWatchFolderPath TEXT COLLATE NOCASE, Description TEXT    \
        Collate NOCASE, PosterFileID INTEGER, PosterFile TEXT, BackdropFileID INTEGER,           \
        BackdropFile TEXT, ParentFolderID INTEGER, ParentFolder TEXT, TopLevelWatchFolder TEXT,  \
        ContentRatingID INTEGER, ContentRatingName TEXT, RatingCountry TEXT, var1 TEXT,          \
        var2 TEXT, var3 TEXT, var4 TEXT)')

        db.execute('CREATE INDEX IF NOT EXISTS folders_1 ON mWatchFolders (ID)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_2 ON mWatchFolders (dateAdded)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_3 ON mWatchFolders (SubWatchFolderPath    \
        COLLATE NOCASE)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_4 ON mWatchFolders (Description COLLATE   \
        NOCASE)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_5 ON mWatchFolders (dateAdded, source)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_6 ON mWatchFolders (dateAdded, source, ID)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_7 ON mWatchFolders (mezzTable)')
        db.execute('CREATE INDEX IF NOT EXISTS folders_8 ON mWatchFolders (ParentFolderID)')

        db.commit()
        db.close()
 
        mgenlog = "Mezzmo check folder database completed."
        print (mgenlog)
        genLog(mgenlog)

    except Exception as e:
        print (e)
        mgenlog = "There was a problem verifying the folder database file: " + folderdb
        print(mgenlog)
        sys.exit()   


def openFolderDB():

    global folderdb
    
    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
                       
    db = sqlite.connect(folderdb)

    return db


def openMezDB():

    global tr_config

    dbfile = tr_config['dbfile']
   
    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
                       
    db = sqlite.connect(dbfile)
    db.execute('PRAGMA journal_mode = WAL;')
    db.execute('PRAGMA synchronous = NORMAL;')
    db.execute('PRAGMA cache_size = -10000;')

    return db


def checkFolders():                                # Check folders and files

    try:
        global tr_config
        mdbfile = tr_config['dbfile']

        if not os.path.exists('backups'):          #  Check backup files location
            os.makedirs('backups')
            mgenlog = 'Backup folder created.'
            genLog(mgenlog)
            print('\t' + mgenlog)

        if not os.path.exists('import'):           #  Check CSV import files location
            os.makedirs('import')
            mgenlog = 'Import folder created.'
            genLog(mgenlog)
            print('\t' + mgenlog)

        if not os.path.exists('export'):           #  Check CSV export files location
            os.makedirs('export')
            mgenlog = 'Export folder created.'
            genLog(mgenlog)
            print('\t' + mgenlog)              

        if not os.path.isfile(mdbfile):
            mgenlog = 'Mezzmo DB file not found: ' + mdbfile + '.  Please check the config.txt file. '
            genLog(mgenlog)
            print('\t' + mgenlog)            
            mgenlog = 'Mezzmo Folder Manager exiting.'
            genLog(mgenlog)
            print(mgenlog)  
            sys.exit() 

    except Exception as e:
        print (e)
        mgenlog = 'There was a problem checking folders'
        genLog(mgenlog)
        print('\t' + mgenlog)    


def checkCsv(source = '', mezztab = '', criteria = ''):           # Generate CSV files

        if sys.version_info[0] < 3:
            print('\tThe CSV export utility requires Python version 3 or higher')
            exit()    
            
        db = openFolderDB()
        fpart = datetime.now().strftime('%m%d%Y_%H%M%S')
        if mezztab == 'subwatch':
            filename = '.\export\mezfolder_' + source + '_' + fpart + '.csv'
        elif mezztab == 'playlist':
            filename = '.\export\mezplaylist_' + source + '_' + fpart + '.csv'
        else:
            db.close()
            return

        mgenlog = 'CSV file export beginning for - ' + filename
        genLog(mgenlog)

        curm = db.execute('SELECT * FROM mWatchFolders where source = ? and mezzTable = ? \
        and dateAdded = ? ORDER BY ID ASC', (source, mezztab, criteria,))
        recs = curm.fetchall()
        if len(recs) > 0:        
            headers = [i[0] for i in curm.description]      
            writeCSV(filename, headers, recs)
            mgenlog = 'CSV file export completed to - ' + filename
        else:
            mgenlog = 'No matching records found to export.'
        del curm
        db.close()

        genLog(mgenlog)
        print('\n\t' + mgenlog + '\n')   
        time.sleep(5)


def writeCSV(filename, headers, recs):

    try:
        csvFile = csv.writer(open(filename, 'w', encoding = 'utf-8'),
                         delimiter=',', lineterminator='\n',
                         quoting=csv.QUOTE_ALL)
        csvFile.writerow(headers)     # Add the headers and data to the CSV file.
        for row in recs:
            recsencode = []
            for item in range(len(row)):
                if isinstance(row[item], int) or isinstance(row[item], float):  # Convert to strings
                    recitem = str(row[item])
                else:
                    recitem = row[item]
                recsencode.append(recitem) 
            csvFile.writerow(recsencode)               

    except Exception as e:
        print (e)
        mgenlog = 'An error occurred creating the CSV file.'
        genLog(mgenlog)
        print('\t' + mgenlog)


def readFile(importfile):                                            # Read inport file


        mgenlog = 'CSV file import beginning: ' + importfile
        print('\n\t' + mgenlog + '\n')
        genLog(mgenlog)        

        dbf = openFolderDB()

        importfields = ['dateAdded', 'ID', 'source', 'mezzTable', 'SubWatchFolderPath', 'Description',     \
        'PosterFileID', 'PosterFile', 'BackdropFileID', 'BackdropFile', 'ParentFolderID', 'ParentFolder',  \
        'TopLevelWatchFolder', 'ContentRatingID', 'ContentRatingName', 'RatingCountry', 'var1', 'var2',    \
        'var3', 'var4']

        with open(importfile, newline='', encoding="ISO8859") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = next(reader)
            keylist = list(headers.keys())                           # Get CSV column headers
            for i in importfields:                                   # Check for all spreadsheet fields
                if i not in keylist:
                    mgenlog = 'CSV import field: "' + i + '"  missing from spreadsheet: ' + importfile
                    genLog(mgenlog)
                    print('\n\t' + mgenlog)
                    choice = input('\n\n\tEnter to return to main menu  ')
                    dbf.close()
                    return                                        
            #print(str(keylist) + ' ' + str(len(keylist)))
            csvfile.seek(0)                                          # Move back to the beginning of the file
            reader = csv.DictReader(csvfile)                         # Read file again

            currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            count = 0                                                # Record insertion counter

            for row in reader:
                dbf.execute('INSERT into mWatchFolders (dateAdded, ID, source, mezzTable,          \
                SubWatchFolderPath, Description, PosterFileID, PosterFile, BackdropFileID,         \
                BackdropFile, ParentFolderID, ParentFolder, TopLevelWatchFolder, ContentRatingID,  \
                ContentRatingName, RatingCountry, var1, var2, var3, var4)                          \
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',              \
                (currTime, row['ID'], 'import', row['mezzTable'], row['SubWatchFolderPath'],       \
                row['Description'], row['PosterFileID'], row['PosterFile'], row['BackdropFileID'], \
                row['BackdropFile'], row['ParentFolderID'], row['ParentFolder'],                   \
                row['TopLevelWatchFolder'], row['ContentRatingID'], row['ContentRatingName'],      \
                row['RatingCountry'], row['var1'], row['var2'], row['var3'], row['var4'],))
                count += 1

                if count % 100 == 0: 
                    print('\tRecords imported: ' + str(count))
                    dbf.commit()

        dbf.close()

        mgenlog = 'CSV file rows successfully imported: ' + str(count)
        genLog(mgenlog)
        print('\n\t' + mgenlog)
        choice = input('\n\n\tEnter to exit or 0 to return to main menu ?   ')
        if choice == '0':
            return
        else:
            sys.exit()


def checkLogfile():                                   # Checks / trims the size of the logfile

        global tr_config
        logoutfile = tr_config['logoutfile']
        fileh = open(logoutfile, "r+")                #  open log file
        flines = fileh.readlines()
        fcount = len(flines)
        if fcount > 11000:
            fileh.seek(0)
            fileh.truncate()
            fileh.writelines(flines[fcount - 10000:])
        fileh.close()
        mgenlog = 'The number of lines in the logfile is: ' + str(len(flines))
        genLog(mgenlog)  


def checkRecordLimits():                             # Ensure no more than 10 of each type

        dbl = openFolderDB()    

        mgenlog = 'Begin checking record limits'
        #print('\n\t' + mgenlog + '\n')
        genLog(mgenlog)

        dlcurr = dbl.execute('select distinct dateAdded from mWatchFolders where source =   \
        "sync" and mezzTable = "subwatch" order by dateAdded desc, source, mezzTable' )
        dltuples = dlcurr.fetchall()

        if len(dltuples) > 10:
            dbl.execute('DELETE FROM mWatchFolders WHERE source = "sync" and mezzTable =    \
            "subwatch" and dateAdded < ?', (dltuples[9][0],))
            dbl.commit()

        dlcurr = dbl.execute('select distinct dateAdded from mWatchFolders where source =   \
        "import" and mezzTable = "subwatch" order by dateAdded desc, source, mezzTable' )
        dltuples = dlcurr.fetchall() 

        if len(dltuples) > 10:
            dbl.execute('DELETE FROM mWatchFolders WHERE source = "import" and mezzTable =  \
            "subwatch" and dateAdded < ?', (dltuples[9][0],))
            dbl.commit()

        dlcurr = dbl.execute('select distinct dateAdded from mWatchFolders where source =   \
        "sync" and mezzTable = "playlist" order by dateAdded desc, source, mezzTable' )
        dltuples = dlcurr.fetchall()

        if len(dltuples) > 10:
            dbl.execute('DELETE FROM mWatchFolders WHERE source = "sync" and mezzTable =    \
            "playlist" and dateAdded < ?', (dltuples[9][0],))
            dbl.commit()

        dlcurr = dbl.execute('select distinct dateAdded from mWatchFolders where source =   \
        "import" and mezzTable = "playlist" order by dateAdded desc, source, mezzTable' )
        dltuples = dlcurr.fetchall()

        if len(dltuples) > 10:
            dbl.execute('DELETE FROM mWatchFolders WHERE source = "import" and mezzTable =  \
            "playlist" and dateAdded < ?', (dltuples[9][0],))
            dbl.commit()
       
        dbl.close()

        mgenlog = 'Checking record limits completed'
        #print('\n\t' + mgenlog + '\n')
        genLog(mgenlog)


def makeBackups():                                   # Make database backups

    try:
        from sqlite3 import dbapi2 as sqlite
    except:
        from pysqlite2 import dbapi2 as sqlite
    
    try:
        #if len(sysarg1) == 0 or sysarg1.lower() not in 'backup':
        #    return
        DB = 'backups/mezzmo_folders_' + datetime.now().strftime('%m%d%Y-%H%M%S') + '_.db'
        dbout = sqlite.connect(DB)
        dbin = openFolderDB()

        with dbout:
            dbin.backup(dbout, pages=100)
        dbout.close()
        dbin.close()
        mgenlog = 'Mezzmo Folder Manager backup successful: ' + str(DB)
        genLog(mgenlog)
        print('\n\t' + mgenlog) 

    except Exception as e:
        print (e)
        mgenlog = 'An error occurred creating a Mezzmo Folder Manager backup.'
        genLog(mgenlog)
        print('\t' + mgenlog)      


getConfig()                                                  # Read config file                                  
checkDatabase()                                              # Check trailer database 
checkFolders()                                               # Check trailer and temp folder locations
checkLogfile()                                               # Checks / trims the size of the logfile
checkRecordLimits()
checkCommands(sysarg1, sysarg2)                              # Check for valid commands
