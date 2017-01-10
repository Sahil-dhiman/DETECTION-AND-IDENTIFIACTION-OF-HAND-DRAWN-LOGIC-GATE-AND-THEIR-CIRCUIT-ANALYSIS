import cv2
import numpy as np
from matplotlib import pyplot as plt
import showfig as sf
import glob as gb
import string
import validate_1 as vl

#class of line
class line:
	def __init__(self,id_no,left,right):												#constructor
		self.id_no=id_no																	#id_no of line	
		self.left_cordinate=left															#left_cordinate of line
		self.right_cordinate=right													#right_cordinate of line
		self.left_gate=-1																		#id_no of left gate attached to line
		self.right_gate=-1																	#id_no of right gate attached to line
		self.done=0																			#done key 
	def insert1(self,left_gate):
		self.left_gate=left_gate
	def insert2(self,right_gate):
		self.right_gate=right_gate

lines=[]																																			#list data structure for storing lines
expression=""																																#expression variable for storing boolean expression of circuit

def input_bool():
    while True:
        try:
            inp = float(input('Enter the input  -:'))
            if inp > 1 or inp < 0:
                raise ValueError
            return bool(inp)
            break
        except ValueError:
            print('Not a valid input, please re-enter.')
        except NameError:
            print('Please enter a bool value !')
        except SyntaxError:
            print('Please enter something, anything!?')

def evaluation(last_line):																												#Function for evaluating boolean expression
	print(last_line)
	gate_no=lines[last_line].left_gate
	for i in gb.gates[gate_no].input_line:																						#Recursivly calling the fn for finding the input vals
		if lines[i].done==0:
			gb.gates[gate_no].inp_val.append(evaluation(lines[i].id_no))
	gate1=gb.gates[gate_no]
	if gate1.gate_type=="AND":
		gate1.out_val=1
		for inp in range(len(gate1.inp_val)):
			gate1.out_val=bool(gate1.out_val) and bool(gate1.inp_val[inp])
	elif gate1.gate_type=="OR":
		gate1.out_val=0
		for inp in range(len(gate1.inp_val)):
			gate1.out_val=bool(gate1.out_val) or bool(gate1.inp_val[inp])
	elif gate1.gate_type=="XOR":
		gate1.out_val=bool(gate1.inp_val[0])^bool(gate1.inp_val[1])
		if(len(gate1.inp_val)==3):
			gate1.out_val=bool(gate1.out_val)^bool(gate1.inp_val[2])
	elif gate1.gate_type=="NAND":
		gate1.out_val=1
		for inp in range(len(gate1.inp_val)):
			gate1.out_val=bool(gate1.out_val)&bool(gate1.inp_val[inp])
		gate1.out_val=not bool(gate1.out_val)
	elif gate1.gate_type=="NOR":
		gate1.out_val=0
		for inp in range(len(gate1.inp_val)):
			gate1.out_val=bool(gate1.out_val)|bool(gate1.inp_val[inp])
		gate1.out_val=not bool(gate1.out_val)
	elif gate1.gate_type=="NXOR":
		gate1.out_val=bool(gate1.inp_val[0])^bool(gate1.inp_val[1])
		if(len(gate1.inp_val)==3):
			gate1.out_val=bool(gate1.out_val)^bool(gate1.inp_val[2])
		gate1.out_val=not bool(gate1.out_val)
	elif gate1.gate_type=="NOT" :
		gate1.out_val=not bool(gate1.inp_val[0])
	return gate1.out_val

def boolean_expression(last_line):																								#Recursive function for boolean expression
	gate_no=lines[last_line].left_gate
	for i in gb.gates[gate_no].input_line:
		if lines[i].done==0:																												#Recursivly calling the fn for finding the input_expressions
			gb.gates[gate_no].input.append(boolean_expression(lines[i].id_no))
#			lines[i].done=1
	gate1=gb.gates[gate_no]
	if gate1.gate_type=="AND":
		gate1.output="("+gate1.input[0]+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+gate1.input[2]
		gate1.output=gate1.output+")"
	elif gate1.gate_type=="OR":
		gate1.output="("+gate1.input[0]+"+"+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+"+"+gate1.input[2]
		gate1.output=gate1.output+")"
	elif gate1.gate_type=="XOR":
		gate1.output="("+gate1.input[0]+"^"+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+"^"+gate1.input[2]
		gate1.output=gate1.output+")"
	elif gate1.gate_type=="NOT":
		gate1.output="(~"+gate1.input[0]+")"
	elif gate1.gate_type=="NAND":
		gate1.output=	"(~("+gate1.input[0]+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+gate1.input[2]
		gate1.output=gate1.output+"))"
	elif gate1.gate_type=="NOR":
		gate1.output="(~("+gate1.input[0]+"+"+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+"+"+gate1.input[2]
		gate1.output=gate1.output+"))"
	elif gate1.gate_type=="NXOR":
		gate1.output="(~("+gate1.input[0]+"^"+gate1.input[1]
		if len(gate1.input)==3:
			gate1.output=gate1.output+"^"+gate1.input[2]
		gate1.output=gate1.output+"))"
	return gate1.output
	###
	
