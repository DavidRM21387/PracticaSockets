"""
Display Manager for handling window resizing and coordinate scaling.
This module provides utilities for scaling UI elements and converting coordinates
between virtual and actual screen space.
"""
import pygame

class DisplayManager:
    def __init__(self, virtual_width=800, virtual_height=600):
        """
        Initialize the display manager with virtual dimensions.
        
        Args:
            virtual_width (int): Virtual screen width for coordinate system
            virtual_height (int): Virtual screen height for coordinate system
        """
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height
        self.actual_width = virtual_width
        self.actual_height = virtual_height
        
    def update_actual_size(self, width, height):
        """Update the actual screen dimensions."""
        self.actual_width = width
        self.actual_height = height
        
    def get_scale_factors(self):
        """Get the scale factors for x and y axes."""
        scale_x = self.actual_width / self.virtual_width
        scale_y = self.actual_height / self.virtual_height
        return scale_x, scale_y
        
    def virtual_to_actual(self, x, y):
        """Convert virtual coordinates to actual screen coordinates."""
        scale_x, scale_y = self.get_scale_factors()
        return int(x * scale_x), int(y * scale_y)
        
    def actual_to_virtual(self, x, y):
        """Convert actual screen coordinates to virtual coordinates."""
        scale_x, scale_y = self.get_scale_factors()
        return int(x / scale_x), int(y / scale_y)
        
    def scale_rect(self, virtual_rect):
        """
        Scale a virtual rectangle to actual screen coordinates.
        
        Args:
            virtual_rect (pygame.Rect): Rectangle in virtual coordinates
            
        Returns:
            pygame.Rect: Rectangle in actual coordinates
        """
        scale_x, scale_y = self.get_scale_factors()
        return pygame.Rect(
            int(virtual_rect.x * scale_x),
            int(virtual_rect.y * scale_y),
            int(virtual_rect.width * scale_x),
            int(virtual_rect.height * scale_y)
        )
        
    def scale_font_size(self, virtual_size):
        """Scale font size based on current screen scale."""
        scale_x, scale_y = self.get_scale_factors()
        scale = min(scale_x, scale_y)  # Use minimum to maintain aspect ratio
        return max(1, int(virtual_size * scale))
        
    def get_centered_rect(self, width, height):
        """Get a centered rectangle in virtual coordinates."""
        x = (self.virtual_width - width) // 2
        y = (self.virtual_height - height) // 2
        return pygame.Rect(x, y, width, height)