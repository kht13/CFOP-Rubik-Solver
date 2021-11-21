from sympy.combinatorics import Permutation

class cube_move:
    """
    cube_move is a class representation of a Rubik's Cube move.
    The move can be a single move instruction or an alogrithm. This
    class is the parent class of RubikConfiguration, which stores all
    the face moves.
    """

    def __init__(self, corPermArr=[[7]],  edgPermArr=[[11]],
                 cenPermArr=[[5]], corOrArr=[0]*8,
                 edgOrArr=[0]*12):
        """
        Load up a move with permutation arrays (cyclic or not) and two orientation arrays.
        The three permutation arrays will be for corners, edges and centers. 
        The two orientation arrays will be for corner and edges.

        Orientation arrays given should be the orientation arrays of the moves when they
        are applied to a start configuration.

        Args:
            corPermArr: Permutation array for corners.
            edgPermArr: Permutation array for edges.
            cenPermArr: Permutation array for centers.
            corOrArr: Orientation array for corners.
            edgOrArr: Orientation array for edges.
        """
    
        self.__cor = Permutation(corPermArr) #Positions of Corners
        self.__edg = Permutation(edgPermArr) #Positions of Edges
        self.__cen = Permutation(cenPermArr) #Positions of Centers (u, b, r, f, l, d)
        self.__corO = corOrArr               #Orientation of Corners
        self.__edgO = edgOrArr               #Orientation of Edges

    def executeMove(self, moveToBeExecuted, reversed=False):
        """
        Execute move specified by moveToBeExecuted which is a cube_move Object.
        If reversed is True, the move must be executed in reverse order with
        reversed directions.

        Args:
            moveToBeExecuted (cube_move): the move that should be executed to the 
            current object. 
            reversed (bool): when True, the moveToBeExecuted is applied in reverse
            order with reversed directions.
        """
        if not isinstance(self, type(moveToBeExecuted)):
            raise Exception("The move to be executed should be a cube_move object.")
        if(not reversed):
            #Apply the permutations
            self.__cen*=moveToBeExecuted.__cen
            self.__cor*=moveToBeExecuted.__cor
            self.__edg*=moveToBeExecuted.__edg

            #Apply rotations as appropriate
            #The process here is to move the orientation to the new position
            #and if the move to be executed rotates some cubies, we also
            #apply it after moving. Since the moveToBeExecuted has orientation
            #arrays for when it is applied to the start configuration, we can
            #just access the orientations with the new index.
            corO=self.__corO[:]
            for index in range(moveToBeExecuted.__cor.size):
                newIndex=moveToBeExecuted.__cor(index)
                corO[newIndex]=self.__corO[index]
                corO[newIndex]+=moveToBeExecuted.__corO[newIndex]
                corO[newIndex]%=3
            self.__corO=corO
            edgO=self.__edgO[:]
            for index in range(moveToBeExecuted.__edg.size):
                newIndex=moveToBeExecuted.__edg(index)
                edgO[newIndex]=self.__edgO[index]
                edgO[newIndex]+=moveToBeExecuted.__edgO[newIndex]
                edgO[newIndex]%=2
            self.__edgO=edgO
        else:
            self.__cen*=~moveToBeExecuted.__cen
            self.__cor*=~moveToBeExecuted.__cor
            self.__edg*=~moveToBeExecuted.__edg

            #Apply rotations as appropriate
            #Since this is for when reversed is True, we will be doing
            #all the things in reverse. So, after the cubies' orientations
            #are moved, we will be subtracting numbers from moveToBeexecuted's
            #orientation array with the oldIndex
            corO=self.__corO[:]
            for index in range(moveToBeExecuted.__cor.size):
                oldIndex=moveToBeExecuted.__cor(index)
                corO[index]=self.__corO[oldIndex]
                corO[index]-=moveToBeExecuted.__corO[oldIndex]
                corO[index]%=3
            self.__corO=corO
            edgO=self.__edgO[:]
            for index in range(moveToBeExecuted.__edg.size):
                oldIndex=moveToBeExecuted.__edg(index)
                edgO[index]=self.__edgO[oldIndex]
                edgO[index]-=moveToBeExecuted.__edgO[oldIndex]
                edgO[index]%=2
            self.__edgO=edgO
        
        return self
        
    def __mul__(self, other):
        """
        Return the resulting configuration when the multiplicand move is executed.
        This only provides a copy and does not mutate the original object.
        """
        if not isinstance(self, type(other)):
            raise Exception("The multiplicand must be a cube_move object.")
        #for some reason, deepcopy (from copy module) of Permutation objects gives empty ones
        cls=type(self)
        selfCopy=cls()
        selfCopy.__cen*=self.__cen
        selfCopy.__edg*=self.__edg
        selfCopy.__cor*=self.__cor
        selfCopy.__corO=self.__corO[:]
        selfCopy.__edgO=self.__edgO[:]
        return selfCopy.executeMove(other)
    
    def __invert__(self):
        """
        Return the move executed in reverse order and direction.
        """
        return cube_move().executeMove(self,reversed=True)
    
    def __pow__(self, n):
        """
        Return the resulting configuration when the base configuration
        is multipled (__mul__) n times.
        """
        if type(n) is not int:
            raise Exception("The exponent must be an integer.")
        #Set up a start configuration
        result=cube_move()
        if n > 0:
            for x in range(n):
                result*=self
        #Negative exponents means inverses
        elif n < 0:
            for x in range(n):
                result*=~self
        #If n is 0, return the start configuration
        return result

    def toString(self):
        configString = (str(self.__cor) + ", "+str(self.__edg) + ", "+str(self.__cen))
        configString = configString +"\n"+str(self.__corO)+"\n"+str(self.__edgO)
        return configString
    
    def getCorners(self, *indices, indexArr=range(8)):
        """
        TODO: change description
        Return the indices and position-orientation tuples of
        the corner cubies as list pairs for the specified indices.
        """
        # corners=[]
        # for x in indices:
        #     if x<0 or x>=8:
        #         continue
        #     pos = self.__cor(x)
        #     corners.append({'index':x, 'pos':pos, 'or':self.__corO[pos]})
        if not indices:
            indices=indexArr
        indices=[x for x in indices if 0<=x<=7] #discard values outside range
        pos=[self.__cor(x) for x in indices]
        or_ = [self.__corO[x] for x in pos]
        return {"indices": indices, "pos": pos, "or":or_}
    
    def getEdges(self, *indices, indexArr=range(12)):
        """
        TODO: change description
        Return the positions and orientations of the edge
        cubies as tuple pairs for the specified indices.
        """
        # edges=[]
        # for x in indices:
        #     if x<0 or x>=11:
        #         continue
        #     pos = self.__edg(x)
        #     edges.append({'index':x, 'pos':pos, 'or':self.__edgO[pos]})
        if not indices:
            indices=indexArr
        indices=[x for x in indices if 0<=x<=11] #discard values outside range
        pos=[self.__edg(x) for x in indices]
        or_ = [self.__edgO[x] for x in pos]
        return {"indices": indices, "pos": pos, "or":or_}
    
    def getCenters(self, *indices, indexArr=range(6)):
        """
        TODO: change description
        Return the positions of the centers cubies
        for the specified indices.
        """
        if not indices:
            indices=indexArr
        indices=[x for x in indices if 0<=x<=5] #discard values outside range
        pos=[self.__cen(x) for x in indices]
        return {"indices": indices, "pos": pos}

