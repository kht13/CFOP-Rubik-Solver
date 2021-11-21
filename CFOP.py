from cube3_config import cube3_config
from sympy.combinatorics import Permutation

def Cross(cube=cube3_config()):
    """TODO: Write some description"""
    algString = ""
    target_edge_indices=[8,9,10,11]
    finished_edges=[]
    loop_num=1
    index_li, pos_li, or_li=cube.getEdges(*target_edge_indices).values()
    finished=False
    #we are doing four edges for the cross,
    #so, loop four times, once for each edge
    while not finished and loop_num <= 20:
        loop_num+=1

        focus_n=None
        sec_focus_n=None  #for edges with wrong orientation

        for n in range(4):
            if index_li[n] in finished_edges:
                continue
            if pos_li[n] in target_edge_indices:   #check if the edge is in bottom layer
                if or_li[n]==0:
                    if len(finished_edges)<=0:
                        finished_edges.append(index_li[n])
                    else:   #check if this edge in bottom layer is correct in pos relative to the finished edges
                        focus_n=n
                        break
                else:
                    if sec_focus_n is None:           #we will handle the cubies in other layers first
                        sec_focus_n=n
            elif or_li[n]==0:
                focus_n = n
            else:
                sec_focus_n = n
        
        alg_for_the_loop=""
        target_pos=None
        if len(finished_edges)>0:
            # get information on one of the finished edges
            fin_edge_index=finished_edges[0]
            fin_edge_n=index_li.index(fin_edge_index)
            fin_edge_pos=pos_li[fin_edge_n]
            # We want to know where we want to put our focus edge
            # The following indices difference says that if the result
            # is one, it should be on the next counter clockwise edge
            # of the finished edge. Two means on the opposite edge, 
            # and three means the next clockwise edge.
            if(focus_n is not None):
                indices_diff=(index_li[focus_n] - fin_edge_index)%4
            elif(sec_focus_n is not None):
                indices_diff=(index_li[sec_focus_n] - fin_edge_index)%4
            # Now that we know the relative position, we need to find
            # the absolute position. Since the edge's index goes up 
            # in counter-clockwise direction for the D face, we need to
            # add the position of the finished edge and indices diffrence
            # to get the absolute target position. Although, since the 
            # next counter-clockwise edge of 11 is 8, we need to subtract
            # 4 (=11+1-8) if the result goes over 11.
            target_pos=fin_edge_pos + indices_diff
            if target_pos > 11:
                target_pos=target_pos-4
    
        if focus_n is not None:
            if pos_li[focus_n] in target_edge_indices:
                if(pos_li[focus_n]==target_pos): 
                    #Focus edge is already in position
                    finished_edges.append(index_li[focus_n])
                    continue
                else:
                    # If focus edge is in pos 8 or 10, we need to
                    # move it to pos 9 or 11 so that we can use
                    # L or R moves to knock it out
                    if(pos_li[focus_n] in [8, 10]):
                        alg_for_the_loop+="D' "
                        # D' moves counter clockwise, so, target_pos should be
                        # increased by 1 while making sure it stays in range
                        target_pos+=1
                        if target_pos >11:
                            target_pos=target_pos-4
                        # same with focus edge's position. However, since it 
                        # will never go over 11, we don't need the if block
                        pos_li[focus_n]+=1

                    if(pos_li[focus_n]==9):
                        alg_for_the_loop+="R' "
                        pos_li[focus_n]=5
                    else:
                        alg_for_the_loop+="L "
                        pos_li[focus_n]=4

            if pos_li[focus_n] in [0, 2]:
                # if target_pos is 9 and focus edge is in 0, or
                # if target_pos is 11 and focus edge is in 2
                if target_pos and target_pos-pos_li[focus_n]==9:
                    alg_for_the_loop+="U "
                    # U adds one since it moves clockwise
                    pos_li[focus_n]+=1
                else:
                    alg_for_the_loop+="U' "
                    pos_li[focus_n]-=1
                    pos_li[focus_n]%=4

            if target_pos is not None:
                num_D_turns=0 # number of D(clockwise) turns needed
                if pos_li[focus_n] in [3, 4, 7]:    
                    # if focus edge is in L face, we need to move
                    # target position to 11
                    num_D_turns=(target_pos-11) %4
                elif pos_li[focus_n] in [1, 5, 6]:
                    # if focus edge is in R face, we need to move
                    # target position to 9
                    num_D_turns=(target_pos-9) %4
                if num_D_turns==1:
                    alg_for_the_loop+="D "
                elif num_D_turns==2:
                    alg_for_the_loop+="D2 "
                elif num_D_turns==3:
                    alg_for_the_loop+="D' "
            # the following three if-elif blocks 
            # are for when focus edge is in L face
            if pos_li[focus_n]==7:
                alg_for_the_loop+="L "
            elif pos_li[focus_n]==3:
                alg_for_the_loop+="L2 "
            elif pos_li[focus_n]==4:
                alg_for_the_loop+="L' "
            # the rest elif-else blocks are for
            # when focus edge is in R face
            elif pos_li[focus_n]==6:
                alg_for_the_loop+="R' "
            elif pos_li[focus_n]==1:
                alg_for_the_loop+="R2 "
            else:
                alg_for_the_loop+="R "
            finished_edges.append(index_li[focus_n])

        elif sec_focus_n is not None:
            focus_n=sec_focus_n
            # if the edge is in the upper layer, we can use
            # the three move algorithms "L F' L'" and 
            # "R' F R" to move and rotate edges from 3 or 1
            # to pos 10
            if pos_li[focus_n] in [0, 1, 2, 3]:
                if pos_li[focus_n] in [0, 2]:
                    alg_for_the_loop+="U "
                    pos_li[focus_n]+=1
                # move target position to 10
                if target_pos is not None:
                    num_D_turns=(target_pos-10) %4
                    if num_D_turns==1:
                        alg_for_the_loop+="D "
                    elif num_D_turns==2:
                        alg_for_the_loop+="D2 "
                    elif num_D_turns==3:
                        alg_for_the_loop+="D' "
                if pos_li[focus_n]==1:
                    alg_for_the_loop+="R' F R "
                else:
                    alg_for_the_loop+="L F' L' "
            elif pos_li[focus_n] in target_edge_indices:
                if(pos_li[focus_n] in [8, 10]):
                    alg_for_the_loop+="D' "
                    if target_pos is not None:
                    # D' moves counter clockwise, so, target_pos should be
                    # increased by 1 while making sure it stays in range
                        target_pos+=1
                        if target_pos >11:
                            target_pos=target_pos-4
                    # same with focus edge's position. However, since it 
                    # will never go over 11, we don't need the if block
                    pos_li[focus_n]+=1
                if(pos_li[focus_n]==11):
                    if(target_pos and target_pos==8):
                        alg_for_the_loop+="L "
                        pos_li[focus_n]=4
                    else:
                        alg_for_the_loop+="L' "
                        pos_li[focus_n]=7
                else:
                    if(target_pos and target_pos==8):
                        alg_for_the_loop+="R' "
                        pos_li[focus_n]=5
                    else:
                        alg_for_the_loop+="R "
                        pos_li[focus_n]=6
            
            if pos_li[focus_n] in [6, 7]:
                if not target_pos or target_pos==10:
                    alg_for_the_loop+="F"
                elif target_pos==11:
                    alg_for_the_loop+="u L"
                elif target_pos==8:
                    alg_for_the_loop+="u D L"
                else:
                    alg_for_the_loop+="u' R"
                # if position of the focus edge was 6 before the
                # above if-elif-else block, then, the last moves
                # should be clockwise, thus, only trailing space was
                # added.
                if pos_li[focus_n]==6:
                    alg_for_the_loop+=" "
                # if it was 7, however, the last moves should be
                # counter-clockwise, so, both "'" sign and trailing
                # space were added
                else:
                    alg_for_the_loop+="' "
            elif pos_li[focus_n] in [4, 5]:
                if not target_pos or target_pos==8:
                    alg_for_the_loop+="B"
                elif target_pos==9:
                    alg_for_the_loop+="u R"
                elif target_pos==10:
                    alg_for_the_loop+="u D R"
                else:
                    alg_for_the_loop+="u' L"
                # if position of the focus edge was 4 before the
                # above if-elif-else block, then, the last moves
                # should be clockwise, thus, only trailing space was
                # added.
                if pos_li[focus_n]==4:
                    alg_for_the_loop+=" "
                # if it was 5, however, the last moves should be
                # counter-clockwise, so, both "'" sign and trailing
                # space were added
                else:
                    alg_for_the_loop+="' "
            finished_edges.append(index_li[focus_n])

        cube.apply(alg_for_the_loop)
        algString+=alg_for_the_loop

        index_li, pos_li, or_li=cube.getEdges(*target_edge_indices).values()
        finished=(set(pos_li)==set(index_li))
        finished=(finished and(or_li==[0]*4))
        finished=(finished and len(finished_edges)==4)

    assert (8 in pos_li)

    posTest=pos_li[:]
    for x in range(list(pos_li).index(8)):
        posTest.append(posTest.pop(0))
    
    assert index_li==posTest
    assert or_li==[0]*4

    cen_displacement=check_Y_ro(cube) #centers clockwise displacement when looked from D
    D_edg_displacement=(index_li[0]-pos_li[0])%4
    num_D_turns=(cen_displacement-D_edg_displacement)%4 # numbers of D turns needed to align with center pieces
    if(num_D_turns==1):
        algString+="D"
        cube.apply("D")
    elif(num_D_turns==2):
        algString+="D2"
        cube.apply("D2")
    elif(num_D_turns==3):
        algString+="D'"
        cube.apply("D'")
    return algString.strip()

