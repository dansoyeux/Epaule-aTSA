# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:00:51 2023

@author: user
Fit a sphere on the glenoid implant surface to find it's center and define the ghJoint
Script from : https://programming-surgeon.com/en/sphere-fit-python/



"""

def sphere_fit(point_cloud):
    
    import numpy as np
    """
    input
        point_cloud: xyz of the point clouds　numpy array
    output
        radius : radius of the sphere
        sphere_center : xyz of the sphere center
    """

    A_1 = np.zeros((3,3))
    #A_1 : 1st item of A
    v_1 = np.array([0.0,0.0,0.0])
    v_2 = 0.0
    v_3 = np.array([0.0,0.0,0.0])
    # mean of multiplier of point vector of the point_clouds
    # v_1, v_3 : vector, v_2 : scalar

    N = len(point_cloud)
    #N : number of the points

    """Calculation of the sum(sigma)"""
    for v in point_cloud:
        v_1 += v
        v_2 += np.dot(v, v)
        v_3 += np.dot(v, v) * v

        A_1 += np.dot(np.array([v]).T, np.array([v]))

    v_1 /= N
    v_2 /= N
    v_3 /= N
    A = 2 * (A_1 / N - np.dot(np.array([v_1]).T, np.array([v_1])))
    # formula ②
    b = v_3 - v_2 * v_1
    # formula ③
    sphere_center = np.dot(np.linalg.inv(A), b)
    #　formula ①
    radius = (sum(np.linalg.norm(np.array(point_cloud) - sphere_center, axis=1))
              /len(point_cloud))

    return(radius, sphere_center)

"""create point clouds by inputting radius and center"""
def draw_sphere(radius, sphere_center):
    """
    inpu
        radius:radius (scalar)
        sphere_center : xyz of the sphere center (numpy array)
    """

    import numpy as np
    point_list = []

    """create point_cloud"""
    for i in range(360):
        i = i * np.pi / 180   # use radian
        for j in range(360):
            j = j * np.pi / 180  # use radian
            point = radius * np.array([np.sin(i) * np.cos(j),np.sin(i) * np.sin(j), np.cos(i)]) + sphere_center
            # adding a point on the sphere
            point_list.append(point)

    point_list = np.array(point_list)
    # data are stored in numpy array type
    np.savetxt('sphere.asc', point_list)
    # save as '.asc' file for Meshlab
    return