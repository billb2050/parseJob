#!/usr/bin/env python3
"""
  This Python 3 CLI program reads the Hercules prt00e.txt from MVS
  (tk4- in my case) output which contains multiple jobs, back to back, 
  and splits each job out to it's own file. It was  written for use in
  the Linux OS. 

  It opens the print file, read-only and can run while Hercules is active.
  There is maybe a likelihood that there could be problems reading while
  Hercules is writing. So it's probably best run between Job execution.

  This program extracts the individual jobs into a "jobs" subdirectory, 
  which It will create it if it doesn't exist in the "prt" directory. .

  Files are named "JobNo-JobName(date&time).txt"
  
  I had to add date & time because some Jobs with the same Job Name & 
  Job Number appear multiple times. Such as the "MF1" job. This program 
  makes some assumtions based on what was in my Hercules print file on 
  the day I wrote it. YMMV!

  I store & run it in Hercules "prt" subdirectory. It can run in a terminal,
  by typing './parseJob.py' in the Hercules prt directory, on my system you 
  can also just double click it in the file manager within that directory. 
  Obviously it must be set as executable. If you run it in a terminal it will
  provide further information.

  It's fast
  Read a 7MB+, 80322 line prt file and wrote (extracted) 42 files (jobs)
  in less than a second.

  By: Bill Blasingim
  On: 10/29/2019

prt002.txt (SYSOUT=X, when released),
prt00e.txt (SYSOUT=A) 
prt00f.txt (SYSOUT=Z) in folder tk4-/prt.

  11/09/2019  Process prt00e and prt00f also.
              Change open because of special characters in prt00f
  02/27/2021  Fix 'Written' count
  03/16/2021  Check if print file exists
  
"""
import os, string, time
cr=chr(13)	# Carriage return
lf=chr(10)	# Line Feed
crlf=cr+lf
nl="\n"	# New line
start=True
end=False
endCnt=0
lastLine=0
firstLine=1
jobs = {}
#tmpFil=subdir+"tmp"+str(int(time.time()))+".txt"
tmpFil="tmp"+str(int(time.time()))+".txt" #create temp workfile
#CUUs=['00e','00f','002']
CUUs=['00e','00f']

for cuu in CUUs:
  start=True
  end=False      
  FILEIN = "prt"+cuu+".txt"
  print("\nReading "+FILEIN)
  alpha='A'
  if FILEIN[5:6]=='f':
    alpha='Z'

  #fi = open(FILEIN, "r")
  try:
    fi = open(FILEIN, "r", encoding = "ISO-8859-1")
  except IOError:
    print("File "+FILEIN+" does not exist!")
    continue    
  # Create "jobs" subdirectory if it doesn't exist
  subdir="jobs"+"-"+cuu+"/"
  if not os.path.exists(subdir):
      os.makedirs(subdir)

  ln=0
  filCnt=0
  while 1:
    line = fi.readline()
    if not line: break
    ln=ln+1
    LineOut=line[:]

    if start:
      fo = open(tmpFil, "w")
      filCnt+=1
      start=False

    if LineOut[:12]=='****'+alpha+'  START':
      endCnt=0
      job=LineOut[17:23]
      jobName=LineOut[24:33]
      timeDate=LineOut[67:88]
      # File name = job# then job name
      ofile=job.strip()+'-'+jobName.strip()+' ('+timeDate.strip()+').txt'

    fo.write(LineOut)

    if LineOut[:11]=='****'+alpha+'   END':
      endCnt+=1
      lastLine=ln
      if endCnt>3:
        firstLine=lastLine+1
        fo.close()
        print("Wrote "+ofile)
        os.rename(tmpFil, subdir+ofile)
        start=True
  print(str(ln) + " lines read.")
  print(str(filCnt-1) + " Jobs written.")

os.remove(tmpFil)      # Remove last temp file
fi.close()
fo.close()
