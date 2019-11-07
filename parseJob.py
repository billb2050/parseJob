#!/usr/bin/env python
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

  Files are named "JobName-JobNo (date&time).txt"
  
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
FILEIN = "prt00e.txt"

fi = open(FILEIN, "r")
#fo = open(FILEOUT, "w")
# Create "jobs" subdirectory if it doesn't exist
subdir="jobs"
if not os.path.exists(subdir):
    os.makedirs(subdir)
tmpFil=subdir+"/tmp"+str(int(time.time()))+".txt"
ln=0
filCnt=0
while 1:
  line = fi.readline()
  if not line: break
  ln=ln+1
  LineOut=line[:]

  if start:
    #print("Temp "+tmpFil)
    fo = open(tmpFil, "w")
    filCnt+=1
    start=False

  if LineOut[:12]=='****A  START':
    endCnt=0
    #print(LineOut)
    job=LineOut[19:23]
    jobName=LineOut[24:33]
    timeDate=LineOut[67:88]
    ofile=jobName.strip()+'-'+job.strip()+' ('+timeDate.strip()+').txt'

  fo.write(LineOut)

  if LineOut[:11]=='****A   END':
    endCnt+=1
    lastLine=ln
    if endCnt>3:
      firstLine=lastLine+1
      fo.close()
      print("Wrote "+ofile)
      os.rename(tmpFil, "jobs/"+ofile)
      start=True

os.remove(tmpFil)      # Remove last temp file
fi.close()
fo.close()
print(str(ln) + " lines read.")
print(str(filCnt-1) + " Jobs written.")
