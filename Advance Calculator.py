num = input("What is your expression? :")

def idxfinder(lst, value):
    '''takes a value and searches for it in a list, returns all the indexes of the value in the given list''' 
    idxop = ''
    startpos = 0
    poslst = []
    
    for idx in lst: #this for loop finds all the indexes of a given value 
        
        if idx == value:#if the idx is the value we're looking for
            idxop = lst.index(value, startpos)#put the index value into this variable
            poslst.append(idxop)#adds the index found into a new list
            startpos = 0#resets the starting position to 0 
            startpos += idxop + 1#the loop will now search for the value from the previous index of the operator found onwards
    
        
    return(poslst)#returns the indexes
        
def calculator(idx, lst, op):
    '''takes the index list of an operator, the list, the operator, and does the required operation'''
    idxleft = 0
    idxright = 0
    leftval = 0
    rightval = 0
   
    for i in idx:#goes through the list of index values for the operator
        idxleft = i - 1#takes the index value of the operator and minus one to find the index of the number on the left side of the operator
        idxright = i + 1#does the same thing for the index value to the right of the operator
        rightval = (lst.pop(idxright))#takes the actual value of the right index by popping it from the list
        leftval = (lst.pop(idxleft))#same thing for the left value 
        if op == '**':#if theres an exponent sign in the list
            answer = (float(leftval)) ** (float(rightval))#take the value to the left of the exponent to the power of the value to the right of the exponent
        if op == '//':#if there is a floor division sign in the list
            '''turns left and right value into floats so that they can get rounded, I did this to avoid an error. Would get an error if the left or right value was not a float'''
            leftval = float(leftval)
            rightval = float(rightval)
            rightval = round(rightval)
            leftval = round(leftval)
            answer = (leftval) // (rightval)#does operation
        if op == '/':#same concept as before
            answer = (float(leftval)) / (float(rightval)) 
        if op == '*':#same concept as before
            answer = (float(leftval)) * (float(rightval))
        
        if op == '+':#same concept as before
            answer = (float(leftval)) + (float(rightval))
        if op == '-':#same concept as before
            answer = (float(leftval)) - (float(rightval))
            
        lst[idxleft] = (str(answer))#turns the value to the left of the operator into the answer of the operation
    
        for e in range(len(idx)):
            #the indexes of the operation signs will shift two units down so i made this for loop to substract 2 from each element in the list of indexes
            #minuses 2 from each number in a list
            idx[e] -= 2  
        
    return(lst)

def bedmas(lst):
    '''Takes a list as a parameter and searches through the list for operation signs in bedmas order, then it does the required calculation using the calculator fucntion'''
    #does bedmas
    leftxp = 0
    rightxp = 0
   
                
    if '**' in lst:
        #first makes a list of all indexes of this specific operator(**) in the list. This is required to do the calculation
        #then uses the calculator function to do the operation 
        idxxpo = idxfinder(lst, '**')#finds the index of the operator
        lst = calculator(idxxpo, lst, '**')#does the calculation and puts the answer in the correct spot
        
    
    if '//' in lst:#same concept as before
        idxfloor = idxfinder(lst, '//')
        lst = calculator(idxfloor, lst, '//')
        
    if '/' in lst:#same concept as before
        idxdiv = idxfinder(lst, '/') 
        lst = calculator(idxdiv, lst, '/')
        
    if '*' in lst:#same concept as before
        idxmult = idxfinder(lst, '*')           
        lst = calculator(idxmult, lst, '*')
        
    if '+' in lst:#same concept as before
        idxplus = idxfinder(lst, '+')
        lst = calculator(idxplus, lst, '+')
        
    if '-' in lst:#same concept as before
        idxminus = idxfinder(lst, '-')
        lst = calculator(idxminus, lst, '-')      
                
    return(lst)#returns the list after bedmas is done

