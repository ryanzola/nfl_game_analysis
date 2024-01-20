import math

# Function to create a space holder for the logo
def create_logo_placeholder(placeholder, logo_path=None, width=150, height=162):
    if logo_path:
        placeholder.image(logo_path, width=width)
    else:
        # Create an empty space of specified height
        placeholder.markdown(f"<div style='height: {height}px; aspect-ratio: 1/1'></div>", unsafe_allow_html=True)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    """Calculate the Euclidean distance between two RGB colors."""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def are_colors_too_similar(color1, color2, threshold=100):
    """Check if two colors are too similar based on a distance threshold."""
    return color_distance(color1, color2) < threshold
