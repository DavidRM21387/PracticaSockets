"""
Multiplayer Game class with complete resizing and coordinate scaling support.
This fixes the IP input screen resizing issues mentioned in the problem statement.
"""
import pygame
import sys
import socket
from display_manager import DisplayManager

class MultiplayerGame:
    def __init__(self, screen, display_manager):
        """
        Initialize the multiplayer game.
        
        Args:
            screen: Pygame screen surface
            display_manager: DisplayManager instance for scaling
        """
        self.screen = screen
        self.display_manager = display_manager
        self.running = True
        self.current_state = "ip_input"  # ip_input, connecting, playing
        self.result = None
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 200)
        self.DARK_BLUE = (0, 50, 150)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.LIGHT_GRAY = (200, 200, 200)
        
        # Store actual button rectangles for collision detection
        self.button_rects = {}
        
        # IP input fields
        self.ip_input = ""
        self.port_input = "12345"
        self.active_field = "ip"  # "ip" or "port"
        self.input_rects = {}
        
        # Connection status
        self.connection_status = ""
        self.socket = None
        
    def draw_button(self, text, virtual_rect, button_id, color=None):
        """
        Draw a button and store its actual rectangle for collision detection.
        Uses display_manager for proper scaling.
        
        Args:
            text (str): Button text
            virtual_rect (pygame.Rect): Button rectangle in virtual coordinates
            button_id (str): Unique identifier for the button
            color (tuple): Button color, defaults to blue
        """
        if color is None:
            color = self.BLUE
            
        # Scale the virtual rectangle to actual coordinates
        actual_rect = self.display_manager.scale_rect(virtual_rect)
        
        # Store the actual rectangle for collision detection
        self.button_rects[button_id] = actual_rect
        
        # Draw button background
        pygame.draw.rect(self.screen, color, actual_rect)
        pygame.draw.rect(self.screen, self.BLACK, actual_rect, 2)
        
        # Draw button text
        font_size = self.display_manager.scale_font_size(32)
        font = pygame.font.Font(None, font_size)
        button_text = font.render(text, True, self.WHITE)
        
        # Center text in button
        text_rect = button_text.get_rect()
        text_rect.center = actual_rect.center
        
        self.screen.blit(button_text, text_rect)
        
    def draw_input_field(self, text, virtual_rect, field_id, is_active=False):
        """
        Draw an input field and store its actual rectangle for click detection.
        Uses display_manager for proper scaling.
        
        Args:
            text (str): Current text in the field
            virtual_rect (pygame.Rect): Field rectangle in virtual coordinates
            field_id (str): Unique identifier for the field
            is_active (bool): Whether this field is currently active
        """
        # Scale the virtual rectangle to actual coordinates
        actual_rect = self.display_manager.scale_rect(virtual_rect)
        
        # Store the actual rectangle for click detection
        self.input_rects[field_id] = actual_rect
        
        # Choose colors based on active state
        bg_color = self.WHITE if is_active else self.LIGHT_GRAY
        border_color = self.BLUE if is_active else self.BLACK
        border_width = 3 if is_active else 2
        
        # Draw field background
        pygame.draw.rect(self.screen, bg_color, actual_rect)
        pygame.draw.rect(self.screen, border_color, actual_rect, border_width)
        
        # Draw field text
        font_size = self.display_manager.scale_font_size(28)
        font = pygame.font.Font(None, font_size)
        field_text = font.render(text, True, self.BLACK)
        
        # Position text with some padding
        text_rect = field_text.get_rect()
        text_rect.left = actual_rect.left + 10
        text_rect.centery = actual_rect.centery
        
        self.screen.blit(field_text, text_rect)
        
        # Draw cursor if active
        if is_active:
            cursor_x = text_rect.right + 2
            cursor_y1 = actual_rect.top + 5
            cursor_y2 = actual_rect.bottom - 5
            pygame.draw.line(self.screen, self.BLACK, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
        
    def draw_title(self, title_text):
        """Draw a title at the top of the screen using display_manager for scaling."""
        title_font = pygame.font.Font(None, self.display_manager.scale_font_size(48))
        title = title_font.render(title_text, True, self.BLACK)
        
        # Center the title using virtual coordinates
        title_rect = title.get_rect()
        title_rect.center = self.display_manager.virtual_to_actual(
            self.display_manager.virtual_width // 2, 80
        )
        
        self.screen.blit(title, title_rect)
        
    def draw_text(self, text, virtual_x, virtual_y, font_size=24, color=None):
        """
        Draw text at virtual coordinates using display_manager for scaling.
        
        Args:
            text (str): Text to draw
            virtual_x (int): X coordinate in virtual space
            virtual_y (int): Y coordinate in virtual space  
            font_size (int): Font size in virtual space
            color (tuple): Text color, defaults to black
        """
        if color is None:
            color = self.BLACK
            
        font = pygame.font.Font(None, self.display_manager.scale_font_size(font_size))
        text_surface = font.render(text, True, color)
        
        # Convert virtual coordinates to actual coordinates
        actual_pos = self.display_manager.virtual_to_actual(virtual_x, virtual_y)
        text_rect = text_surface.get_rect()
        text_rect.center = actual_pos
        
        self.screen.blit(text_surface, text_rect)
        
    def draw_ip_input_screen(self):
        """
        Draw the IP input screen with proper resizing support.
        This method fixes the resizing issues mentioned in the problem statement.
        """
        self.screen.fill(self.WHITE)
        
        # Clear rectangles
        self.button_rects.clear()
        self.input_rects.clear()
        
        # Draw title
        self.draw_title("MULTIJUGADOR - CONECTAR")
        
        # Define field dimensions in virtual coordinates
        field_width = 300
        field_height = 40
        label_height = 30
        
        # IP Address section
        ip_label_y = 180
        ip_field_y = ip_label_y + label_height + 10
        
        # Draw IP label
        self.draw_text("Dirección IP del servidor:", 
                      self.display_manager.virtual_width // 2, ip_label_y)
        
        # Draw IP input field
        ip_field_rect = self.display_manager.get_centered_rect(field_width, field_height)
        ip_field_rect.y = ip_field_y
        self.draw_input_field(self.ip_input, ip_field_rect, "ip", 
                             self.active_field == "ip")
        
        # Port section
        port_label_y = ip_field_y + field_height + 30
        port_field_y = port_label_y + label_height + 10
        
        # Draw Port label
        self.draw_text("Puerto:", 
                      self.display_manager.virtual_width // 2, port_label_y)
        
        # Draw Port input field
        port_field_rect = self.display_manager.get_centered_rect(field_width, field_height)
        port_field_rect.y = port_field_y
        self.draw_input_field(self.port_input, port_field_rect, "port", 
                             self.active_field == "port")
        
        # Buttons section
        button_width = 150
        button_height = 50
        button_y = port_field_y + field_height + 50
        button_spacing = 50
        
        # Connect button
        connect_rect = pygame.Rect(0, button_y, button_width, button_height)
        connect_rect.centerx = self.display_manager.virtual_width // 2 - button_width // 2 - button_spacing // 2
        self.draw_button("CONECTAR", connect_rect, "connect", self.GREEN)
        
        # Back button  
        back_rect = pygame.Rect(0, button_y, button_width, button_height)
        back_rect.centerx = self.display_manager.virtual_width // 2 + button_width // 2 + button_spacing // 2
        self.draw_button("VOLVER", back_rect, "back")
        
        # Connection status
        if self.connection_status:
            status_color = self.RED if "Error" in self.connection_status else self.BLUE
            self.draw_text(self.connection_status,
                          self.display_manager.virtual_width // 2, 
                          button_y + button_height + 40,
                          color=status_color)
        
    def draw_connecting_screen(self):
        """Draw the connecting screen."""
        self.screen.fill(self.WHITE)
        
        # Clear rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("CONECTANDO...")
        
        # Draw connecting message
        self.draw_text("Conectando al servidor...", 
                      self.display_manager.virtual_width // 2, 300)
        
        # Cancel button
        cancel_rect = self.display_manager.get_centered_rect(200, 50)
        cancel_rect.y = 400
        self.draw_button("CANCELAR", cancel_rect, "cancel", self.RED)
        
    def draw_playing_screen(self):
        """Draw the multiplayer game screen."""
        self.screen.fill(self.WHITE)
        
        # Clear rectangles
        self.button_rects.clear()
        
        # Draw title
        self.draw_title("JUGANDO EN LÍNEA")
        
        # Draw game area (placeholder)
        game_area_rect = pygame.Rect(50, 150, 700, 350)
        actual_game_rect = self.display_manager.scale_rect(game_area_rect)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, actual_game_rect)
        pygame.draw.rect(self.screen, self.BLACK, actual_game_rect, 3)
        
        # Game instructions
        self.draw_text("Juego multijugador en progreso", 
                      self.display_manager.virtual_width // 2, 325)
        self.draw_text("Presiona ESC para desconectar", 
                      self.display_manager.virtual_width // 2, 550, font_size=20)
        
    def handle_input_click(self, mouse_pos):
        """Handle clicks on input fields."""
        for field_id, rect in self.input_rects.items():
            if rect.collidepoint(mouse_pos):
                self.active_field = field_id
                return True
        return False
        
    def handle_button_click(self, mouse_pos):
        """Handle clicks on buttons using direct collision detection."""
        for button_id, rect in self.button_rects.items():
            if rect.collidepoint(mouse_pos):
                if button_id == "connect":
                    self.attempt_connection()
                elif button_id == "back":
                    self.result = "back_to_main"
                    self.running = False
                elif button_id == "cancel":
                    self.current_state = "ip_input"
                    self.connection_status = "Conexión cancelada"
                return True
        return False
        
    def handle_text_input(self, text):
        """Handle text input for the active field."""
        if self.active_field == "ip":
            if len(self.ip_input) < 15:  # IP address length limit
                self.ip_input += text
        elif self.active_field == "port":
            if len(self.port_input) < 5 and text.isdigit():  # Port number limit
                self.port_input += text
                
    def handle_backspace(self):
        """Handle backspace for the active field."""
        if self.active_field == "ip":
            self.ip_input = self.ip_input[:-1]
        elif self.active_field == "port":
            self.port_input = self.port_input[:-1]
            
    def attempt_connection(self):
        """Attempt to connect to the server."""
        if not self.ip_input.strip():
            self.connection_status = "Error: Ingrese una dirección IP"
            return
            
        if not self.port_input.strip() or not self.port_input.isdigit():
            self.connection_status = "Error: Puerto inválido"
            return
            
        try:
            port = int(self.port_input)
            if port < 1 or port > 65535:
                self.connection_status = "Error: Puerto debe estar entre 1 y 65535"
                return
                
            self.connection_status = "Conectando..."
            self.current_state = "connecting"
            
            # Simulate connection attempt (replace with actual socket code)
            # This is where you would implement the real socket connection
            self.simulate_connection()
            
        except ValueError:
            self.connection_status = "Error: Puerto inválido"
            
    def simulate_connection(self):
        """Simulate connection for demonstration purposes."""
        # In a real implementation, this would be actual socket connection code
        import time
        
        # Simulate connection delay
        pygame.time.wait(1000)
        
        # For demo purposes, assume connection succeeds
        self.current_state = "playing"
        self.connection_status = "Conectado exitosamente"
        
    def handle_key_press(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            if self.current_state == "playing":
                self.current_state = "ip_input"
                self.connection_status = "Desconectado"
            else:
                self.result = "back_to_main"
                self.running = False
        elif key == pygame.K_TAB and self.current_state == "ip_input":
            # Switch between input fields
            self.active_field = "port" if self.active_field == "ip" else "ip"
        elif key == pygame.K_RETURN and self.current_state == "ip_input":
            self.attempt_connection()
        elif key == pygame.K_BACKSPACE and self.current_state == "ip_input":
            self.handle_backspace()
            
    def run(self):
        """Run the multiplayer game loop with proper resizing support."""
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.result = "exit"
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize - this was missing in the original
                    self.display_manager.update_actual_size(event.w, event.h)
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Try input fields first, then buttons
                        if not self.handle_input_click(event.pos):
                            self.handle_button_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                elif event.type == pygame.TEXTINPUT and self.current_state == "ip_input":
                    # Handle text input for fields
                    self.handle_text_input(event.text)
                    
            # Draw current state
            if self.current_state == "ip_input":
                self.draw_ip_input_screen()
            elif self.current_state == "connecting":
                self.draw_connecting_screen()
            elif self.current_state == "playing":
                self.draw_playing_screen()
                
            pygame.display.flip()
            clock.tick(60)
            
        return self.result