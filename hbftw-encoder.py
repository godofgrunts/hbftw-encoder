import os, subprocess, time

def ensureDir(x):
	#Check to see if the destination\shortName directory exist. If it doesn't exist, we're going to make it.
	dir = os.path.dirname(x)
	if not os.path.exists(dir):
		os.makedirs(dir)

def encodeVid(v,d,s,x,y):
	#This is where the magic happens!
	#I don't know why I declared epNumber way up here. Nice to have the variables up top I guess.
	#Need to decided if I want to have all the variables up here or not.
	epNumber = 0

	for filename in os.listdir(v):
		#Currently, the only HandBrakeCLI that I have is 64 bit. I need to get the 32 bit files and somehow seperate them, or I could just provided two downloads I suppose.
		hbcli = "handbrake\HandBrakeCLI.exe"
	
		#Reminder: filename is being created in the FOR loop via the directory list.
		source = v + "\\" + filename
		scan = [hbcli, "-i", source, "--scan"] 
		
		#This is some bullshit that I found on the internet to write my stdout to a file. I have no idea how this works and should really figure it out.
		
		with open('output.txt', 'wt') as output_f:
			p = subprocess.Popen(scan, stdout=output_f, stderr=output_f)
			time.sleep(3) #For some reason, Python will continue to the next line of code even though the file hasn't been writen yet... I assume this is because subprecoess is passing the code to a different thread or something...
			#print("File should be written.") #For debugging purposes.
		f = open('output.txt', 'r') # I seem to have to open the file again even though I just did as output_f. I think this is part of the same issue I'm patching via time.sleep
		string = f.read()
		f.close()
		
		#Feel pretty good about this one. Checks to see if sSplit2str[-1] return a number (should be a track number). If the partition doesn't get Japanese, sSplit2str[-1] will be a period which != an interger.
		try:
			audioSplit = string.partition(", Japanese")
			aSplit2str = "{}".format(audioSplit[0])
			audioTrack = aSplit2str[-1]
			print(audioTrack)
			val = int(audioTrack)
			
		except ValueError:
			audioSplit = string.partition(", Unknown") 
			aSplit2str = "{}".format(audioSplit[0])
			audioTrack = aSplit2str[-1]
			val = int(audioTrack)
			
		
		
		#Feel pretty good about this one. Checks to see if sSplit2str[-1] return a number (should be a track number). If the partition doesn't get English, sSplit2str[-1] will be a period which != an interger.
		try:
			subtitleSplit = string.partition(", English (iso639-2: eng) (Text)") 
			sSplit2str = "{}".format(subtitleSplit[0])
			subtitleTrack = sSplit2str[-1]
			val = int(subtitleTrack)
			
		except ValueError:
			subtitleSplit = string.partition(", Unknown (iso639-2: und) (Text)") #I really need to learn regex TODO: Make an exception for Unknown languages. Will fail if language isn't labeled as English.
			sSplit2str = "{}".format(subtitleSplit[0])
			subtitleTrack = sSplit2str[-1]
			val = int(subtitleTrack)
			
		
		epNumber = epNumber + 1
		#print("Encoding file : " + filename) #I thought this would be nice to have, but you never seen it because handbrake takes up ALL the space.
		destination = d + s + "_" + str(epNumber) + "_" + "ns.mkv" #d estination + s hort name + _ + epNumber (changed to a string) + ns.mkv which is for animeftw.tv
		#Just a reminder, any argument coming after -o is ignored!
		encode = [hbcli, "-i", source, "-f", "mkv", "--height", str(x), "--width", str(y), "-e", "x264", "--x264-tune", "animation", "-a", audioTrack, "-2", "-T", "-b", "600", "-E", "faac", "-B", "128", "-s", subtitleTrack,"--subtitle-burned", subtitleTrack, "-o", destination]
		subprocess.call(encode)

def main():
	print("Please insert path directory to anime (Ex. D:\Finshed\Dragon Ball Z): ")
	path = input()
	print("Please insert destination directory (Ex. D:\Encoded\Anime): ")
	dest = input()
	print("Please input short name (Ex. dbz): ")
	shortName = input()
	
	#This section allows me to take advantage of input() returning a string and check to see if the user put in an interger
	x = 0
	while x != 1:
		#TODO: Make resx and resy give results based on --scan
		print("Please input height (Default 480): ")
		resx = input()
		if resx != "":	
			try:
				val = int(resx)
				x = 1
			except ValueError:
				print("Not an interger... Please try again.")
				x = 0
		else:
			resx = 480
			x = 1
	
	y = 0
	while y != 1:
		print("Please input width (Default 848): ")
		resy = input()
		if resy != "":
			try:
				val = int(resy)
				y = 1
			except ValueError:
				print("Not an interger... Please try again.")
				x = 0
		else:
			resy = 848
			y = 1
	
	newDest = dest + "\\" + shortName + "\\"
	
	ensureDir(newDest)
	encodeVid(path,newDest,shortName,resx,resy)


main()