def F2L_one_pair(cube=cube3_config()):
    """TODO: Write some description"""
    algString=""
    cen_displacement=check_Y_ro(cube) #how many y moves do we need for centers to return to their places?
    edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values() #for this step, we only need to look at these 4 edges
    cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values() #corresponding corners in the same order
    focus_n = None
    focus_edg_ready=False
    n_for_p6=cen_displacement  #which edge should be put in pos 6 right now?
    FR_not_solved=not F2L_pair_is_solved(n_for_p6, edg_pos_li[n_for_p6], 
                                         cor_pos_li[n_for_p6], edg_or_li[n_for_p6], 
                                         cor_or_li[n_for_p6], cen_displacement)
    if(FR_not_solved):
        if edg_pos_li[n_for_p6] not in [7, 4, 5]:
            focus_n=n_for_p6
            focus_edg_ready=True

    if (focus_n is None):
        for n in range(4):
            if edg_pos_li[n] in [0, 1, 2, 3]: #check if the edge is in top layer
                focus_n=n
                focus_edg_ready=True
                break
            else:
                n_pair_solved=F2L_pair_is_solved(n, edg_pos_li[n], cor_pos_li[n], 
                                                 edg_or_li[n], cor_or_li[n], 
                                                 cen_displacement)
                if(not n_pair_solved):
                    focus_n=n
        if(focus_n is None):
            return None
    # if edge pair for edge in pos 6 is not solved, and there is no edge in top layer
    # then, we will focus on pos 6
    if(FR_not_solved and not focus_edg_ready):
        focus_n=n_for_p6
    
    #focus n is the same as the number of y' moves needed to move
    #the focus edge's target to edge 6's target
    num_y_moves=(-focus_n+cen_displacement)%4
    if num_y_moves!=0:
        if (num_y_moves==1):
            algString+="y "
        elif (num_y_moves==2):
            algString+="y2 "
        elif (num_y_moves==3):
            algString+="y' "
        cube.apply(algString)
        edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values()
        cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values()
        cen_displacement=check_Y_ro(cube)
    
    #if focus edge is not ready yet, it is in the bottom layer
    #If it is in pos 6, then, we can say it's ready but for
    #other positions, we need to knock the edge out
    if (not focus_edg_ready):
        knock_out_alg=None
        if edg_pos_li[focus_n]==7:
            if cor_pos_li[focus_n]==0:
                knock_out_alg="L' U2 L"
            else: 
                knock_out_alg="L' U' L"
        if edg_pos_li[focus_n]==4:
            if cor_pos_li[focus_n]==3:
                knock_out_alg="L U2 L'"
            else:
                knock_out_alg="L U L'"
        if edg_pos_li[focus_n]==5:
            if cor_pos_li[focus_n]==2:
                knock_out_alg="R' U2 R"
            else:
                knock_out_alg="R' U' R"
        if(knock_out_alg is not None):
            cube.apply(knock_out_alg)
            edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values()
            cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values()
            algString+=knock_out_alg+" "
        focus_edg_ready=True

    #knock out the corresponding corner if it's in pos 5, 4 or 7
    if cor_pos_li[focus_n] in [5, 4, 7]:
        knock_out_alg=None
        if cor_pos_li[focus_n]==5:
            if edg_pos_li[focus_n]==0:
                knock_out_alg="L' U2 L"
            else: 
                knock_out_alg="L' U' L"
        if cor_pos_li[focus_n]==4:
            if edg_pos_li[focus_n]==2:
                knock_out_alg="L U2 L'"
            else:
                knock_out_alg="L U L'"
        if cor_pos_li[focus_n]==7:
            if edg_pos_li[focus_n]==2:
                knock_out_alg="R' U2 R"
            else:
                knock_out_alg="R' U' R"
        cube.apply(knock_out_alg)
        edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values()
        cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values()
        algString+=knock_out_alg+" "
    
    if cor_pos_li[focus_n] not in [1, 6]:
        U_move_instr="" #U move for moving cor to pos 1
        if cor_pos_li[focus_n]==2:
            U_move_instr="U"
        elif cor_pos_li[focus_n]==3:
            U_move_instr="U2"
        elif cor_pos_li[focus_n]==0:
            U_move_instr="U'"
        cube.apply(U_move_instr)
        edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values()
        cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values()
        algString+=U_move_instr+" "
    
    edg_or_correct=not ((edg_or_li[focus_n]-cen_displacement)%2)
    F2L_alg=get_F2L_alg(edg_pos_li[focus_n], cor_pos_li[focus_n], 
                        edg_or_correct, cor_or_li[focus_n])
    if(F2L_alg):
        cube.apply(F2L_alg)

    edg_ind_li, edg_pos_li, edg_or_li=cube.getEdges(6, 7, 4, 5).values()
    cor_ind_li, cor_pos_li, cor_or_li=cube.getCorners(6, 5, 4, 7).values()
    cen_displacement=check_Y_ro(cube)
    assert F2L_pair_is_solved(focus_n, edg_pos_li[focus_n], 
                              cor_pos_li[focus_n], edg_or_li[focus_n], 
                              cor_or_li[focus_n], cen_displacement)
    #Is the last move some U turn and the next move the same?
    #If so, combine them in the string.
    #We won't count the next U move if it's in parantheses
    if F2L_alg[0]=="U":
        num_last_U_turns=None
        if algString!="":
            if len(algString)>=2 and algString[-2]=="U":
                num_last_U_turns=1
                algString=algString[0:-2]
            elif len(algString)>=3 and algString[-3]=="U":
                if algString[-2]=="2":
                    num_last_U_turns=2
                elif algString[-2]=="'":
                    num_last_U_turns=3
                algString=algString[0:-3]
        if (num_last_U_turns):
            if F2L_alg[1]==" ":
                num_next_U_turns=1
                F2L_alg=F2L_alg[2:]
            elif F2L_alg[1]=="2":
                num_next_U_turns=2
                F2L_alg=F2L_alg[3:]
            elif F2L_alg[1]=="'":
                num_next_U_turns=3
                F2L_alg=F2L_alg[3:]
            num_U_turns=(num_last_U_turns+num_next_U_turns)%4
            if num_U_turns==1:
                algString+="U "
            elif num_U_turns==2:
                algString+="U2 "
            elif num_U_turns==3:
                algString+="U' "
    
    return algString+F2L_alg

