class gate:
	def __init__(self,gate_type,x_cord,y_cord,height,width,id_no)	:	#constructor
		self.x_cord=x_cord								#x_cordinate of gate
		self.y_cord=y_cord								#y_cordinate of gate
		self.gate_type=gate_type						#type of gate
		self.height=height									#height of gate
		self.width=width									#width of gate
		self.id_no=id_no									#id_no of gate
		self.input_line=[]									#index of input gate 
		self.output_line=[]									#index of output gate
		self.input=[]											#boolean expressions for  input
		self.output=""										#boolean expression for output
		self.inp_val=[]
		self.out_val=0
	def exp_left(self,exp):
		self.input.append(exp)
gates=[]
def init(temp):
	global original_image
	global x_cord
	global y_cord
	original_image = temp
def insert(obj):
	gates.append(obj)
def insert1(idx,val):
	gates[idx].input_line.append(val)
def insert2(idx,val):
	gates[idx].output_line.append(val)
