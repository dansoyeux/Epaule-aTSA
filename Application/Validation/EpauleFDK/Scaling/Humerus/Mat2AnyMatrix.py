# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 13:41:27 2023

@author: Dan
converts a matrix to a string in the AnyMatrix format in AnyBody and adds a comment at the end of each line
"""



def Mat2AnyMatrix(MatrixName=str,mat=list, comment=None):
      
    
    
    if comment:
        CommentString = 1
        
    else:
        CommentString = 0
        comment = [""]*len(mat)
    
    
    
    string ="AnyMatrix " + MatrixName + " = {\n"
    for i in range(len(mat)):
        string += "  {"
        for j in range(len(mat[0])):
            if j != len(mat[0])-1:
                string += str(mat[i,j]) + ", " 
            else:
                string += str(mat[i,j]) + "}"
            
        if i == len(mat)-1:
            string += ("  // " + comment[i]) * CommentString + "\n};"
        else:
            string += "," + ("  // " + comment[i]) * CommentString + "\n"
            
    print(string)