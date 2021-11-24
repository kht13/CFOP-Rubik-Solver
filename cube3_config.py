from cube_move import cube_move
from types import SimpleNamespace
import re, random

class cube3_config(cube_move):
    """
    This class stores the configuration of a 3x3x3 Rubik's Cube.
    This includes the cube_move objects with all the possible
    single moves (moves with only one letter instruction).
    TODO: adjust description
    """
    _centers=["U", "B", "R", "F", "L", "D"]
    _centersCol=["Y", "B", "O", "G", "R", "W"]
    _startingAlg=""

    def __init__(self):
        """
        Constructs a cube3_config object which contains the starting
        configuration of a 3x3x3 Rubik's Cube.
        """
        super().__init__(corPermArr=[[7]],  edgPermArr=[[11]],
                         cenPermArr=[[5]], corOrArr=[0]*8,
                         edgOrArr=[0]*12)
    
    @classmethod
    def fromAlgorithm(cls, startingAlg=""):
        """
        Construct a cube3_config object from given algorithm.

        Args:
            startingAlg (str): A 3x3 Rubik's Cube algorithm
        """
        cube=cls()
        cube._startingAlg+=startingAlg
        return cube.apply(startingAlg)

    @classmethod
    def fromConfiguration(cls, configDict={}):
        """
        Construct a cube3_config object from the given 3x3x3
        Rubik's Cube configuration. The configuration should be
        a dict containing 6 strings with keys corresponding to
        the faces of the cube: F, U, D, L, R and B. Each string
        must be of length 9, containing the colors of each visible
        face of all the cubies belonging to the respective face.
        """
        return cls().changeConfiguration(configDict)

    @property
    def startingAlg(self):
        return self._startingAlg
    
    @property
    def configDict(self):
        """
        ConfigDict is the configuration of the cube stored in
        a dict with keys being letters representing the faces 
        of the cube and the values being strings of length 9.
        """
        origCor=['ufl', 'urf', 'ubr', 'ulb', 
                 'dbl', 'dlf', 'dfr', 'drb']
        origEdg=['ub', 'ur', 'uf', 'ul', 'bl', 'br',
                 'fr', 'fl', 'db', 'dr', 'df', 'dl']

        corDict=self.getCorners()
        edgDict=self.getEdges()
        cenDict=self.getCenters()

        corners=['']*8
        edges=['']*12
        centers=['']*6

        for focus in range(3):
            new_li=orig_li=target_dict=None
            if focus==0:    #we will focus on corners
                target_dict=corDict
                orig_li=origCor
                new_li=corners
            elif focus==1:  #we will focus on edges
                target_dict=edgDict
                orig_li=origEdg
                new_li=edges
            elif focus==2:  #we will focus on centers
                target_dict=cenDict
                orig_li=list(map(lambda x: x.lower(), self._centers))
                new_li=centers
            for i in range(len(orig_li)):
                if focus!=2:    #if the focus is on centers, we don't need to rotate strings
                    n=target_dict['or'][i]
                    # rotate the string left (clockwise) n times (orientation)
                    # and assign
                    new_li[target_dict['pos'][i]]=orig_li[i][n:] + orig_li[i][:n]
                else:
                    new_li[target_dict['pos'][i]]=orig_li[i]

        #ordered arrays which stores face letters of each cubie for each face
        U = [corners[3][0],  edges[0][0], corners[2][0],
               edges[3][0],   centers[0],   edges[1][0], 
             corners[0][0],  edges[2][0], corners[1][0]]
 
        B = [corners[2][1],  edges[0][1], corners[3][2],
               edges[5][0],   centers[1],   edges[4][0], 
             corners[7][2],  edges[8][1], corners[4][1]]
 
        R = [corners[1][1],  edges[1][1], corners[2][2],
               edges[6][1],   centers[2],   edges[5][1], 
             corners[6][2],  edges[9][1], corners[7][1]]
 
        F = [corners[0][1],  edges[2][1], corners[1][2],
               edges[7][0],   centers[3],   edges[6][0], 
             corners[5][2], edges[10][1], corners[6][1]]
 
        L = [corners[3][1],  edges[3][1], corners[0][2],
               edges[4][1],   centers[4],   edges[7][1], 
             corners[4][2], edges[11][1], corners[5][1]]
 
        D = [corners[5][0], edges[10][0], corners[6][0],
              edges[11][0],   centers[5],   edges[9][0], 
             corners[4][0],  edges[8][0], corners[7][0]]
        
        #ordered arrays to dict with 6 string values, each having length 9
        cube = {
            'U': ''.join(U), 'B': ''.join(B), 
            'R': ''.join(R), 'F': ''.join(F), 
            'L': ''.join(L), 'D': ''.join(D)
        }

        #replace face letters with color letters, which are stored in the
        #cube3_config class. The strings in the dict are already lower cases.
        for key, val in cube.items():
            for i in range(len(self._centers)):
                if self._centers[i].lower() in val:
                    val=val.replace(self._centers[i].lower(),self._centersCol[i])
            cube[key]=val

        return cube
    
    @configDict.setter 
    def configDict(self, value):
        self.changeConfiguration(value)

    #one-layer moves
    cubeMoveList={
    'U':cube_move(corPermArr=[[0, 3, 2, 1]], edgPermArr=[[0, 1, 2, 3]]),
    'D':cube_move(corPermArr=[[4, 5, 6, 7]], edgPermArr=[[8, 11, 10, 9]]),
    'F':cube_move(corPermArr=[[0, 1, 6, 5]], edgPermArr=[[2, 6, 10, 7]],
                  corOrArr=[1, 2, 0, 0, 0, 2, 1, 0], 
                  edgOrArr=[0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0]),
    'B':cube_move(corPermArr=[[2, 3, 4, 7]], edgPermArr=[[0, 4, 8, 5]],
                  corOrArr=[0, 0, 1, 2, 1, 0, 0, 2], 
                  edgOrArr=[1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]),
    'L':cube_move(corPermArr=[[3, 0, 5, 4]], edgPermArr=[[3, 7, 11, 4]],
                  corOrArr=[2, 0, 0, 1, 2, 1, 0, 0]),
    'R':cube_move(corPermArr=[[1, 2, 7, 6]], edgPermArr=[[1, 5, 9, 6]],
                  corOrArr=[0, 1, 2, 0, 0, 0, 2, 1]),
    'M':cube_move(edgPermArr=[[0, 2, 10, 8]], cenPermArr=[[0, 3, 5, 1]],
                  edgOrArr=[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0]),
    'E':cube_move(edgPermArr=[[4, 7, 6, 5]], cenPermArr=[[1, 4, 3, 2]],
                  edgOrArr=[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]),
    'S':cube_move(edgPermArr=[[1, 9, 11, 3]], cenPermArr=[[0, 2, 5, 4]],
                  edgOrArr=[0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1])
    }

    #two-layer moves
    cubeMoveList['u']=cubeMoveList['U']*~cubeMoveList['E']
    cubeMoveList['d']=cubeMoveList['D']* cubeMoveList['E']
    cubeMoveList['l']=cubeMoveList['L']* cubeMoveList['M']
    cubeMoveList['r']=cubeMoveList['R']*~cubeMoveList['M']
    cubeMoveList['f']=cubeMoveList['F']* cubeMoveList['S']
    cubeMoveList['b']=cubeMoveList['B']*~cubeMoveList['S']

    #three-layer moves or whole cube rotatation
    cubeMoveList['x']=cubeMoveList['R']*~cubeMoveList['l']
    cubeMoveList['y']=cubeMoveList['U']*~cubeMoveList['d']
    cubeMoveList['z']=cubeMoveList['f']*~cubeMoveList['B']
    cubeMoveList['X']=cubeMoveList['x']
    cubeMoveList['Y']=cubeMoveList['y']
    cubeMoveList['Z']=cubeMoveList['z']

    def changeConfiguration(self, configDict={}):
        """
        Change the current cube's configuration to that provided. 
        The configuration should be a dict containing 6 strings with 
        keys corresponding to the faces of the cube: F, U, D, L, R 
        and B. Each string must be of length 9, containing the colors 
        of each visible face of all the cubies belonging to the 
        respective face.
        """
        #reset the cube to starting configuration
        self.executeMove(~self)

        #set up variables
        corPermArr=[0]*8
        corOrArr=[0]*8
        edgPermArr=[0]*12
        edgOrArr=[0]*12

        cube=SimpleNamespace(**configDict)
        _centersCol=[cube.U[4].upper(), cube.B[4].upper(),
                     cube.R[4].upper(), cube.F[4].upper(), 
                     cube.L[4].upper(), cube.D[4].upper()]

        #Replace the color letters with face letters. 
        for key, val in cube.__dict__.items():
            valLower=val.lower()
            for i in range(len(_centersCol)):
                if _centersCol[i].lower() in valLower:
                    valLower=valLower.replace(_centersCol[i].lower(),self._centers[i])
            cube.__dict__[key]=valLower

        self._centersCol=_centersCol
        
        # array describing the corners. Each element has
        # a string of length 3, recording the faces of
        # the corner cubies in clockwise direction starting
        # from the U or D face of the CUBE.
        corners=[
            "".join([cube.U[6], cube.F[0], cube.L[2]]),
            "".join([cube.U[8], cube.R[0], cube.F[2]]),
            "".join([cube.U[2], cube.B[0], cube.R[2]]),
            "".join([cube.U[0], cube.L[0], cube.B[2]]),
            "".join([cube.D[6], cube.B[8], cube.L[6]]),
            "".join([cube.D[0], cube.L[8], cube.F[6]]),
            "".join([cube.D[2], cube.F[8], cube.R[6]]),
            "".join([cube.D[8], cube.R[8], cube.B[6]])
        ]
        # array containing original positions for corners
        # Since this array is not for orientation, the order
        # of the faces do not matter
        # To make it easier to compare, we will be listing the
        # faces in an alphabetical order
        corOrigPos=["FLU", "FRU", "BRU", "BLU",
                    "BDL", "DFL", "DFR", "BDR"]
        #Array containing the given corners config with sorted faces
        corSortedFace=list(map(lambda x:"".join(sorted(x)), corners))
        for n in range(8):
            # What we want to store is an array that says the corner with
            # the number n is at the position number corPermArr[n].
            # This means we will go through each of corOrigPos, and then,
            # find where it ended up. The former will be represented as n,
            # and the latter will be stored in corPermArr[n].
            corPermArr[n]=corSortedFace.index(corOrigPos[n])
            # The orientation array stores what orientation the corner is
            # at position number n. The number stored is how far U or D face
            # of the corner will have to go in clockwise direction to get to
            # to either U or D position of the cube. This means that each of
            # the orientation array will have (3-(pos of u in corners[n]))%3
            # (as corners record the faces of the cubies in clockwise direction 
            # starting from U or D face).
            # Although recording the orientation is not very related to recording
            # position, since for loop is already set up, we will be putting them
            # together under one for loop.
            if "U" in corners[n]:
                corOrArr[n]=(3-corners[n].index("U"))%3
            else:
                corOrArr[n]=(3-corners[n].index("D"))%3

        # array describing the edges. Each element has
        # a string of length 2, recording the faces of
        # the corner cubies in clockwise direction starting
        # from the U, D, B or F (checked in this order)
        # face of the CUBE.
        edges=[
            "".join([cube.U[1], cube.B[1]]),
            "".join([cube.U[5], cube.R[1]]),
            "".join([cube.U[7], cube.F[1]]), 
            "".join([cube.U[3], cube.L[1]]),
            "".join([cube.B[5], cube.L[3]]), 
            "".join([cube.B[3], cube.R[5]]),
            "".join([cube.F[5], cube.R[3]]), 
            "".join([cube.F[3], cube.L[5]]),
            "".join([cube.D[7], cube.B[7]]), 
            "".join([cube.D[5], cube.R[7]]),
            "".join([cube.D[1], cube.F[7]]), 
            "".join([cube.D[3], cube.L[7]])
        ]
        # array containing original positions for edges
        # Similar to corners, we can have letters with
        # alphabetical order for each string
        edgOrigPos=['BU', 'RU', 'FU', 'LU', 'BL', 'BR',
                    'FR', 'FL', 'BD', 'DR', 'DF', 'DL']
        #Array containing the given edges config with sorted faces
        edgSortedFace=list(map(lambda x:"".join(sorted(x)), edges))
        for n in range(12):
            # Similar to the position recording process of corners.
            edgPermArr[n]=edgSortedFace.index(edgOrigPos[n])
            # This time, since edges have only two faces, we can
            # just check if the first letter is the desired letter
            # or not. If so, orientation is 0 and if not, the
            # orientation is 1. First, we will check if an edge
            # has U or D face. If so, the desired letter is U or
            # D. If not, the desired letter will be F or B.
            if "U" in edges[n]:
                edgOrArr[n]=0 if edges[n][0]=="U" else 1
            elif "D" in edges[n]:
                edgOrArr[n]=0 if edges[n][0]=="D" else 1
            elif "B" in edges[n]:
                edgOrArr[n]=0 if edges[n][0]=="B" else 1
            else:
                edgOrArr[n]=0 if edges[n][0]=="F" else 1
        
        # We could consider what we have recorded as a series
        # of moves. So, we will be creating a cube_move object
        # with the recorded arrays. The centers are already in
        # position (since we selected the colors based on them).
        moveAlgorithm=cube_move(corPermArr=corPermArr,
                               edgPermArr=edgPermArr,
                               corOrArr=corOrArr, 
                               edgOrArr=edgOrArr)
        # Now, execute the move on a starting configuration
        return self.executeMove(moveAlgorithm)

    def apply(self, algString=""):
        """
        Apply the moves given in the algString to the cube.

        Args:
            algString: An alogrithm string consisting of move instructions.
        """

        pattern = re.compile(r'[UDLRFBMESudlrfbxyzXYZ][0-9\']?')
    
        for moveMatch in re.finditer(pattern, algString):
            moveInstr = moveMatch[0] #get move instruction from re.MatchObject
            move = self.cubeMoveList[moveInstr[0]]
            num = 1
            reversed = False
            if(len(moveInstr)>1):
                if(moveInstr[1]=="'"):
                    move=~move
                else:
                    num = int(moveInstr[1])
            self.executeMove(move**num)
        return self

    def randomizeCube(self, numOfMoves=20):
        """
        Generates a series of random moves and apply them.
        No two moves generated must be in the same face and
        no two consecutive pairs of moves must be parallel. 
        For example, the algorithms "R R2" and "R L R" violates
        the first and second restrictions respectively.

        Args:
            numOfMoves: Number of moves (in half turn metric) 
            the method generates.
        """

        moveFaceList=['F','B','L','R','U','D']
        availMoveFaceList=moveFaceList[:]
        addOnList=["","'","2"]
        currentMoveFace=""
        alg=""
        for index in range(numOfMoves):
            lastMoveFace=currentMoveFace                        #store last move face
            currentMoveFace=random.choice(availMoveFaceList)
            if(lastMoveFace!=""):                               #If this is not the first move of the algorithm
                # If last move face was not parallel to the current 
                # move face, then, the available move faces should be reset.
                if(currentMoveFace in "UD"):                    
                    if(lastMoveFace not in "UD"):               
                        availMoveFaceList=moveFaceList[:]
                elif(currentMoveFace in "RL"):
                    if(lastMoveFace not in "RL"):
                        availMoveFaceList=moveFaceList[:]
                else:
                    if(lastMoveFace not in "BF"):
                        availMoveFaceList=moveFaceList[:]
            alg+=currentMoveFace
            availMoveFaceList.remove(currentMoveFace)
            alg+=random.choice(addOnList)
            if (index==numOfMoves-1):   #Don't add the trailing space for the last move
                break
            alg+=" "
        # if cube is solved, the cube will be randomized according to the standard procedure,
        # meaning that the cube's F face will be green and U face will be white
        if(self.isSolved()):
            self.resetCubeOr()
            self._startingAlg=alg
            self._centersCol=['W', 'B', 'R', 'G', 'O', 'Y']
            self.apply(alg)
            return alg
        else:
            self.apply(alg)
            return alg

    def isSolved(self):
        """
        Returns True when the cube is solved regardless of the cube orientation.
        """
        #Copy self to cube so that self won't change even if cube is manipulated
        cube = cube3_config()*self
        cube.resetCubeOr()
        #Now that the copy of the cube is oriented, we can check
        #the positions and orientations of corners and edges
        cor_dict = cube.getCorners()
        edg_dict = cube.getEdges()
        cor_permutated = (cor_dict['indices']==cor_dict['pos'])
        cor_oriented = (cor_dict['or']==[0]*8)
        edg_permutated = (edg_dict['indices']==edg_dict['pos'])
        edg_oriented = (edg_dict['or']==[0]*12)
        return ((cor_permutated and cor_oriented) and 
                (edg_permutated and edg_oriented))
    
    def resetCubeOr(self):
        """
        Resets the Cube orientation so that F faces front and U faces up
        """
        #check where the top center cubie is
        U_cen_pos = self.getCenters(0)['pos'][0]
        if(U_cen_pos==1):
            self.executeMove(~self.cubeMoveList['x'])
        elif(U_cen_pos==2):
            self.executeMove(~self.cubeMoveList['z'])
        elif(U_cen_pos==3):
            self.executeMove(self.cubeMoveList['x'])
        elif(U_cen_pos==4):
            self.executeMove(self.cubeMoveList['z'])
        elif(U_cen_pos==5):
            self.executeMove(self.cubeMoveList['x']**2)
        #Now check where F center cubie is
        F_cen_pos = self.getCenters(3)['pos'][0]
        if(F_cen_pos==1):
            self.executeMove(self.cubeMoveList['y']**2)
        elif(F_cen_pos==2):
            self.executeMove(self.cubeMoveList['y'])
        elif(F_cen_pos==4):
            self.executeMove(~self.cubeMoveList['y'])
        
        return self

    def __invert__(self):
        """
        Return the inverse position of the cube such that
        the move executed to get to the original cube is inverted
        and applied to the starting configuration.
        """
        return cube3_config().executeMove(self,reversed=True)