def F2L_pair_is_solved(n, edg_pos, cor_pos, edg_or, cor_or, cen_displacement):
    """
    Return whether the nth pair is solved or not, F2L wise. 

    Args:
        n: if checking for edge 6's pair, n=0. For edge 7's pair, n=1.
        For edge 4's pair, n=2. For edge 5's pair, n=3.
        edg_pos: The current position of the edge being checked.
        cor_pos: The current position of the corresponding corner of 
        the edge being checked.
        edg_or: The current orientation of the edge being checked.        
        cor_or: The current orientation of the corresponding corner of 
        the edge being checked.
        cen_displacement: The number of y moves needed to return the centers to
        its original place.
    """
    edg_ind_li=[6, 7, 4, 5]
    cor_ind_li=[6, 5, 4, 7]
    if(edg_pos==edg_ind_li[n-cen_displacement]):
        if(cor_pos==cor_ind_li[n-cen_displacement]):
            if(edg_or==(cen_displacement%2)):
                if(cor_or==0):
                    return True
    return False
    
def get_F2L_alg(edg_pos, cor_pos, edg_or_correct, cor_or):
    """
    Returns the required F2L algorithm from 
    https://ruwix.com/the-rubiks-cube/advanced-cfop-fridrich/first-two-layers-f2l/
    Before calling this function, one should make sure that the place where
    the corner edge pair should be put in is in FR position, that the corner cubie
    is in either position 1 or 6, and that the edge cubie is in either top layer or
    pos 6.

    Args:
        edg_pos: Position of the edge cubie. (0, 1, 2, 3 or 6)
        cor_pos: Position of the corner cubie. (1 or 6)
        edg_or_correct: Is the orientation of the edge correct? It is if the
        edge orientation is the same as the orientation of the solved edges in the
        middle layer.
        cor_or: Orientation of the corner cubie.
    """
    cor_pos_correct=(cor_pos==6)
    if(not cor_pos_correct):
        if(cor_or==2):
            if(edg_or_correct):
                if(edg_pos==0):
                    # ruwix 1st case, row 1, left algorithm
                    return "R U R'"
                elif(edg_pos==1):
                    # ruwix 4th case, row 4, left algorithm
                    return "(U' R U' R' U) (R U R')"
                elif(edg_pos==2):
                    # ruwix 4th case, row 6, left algorithm
                    return "(U F' U2 F U') (R U R')"
                elif(edg_pos==3):
                    # ruwix 4th case, row 5, left algorithm
                    return "(U' R U R' U) (R U R')"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 2, left algorithm
                    return "(U F' U F) (U F' U2 F)" 
            elif(not edg_or_correct):
                if(edg_pos==0):
                    # ruwix 4th case, row 2, left algorithm
                    return "(U F' U2 F) (U F' U2 F)"
                elif(edg_pos==1):
                    # ruwix 4th case, row 1, left algorithm
                    return "(R U' R' U) (d R' U' R)"
                elif(edg_pos==2):
                    # ruwix 1st case, row 2, left algorithm
                    return "U' F' U F"
                elif(edg_pos==3):
                    # ruwix 4th case, row 3, left algorithm
                    return "(U F' U' F) (U F' U2 F)"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 2, right algorithm
                    return "(U F' U' F) (d' F U F')"
        elif(cor_or==1):
            if(edg_or_correct):
                if(edg_pos==0):
                    # ruwix 4th case, row 3, right algorithm
                    return "(U' R U R') (U' R U2 R')"
                elif(edg_pos==1):
                    # ruwix 1st case, row 2, right algorithm
                    return "U R U' R'"
                elif(edg_pos==2):
                    # ruwix 4th case, row 1, right algorithm
                    return "(F' U F U') (d' F U F')"
                elif(edg_pos==3):
                    # ruwix 4th case, row 2, right algorithm
                    return "(U' R U2 R') (U' R U2 R')"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 3, left algorithm
                    return "(U' R U' R') (U' R U2 R')"
            elif(not edg_or_correct):
                if(edg_pos==0):
                    # ruwix 4th case, row 5, right algorithm
                    return "(U F' U' F U') (F' U' F)"
                elif(edg_pos==1):
                    # ruwix 4th case, row 6, right algorithm
                    return "(U' R U2 R' U) (F' U' F)"
                elif(edg_pos==2):
                    # ruwix 4th case, row 4, right algorithm
                    return "(U F' U F U') (F' U' F)"
                elif(edg_pos==3):
                    # ruwix 1st case, row 1, right algorithm
                    return "F' U' F"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 3, right algorithm
                    return "(U' R U R') (d R' U' R)"
        else:
            if(edg_or_correct):
                if(edg_pos==0):
                    # ruwix 5th case, row 3, left algorithm
                    return "(U R U2 R') (U R U' R')"
                elif(edg_pos==1):
                    # ruwix 5th case, row 4, left algorithm
                    return "(R U2 R') (U' R U R')"
                elif(edg_pos==2):
                    # ruwix 5th case, row 1, left algorithm
                    return "(R U R' U') U' (R U R' U') (R U R')"
                elif(edg_pos==3):
                    # ruwix 5th case, row 2, left algorithm
                    return "(U2 R U R') (U R U' R')"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 1, right algorithm
                    return "(R U R' U') (R U R' U') (R U R')"
            elif(not edg_or_correct):
                if(edg_pos==0):
                    # ruwix 5th case, row 2, right algorithm
                    return "(U2 F' U' F) (U' F' U F)"
                elif(edg_pos==1):
                    # ruwix 5th case, row 1, right algorithm
                    return "y' (R' U' R U) U (R' U' R U) (R' U' R)"
                elif(edg_pos==2):
                    # ruwix 5th case, row 4, right algorithm
                    return "(F' U2 F) (U F' U' F)"
                elif(edg_pos==3):
                    # ruwix 5th case, row 3, right algorithm
                    return "(U' F' U2 F) (U' F' U F)"
                elif(edg_pos==6):
                    # ruwix 3rd case, row 1, left algorithm
                    return "(R U' R') (d R' U R)"
    else:
        if(edg_pos!=6):
            U_move_instr=""
            if(edg_or_correct):
                if(edg_pos==0):
                    U_move_instr+="U "
                elif(edg_pos==3):
                    U_move_instr+="U2 "
                elif(edg_pos==2):
                    U_move_instr+="U' "
                if(cor_or==0):
                    # ruwix 2nd case, row 1, right algorithm
                    return U_move_instr+"(U' F' U F) (U R U' R')"
                elif(cor_or==1):
                    # ruwix 2nd case, row 2, right algorithm
                    return U_move_instr+"(R U R') (U' R U R')"
                else:
                    # ruwix 2nd case, row 3, left algorithm
                    return U_move_instr+"(R U' R') (U R U' R')"
            else:
                if(edg_pos==1):
                    U_move_instr+="U "
                elif(edg_pos==0):
                    U_move_instr+="U2 "
                elif(edg_pos==3):
                    U_move_instr+="U' "
                if(cor_or==0):
                    # ruwix 2nd case, row 1, left algorithm
                    return U_move_instr+"(U R U' R') (U' F' U F)"
                elif(cor_or==1):
                    # ruwix 2nd case, row 2, left algorithm
                    return U_move_instr+"(F' U F) (U' F' U F)"
                else:
                    # ruwix 2nd case, row 3, right algorithm
                    return U_move_instr+"(F' U' F) (U F' U' F)"
        else:
            if(cor_or==2):
                if(edg_or_correct):
                    # ruwix 6th case, row 2, right algorithm
                    return "(R U' R' U' R U R') (U' R U2 R')"
                else:
                    # ruwix 6th case, row 3, right algorithm
                    return "(R U' R' d R' U' R) (U' R' U' R)"
            if(cor_or==1):
                if(edg_or_correct):
                    # ruwix 6th case, row 2, left algorithm
                    return "(R U' R' U R U2 R') (U R U' R')"
                else:
                    # ruwix 6th case, row 3, left algorithm
                    return "(R U R' U' R U' R') (U d R' U' R)"
            elif(cor_or==0):
                if(edg_or_correct):
                    # corner edge pair already solved!
                    return None
                else:
                    # ruwix 6th case, row 1, left algorithm (the only algorithm on this row)
                    return "(R U' R' d R' U2 R) (U R' U2 R)"
    return None
        
