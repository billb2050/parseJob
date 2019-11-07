#parseJob
  This Python 3 CLI program reads the Hercules prt00e.txt output which contains  multiple jobs, back to back, and splits each job out to it's own file. It was written for use in the Linux OS. 

  It opens the print file, read-only and can run while Hercules is active. There is maybe a likelihood that there could be problems reading while Hercules is writing. So it's probably best run between Job execution.

  This program assumes there is a "jobs" subdirectory in the "prt" directory because that is where it writes the individual Job files. It will try to create it if it doesn't exist.

Files are named "JobName-JobNo (date&time).txt"
  
I had to add date & time because some Jobs with the same  Job Name & Job Number appear multiple times. Such as the "MF1" job.

  This program makes some assumtions based on what was in my Hercules print  file on the day I wrote it. YMMV!

  It's fast
  Read a 7MB+, 80322 line prt file and wrote (extracted) 42 files (jobs)
  in less than a second.
