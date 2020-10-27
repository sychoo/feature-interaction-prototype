# 3d_map_utils.py
# support 3D map objects, including 3D map cells and 3D map coordinates

# Wed Oct 21 20:46:51 EDT 2020
# Designed with ❤️ by Simon Chu

# support 3D coordinates
class Coords:
    def __init__(self, x_cor, y_cor, z_cor):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.z_cor = z_cor
    
    def x(self):
        return self.x_cor
    
    def y(self):
        return self.y_cor
    
    def z(self):
        return self.z_cor

    def set_x(self, x_cor):
        self.x_cor = x_cor
    
    def set_y(self, y_cor):
        self.y_cor = y_cor

    def set_z(self, z_cor):
        self.z_cor = z_cor
        
    def __repr__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ")"

    def __str__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ")"   