def check_Y_ro(cube):
    """
    Returns an integer indicating how much y moves need to be applied
    in order to return the cube to its original position. The upper
    and lower faces must be the U and D faces for this function to
    work correctly.
    """
    indices, pos = cube.getCenters(1, 2, 3, 4).values()
    return (indices[0]-pos[0])%4    
        
def OLL(cube=cube3_config()):
    """
    TODO: write some description
    """    
    ind, pos, or_=cube.getCorners(0,1,2,3).values()
    cor_or_li=[0]*4
    for n in range(4):
        cor_or_li[pos[n]]=or_[n]
    ind, pos, or_=cube.getEdges(0,1,2,3).values()
    edg_or_li=[0]*4
    for n in range(4):
        edg_or_li[pos[n]]=or_[n]
    OLL_alg=""

    for num_U_turns in range(4):
        OLL_alg=get_OLL_alg(cor_or_li, edg_or_li)
        if OLL_alg is None:
            return None
        elif OLL_alg!="":
            break
        cor_or_li.append(cor_or_li.pop(0))
        edg_or_li.insert(0, edg_or_li.pop())
    
    assert OLL_alg!=""

    U_move_instr = ""
    if num_U_turns==1:
        U_move_instr = "U "
    elif num_U_turns==2:
        U_move_instr = "U2 "
    elif num_U_turns==3:
        U_move_instr = "U' "

    algString = U_move_instr +"|"+OLL_alg+"|"
    cube.apply(algString)
    ind, pos, or_=cube.getCorners().values()
    assert or_==[0]*8
    ind, pos = cube.getCenters().values()
    assert pos[0]==0
    ind, pos, or_=cube.getEdges().values()
    cen_displacement = check_Y_ro(cube)
    assert or_==[0]*4+[cen_displacement%2]*4+[0]*4
    return algString
    