def bracket(thelst):
    '''Searches through the list for any brackets then solves any operations done inside of brackets'''
    todo = []
    start = 0
    end = 0
    y = 0
    realend = 0
    if '(' in thelst:
        #if there is an open bracket in the list
        idxopen = idxfinder(thelst, '(')    #find all the indexes of all open brackets in the list and puts it in another list          
        idxclose = idxfinder(thelst, ')')#find all the indexes of all closed brackets in the list and puts it in another list
        for i in idxopen:
            #takes the elemts between the first open bracket and the first closed bracket and puts it in a different list, and so on until there are no more brackets
            todo.extend(thelst[i+1:idxclose[y]]) #i+1 = index of first value after open bracket and idxclose[y] = index of first closed bracket since y starts off at 0

            todo = xpofloor(todo)#if any exponents between brackets, turn '*', '*' into '**'
            todo = minussign(todo)#checks for minus signs inside the brackets 
            todo = bedmas(todo)#finally does bedmas
           
            
            item = todo.pop(0)#puts the answer into this variable called item
            thelst[i+1] = item#turns the first value after the open bracket into the answer
           
            
            del thelst[i+2:idxclose[y]]#deletes everything else in the brackets except the answer and the brackets
            y +=1#adds 1 to y so that for the next open bracket, the next closed bracket index will be used to create the new todo variable 
            todo.clear()#clear the todo varriable 
            for e in range(len(idxopen)):
                #minus 2 from the lists since it deleted two values from the list
                idxopen[e] -= 2
                idxclose[e] -= 2
         
            
            
            
    return(thelst)     #return the list       
                
            
def xpofloor(lstval):
    '''searches through the list for any any exponents or floor division signs in the list and changes its format from ['*','*'] to ['**'] or from ['/','/'] to ['//']'''
    if '*' in lstval:
        #if there is a multiplication in the list
        idxxp = idxfinder(lstval, '*')#find all indexes of multiplication signs in the list and assign that to this new list
        for xpval in idxxp:
            #for exponent value in index for exponent 
            if lstval[xpval] == '*' and lstval[xpval+1] == '*':
                #if the elemnt next to the multiplication sign is another multiplication sign
                lstval[xpval] = '**'#change the left multiplication sign into to multiplication signs 
                val2 = xpval+1#val2 is the second multiplication sign
                del lstval[val2]#delete second multiplication sign
                for e in range(len(idxxp)):
                    #substracts two from the list of indexes since two indexes were deleted 
                    idxxp[e] -= 2  
    if '/' in lstval:
        #if there are any division signs in the list 
        idxfloor = idxfinder(lstval, '/')#find all indexes of division signs in the list and assings those values to this new list 
        for fval in idxfloor:
            #for floor division value in the index of floor division signs
            if lstval[fval] == '/' and lstval[fval+1] == '/':    
                #if there is another division sign beside the first division sign 
                lstval[fval] = '//'#change the left division sign in to two division signs or into a floor division sign 
                fval2 = fval + 1#fval2 is the second division sign 
                del lstval[fval2]#delete the second division sign 
                for e in range(len(idxfloor)):
                    #substracts two from the list of indexes since two indexes were deleted 
                    idxfloor[e] -= 2
    return(lstval)#returns list 

def clearbrackets(lst):
    '''After simplifying inside brackets, this funtion gets rid of all brackets since there is no need for it anymore after the values inside the brackets are found'''
    bracket1 = idxfinder(lst, '(')#finds the index of all closed brackets 
    
    for brack in bracket1:
        del lst[brack]#deltes all closed brackets in the list 
        for e in range(len(bracket1)):
            #minuses one from the list of closed brackets since one element of the list was deleted 
            bracket1[e] -= 1
    bracket2 = idxfinder(lst, ')')#finds all indexes of open brackets in the list
    for brack2 in bracket2:
        del lst[brack2]#same concept as before 
        for e in range(len(bracket2)):
            bracket2[e] -= 1
    return(lst)

def clearall(lst):
    '''searches through the list for empty spaces and deletes them'''
    emptidx = idxfinder(lst, '')#find all indexes of empty spaces in the list
    for empt in emptidx:
        del lst[empt]#deletes the empty space 
        for e in range(len(emptidx)):#same concept as before
            emptidx[e] -= 1
    return(lst)