if __name__ == "__main__":
    rubik3=cube_move()
    U=cube_move(corPermArr=[[0, 3, 2, 1]], edgPermArr=[[0, 1, 2, 3]])
    D=cube_move(corPermArr=[[4, 5, 6, 7]], edgPermArr=[[8, 11, 10, 9]])
    F=cube_move(corPermArr=[[0, 1, 6, 5]], edgPermArr=[[2, 6, 10, 7]],
                 corOrArr=[1, 2, 0, 0, 0, 2, 1, 0], 
                 edgOrArr=[0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0])
    B=cube_move(corPermArr=[[2, 3, 4, 7]], edgPermArr=[[0, 4, 8, 5]],
                 corOrArr=[0, 0, 1, 2, 1, 0, 0, 2], 
                 edgOrArr=[1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0])
    L=cube_move(corPermArr=[[3, 0, 5, 4]], edgPermArr=[[3, 7, 11, 4]],
                 corOrArr=[2, 0, 0, 1, 2, 1, 0, 0])
    R=cube_move(corPermArr=[[1, 2, 7, 6]], edgPermArr=[[1, 5, 9, 6]],
                 corOrArr=[0, 1, 2, 0, 0, 0, 2, 1])
    M=cube_move(edgPermArr=[[0, 2, 10, 8]], cenPermArr=[[0, 3, 5, 1]],
                 edgOrArr=[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0])
    E=cube_move(edgPermArr=[[4, 7, 6, 5]], cenPermArr=[[1, 4, 3, 2]],
                 edgOrArr=[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0])
    S=cube_move(edgPermArr=[[1, 9, 11, 3]], cenPermArr=[[0, 2, 5, 4]],
                 edgOrArr=[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])

    print((rubik3*R*L*U**2*F*~U*D*F**2*R**2*B**2*L*U**2*~F*~B*U*R**2*D*F**2*U*R**2*U).toString())
    print((rubik3*R*U*~R*~U*R*U*~R*~U*D*R*U*~R*~U*R*U*~R*~U*D*R*U*~R*~U*R*U*~R*~U*D**2).toString())
    
    #"R L U2 F U' D F2 R2 B2 L U2 F' B' U R2 D F2 U R2 U M E M' E' S E S' E'