def get_OLL_alg(cor_or_li, edg_or_li):
    """
    Returns the required OLL algorithm from 
    https://ruwix.com/the-rubiks-cube/advanced-cfop-fridrich/permutate-the-last-layer-pll/.
    If this function is called while the configuration is not one listed in the
    ruwix website, this function will return blank string instead. Typically,
    this means some U move must be applied before this function is called.

    Args:
        cor_or_li: List of the top layer's corner cubies' orientations in 
        order of pos 0, 1, 2 and 3.
        edg_or_li: List of the top layer's edge cubies' orientations in 
        order of pos 0, 1, 2 and 3.
    """

    dot = [["R U B' l U l2' x' U' R' F R F'", "R' F R F' U2 R' F R y' R2 U2 R"],
           ["y L' R2 B R' B L U2' L' B M' x'", "R' U2 x R' U R U' y R' U' R' U R' F z'"],
           ["(R U R' U) R' F R F' U2 R' F R F'", "M' U2 M U2 M' U M U2 M' U2 M"], 
           ["R' U2 F (R U R' U') y' R2 U2 x' R U x", "F (R U R' U) y' R' U2 (R' F R F')"]]

    line = [["R' U' y L' U L' y' L F L' F R", "R U' y R2 D R' U2 R D' R2 d R'"],
            ["F U R U' R' U R U' R' F'", "L' B' L U' R' U R U' R' U R L' B L"]]

    U_cross = [["L U' R' U L' U (R U R' U) R", "(R U R' U) R U' R' U R U2 R'"],
               ["L' U R U' L U R'", "R' U2 (R U R' U) R"], 
               ["R' F' L F R F' L' F", "R2 D R' U2 R D' R' U2 R'"],
               ["R' F' L' F R F' L F"]]

    oll4_corners=[["M' U' M U2' M' U' M", "L' (R U R' U') L R' F R F'"]]
    # Shape _|
    shape_1 = [["L F R' F R F2 L'", "F R' F' R U R U' R'"],
               ["R' U' R y' x' R U' R' F R U R' x", "U' R U2' R' U' R U' R2 y' R' U' R U B"],
               ["F (R U R' U') (R U R' U') F'", "L F' L' F U2 L2 y' L F L' F"]]
    # Shape |_
    shape_2 = [["U' R' U2 (R U R' U) R2 y (R U R' U') F'", "r U2 R' U' R U' r'"],
               ["R' U2 l R U' R' U l' U2 R", "F' L' U' L U L' U' L U F"], 
               ["R' F R' F' R2 U2 x' U' R U R' x", "R' F R F' U2 R2 y R' F' R F'"]]
    #Shape ¯|
    shape_3=[["R U R' y R' F R U' R' F' R", "L' B' L U' R' U R L' B L"],
             ["U2 r R2' U' R U' R' U2 R U' M", "x' U' R U' R2' F x (R U R' U') R B2"]]
    #Shape |¯
    shape_4=[["L U' y' R' U2' R' U R U' R U2 R d' L'", "U2 l' L2 U L' U L U2 L' U M"],
             ["R2' U R' B' R U' R2' U l U l'", "r' U2 (R U R' U) r"]]
    
    C = [["R U x' R U' R' U x U' R'", "(R U R' U') x D' R' U R E' z'"]]

    L = [["R' F R U R' F' R y L U' L'", "L F' L' U' L F L' y' R' U R"],
         ["L' B' L R' U' R U L' B L", "R B R' L U L' U' R B' R'"]]

    P = [["F U R U' R' F'", "R' d' L d R U' R' F' R"], 
         ["L d R' d' L' U L F L'", "F' U' L' U L F"]]
    
    T = [["F (R U R' U') F'", "(R U R' U') R' F R F'"]]

    W = [["L U L' U L U' L' U' y2' R' F R F'", "R' U' R U' R' U R U y F R' F' R"]]

    Z = [["R' F (R U R' U') y L' d R", "L F' L' U' L U y' R d' L'"]]
    #classifications found on ruwix's site. Not necessarily have just ruwix's algorithms
    #but for the initial stage, all the algorithms are from ruwix site's CFOP 
    ruwix_OLL={'dot':dot, 'line':line, 'cross':U_cross, '4 corners':oll4_corners,
               'Shape _|':shape_1, 'Shape |_':shape_2, 'Shape ¯|':shape_3,
               'Shape |¯':shape_4, 'C':C, 'L':L, 'P':P, 'T':T, 'W':W, 'Z':Z}

    if(edg_or_li==[1]*4):
        # ruwix dot algorithms
        if(cor_or_li[2]==1 and cor_or_li[3]==2):
            if(cor_or_li[0]==1):
                #ruwix dot first row, left algorithm
                return ruwix_OLL["dot"][0][0]
            elif(cor_or_li[0]==2):
                #ruwix dot first row, right algorithm
                return ruwix_OLL["dot"][0][1]
        elif(cor_or_li==[1, 0, 1, 1]):
            #ruwix dot second row, left algorithm
            return ruwix_OLL["dot"][1][0]
        elif(cor_or_li==[2, 2, 0, 2]):
            #ruwix dot second row, right algorithm
            return ruwix_OLL["dot"][1][1]
        elif(cor_or_li[1]==cor_or_li[3]==0):
            if(cor_or_li[0]==1):
                #ruwix dot third row, left algorithm
                return ruwix_OLL["dot"][2][0]
            elif(cor_or_li[0]==0):
                #ruwix dot third row, right algorithm
                return ruwix_OLL["dot"][2][1]
        elif(cor_or_li==[1, 2, 0, 0]):
            #ruwix dot fourth row, left algorithm
            return ruwix_OLL["dot"][3][0]
        elif(cor_or_li==[0, 0, 2, 1]):
            #ruwix dot fourth row, right algorithm
            return ruwix_OLL["dot"][3][1]

    elif((edg_or_li in [[0,1]*2, [1,0]*2]) and 0 not in cor_or_li):
        #ruwix line algorithms
        if(edg_or_li==[0,1]*2):
            #first row
            if(cor_or_li==[2, 2, 1, 1]):
                #ruwix line first row, left algorithm
                return ruwix_OLL["line"][0][0]
            elif(cor_or_li==[1, 2, 1, 2]):
                #ruwix line first row, right algorithm
                return ruwix_OLL["line"][0][1]
        elif(edg_or_li==[1,0]*2):
            if(cor_or_li==[2, 2, 1, 1]):
                #ruwix line second row, left algorithm
                return ruwix_OLL["line"][1][0]
            elif(cor_or_li==[1, 2, 1, 2]):
                #ruwix line second row, right algorithm
                return ruwix_OLL["line"][1][1]

    elif(edg_or_li==[0]*4):
        if(cor_or_li==[0]*4):
            #top layer already oriented!
            return None
        #ruwix cross algorithms
        elif(cor_or_li[1]==2 and cor_or_li[2]==1):
            if(cor_or_li[0]==2):
                #ruwix cross first row, left algorithm
                return ruwix_OLL["cross"][0][0]
            elif(cor_or_li[0]==1):
                #ruwix cross first row, right algorithm
                return ruwix_OLL["cross"][0][1]
        elif(cor_or_li[0]==cor_or_li[2]==cor_or_li[3]):
            if(cor_or_li[0]==2):
                #ruwix cross second row, left algorithm
                return ruwix_OLL["cross"][1][0]
            elif(cor_or_li[0]==1):
                #ruwix cross second row, right algorithm
                return ruwix_OLL["cross"][1][1]
        if(cor_or_li[3]==0):
            if(cor_or_li[1]==1 and cor_or_li[2]==2):
                #ruwix cross third row, left algorithm
                return ruwix_OLL["cross"][2][0]
            elif(cor_or_li[0]==2 and cor_or_li[1]==1):
                #ruwix cross third row, right algorithm
                return ruwix_OLL["cross"][2][1]
            elif(cor_or_li[0]==1 and cor_or_li[2]==2):
                #ruwix cross fourth row, left (and the only) algorithm
                return ruwix_OLL["cross"][3][0]

    elif(cor_or_li==[0]*4):
        #ruwix 4 corners algorithms
        if(edg_or_li==[1, 1, 0, 0]):
            #ruwix 4 corners first (and the only) row, left algorithm
            return ruwix_OLL["4 corners"][0][0]
        elif(edg_or_li==[1, 0]*2):
            #ruwix 4 corners first (and the only) row, right algorithm
            return ruwix_OLL["4 corners"][0][1]

    elif(edg_or_li[0]==edg_or_li[3]==0 and not (cor_or_li[0]==cor_or_li[3]==0)):
        #ruwix shape _| algorithms
        if(cor_or_li[2]==1):
            if(cor_or_li[1]==cor_or_li[3]==1):
                # ruwix shape _| first row, left algorithm
                return ruwix_OLL["Shape _|"][0][0]
            elif(cor_or_li[1]==cor_or_li[3]==0):
                # ruwix shape _| first row, right algorithm
                return ruwix_OLL["Shape _|"][0][1]
        elif(cor_or_li[2]==2 and cor_or_li[1]==0):
            if(cor_or_li[0]==2):
                # ruwix shape _| second row, left algorithm
                return ruwix_OLL["Shape _|"][1][0]
            elif(cor_or_li[0]==0):
                # ruwix shape _| second row, right algorithm
                return ruwix_OLL["Shape _|"][1][1]
        elif(cor_or_li[2]==2 and cor_or_li[1]==1):
            if(cor_or_li[0]==1):
                # ruwix shape _| third row, left algorithm
                return ruwix_OLL["Shape _|"][2][0]
            elif(cor_or_li[0]==2):
                # ruwix shape _| third row, right algorithm
                return ruwix_OLL["Shape _|"][2][1]
    
    elif(edg_or_li[0:2]==[0]*2 and not (cor_or_li[1:3]==[0]*2)):
        # ruwix shape |_ algorithms
        if(cor_or_li==[0, 0, 2, 1]):
            #ruwix shape |_ first row, left algorithm
            return ruwix_OLL["Shape |_"][0][0]
        elif(cor_or_li==[2, 2, 0, 2]):
            #ruwix shape |_ first row, right algorithm
            return ruwix_OLL["Shape |_"][0][1]
        elif(cor_or_li[1]==2 and cor_or_li[3]==1):
            if(cor_or_li[0]==cor_or_li[2]==0):
                #ruwix shape |_ second row, left algorithm
                return ruwix_OLL["Shape |_"][1][0]
            elif(cor_or_li[0]==2 and cor_or_li[2]==1):
                #ruwix shape |_ second row, right algorithm
                return ruwix_OLL["Shape |_"][1][1]
        elif(cor_or_li[1:3]==[1,2]):
            if(cor_or_li[0]==1 and cor_or_li[3]==2):
                #ruwix shape |_ third row, left algorithm
                return ruwix_OLL["Shape |_"][2][0]
            elif(cor_or_li[0]==2 and cor_or_li[3]==1):
                #ruwix shape |_ third row, right algorithm
                return ruwix_OLL["Shape |_"][2][1]

    elif(edg_or_li[2:]==[0]*2 and not (cor_or_li[1]==cor_or_li[3]==0)):
        #ruwix shape ¯| algorithms
        if(cor_or_li==[1, 1, 0, 1]):
            #ruwix shape ¯| first row, left algorithm
            return ruwix_OLL["Shape ¯|"][0][0]
        elif(cor_or_li==[2, 2, 2, 0]):
            #ruwix shape ¯| first row, right algorithm
            return ruwix_OLL["Shape ¯|"][0][1]
        elif(cor_or_li==[2, 0, 2, 2]):
            #ruwix shape ¯| second row, left algorithm
            return ruwix_OLL["Shape ¯|"][1][0]
        elif(cor_or_li==[1, 2, 0, 0]):
            #ruwix shape ¯| second row, right algorithm
            return ruwix_OLL["Shape ¯|"][1][1]
    
    elif(edg_or_li[1:3]==[0]*2 and not (cor_or_li[0]==cor_or_li[2]==0)):
        #ruwix shape |¯ algorithms
        if(cor_or_li==[1, 1, 2, 2]):
            #ruwix shape |¯ first row, left algorithm
            return ruwix_OLL["Shape |¯"][0][0]
        elif(cor_or_li==[0, 1, 1, 1]):
            #ruwix shape |¯ first row, right algorithm
            return ruwix_OLL["Shape |¯"][0][1]
        elif(cor_or_li==[1, 2, 0, 0]):
            #ruwix shape |¯ second row, left algorithm
            return ruwix_OLL["Shape |¯"][1][0]
        elif(cor_or_li==[1, 0, 1, 1]):
            #ruwix shape |¯ second row, right algorithm
            return ruwix_OLL["Shape |¯"][1][1]
    
    #ruwix C algorithms (following 2 elif blocks)
    elif(edg_or_li==[0, 1]*2 and cor_or_li==[0, 2, 1, 0]):
        #ruwix C first row, left algorithm
        return ruwix_OLL["C"][0][0]

    elif(edg_or_li==[1, 0]*2 and cor_or_li==[0, 0, 1, 2]):
        #ruwix C first row, right algorithm
        return ruwix_OLL["C"][0][1]
    
    elif(edg_or_li==[1, 0]*2 and cor_or_li[2]==cor_or_li[3]):
        #ruwix L algorithms
        if(cor_or_li==[2, 0, 2, 2]):
            #ruwix L first row, left algorithm
            return ruwix_OLL["L"][0][0]
        elif(cor_or_li==[0, 1, 1, 1]):
            #ruwix L first row, right algorithm
            return ruwix_OLL["L"][0][1]
        elif(cor_or_li==[1, 0, 1, 1]):
            #ruwix L second row, left algorithm
            return ruwix_OLL["L"][1][0]
        elif(cor_or_li==[0, 2, 2, 2]):
            #ruwix L second row, right algorithm
            return ruwix_OLL["L"][1][1]

    elif(edg_or_li[0]==0 and edg_or_li[2]==1):
        #ruwix P algorithms
        #here, edges cannot all be 0 (cross is already checked) and
        #P will always come here (since P was checked to not be in 
        # shape _| and shape |_). So, we need to check only one corner's
        # orientation
        if(cor_or_li[1]==2):
            #ruwix P first row, left algorithm
            return ruwix_OLL["P"][0][0]
        elif(cor_or_li[0]==2):
            #ruwix P first row, right algorithm
            return ruwix_OLL["P"][0][1]
        elif(cor_or_li[1]==1):
            #ruwix P second row, left algorithm
            return ruwix_OLL["P"][1][0]
        elif(cor_or_li[0]==1):
            #ruwix P second row, right algorithm
            return ruwix_OLL["P"][1][1]

    elif(edg_or_li==[1, 0]*2 and cor_or_li[1:3]==[0]*2):
        #ruwix T algorithm
        if(cor_or_li[0]==1):
            #ruwix T first row, left algorithm
            return ruwix_OLL["T"][0][0]
        elif(cor_or_li[0]==2):
            #ruwix T first row, right algorithm
            return ruwix_OLL["T"][0][1]
    
    elif(edg_or_li[0]==1 and edg_or_li[2]==0):
        #ruwix W algorithm
        if(cor_or_li[1]==1):
            #ruwix W first row, left algorithm
            return ruwix_OLL["W"][0][0]
        elif(cor_or_li[0]==2):
            #ruwix W first row, right algorithm
            return ruwix_OLL["W"][0][1]
    
    elif(edg_or_li==[1, 0]*2):
        #ruwix Z algorithm
        #all other configurations (present in ruwix) should be checked
        #already, so, checking only edges should be okay for outer elif
        if(cor_or_li==[1, 0, 2, 0]):
            #ruwix Z first row, left algorithm
            return ruwix_OLL["Z"][0][0]
        elif(cor_or_li==[0, 2, 0, 1]):
            #ruwix Z first row, right algorithm
            return ruwix_OLL["Z"][0][1]

    return ""