def condition(x1,x2,y1,y2,pt):																																				#condition function for checking if line in inside gate
	if pt[0]<=x2 and pt[0]>=x1 and pt[1]<=y2 and pt[1]>=y1:
		return True
	return False

def line_code(name):
	last_line=0
	img = cv2.imread('image7.png',0)																																	#reading an image containing line 
	cv2.imwrite("circuit1/wire/wires.png", img)
#	sf.showfig(img,plt.get_cmap('gray'))
	ha1,contours,ha2=cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)							#Applying contour to the image
#	print len(contours)
	orginal_image=cv2.imread(name);
	index=0
	for k in contours:																																								#Building line DS
		if vl.validate(k):
			ak=[]
			for i in k:
				flat = [x for sublist in i for x in sublist]
				ak.append(flat)
			ak1=sorted(ak, key=lambda x: (x[0], x[1]))																												#sorting all point and taking two end points of line
			obj=line(index,ak1[0],ak1[-1])
			index+=1
			if (ak1[-1][0]-ak1[0][0]>10):
				lines.append(obj)																																						#Adding line to the lines DS
				for ii in range(ak1[0][1]-20,ak1[0][1]+20):
					orginal_image[ii][ak1[0][0]]=[0,0,255]
					orginal_image[ii][ak1[0][0]+1]=[0,0,255]
					orginal_image[ii][ak1[0][0]-1]=[0,0,255]
				for ii in range(ak1[-1][1] - 20, ak1[-1][1] + 20):
					orginal_image[ii][ak1[-1][0]] = [0, 110, 0]
					orginal_image[ii][ak1[-1][0] + 1] = [0, 110, 0]
					orginal_image[ii][ak1[-1][0] - 1] = [0, 110, 0]


	sf.showfig(orginal_image,None)
	cv2.imwrite("circuit1/wire/wire_endpoints.png", orginal_image)
	lines_temp=sorted(lines,key=lambda x: x.left_cordinate[1])																						#sorting lines according to y_cordinates of line
#	print(len(gb.gates))
	for g in gb.gates:
		idx=g.id_no
		for li in lines_temp:
			if condition(g.x_cord-20,g.x_cord+5,g.y_cord-5,g.y_cord+g.height+5,li.right_cordinate)==True:													#left cordinate
				gb.insert1(idx,li.id_no)																																											#Adding line to gate DS
				lines[li.id_no].insert2(idx)																																										#Adding gate to line DS
			if condition(g.x_cord,g.x_cord+g.width+10,g.y_cord-5,g.y_cord+g.height+5,li.left_cordinate)==True:										#right cordinate
				gb.insert2(idx,li.id_no)																																											#Adding line to gate DS
				lines[li.id_no].insert1(idx)																																										#Adding gate to line DS
	
	print("GATES DATA STRUCTURE")																																								#printing gate data strucure attribues
	for g in gb.gates:
		print(str(g.id_no)+" "+g.gate_type+" ")
		print("The dimension of gate-:"+str(g.x_cord)+" "+str(g.y_cord)+" "+str(g.width)+" "+str(g.height))
		print("The inputs lines of the gate are-:"+str(g.input_line))
		print("The output line of the gate is-:"+str(g.output_line))
		print
		
	print
	print("LINES DATA STRUCTURE")																																									#printing line data strucure attribues
	for i in lines:
		print (str(i.id_no)+" "+str(i.left_cordinate)+" "+str(i.right_cordinate)+" "+str(i.left_gate)+" "+str(i.right_gate))

	print
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	input_var=list(string.ascii_uppercase)
	for i in lines_temp:																																																						
		if i.right_gate==-1:																												#finding last line
			last_line=i.id_no
		if(i.left_gate==-1):																																															#Assigning labels to all inputs
			i.done=1
			gb.gates[i.right_gate].exp_left(input_var[0])																																			#Adding inputs to the line DS
			cv2.putText(gb.original_image,input_var[0],(i.left_cordinate[0]-50,i.left_cordinate[1]+10), font, 2,(0,0,255),3,cv2.LINE_AA)		#Putting lable for inputs to the logic_ciruit
			del input_var[0]

	print(last_line)
	expression=boolean_expression(last_line)																																						#Computing expression of logic_circuit
	print
	print("The boolean expression for the circuit is-:"+gb.gates[lines[last_line].left_gate].output)
	print
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(gb.original_image,expression,(800,1000), font, 1,(0,0,255),3,cv2.LINE_AA)																			#Putting expression on the input_image
	sf.showfig(gb.original_image, None)
	cv2.imwrite("circuit1/final_result/result.png", gb.original_image)
	for i in lines_temp:
	    if(i.left_gate==-1):																																															#Assigning labels to all inputs
                gb.gates[i.right_gate].inp_val.append(input_bool())																																		#Taking inputs for logic gate			del input_var[0]
	print ("The above inputs to the circuit gives output-: " + str(evaluation(last_line)))																					#Evaluating the expression on the inputs
	print
	print("GATES DATA STRUCTURE")																																								#printing gate data strucure attribues
	for g in gb.gates:
		print(g.gate_type)
		print(g.inp_val)
		print(g.out_val)
