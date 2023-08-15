# G-Code Ripper Version 0.22 (Miimiikiu Custom)

## Description

G-Code-Ripper (originally developed by Scorch Works) is an auto-levelling software for CNC routers.

Generally, G-Code-Ripper stores its information in system memory, which can easily take up 20 or more gigabytes for even 50KB G-Code files, making it nearly impossible to complete. This custom build writes the necessary information to the hard drives as binary files, so memory usage is minimal, and temporary hard drive space required is only around 2GB for a 50KB input file.

## Usage

1. Start G-Code-Ripper (python3 g-code-ripper.py) 

2. File -> Open G-Code File (You won't see the plot on the GUI)

3. Save G-Code File - Probe Only  

4. Collect probe data on CNC 

5. Exit/Open G-Code-Ripper 

6. File -> Open G-Code File 

7. Read Probe Data File 

8. File is automatically saved to ./myfile_adjusted.ngc (GUI remains frozen/"Calculating..." and it is safe to close at this point) 

9. Remove temp folder: Exit & restart G Code Ripper, then exit. Or Manually delete ./gcr_temp

## Changes from Version 0.22

-Replaced large lists with writing binaries to ./gcr_temp to save memory (~2GB free storage space required for a 50KB original G Code file)

-Deletes & replaces ./gcr_temp on restart

-Set default operation to probe

-Read Probe also saves adjusted g code file as a workaround to GUI freezing after reading probe file

-Disabled plotting to save memory & time

-Added MANUAL_PROBE variable for uses whose machines can't write G31 data to file to allow for manual recording

## Known Issues

-Only tested on Python 3.8 on Windows x86_64 

-Only tested with Read Probe Data File button

-GUI freezes while reading probe file

-No plots visible

