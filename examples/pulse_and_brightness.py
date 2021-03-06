#!/usr/bin/env python

import time
import sys
import pypowermate
import glob

MinSpeed=240	#0
MaxSpeed=280	#512

if __name__ == '__main__':
	if len(sys.argv) > 2 :
		sys.stderr.write('usage: %s [device_path]\n  if no arg, use glob to get first powermate' % sys.argv[0])
		sys.exit(1)
	if len(sys.argv) > 1 :
		device=sys.argv[1]
	else :
		powermates=glob.glob('/dev/input/by-id/*PowerMate*')
		if len(powermates) == 0 :
			print('no powermate found !')
			sys.exit(1)
		device=powermates[0]
	
	
	# open the device
	p = pypowermate.Powermate(device)

	speed = 255
	brightness = 255
	speed_mode = True

	count = 0

	print("- Rotate the knob to test different pulse speeds.")
	print("- Rotate the knob while it's pushed test different brightness levels.")

	while True:
		retval = p.read_event(0) # with no timeout value, the read will wait
		if retval == None :
			time.sleep(0.05)
			count=(count+1)%10
			if count == 0:
				sys.stdout.write('.')
				sys.stdout.flush()
			continue
		else :
			(ts,evt,val) = retval
		if evt == pypowermate.Powermate.EVENT_BUTTON:
			if val == pypowermate.Powermate.BUTTON_UP:
				speed_mode = True
				print("Speed mode activated.")
			else:
				speed_mode = False
				print("Brightness mode activated.")
		elif evt == p.EVENT_ROTATE:
			if speed_mode:
				speed += val
				speed = min(max(speed, MinSpeed), MaxSpeed)
				ispeed=speed
				if speed == MinSpeed :
					ispeed=0
				print("Setting pulse speed %d" % ispeed)
				p.set_pulse(ispeed)
			else:
				brightness += val
				brightness = min(max(brightness, 0), 255)
				print("Setting brightness level %d" % brightness)
				p.set_steady_led(brightness)
		
