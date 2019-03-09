# Eye-Detection-Tracking
Eye movement detection for Senior Project

This was another robot that was part of our overall Senior Design project at NIU

If you look back at the leap motion, this project also uses sockets to transmit data wirelessly via IP addresses anywhere you 
are connected to WiFi using IoT

We were able to successfully run one program on a computer to get the eye positions and calibrate through an external webcam 
that we tied onto a hat. This allows the user to not have to hold anything while using this. OpenCV was the main part of the 
program to do the filtering.

Then the positions of the eye would send out commands to a raspberry pi attached to a car.We used Haar Cascades which are 
files that have some preset data on eyes and smart learning, and used that data to track an eye over the video stream. We 
applied a few different filters to the video footage that made it black and white, to help determine the pupil area, and which
way the eye was looking. After callibrating it to the users specific eye, we used blink detection, meaning if you blink 3 
times for a certain amount of seconds, the program would start to run.

Once the different directions were tracked (ex. looking left or looking up) we used sockets to submit the readings wireslessly
to a raspberry pi that was on a rc car. The raspberry pi would then take a command such as "turn left" that was outputted from
the computer and run a series of motors (front motor turns left and right, back motor turns forward and backward). It was not 
as complex as the Leap Motion car, and was just a smaller car with smaller servo motors essentially. We also used an AmsPi 
board to control the motors that was connected to the raspberry pi. 

When Downloading the code, you will have to download the xml files that are associated with the code for it to work correctly.















