import math

class vec:
    #init method - vector w/ three components
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    #function to return the vector as a string    
    def toString(self):
        return("<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">")
    
    #addition (of infinitely many vectors)
    def vecAdd(*args): #takes as many inputs as you need
        result = vec(0,0,0) #start the result at 0
        for i in args: #repeats the process for each inputted vector
            result.x += i.x
            result.y += i.y
            result.z += i.z
        return result
    
    #addition replace (of infinitely many vectors)
    def vecAddRep(v1, *args): #same process as above for multiple inputs, except the first input is always the vector being replaced
        for i in args:
            v1.x += i.x
            v1.y += i.y
            v1.z += i.z 
        #don't need to return anything bc you're replacing the original value
        #this should be the same for all of the "replace" functions
    
    #basic operations after this follow a similar blueprint
    
    #subtraction
    def vecSub(v1, v2):
        result = vec(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        return result
    
    #subtraction replace
    def vecSubRep(v1, v2):
        v1.x -= v2.x
        v1.y -= v2.y
        v1.z -= v2.z
    
    #scalar multiplication
    def vecMult(v1, s):
        result = vec(v1.x * s, v1.y * s, v1.z * s)
        return result
    
    #scalar multiplication replace
    def vecMultRep(v1, s):
        v1.x *= s
        v1.y *= s
        v1.z *= s
    
    #scalar division
    def vecDiv(v1, s):
        result = vec(v1.x / s, v1.y / s, v1.z / s)
        return result
    
    #scalar division replace
    def vecDivRep(v1, s):
        v1.x /= s
        v1.y /= s
        v1.z /= s
    
    #magnitude
    def vecMag(v1):
        result = math.sqrt((v1.x**2)+(v1.y**2)+(v1.z**2)) #square each component, add them together, then take the sqrt of all of that
        return result
    
    #normalize
    def vecNorm(v1):
        result = vec.vecDiv(v1, vec.vecMag(v1)) #the vector divided by its magnitude - turns it into a unit vector in the same direction
        return result
    
    #normalize replace
    def vecNormRep(v1):
        vSub = vec.vecDiv(v1, vec.vecMag(v1)) #create a substitute vector to perform the same operation as above
        v1.x = vSub.x #then replace v1's values with vSub's values
        v1.y = vSub.y
        v1.z = vSub.z
        #this method can be used for all the "replace" operations, but it's not ideal for the basic operations
        #you need to do this because otherwise the value of vec.vecMag(v1) changes with each component addressed
    
    #dot product
    def vecDot(v1, v2):
        result = (v1.x*v2.x)+(v1.y*v2.y)+(v1.z*v2.z)
        return result #returns a value, not a vector
    
    #cross product
    def vecCross(v1, v2):
        result = vec(0,0,0) #I split this into each component to make it easier to read
        result.x += ((v1.y*v2.z)-(v1.z*v2.y))
        result.y += ((v1.z*v2.x)-(v1.x*v2.z))
        result.z += ((v1.x*v2.y)-(v1.y*v2.x))
        return result #returns a vector, not a value
    
    #cross product replace
    def vecCrossRep(v1, v2):
        v1.x += ((v1.y*v2.z)-(v1.z*v2.y))
        v1.y += ((v1.z*v2.x)-(v1.x*v2.z))
        v1.z += ((v1.x*v2.y)-(v1.y*v2.x))
 
    #angle between 2 vectors in radians
    def vecAngle(v1, v2):
        angle = math.acos(vec.vecDot(v1, v2)/(vec.vecMag(v1)*vec.vecMag(v2))) #v1 dot v2 / |v1| * |v2| = cos theta
        return angle #returns a value in radians

    def vecRotate(v1, theta):
        result = vec(v1.x*math.cos(theta)+v1.y*math.sin(theta),v1.y*math.cos(theta)-v1.x*math.sin(theta),0)
        return result

    def vecRotateRep(v1, theta):
        v1 = vec(v1.x*math.cos(theta)+v1.y*math.sin(theta),v1.y*math.cos(theta)-v1.x*math.sin(theta),0)