if __name__ == "__main__":
    from sympy.interactive import init_printing
    init_printing(perm_cyclic=True, pretty_print=True)
    rubik3=cube3_config()
    print(str(rubik3.isSolved()))
    rubik3.apply("x y")
    print(str(rubik3.isSolved()))
    print(rubik3.toString())
    rubik3.randomizeCube()
    # rubik3.apply("R2 L F L2 R U' F L D2 R2 L2 F2 R2 F' B' D' R' D2 B2 U")
    # rubik3.apply("u D L' D' R u' R D' L' u L'")
    # rubik3.apply("y L U L' U (U F' U F U') (F' U' F)")
    # rubik3.apply("y2 U2 R U R'")
    # rubik3.apply("y' (U F' U2 F U') (R U R')")
    # rubik3.apply("y")
    # print(rubik3.toString())
    # config={'F':'YYOGGGGGG', 
    #         'U':"BOYGYROBG", 
    #         'D':'WWWWWWWWW', 
    #         'L':'YYBRRRRRR',
    #         'R':'YYROOOOOO', 
    #         'B':'GYRBBBBBB'}
    # rubik3 =  cube3_config.fromConfiguration(config)
    # indices=[4,5,6,7,100,10]
    # print(rubik3.getEdges(*indices))
    # rubik3.randomizeCube()
    # rubik3.apply("U' R2 B R' D2 F B L D2 U' B U2 L' F2 R' L2 D' B2")
    # #(0 4)(1 2 3 7 6), (1 2 6 8 3 5 9)(10 11), (5)
    # #[1, 2, 2, 2, 1, 2, 1, 1]
    # #[0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
    # rubik3.apply("d' R2 d L2 u' U' R2")                     #Cross done!
    # #(0 3)(2 5 7), (0 2 6 3 5 1)(8 11 10 9), (5)(1 4 3 2)
    # #[1, 2, 1, 1, 1, 2, 2, 2]
    # #[0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    # rubik3.apply("y")
    # rubik3.apply("U2 L' R U' R' L")
    # #(0 5 1 2 4 7 3), (11)(0 1 3)(4 5 7), (5)
    # #[2, 1, 2, 1, 2, 0, 0, 1]
    # #[1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    # rubik3.apply("R' U  R U R' U R U2 L U L'")
    # #(0 5 3 1 7), (11)(0 2 5 7)(1 3), (5)
    # #[0, 0, 0, 2, 0, 0, 0, 1]
    # #[1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
    # rubik3.apply("L' U2 L d' L U L'")
    # #(0 1 6 5 4 7 3), (0 1 3)(2 6 7 4 5)(8 9 10 11), (5)(1 2 3 4)
    # #[2, 2, 2, 2, 0, 0, 1, 0]
    # #[0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0]
    # rubik3.apply("U2 R U R'")                               #First 2 layers done!
    # #(0 1)(2 3)(4 7 6 5), (4 5 6 7)(8 9 10 11), (5)(1 2 3 4)
    # #[2, 0, 2, 2, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    # rubik3.apply("U'")                                      #preparing to apply OLL algorithm
    # #(0 2)(4 7 6 5), (0 3 2 1)(4 5 6 7)(8 9 10 11), (5)(1 2 3 4)
    # #[2, 2, 0, 2, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    # rubik3.apply("R U2  R' U' R U' R'")                     #Applied a cross OLL algorithm
    # #(1 3)(4 7 6 5), (2 3)(4 5 6 7)(8 9 10 11), (5)(1 2 3 4)
    # #[0, 0, 0, 0, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    # rubik3.apply("U2")                                      #preparing to apply PLL algorithm
    # #(0 2)(4 7 6 5), (0 2 1 3)(4 5 6 7)(8 9 10 11), (5)(1 2 3 4)
    # #[0, 0, 0, 0, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    # rubik3.apply("R' U R' d' R' F' R2 U' R' U R' F R F")    #Applied V PLL algorithm
    # #(0 1 2 3)(4 6)(5 7), (0 3 2 1)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    # #[0, 0, 0, 0, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # rubik3.apply("U'")                                      #Cube solved!
    # #(0 2)(1 3)(4 6)(5 7), (0 2)(1 3)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    # #[0, 0, 0, 0, 0, 0, 0, 0]
    # #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # rubik3.apply("y2")                                      #Original state again
    #rubik3.apply("R' D L U2 D R2 L F2 B2 R' L' F2 B2 R' U B R' L2 U' R'")       #Here we go again...
    ##(0 2 5 1 3 7 6 4), (0 11 4 8 6 5 3 1 2 9 7 10), (5)
    ##[2, 0, 1, 0, 2, 0, 2, 2]
    ##[1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
    #rubik3.apply("R' U2 F' L D L2")                         #Cross done!
    ##(0 4 2 7)(1 6 5), (11)(0 7 6 4 3 2 5 1), (5)
    ##[0, 1, 2, 2, 1, 0, 2, 1]
    ##[0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
    #rubik3.apply("U R' U2 R d L' U L")
    ##(1 7)(4 5), (0 6)(1 2 3 4 7 5)(8 11 10 9), (5)(1 4 3 2)
    ##[2, 2, 1, 0, 2, 0, 0, 2]
    ##[1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    #rubik3.apply("U' R U' R' U' L U L'")
    ##(1 7 4 5 2 3 6), (0 3)(2 6)(4 7 5)(8 11 10 9), (5)(1 4 3 2)
    ##[1, 2, 0, 2, 0, 0, 2, 2]
    ##[0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
    #rubik3.apply("U2 R' U R")
    ##(1 2)(3 6 7 4 5), (0 1)(2 6 5 4 7)(8 11 10 9), (5)(1 4 3 2)
    ##[2, 2, 0, 0, 0, 0, 2, 0]
    ##[0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]
    #rubik3.apply("y' R' U' R U' R' U R")                    #First 2 layers done!
    ##(4 6)(5 7), (0 3 2)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[0, 0, 2, 1, 0, 0, 0, 0]
    ##[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("U2")                                      #Preparing for OLL algorithm
    ##(0 2)(1 3)(4 6)(5 7), (0 1 3)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[2, 1, 0, 0, 0, 0, 0, 0]
    ##[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("R' U' F' U F R")                          #Applied OLL algorithm
    ##(0 1)(2 3)(4 6)(5 7), (0 3)(1 2)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[0, 0, 0, 0, 0, 0, 0, 0]
    ##[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("U'")                                      #Preparing for PLL algorithm
    ##(0 2)(4 6)(5 7), (0 2)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[0, 0, 0, 0, 0, 0, 0, 0]
    ##[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("R' U L' U2 R U' L R' U L' U2 R U' L")     #Applied PLL algorithm
    ##(0 3 2 1)(4 6)(5 7), (0 1 2 3)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[0, 0, 0, 0, 0, 0, 0, 0]
    ##[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("U")                                      #Cube is solved!
    ##(0 2)(1 3)(4 6)(5 7), (0 2)(1 3)(4 6)(5 7)(8 10)(9 11), (5)(1 3)(2 4)
    ##[0, 0, 0, 0, 0, 0, 0, 0]
    ##[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #rubik3.apply("y2")                                     #Back to original state

    #rubik3.apply("F B D2 R2 B2 R D2 R' U D2 L D B' F' R2 L U' D F' L2")
    #rubik3.apply("R2 D' R D' R' U2 R' D2 F D")
    #rubik3.apply("R' D U2 R' L2 F D")

    #rubik3.apply("L2 R U L2 U F L2 D' L2 U2 B2 F R D F2 U L B F2 U")
    #([11, 1, 3, 4], [0, 0, 0, 1])  #this is in the form (edg, edgO) for the edges 8, 9, 10, 11
    #rubik3.apply("D' R2 D' L2 D2 F' D'")   #made a cross by keeping in mind the position of most of the concerned edges

    #rubik3.apply("L' F2 D2 L' U2 R2 F' R B2 U F2 U' B2 U B D' R F' B2 U'")
    #([11, 7, 4, 6], [1, 0, 0, 1])
    #rubik3.apply("L' D' F' L2 U' R2 D2")   #made a cross by keeping in mind the position of most of the concerned edges
    #rubik3.apply("L")              #Look at the first edge (of the 4) with correct orientation and put it in bottom layer
    #([4, 11, 3, 6], [1, 0, 0, 1])  #looking at the next edge (10), we see it's in pos 3, which is directly above pos 11
    #rubik3.apply("D")              #So, with first edge (9) in pos 11, we move it to pos 10 so edge 10 can go to pos 11
    #rubik3.apply("L2")             #Now, edge 10 is in pos 11 and edge 9 is in pos 10
    #([7, 10, 11, 6], [1, 0, 0, 1]) #Next edges are not in correct orientation. This means F move should be used now
                                    #edge 8 is in 7. Using F' will put it in 10 where edge 9 is
    #rubik3.apply("D'")             #So, apply D' to move edge 9 to 11, and 8 can now be placed in 10
    #rubik3.apply("F'")             #F' move applied
    #([10, 11, 8, 2], [0, 0, 0, 0]) #Wow, the orientation of edge 11 changed, so, R or L moves are okay now!
                                    #Since edge 11 is in 2 and the only place available is pos 9
    #rubik3.apply("U'")             #apply U' to put edge 11 in pos 1, directly above pos 9
    #rubik3.apply("R2")             #Now, edge 11 is in 9. Cross is basically done but they are not in the right places
    #([10, 11, 8, 9], [0, 0, 0, 0]) #edge 8 is in 10, so, we need to apply D twice
    #rubik3.apply("D2")             #Yay, cross is done!
    #rubik3.apply("L D L2 D' F' U' R2 D2") #Final algorithm for this cross

    #rubik3.apply("U2 B2 R2 B' F R2 B2 D2 L2 B' R' D' B2 L2 B' R2 D2 B' F' U")
    #([4, 9, 1, 10], [0, 0, 0, 1])  #edge 9 is in pos 9. Also, its orientation is correct
                                    #edge 8 is in 4 (which is on the same face with 11) with correct orientation
                                    #To put 8 beside 9, we need to move 9 to 8, meaning apply D once
    #rubik3.apply("D")              #edge 9 is now in 8, so, 8 could now be put in 11
    #rubik3.apply("L'")             #From 4 to 11 means executing reversed L
    #([11, 8, 1, 9], [0, 0, 0, 1])  #edge 10 is in pos 1, directly above pos 9
                                    #Since edge 9 is in pos 8, edge 10 should be in pos 9
    #rubik3.apply("R2")             #pos 1 to pos 9 is applying R twice
    #([11, 8, 9, 1], [0, 0, 0, 1])  #edge 11 is in pos 1 with wrong orientation
    #rubik3.apply("R' F R")         #Although the first move knocked the edge in pos 9, the last move put it back in pos 9
                                    #Moreover, the F move (that changes orientations) does not affect all the original edges
                                    #in bottom layer (except for the edge in pos 10)
                                    #So, this move ultimately moves edge in pos 1 to pos 10 and changes its orientation
    #([11, 8, 9, 10], [0, 0, 0, 0]) #To change edge 8 from pos 11 to pos 8, we need to apply D thrice, so, D'
    #rubik3.apply("D'")             #Yay, cross is done!
    #rubik3.apply("D L' R2 R' F R D'")     #Final algorithm for this cross

    #rubik3.apply("F B' R2 B' F' D2 R F U' F2 D' U F R F2 R' F' B U F")
    #([4, 1, 7, 0], [1, 1, 0, 1])   #no concerned edges are in the concerned positions
                                    #Next edge is edge 10, being the only edge with correct orientation
                                    #It is in pos 7. So, apply L to move it into pos 11
    #rubik3.apply("L")
    #([3, 1, 11, 0], [1, 1, 0, 1])  #Edge 8 is in pos 3 with wrong orientation.
                                    #We can move it to pos 10 with three moves but edge 10 is in 11
    #rubik3.apply("D'")             #To change edge 10 from pos 11 to pos 8, we need to apply D thrice, so, D'
    #rubik3.apply("L F' L'")        #Similar to line 397, applying this move does not affect edges in concerned position
                                    #So, this move ultimately moves edge in pos 3 to pos 10 and changes its orientation
    #([10, 1, 8, 0], [0, 1, 0, 1])  #Edge 9 is in pos 1 (with wrong orientation). 
                                    #We can move it to pos 10 with three moves but edge 8 is in 10
                                    #We need edge 8 to be in pos 9, so that edge 9 can be beside it when it is put in pos 10
    #rubik3.apply("D")              #This means applying D once (meaning it will subtract 1)
    #rubik3.apply("R' F R")         #3-move algorithm applied
    #([9, 10, 11, 0], [0, 0, 0, 1]) #Edge 11 is in pos 0 with wrong orientation. We need it to be in either pos 1 or pos 3
    #rubik3.apply("U")              #U is easier than U' for the program. This moves edge 11 to pos 1
                                    #We need edge 10 to be in pos 9, so that edge 11 can be beside it when it is put in pos 10
    #rubik3.apply("D2")             #This means applying D twice (meaning it will subtract 2)
    #rubik3.apply("R' F R")         #3-move algorithm applied
    #([11, 8, 9, 10], [0, 0, 0, 0]) #To change edge 8 from pos 11 to 8, we need to sutract 3
    #rubik3.apply("D'")             #This means applying D thrice or applying D'
                                    #Yay, cross done!
    #rubik3.apply("L D' L F' L' D R' F R U D2 R' F R D'")    #Final algorithm for this cross
                                                             #This is a bit long, may be we can reduce it 
                                                             #while maintaining it to be easily programmable?
    
    #rubik3.apply("R' F R U' R' D' U' F R B F' L2 B R2 U2 D F2 L F R2")
    #([0, 2, 4, 7], [1, 1, 0, 1])   #Only edge 10 has right orientation. It is in pos 4
    #rubik3.apply("L'")             #Applying L' will move pos 4 to pos 11
    #([0, 2, 11, 3], [1, 1, 0, 1])  #Edge 8 is in pos 0 with wrong orientation, so, move it to pos 1 or pos 3
    #rubik3.apply("U")              #Applying U is easier for the program, moving from pos 0 to pos 1
                                    #Edge 10 is in pos 11 and 3-move algorithm moves edge to pos 10
                                    #Since 10-8=2, with 8 going to be in pos 10, 10 should stay in pos 8 ((12-8)%4+8=8)
    #rubik3.apply("D'")             #Applying D thrice or D' subtracts 3
    #rubik3.apply("R' F R")         #Apply 3-move algorithm for pos 1
    #([10, 3, 8, 0], [0, 1, 0, 1])  #Edge 9 is in pos 3 with wrong orientation, ready for 3-move algorithm
                                    #Edge 8 is in pos 10 and 3-move algorithm moves edge to pos 10
                                    #Since 9-8=1, with 9 going to be in pos 10, 8 should stay in pos 9
    #rubik3.apply("D")              #Applying D subtracts 1
    #rubik3.apply("L F' L'")        #Apply 3-move algorithm for pos 3
    #([9, 10, 11, 0], [0, 0, 0, 1]) #Edge 11 is in pos 0 with wrong orientation, so, move it to pos 1 or pos 3
    #rubik3.apply("U")              #Applying U is easier for the program, moving from pos 0 to pos 1
                                    #Edge 10 is in pos 11 and 3-move algorithm moves edge to pos 10
                                    #Since 11-10=1, with 11 going to be in pos 10, 10 should stay in pos 9
    #rubik3.apply("D2")             #Applying D twice subtracts 2
    #rubik3.apply("R' F R")         #Apply 3-move algorithm for pos 1
    #([11, 8, 9, 10], [0, 0, 0, 0]) #Edge 8 should be in pos 8 but is in pos 11. So, subtract 3
    #rubik3.apply("D'")             #Applying D' or D thrice subtracts 3.
                                    #Yay! Cross done!
    #rubik3.apply("L' U D' R' F R D L F' L' U D2 R' F R D'") #Final algorithm for this cross

    print(rubik3.toString())        