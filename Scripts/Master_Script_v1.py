import sys
import clr
import time
import threading
from math import *
import MissionPlanner #import *

clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class

# Return_To_Launch is Working
def Return_To_Launch(user_alt):
	if user_alt==1:
		Script.ChangeParam("RTL_ALT",cs.alt*100)
		print "User RTL altitude set"
	else:
		Script.ChangeParam("RTL_ALT",2000)
		print "Default RTL altitude set"
	Script.ChangeMode("RTL")
	print "Returning to Launch"
	
	return True

# check_position_outer is working (field test pending)
def check_position_outer(lat,lng,alt,tol):
	distance=10
	print "Checking Outer Precision"
	while (distance>tol):
		dlat=(cs.lat-lat)*pi/180
		dlng=(cs.lng-lng)*pi/180
		a=(sin(dlat/2))**2+cos(cs.lat*pi/180)*cos(lat*pi/180)*(sin(dlng/2))**2
		c=2*atan2(sqrt(a),sqrt(1-a))
		d=6378100*c
		distance=sqrt((d**2)+(cs.alt-alt)**2)	
	print "Outer Precision Achieved"
	return True

# check_position_inner is working (field test pending)	
def check_position_inner(lat,lng,alt,tol,timeout):
	timein=0;
	distance=10
	print "Checking Inner Precision"
	while (distance>tol):
		dlat=(cs.lat-lat)*pi/180
		dlng=(cs.lng-lng)*pi/180
		a=(sin(dlat/2))**2+cos(cs.lat*pi/180)*cos(lat*pi/180)*(sin(dlng/2))**2
		c=2*atan2(sqrt(a),sqrt(1-a))
		d=6378100*c
		distance=sqrt((d**2)+(cs.alt-alt)**2)
		timein=timein+5
		if(timein>timeout):
			return True
	return True

#MAIN	

# Initial Set up

print "Arming Motors"
armstatus=Script.arm_motors(20000)

if(armstatus):
	print "Motors Armed"
	
else:
	sys.exit(0)

Script.Sleep(5)
Script.SendRC(3,2000,True)
Script.Sleep(1000)


#_______EDIT ACCODRDING TO MISSION_______ Switch "Guided" to "Stabilize" when doing vector controlling

# Guided Mode on
Script.ChangeMode("Guided")
print "Guided Mode on"
item = MissionPlanner.Utilities.Locationwp()

lat = 37.871460                                          
lng = -122.317564                                       
alt = 8

MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)     
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)  
print 'WP 1 set'
MAV.setGuidedModeWP(item)                                    
print 'Going to WP 1'

# check_position_outer(lat,lng,alt,3)
# check_position_inner(lat,lng,alt,cs.hdop,10000)

time.sleep(20) # Use this if check_position_inner and check_position_outer fail
	
print 'Ready for next WP'
	
lat = lat+.0003
lng = lng
alt = alt
MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)
print 'WP 2 set'
MAV.setGuidedModeWP(item)
print 'Going to WP 2'

# check_position_outer(lat,lng,alt,3)
# check_position_inner(lat,lng,alt,cs.hdop,10000)

time.sleep(20) # Use this if check_position_inner and check_position_outer fail

print "Reached WP 2"

#______End Mission______

# Ending Sequence
Return_To_Launch(1); # 1. Return from same altitude 0. Use altitude of 20m (Default: Use altitude of 20m)
time.sleep(300)
