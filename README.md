  This Python 3 CLI program reads the Hercules prt00e.txt and prt00f.txt output which contains multiple jobs, back to back, and splits each job out to it's own file. It was written for use in the Linux OS. 

  It opens the print files, read-only and can run while Hercules is active. There is a small likelihood that there could be problems reading if Hercules is writing. But only on output, not with the Hercules prt file so it's probably best run between Job execution. However I've never had a problem.

  This program assumes there is a "jobs-00x" subdirectory for each prt file in the "prt" directory because that is where it writes the individual Job files. It will try to create it if it doesn't exist.

Files are named "JobNo-JobName (date&time).txt"
  
I had to add date & time because some Jobs with the same Job Number &  Job Name appear multiple times. Such as the "MF1" job.

  I store & run it in Hercules "prt" subdirectory. It can run in a terminal, by typing './parseJob.py' in the Hercules prt directory, on my system you  can also just double click it in the file manager within that directory. Obviously it must be set as executable. If you run it in a terminal it will provide further information.

  This program makes some assumtions based on what was in my Hercules print  file on the days I wrote and tested it. YMMV!

On my system it's fast...sub second.