def PLL(cube=cube3_config()):
    """
    TODO: Write some description
    """
    top_cor=cube.getCorners(0, 1, 2, 3)
    cor_pos_li=top_cor["pos"]
    top_edg=cube.getEdges(0, 1, 2, 3)
    edg_pos_li=top_edg["pos"]
    algString=PLL_alg=""
    U_cor_perm = Permutation([[0, 3, 2, 1]])
    U_edg_perm = Permutation([[0, 1, 2, 3]])
    for num_U_turns in range(4):
        PLL_alg=get_PLL_alg(cor_pos_li, edg_pos_li)
        if PLL_alg is None or PLL_alg!="":
            break
        #the process below is not the same with switching orientations
        cor_pos_li=(Permutation(cor_pos_li)*U_cor_perm).array_form
        edg_pos_li=(Permutation(edg_pos_li)*U_edg_perm).array_form
    
    if(PLL_alg is not None):
        assert PLL_alg!=""

        U_move_instr = ""
        if num_U_turns==1:
            U_move_instr = "U "
        elif num_U_turns==2:
            U_move_instr = "U2 "
        elif num_U_turns==3:
            U_move_instr = "U' "

        algString = U_move_instr +"|"+PLL_alg+"|"
        cube.apply(algString)
    
    assert cube.getCenters(0)['pos'][0]==0
    cen_dispacement = check_Y_ro(cube)
    edg_pos= cube.getEdges(0)['pos'][0]
    top_edg_displacement=(0-edg_pos)%4
    num_U_turns=(top_edg_displacement-cen_dispacement)%4

    U_move_instr = ""
    if num_U_turns==1:
        U_move_instr = " U"
    elif num_U_turns==2:
        U_move_instr = " U2"
    elif num_U_turns==3:
        U_move_instr = " U'"
    cube.apply(U_move_instr)

    return (algString+U_move_instr).strip()

