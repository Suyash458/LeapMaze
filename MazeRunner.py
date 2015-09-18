import Leap
import os,sys,time
import serial,struct
	
	
class Processor(Leap.Listener):

	def get_filtered_angles(self,Pitch,Roll):
		self.Pitch_readings.append(Pitch)
		self.Roll_readings.append(Roll)
		self.Pitch_readings.pop(0)
		self.Roll_readings.pop(0)
		for i in range(20):
			self.Average_Pitch += self.Pitch_readings[i]
			self.Average_Roll += self.Roll_readings[i]
		self.Average_Pitch /= 20
		self.Average_Roll /= 20
		Filtered_Pitch = int((0.9*self.Prev_Pitch) + (0.1*self.Average_Pitch))
		Filtered_Roll = int((0.9*self.Prev_Roll) + (0.1*self.Average_Roll))
		self.Prev_Pitch = self.Average_Pitch
		self.Prev_Roll = self.Average_Roll
		return (Filtered_Pitch, Filtered_Roll)
	
	def initialize(self):
		self.Pitch_readings = []
		self.Roll_readings = []
		for i in range(20):
			self.Pitch_readings.append(0)
			self.Roll_readings.append(0)
		self.Average_Pitch = 0
		self.Average_Roll = 0
		self.Prev_Pitch = 0
		self.Prev_Roll = 0
		self.Port = serial.Serial('COM25',9600,timeout = 0,rtscts = False)
		
	def on_init(self,controller):
		self.initialize()
		print "Initialized."
		
	def on_connect(self,controller):
		print "Connected."
		
	def on_disconnect(self,controller):
			print "Disconnected."
			
	def on_exit(self,controller):
		print "Exited."
		
	def on_frame(self,controller):
		frame = controller.frame()
		oldFrame = controller.frame(10)
		if not frame.hands.is_empty:
			hand = frame.hands[0]
			if hand.rotation_probability(oldFrame) > 0.5:
				normal = hand.palm_normal
				direction = hand.direction
				Pitch = (direction.pitch*Leap.RAD_TO_DEG)
				Roll = (normal.roll*Leap.RAD_TO_DEG)
				Filtered_Pitch, Filtered_Roll = self.get_filtered_angles(Pitch, Roll)
				sync = struct.pack('>b',60)
				A = (struct.pack('>b',Filtered_Pitch))
				B = struct.pack('>b',Filtered_Roll)
				self.Port.write([sync,A,B])
				print "Pitch: " + str(Filtered_Pitch) + " Roll: " + str(Filtered_Roll)
				#time.sleep(0.01)
				time.sleep(0.008)
				#data =  self.Port.readlines()
				#print struct.unpack('>b',data)
				#if(data != []):
				#   print data 
				#self.Port.flushInput()
				#self.Port.flushOutput()		
def main():
	listener = Processor()
	controller = Leap.Controller()
	controller.add_listener(listener)
	print "Press Enter to quit..."
	sys.stdin.readline()
	controller.remove_listener(listener)
	
if __name__ == "__main__":
	main()
            