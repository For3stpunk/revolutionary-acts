import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("198 Nonviolent Revolutionary Actions.xlsx")

df = load_data()

def get_font(size, bold=False):
    # Cross-platform font path resolution
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
                
    return ImageFont.load_default()

def generate_card():
    # Pick a random action (1 to 198)
    uuid = random.randint(1, 198)
    row = df[df['ID'] == uuid]
    action_text = row['Action'].values[0] if not row.empty else "Unknown Action"

    # Set up the image (1080x1080 square for social media)
    width, height = 1080, 1080
    bg_color = "#F9F9F7" # Off-white background
    text_color = "#1A1A1A" # Dark text
    accent_color = "#555555" # Gray for footer

    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Load significantly larger, bold fonts for high impact
    font_bold = get_font(140, bold=True)
    font_regular = get_font(84, bold=True)
    font_footer = get_font(26, bold=False)

    # 1. Render Centered Action ID near the top
    id_str = str(uuid)
    id_bbox = draw.textbbox((0, 0), id_str, font=font_bold)
    id_width = id_bbox[2] - id_bbox[0]
    draw.text(((width - id_width) / 2, 140), id_str, font=font_bold, fill=text_color)

    # 2. Render Centered Action Text below with proportional wrapping
    wrapped_action = textwrap.wrap(action_text, width=14)
    
    line_height = 100
    y_text = 420

    for line in wrapped_action:
        line_bbox = draw.textbbox((0, 0), line, font=font_regular)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(((width - line_width) / 2, y_text), line, font=font_regular, fill=text_color)
        y_text += line_height

    # 3. Render Footer perfectly on the bottom margin
    footer_text = "The Chicago Commons Independent Media for the Public Square"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
    footer_width = footer_bbox[2] - footer_bbox[0]
    
    draw.text(((width - footer_width) / 2, height - 60), footer_text, font=font_footer, fill=accent_color)

    return image, uuid, action_text

# Streamlit UI
st.title("The Chicago Commons: 198 Actions Card Generator")
st.write("Generate minimalist social media cards based on the 198 nonviolent actions dataset.")

if st.button("Generate Random Card"):
    img, uuid, action = generate_card()
    st.image(img, caption=f"Action #{uuid}: {action}", use_container_width=True)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Card (PNG)",
        data=byte_im,
        file_name=f"action_{uuid}_card.png",
        mime="image/png"
    )
