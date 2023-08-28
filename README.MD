# G-Code Ripper Version 0.22 (Miimiikiu Custom)

## Description

G-Code-Ripper (originally developed by Scorch Works) is an auto-levelling software for CNC routers.

Generally, G-Code-Ripper stores its information in system memory, which can easily take up 20 or more gigabytes for even 50KB G-Code files using 3x3 probe points, making it nearly impossible to complete. This custom build writes the necessary information to the hard drives as binary files, so memory usage is minimal, and temporary hard drive space required is only around 2GB for a 50KB input file using 3x3 probing points.

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

### manual_probe_generator.py

The probe files generated from g-code-ripper often probe outside of the stock due to lead-ins in the g code, so manual_probe_generator.py accepts the raw stock dimensions and leaves a buffer for safety. While probing, record the z values in stock_probe_W_xx_L_yy_data.txt. You can now use this instead of steps 1-3.

## Changes from Version 0.22

-Replaced large lists with writing binaries to ./gcr_temp to save memory (~2GB free storage space required for a 50KB original G Code file using 3x3 probe points)

-Deletes & replaces ./gcr_temp on restart

-Set default operation to probe

-Read Probe also saves adjusted g code file as a workaround to GUI freezing after reading probe file on some systems

-Disabled plotting to save memory & time

-Added MANUAL_PROBE variable for uses whose machines can't write G31 data to file to allow for manual recording

-Repo now contains manual_probe_generator.py for easier & safer manual probing instead of using MANUAL_PROBE. Input file is not required for this.

## Known Issues

-Only tested on Python 3.8 on Windows x86_64 

-Only tested with Read Probe Data File and Probe Only buttons, not Probe & Cut

-GUI freezes while reading probe file on some systems

-No plots visible

