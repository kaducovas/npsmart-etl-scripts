import subprocess
import os
import telepot
import emoji

dir = "/usr/bin/yowsup-master/"
bot = telepot.Bot('194101126:AAFDRz3cHj-Y7YOQsad_ZFRFJKn2qt2oBmQ')
WARNING = emoji.emojize(':warning_sign:')
DISK = emoji.emojize(':minidisc:')

disk = os.statvfs('/etl')
totalBytes = float(disk.f_bsize*disk.f_blocks)
totalAvailSpace = float(disk.f_bsize*disk.f_bavail)

if totalAvailSpace/1024/1024 > 1024:
   message= "There is %.2f GB of available HD space on server 200 (%.1f%% used)" % (totalAvailSpace/1024/1024/1024,(1-totalAvailSpace/totalBytes)*100)

elif totalAvailSpace/1024/1024 < 500:
   message= "WARNING %s\n\nThere is only %.2f MB of available HD space on server 200 (%.1f%% used)" % (WARNING,totalAvailSpace/1024/1024,(1-totalAvailSpace/totalBytes)*100)

else:
   message= "There is %.2f MB of available HD space on server 200 (%.1f%% used)" % (totalAvailSpace/1024/1024,(1-totalAvailSpace/totalBytes)*100)

print(message)

bot.sendMessage('@NPSmart2', message+' '+DISK)
#subprocess.call([dir+"yowsup-cli", "demos", "-l", "5521981601755:ncphLavpww3Hxs7kZ5l9T9JWCeE=", "-s", "5521993094645-1444371705", message, "-M"])