def firstminus(lst):
    '''Checks if the first element in the list is a negative sign'''
    if lst[0] == '-':
        #if first element is a negative sign 
        if lst[1] == '(':#if theres a closed bracket after this negative 
            del lst[0]#delete the negative sign 
            lst = minussign(lst)#turns all negative numbers into actual negative numbers 
            lst = bracket(lst)#does all operations inside of brackets
            lst = clearbrackets(lst)#deletes all brackets
            lst.insert(0, '-')#add a negative sign at the front of the list 
            
            
        val = lst.pop(1)#takes the element to the right of the minu sign 
        val = float(val)#turns it into a float 
        realval = (-1)*(val)#multiplies that value by a negative sign
        lst[0] = str(realval)#turns the first element in the list into the answer with a negative sign instead 
    if '(' in lst:
        idxbr = idxfinder(lst, '(')
        for i in idxbr:
            if lst[i+1] == '-':#if there is a negative sign right after a closed bracket ex (-5+6)
                val2 = lst.pop(i+2)#takes the number after the negative sign 
                val2 = int(val2)#turns it into an integer 
                realval2 = (-1)*val2#multiplies it by a negative sign
                lst[i+1] = str(realval2)#replaces the negative sign by the number to the right of the negative sign times a negative sign
  
    return(lst)
        
def minussign(lst):
    '''Checks if there are any negative signs followed by numbers in the list'''
    actualval = 0
    val = 0

    if '-' in lst:
    
        minusidx = idxfinder(lst, '-')
        
        for i in minusidx:
            
            if lst[i-1] == ")" and lst[i+1] == '(':
            #if there is a negative in between brackets like this (5+8)-(8**9)
                return(lst)
            else:
                #take the number to the right of the negative sign
                checkval1 = lst[i+1]
                checkval1 = float(checkval1)
                checkval1 = round(checkval1)
                checkval1 = str(checkval1)
                
                if lst[i-1].isdigit() == False and checkval1.isdigit() == True:#if the value on the left side of the minus sign is not a number and on the righ side, it is:
                    
                    if lst[i-1] == '*' or lst[i-1] == '/' or lst[i-1] == '//' or lst[i-1] == '**':
                        #this deals with cases like this 5*-55 or 5/-55
                       
                        
                        val1 = lst.pop(i+1)#takes the value on the right side of the minus sign as val1
                       
                        val1 = float(val1)#turns it into a float 
                       
                        actualval1 = val1*-1#multiplies it by -1
                        
                   
                        lst[i] = str(actualval1)#replaces the minus sign by the value to the right of the negative sign multiplies by -1
                        for e in range(len(minusidx)):
                            #minus one from the minu sign index list
                            minusidx[e] -= 1
  
    return(lst)

def main(value):
    '''main funtion, sorts the input from user into a list, seperated by operators'''
    newlist = []
    operators = []
    idx = ''
    empty = ''
    numbers = []
    numidx = 1
    y = 0
   
    
    for signs in value:
        if signs.isdigit() == False:
            #if there is anything other than a number in the list, considers it an operator
            operators.extend(signs)#adds that value into this list 

    
    for dig in value:
        while dig.isdigit() == True:
           
            numbers.append(dig) #adds all numbers into this list without operators 
            break
        if dig.isdigit() == False:
            
            numbers.append(',')#if there is a value that is not a number in the list, add a comma at that point in the numbers list
        
 
    empty = empty.join(numbers)#joins all numbers together 
    empty = empty.split(',')#splits the list every time there is a comma (every time there is an operator bassicaly)
    newlist.extend(empty)#adds this to the newlist
    
    #I didn't use replace, i didnt know i could use it so i made my own version
    #since i know the order of the operators all i have to do is add the operator(in order) at every other interval in the list :)
    for opidx in operators:
        
        newlist.insert(numidx, (operators[y]))#insert an operator at every other interval since numidx starts at 1, it will first insert at index 1
        numidx+=2#skips to every other interval in the list
        y+=1#goes tot he next operator in the operators list
    
    
    
    newlist = clearall(newlist)#clears all empty strings in the list
    newlist = firstminus(newlist)#checks if the first value in the list is a minus sign 
    newlist = minussign(newlist)#looks for any negative numbers and attaches the negative infront of a number if necessary 
   
    
    if '(' in newlist:#if there are any brackets in the list 
        newlist = bracket(newlist)#does the operations inside of the brackets
        
  
    newlist = clearbrackets(newlist)#clears all brackets left after values inside of brackets are found    
    newlist = xpofloor(newlist)#checks for any exponents and floor division signs
    #print(newlist)#prints list before bedmas 
    newlist = bedmas(newlist)#does the math IN ORDER!!!
    print(newlist.pop(0))#prints the result

main(num)

print(eval(num))