def get_PLL_alg(cor_pos_li, edg_pos_li):
    """
    Returns the required PLL algorithm from 
    https://ruwix.com/the-rubiks-cube/advanced-cfop-fridrich/permutate-the-last-layer-pll/.
    If this function is called while the configuration is not one listed in the
    ruwix website, this function will return blank string instead. Typically,
    this means some U move must be applied before this function is called.

    Args:
        cor_pos_li: List of the top layer's corner cubies' positions in 
        order of corner cubie 0, 1, 2 and 3.
        edg_or_li: List of the top layer's edge cubies' positions in 
        order of edge cubie 0, 1, 2 and 3.
    """
    U_Perm = {'cor':[1, 2, 3, 0], 'edg':[3, 0, 1, 2]}
    for n in range(4):
        cor_perm = Permutation(U_Perm['cor'])**n
        edg_perm = Permutation(U_Perm['edg'])**n
        cor_pos_li_test = (Permutation(cor_pos_li)*cor_perm).array_form
        edg_pos_li_test = (Permutation(edg_pos_li)*edg_perm).array_form
        if(cor_pos_li_test==edg_pos_li_test==[0, 1, 2, 3]):
            return None

    ruwix_PLL = {
        'A1': "x [(R' U R') D2] [(R U' R') D2] R2 x'",
        'A2': "x' [(R U' R) D2] [(R' U R) D2] R2 x",
        'U1': "R2 U [R U R' U'] (R' U') (R' U R')",
        'U2': "[R U'] [R U] [R U] [R U'] R' U' R2",
         'H': "M2 U M2 U2 M2 U M2",
         'T': "[R U R' U'] [R' F] [R2 U' R'] U' [R U R' F']",
        'J1': "[R' U L'] [U2 R U' R' U2] [R L U']",
        'J2': "[R U R' F'] {[R U R' U'] [R' F] [R2 U' R'] U'}",
        'R1': "[L U2' L' U2'] [L F'] [L' U' L U] [L F] L2' U",
        'R2': "[R' U2 R U2] [R' F] [R U R' U'] [R' F'] R2 U'",
         'V': "[R' U R' d'] [R' F'] [R2 U' R' U] [R' F R F]",
        'G1': "R2 u R' U R' U' R u' R2 [y' R' U R]",
        'G2': "[R' U' R] y R2 u R' U R U' R u' R2",
        'G3': "R2 u' R U' R U R' u R2 [y R U' R']",
        'G4': "[R U R'] y' R2 u' R U' R' U R' u R2",
         'F': "[R' U2 R' d'] [R' F'] [R2 U' R' U] [R' F R U' F]",
         'Z': "M2 U M2 U M' U2 M2 U2 M' U2",
         'Y': "F R U' R' U' [R U R' F'] {[R U R' U'] [R' F R F']}",
        'N1': "{(L U' R) U2 (L' U R')} {(L U' R) U2 (L' U R')} U",
        'N2': "{(R' U L') U2 (R U' L)} {(R' U L') U2 (R U' L)} U'",
         'E': "X' (R U' R') D (R U R') u2 (R' U R) D (R' U' R) X'"
    }

    ruwix_PLL_Perm = {
        'A1': {'cor':[0, 3, 1, 2], 'edg':[0, 1, 2, 3]},
        'A2': {'cor':[1, 2, 0, 3], 'edg':[0, 1, 2, 3]},
        'U1': {'cor':[0, 1, 2, 3], 'edg':[0, 2, 3, 1]},
        'U2': {'cor':[0, 1, 2, 3], 'edg':[0, 3, 1, 2]},
         'H': {'cor':[0, 1, 2, 3], 'edg':[2, 3, 0, 1]},
         'T': {'cor':[0, 2, 1, 3], 'edg':[0, 3, 2, 1]},
        'J1': {'cor':[0, 1, 3, 2], 'edg':[3, 1, 2, 0]},
        'J2': {'cor':[0, 2, 1, 3], 'edg':[0, 2, 1, 3]},
        'R1': {'cor':[0, 1, 3, 2], 'edg':[0, 1, 3, 2]},
        'R2': {'cor':[0, 1, 3, 2], 'edg':[0, 2, 1, 3]},
         'V': {'cor':[0, 3, 2, 1], 'edg':[1, 0, 2, 3]},
        'G1': {'cor':[3, 1, 0, 2], 'edg':[3, 0, 2, 1]},
        'G2': {'cor':[1, 3, 2, 0], 'edg':[2, 1, 3, 0]},
        'G3': {'cor':[1, 3, 2, 0], 'edg':[0, 2, 3, 1]},
        'G4': {'cor':[3, 1, 0, 2], 'edg':[3, 1, 0, 2]},
         'F': {'cor':[1, 0, 2, 3], 'edg':[0, 3, 2, 1]},
         'Z': {'cor':[0, 1, 2, 3], 'edg':[3, 2, 1, 0]},
         'Y': {'cor':[0, 3, 2, 1], 'edg':[3, 1, 2, 0]},
        'N1': {'cor':[0, 3, 2, 1], 'edg':[2, 1, 0, 3]},
        'N2': {'cor':[2, 1, 0, 3], 'edg':[2, 1, 0, 3]},
         'E': {'cor':[3, 2, 1, 0], 'edg':[0, 1, 2, 3]}
    }

    for key, perm_arr in ruwix_PLL_Perm.items():
        cor_perm = Permutation(perm_arr['cor'])
        edg_perm = Permutation(perm_arr['edg'])
        new_cor_pos_li = (Permutation(cor_pos_li)*cor_perm)
        new_edg_pos_li = (Permutation(edg_pos_li)*edg_perm)
        for n in range(4):
            cor_perm = Permutation(U_Perm['cor'])**n
            edg_perm = Permutation(U_Perm['edg'])**n
            cor_pos_li_test = (new_cor_pos_li*cor_perm).array_form
            edg_pos_li_test = (new_edg_pos_li*edg_perm).array_form
            if(cor_pos_li_test==edg_pos_li_test==[0, 1, 2, 3]):
                return ruwix_PLL[key]

    return ""


__all__ = ['Cross', 'F2L_one_pair', 'OLL', 'PLL']

