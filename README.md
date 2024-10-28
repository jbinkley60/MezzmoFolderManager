# Mezzmo Folder Manager
A utility to help you manage your Mezzmo folder and playlist data.  


## Features:

- Sync folder and playlist information from the Mezzmo database
- Export folder and playlist information to CSV file
- Import folder and playlist information for bulk updating of descriptions
- Update Mezzmo folder and playlist information from Mezzmo Folder Manager database
- Maintain up to 10 timestamped copies of all data for quick restoration
- Detailed logging to local logfile
- Menu driven command functions for easy usage
- Command line support for syncing with Mezzmo for automated backup operation  
- Backup Mezzmo Folder Manager database
- Native Python and Windows 64 exe formats

## Installation and usage:

-  Download the Mezzmo Folder Manager release file
-  Unzip file into an empty folder on your system
-  Ensure you have Python installed on Windows.  Minimum version 3.x (native Python usage only)
-  Edit the config.text file with the location of your Mezzmo
   database, logfile name and other settings. 
-  Open a command window and run mezzmo_folders.py or mezzmo_folders.exe<br/>
   See optional command line arguments below. 
   All commands are also available from the Mezzmo Folder Manager menu   
-  Recommended usage sequence is:
   - mezzmo_folders.exe
   - From Mezzmo Folder Manager menu:
   - sync
   - backup
   - export
   - import (only when making changes)
   - update (only when making changes or restoring data) 

   
## Command line arguments:  (Limit 1 at a time)

- <b>sync</b>	        -  Syncs Mezzmo folders and playlists to the Mezzmo Folder Manager database with timestamp. <br>
- <b>backup</b>         -  Creates a time stamped file name backup of the Mezzmo Folder Manager database <br> 
- <b>help</b>           -  Mezzmo Folder Manager help <br>

          
         
 The CSV export utility currently requires Python version 3 when using native Python format.<br/><br/>

See the latest updates on the <a href="https://github.com/jbinkley60/MezzmoTrailerChecker/wiki">Mezzmo Folder Manager wiki</a>.

<br>




