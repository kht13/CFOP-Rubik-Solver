from cube3_config import cube3_config
from collections import defaultdict
import CFOP
import re

def printCubeConfig(configDict={}):
    """
    Prints the configuration of the cube in a user-friendly way.
    
    Args:
        configDict: A dict object containing the faces of the cube as keys
        and strings of length 9 recording the colors of the cubies on the
        corresponding faces as values.
    """
    cube_faces=['U', 'B', 'R', 'F', 'L', 'D']

    dictCopy=configDict.copy() #copy the configDict so as to not change it

    #check if copyDict has strings of length 9 for each face
    for i in range(len(cube_faces)):
        face = cube_faces[i]
        if face not in dictCopy.keys() or len(dictCopy[face])!=9:
            dictCopy[face]=face.lower()*9

    U_str=["            ║ {} │ {} │ {} ║\n".format(*dictCopy['U'][0:3]),
           "            ║ {} │ {} │ {} ║\n".format(*dictCopy['U'][3:6]),
           "            ║ {} │ {} │ {} ║\n".format(*dictCopy['U'][6:9])]

    D_str=["            ║ {} │ {} │ {} ║\n".format(*dictCopy['D'][0:3]),
           "            ║ {} │ {} │ {} ║\n".format(*dictCopy['D'][3:6]),
           "            ║ {} │ {} │ {} ║\n".format(*dictCopy['D'][6:9])]
    
    L_str=["║ {} │ {} │ {} ║".format(*dictCopy['L'][0:3]),
           "║ {} │ {} │ {} ║".format(*dictCopy['L'][3:6]),
           "║ {} │ {} │ {} ║".format(*dictCopy['L'][6:9])]

    F_str=[" {} │ {} │ {} ║".format(*dictCopy['F'][0:3]),
           " {} │ {} │ {} ║".format(*dictCopy['F'][3:6]),
           " {} │ {} │ {} ║".format(*dictCopy['F'][6:9])]
           
    R_str=[" {} │ {} │ {} ║".format(*dictCopy['R'][0:3]),
           " {} │ {} │ {} ║".format(*dictCopy['R'][3:6]),
           " {} │ {} │ {} ║".format(*dictCopy['R'][6:9])]

    B_str=[" {} │ {} │ {} ║\n".format(*dictCopy['B'][0:3]),
           " {} │ {} │ {} ║\n".format(*dictCopy['B'][3:6]),
           " {} │ {} │ {} ║\n".format(*dictCopy['B'][6:9])]

    LFRB_str=[l + f + r + b for l, f, r, b in zip(L_str, F_str, R_str, B_str)]
    LFRB_str="╟───┼───┼───╫───┼───┼───╫───┼───┼───╫───┼───┼───╢\n".join(LFRB_str)
    U_str="            ╟───┼───┼───╢\n".join(U_str)
    D_str="            ╟───┼───┼───╢\n".join(D_str)
    config_str ="            ╔═══╤═══╤═══╗\n"+U_str
    config_str+="╔═══╤═══╤═══╬═══╪═══╪═══╬═══╤═══╤═══╦═══╤═══╤═══╗\n"+LFRB_str
    config_str+="╚═══╧═══╧═══╬═══╪═══╪═══╬═══╧═══╧═══╩═══╧═══╧═══╝\n"+D_str
    config_str+="            ╚═══╧═══╧═══╝"
    print("      The Current Configuration of the Cube")
    print("      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(config_str)
    print()

def getFaceString(instr : str = None, prompt : str = None, configDict : dict = None) -> str:
    """
    Prints the cube configuration (if provided), instruction (if provided),
    sample face, and then, prompts the user for the face colors.

    Args:
        instr: The instruction to the guide the user in typing the face colors.
        prompt: The prompt for when the program asks for input.
        configDict: A dict object containing the faces of the cube as keys
        and strings of length 9 recording the colors of the cubies on the
        corresponding faces as values.
    """
    if configDict is not None:
        print()
        printCubeConfig(configDict)
    if instr is not None:
        print(instr)
    print("  ╔═══╤═══╤═══╗")
    print("  ║ 1 │ 2 │ 3 ║")
    print("  ╟───┼───┼───╢")
    print("  ║ 4 │ 5 │ 6 ║")
    print("  ╟───┼───┼───╢")
    print("  ║ 7 │ 8 │ 9 ║")
    print("  ╚═══╧═══╧═══╝")
    if prompt is None:
        prompt="Face colors: "
    while True:
        faceStr=input(prompt)
        faceStr=re.sub(r"[^A-Z]+", "", faceStr.upper())
        if len(faceStr)>9:
            print("Please input only the 9 color letters for the face.")
        elif len(faceStr)<9:
            print("Please input all the 9 color letters for the face.")
        elif not set(faceStr).issubset(set('RGBYOW')):
            print("Please input a combination of only R, G, B, Y, O, or W for\n"+
                  "red, green, blue, yellow, orange, and white respectively.")
        else:
            return faceStr.upper()

def getCubeConfig(faces : str = None, configDict : dict = {}) -> dict:
    """
    Asks for user to input the colors for faces provided in the arguments.
    The order the user is asked is the same order provided in the 'faces'
    argument. If faces has not been provided, the function will run for 
    all faces with the order U, F, R, B, L and D.

    Args:
        faces: The string containing the faces for which the user should be asked.
        configDict: A dict object containing the faces of the cube as keys
        and strings of length 9 recording the colors of the cubies on the
        corresponding faces as values.
    """
    if (faces is not None):
        faces=re.sub(r'[^UFRBLD]', '', faces.upper())
    if not faces:
        configDict={}
        faces="UFRBLD"
    
    for x in range(len(faces)):
        face=faces[x]
        instr=""
        instr+=f" input the first letters of the colors of {face} face cubies.\n"
        if x==0:
            instr="Please"+instr
            instr+="The order should be 123456789 (with {} bordering the {} face)\n"
            instr+="for the following configuration."
        else:
            if x==1:
                instr= "Next, please"+instr
            elif x==len(faces)-1:
                instr= "Finally, please" + instr
            elif x==2:
                instr= "After that, please" + instr
            elif x==3:
                instr= "Now, please" + instr
            elif x==4:
                instr= "Next, please" + instr
            instr+="{} should be bordering the {} face."
        if face=='U':
            instr=instr.format("7, 8, and 9", "F")
        elif face=='D':
            instr=instr.format("1, 2, and 3", "F")
        else:
            instr=instr.format("1, 2, and 3", 'U')
        
        prompt= f"Please input {face} face: "
        configDict[face]=getFaceString(instr, prompt, configDict)

    return configDict

print()
print("                  Welcome to Fridrich's Rubik's Cube Solver!")
print("                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("This app will solve any valid 3x3x3 Rubik's cube configuration using Fridrich's CFOP Method.")
rubik = cube3_config()

while True:
    print()
    print("Do you want to start with a random algorithm, or a custom configuration?")
    rand_cust=input("[Random|Custom]: ")
    while rand_cust.lower() not in ["random", "r", "custom", "c"]:
        print("Please choose only Random or Custom!")
        rand_cust=input("[Random|Custom]: ")
    if(rand_cust.lower() in ["custom", "c"]):
        configDict=getCubeConfig()
        new_config = True
        
        while new_config:
            valid_config = False
            while not valid_config:
                valid_config = True
                col_count=defaultdict(int)
                
                for face_str in configDict.values():
                    for i in range(9):
                        col_count[face_str[i]]+=1

                warn_str = ""
                for key, val in col_count.items():
                    diff = val - 9
                    if diff==0:
                        pass
                    elif diff<0:
                        # if one has less, another has more, so, no need to set flag in the other block
                        valid_config = False
                        warn_str+=f"You need {-diff} more {key}!\n"
                    else:
                        warn_str+=f"You have {diff} more {key} than is necessary!\n"
                
                if(not valid_config):
                    print()
                    printCubeConfig(configDict)
                    print(warn_str)
                    print("Your configuration is not valid. Please check again and change the necessary faces.")
                    face_choice=input("[U|F|R|B|L|D]: ")
                    while not (face_choice and set(face_choice.upper()).issubset(set('UFRBLD'))):
                        print("Please change the configuration to a valid one before you proceed!")
                        face_choice=input("[U|F|R|B|L|D]: ")
                    configDict = getCubeConfig(face_choice, configDict)
            
            rubik.configDict = configDict
            #TODO: check if the user is okay with the config or if he/she wants to change specific faces
            print()
            printCubeConfig(rubik.configDict)
            print(rubik.toString())
            print()
            print("Please check if this is the configuration you wish to use. If not, please provide")
            print("the faces you want to change. If you are satisfied, please type C or Continue.")
            while True:
                face_cont = input("[U|F|R|B|L|D|Continue]: ")
                if face_cont.upper() in ["", "C", "CONTINUE"]:
                    new_config = False
                    break
                elif set(face_cont.upper()).issubset(set('UFRBLD')):
                    configDict = getCubeConfig(face_cont, configDict)
                    break
                else:
                    print('Please type only face letters or "Continue".')
    else:
        rand_alg=rubik.randomizeCube()
        print()
        print()
        print()
        print("Please rotate the cube so that the green colored face is facing towards you, and")
        print("the white colored face is facing upwards. Now, execute the following algorithm.")
        print()
        print("    "+rand_alg)
        print()
        printCubeConfig(rubik.configDict)
        print(rubik.toString())
        input("Press Enter to continue...")

    cross_alg = CFOP.Cross(rubik)
    if(cross_alg):
        print()
        print("'Cross' Step (C of CFOP)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━")
        print("The first step is to complete the 'cross' at the bottom layer.")
        print("To do so, please apply the following algorithm.")
        print()
        print("    "+cross_alg)
        print()
        printCubeConfig(rubik.configDict)
        print(rubik.toString())
        input("Press Enter to continue...")
        
    for x in range(4):
        F2L_alg = CFOP.F2L_one_pair(rubik)
        if(F2L_alg is None):
            break
        print()
        print(f"F2L Step (F of CFOP) Part {x+1}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if (x==0):
            print("The next step is to complete the First 2 (bottom) Layers.")
            print("Here, we will try to first complete a pair of corner and edge cubies.")
            print("So, please apply the following algorithm first.")
        else:
            print("To complete the next pair, apply the following algorithm.")
        print()
        print("    "+F2L_alg)
        print()
        printCubeConfig(rubik.configDict)
        print(rubik.toString())
        input("Press Enter to continue...")
    
    OLL_alg = CFOP.OLL(rubik)
    if(OLL_alg):
        print()
        print("OLL Step (O of CFOP)")
        print("━━━━━━━━━━━━━━━━━━━━")
        print("After the F2L step, we will Orient the Last Layer.")
        print("To do so, please apply the following algorithm.")
        print()
        print("    "+OLL_alg)
        print()
        printCubeConfig(rubik.configDict)
        print(rubik.toString())
        input("Press Enter to continue...")
    
    PLL_alg = CFOP.PLL(rubik)
    if(PLL_alg):
        print()
        print("OLL Step (O of CFOP)")
        print("━━━━━━━━━━━━━━━━━━━━")
        print("Finally, we will Permutate the Last Layer.")
        print("To do so, please apply the following algorithm.")
        print()
        print("    "+PLL_alg)
        print()
        printCubeConfig(rubik.configDict)
        print(rubik.toString())

    print()
    print("Now, we have solved the whole cube! Do you want to continue, or exit the program?")
    cont_exit=input("[Continue|Exit]: ")
    while(cont_exit.lower() not in ["continue", "c", "", "exit", "e"]):
        print("Please chooose only continue or exit!")
        cont_exit=input("[Continue|Exit]: ")
    if(cont_exit.lower() in ["exit", "e"]):
        break

print("Have a wonderful day!")