if __name__=="__main__":
    for x in range(1000000):
        if(x%1000==0):
            if(x!=0):
                print(f"Finished {x} iterations...")
        try:
            rubik3=cube3_config()
            rubik3.randomizeCube()
            print("Starting Algorithm: "+rubik3.startingAlg)
            print("   Cross Algorithm: "+Cross(rubik3))
            F2L_alg=""
            for n in range(10):
                print_msg=" F2L Algorithm: "
                if n==0:
                    print_msg=" 1st"+print_msg
                elif n==1:
                    print_msg=" 2nd"+print_msg
                elif n==2:
                    print_msg=" 3rd"+print_msg
                else:
                    print_msg=" "+str(n+1)+"th"+print_msg
                F2L_alg=F2L_one_pair(rubik3)
                if F2L_alg is not None:
                    print(print_msg + F2L_alg)
                else:
                    break
            OLL_alg = OLL(rubik3)
            if OLL_alg is None:
                print("     OLL Alogrithm: Already solved!")
            else:
                print("     OLL Algorithm: "+OLL_alg)
            PLL_alg = PLL(rubik3)
            if PLL_alg is None:
                print("     PLL Algorithm: Already solved!")
            else:
                print("     PLL Algorithm: "+PLL_alg)
            assert rubik3.isSolved()
        except KeyboardInterrupt:
            print(f'Operationg stopped. Finished {x} iterations.')
            break
    # rubik3=cube3_config.fromAlgorithm("L2 R2 B' L2 U' R' B' U2 D2 L2 U2 D F2 R' B D2 L2 D2 L D")
    # # rubik3=cube3_config().randomizeCube()
    # print("Starting Algorithm: "+rubik3.startingAlg)
    # print("Cross Algorithm: "+Cross(rubik3))
    # print("First F2L Algorithm: "+ str(F2L_one_pair(rubik3)))
    # print("Second F2L Algorithm: "+ str(F2L_one_pair(rubik3)))
    # print("Third F2L Algorithm: "+ str(F2L_one_pair(rubik3)))
    # print("Fourth F2L Algorithm: "+ str(F2L_one_pair(rubik3)))
    # print("Fifth F2L Algorithm: "+ str(F2L_one_pair(rubik3)))
    # print("OLL Algorithm: " + str(OLL(rubik3)))
    # print("PLL Algorithm: "+str(PLL(rubik3)))
    # print(rubik3.toString())
    # assert rubik3.isSolved()
    # print(rubik3.toString())
    
        # print(rubik3.startingAlg)
        # rubik3=cube3_config.fromAlgorithm("B' U' D R U2 L' R' B L2 F B' R2 U2 L U L2 B D' R' F")
        # print(Cross(rubik3))
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [6, 7, 3, 1], [1, 0, 2, 1]
        # #  edges - [6, 7, 4, 5], [4, 3, 7, 5], [1, 0, 1, 1]
        # # only edge 7 is on top layer and its corresponding
        # # corner is staying in the lower layer
        # # we will knock that corner out first
        # # we will have to mind the position of edge 7 when
        # # doing so, since we don't want that going to middle
        # # layer
        # # Also, since we will be doing edge 7 and since we 
        # # will be changing the target position to 6, we will
        # # apply y'
        # rubik3.apply("R' U R y'")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [7, 3, 4, 2], [1, 1, 0, 1]
        # #  edges - [6, 7, 4, 5], [7, 3, 6, 1], [0, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [4, 1, 2, 3]
        # # Since we just rotated the cube 90 degrees, the edges 
        # # need to have orientation of 1. So, edge 7 has wrong
        # # orientation now. The algorithms focuses on the corner
        # # being at position 1, so, we will be applying U2
        # rubik3.apply("U2")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [7, 1, 4, 0], [1, 1, 0, 1]
        # #  edges - [6, 7, 4, 5], [7, 1, 6, 3], [0, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [4, 1, 2, 3]
        # # Now we can apply the algorithm
        # rubik3.apply("(U' R U2 R' U) (F' U' F)")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [7, 6, 4, 1], [1, 0, 0, 2]
        # #  edges - [6, 7, 4, 5], [7, 6, 3, 0], [0, 1, 0, 1]
        # #centers - [1, 2, 3, 4], [4, 1, 2, 3]
        # # Edge 7 and its corresponding corner, corner 5 are in place.
        # # Next, we see that edge 4 is on top. Its corresponding corner,
        # # corner 4 appears to be in place with correct orientation. 
        # # However, the cube was rotated, so, corner 4 is in another place.
        # # First, we will rotate the cube so that target position is 6.
        # rubik3.apply("y'")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [4, 7, 5, 2], [1, 0, 0, 2]
        # #  edges - [6, 7, 4, 5], [6, 5, 2, 3], [1, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [3, 4, 1, 2]
        # # Knocking out the corresponding corner, corner 4 from
        # # position 5
        # rubik3.apply("L' U' L")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [4, 7, 1, 0], [1, 0, 2, 1]
        # #  edges - [6, 7, 4, 5], [6, 5, 1, 3], [1, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [3, 4, 1, 2]
        # # Since the corner is at pos 1, we can apply the algorithm.
        # # Since corner does not have correct orientation, we know
        # # it is pointint outward. Also, the rotated centers points
        # # out that the edges are supposed to be with zero orientation
        # # now. 
        # rubik3.apply("(U' R U' R' U) (R U R')")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [4, 7, 6, 2], [1, 0, 0, 0]
        # #  edges - [6, 7, 4, 5], [1, 5, 6, 2], [1, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [3, 4, 1, 2]
        # # We see that edge 6 is on top. We will focus on it.
        # # That means we will rotate the cube 180 degrees so
        # # that the target position will be at 6.
        # rubik3.apply("y2")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [6, 5, 4, 0], [1, 0, 0, 0]
        # #  edges - [6, 7, 4, 5], [3, 7, 4, 0], [1, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [1, 2, 3, 4]
        # # We see that corner 6 is at its place, although with
        # # wrong orientation. Edge 6 is also with wrong orientation.
        # # To apply the algorithm, we see that when the corner is
        # # at its place, we will only need to mind the edge's position.
        # # Since it has wrong orientation, we will have to place it at
        # # pos 2.
        # rubik3.apply("U'")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [6, 5, 4, 1], [1, 0, 0, 0]
        # #  edges - [6, 7, 4, 5], [2, 7, 4, 3], [1, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [1, 2, 3, 4]
        # # We are ready to apply the algorithm
        # rubik3.apply("(F' U F) (U' F' U F)")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [6, 5, 4, 0], [0, 0, 0, 1]
        # #  edges - [6, 7, 4, 5], [6, 7, 4, 0], [0, 0, 0, 1]
        # #centers - [1, 2, 3, 4], [1, 2, 3, 4]
        # # The last one is edge 5. We see that it is on top already.
        # # We will rotate the cube again.
        # rubik3.apply("y")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [5, 4, 7, 3], [0, 0, 0, 1]
        # #  edges - [6, 7, 4, 5], [7, 4, 5, 1], [1, 1, 1, 1]
        # #centers - [1, 2, 3, 4], [2, 3, 4, 1]
        # # We will send the corner to pos 1 again.
        # rubik3.apply('U2')
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [5, 4, 7, 1], [0, 0, 0, 1]
        # #  edges - [6, 7, 4, 5], [7, 4, 5, 3], [1, 1, 1, 1]
        # #centers - [1, 2, 3, 4], [2, 3, 4, 1]
        # # We are ready to apply the algorithm.
        # # Note that the if orientation of the edge is what it
        # # is supposed to be (1 in this case), the top face (if
        # # the edge is on top layer) will have the same color as
        # # the front face of the cube.
        # rubik3.apply("(U' R U2 R') (U' R U2 R')")
        # #             indices      positions   orientations
        # #corners - [6, 5, 4, 7], [5, 4, 7, 6], [0, 0, 0, 0]
        # #  edges - [6, 7, 4, 5], [7, 4, 5, 6], [1, 1, 1, 1]
        # #centers - [1, 2, 3, 4], [2, 3, 4, 1]
        # #F2L completed!
        
        # target_corners=rubik3.getCorners(6, 5, 4, 7).values()
        # target_edges=rubik3.getEdges(6, 7, 4, 5).values()
        # target_centers=rubik3.getCenters(1, 2, 3, 4).values()
        # print(target_corners)
        # print(target_edges)
        # print(target_centers)

        # print(rubik3.toString())
