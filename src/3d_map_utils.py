# 3d_map_utils.py
# support 3D map objects, including 3D map cells and 3D map coordinates

# Wed Oct 21 20:46:51 EDT 2020
# Designed with ❤️ by Simon Chu

class Coord_3D:
    """support 3D coordinate system

    designed to be used in a 3D map

    Attributes:
        x_cor: a integer stores the x coordinate
        y_cor: a integer stores the y coordinate
        z_cor: a integer stores the z coordinate
    """
    def __init__(self, x_cor, y_cor, z_cor):
        """Inits the Coord_3D class with x, y, z coordinates"""
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.z_cor = z_cor
    
    def x(self):
        """return x coordinate"""
        return self.x_cor
    
    def y(self):
        """return y coordinate"""
        return self.y_cor
    
    def z(self):
        """return z coordinate"""
        return self.z_cor

    def set_x(self, x_cor):
        """set x coordinate"""
        self.x_cor = x_cor
    
    def set_y(self, y_cor):
        """set y coordinate"""
        self.y_cor = y_cor

    def set_z(self, z_cor):
        """set z cooridnate"""
        self.z_cor = z_cor
        
    def __repr__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + str(self.z_cor) + ")"

    def __str__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + str(self.z_cor) + ")"   
