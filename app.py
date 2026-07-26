import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("198 Nonviolent Revolutionary Actions.xlsx")

df = load_data()

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

    # Load fonts (using standard default or uploaded TTF fonts)
    try:
        font_bold = ImageFont.truetype("Arial Bold.ttf", 72)
        font_regular = ImageFont.truetype("Arial.ttf", 54)
        font_footer = ImageFont.truetype("Arial.ttf", 26)
    except IOError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # 1. Render Centered Action ID near the top
    id_str = str(uuid)
    id_bbox = draw.textbbox((0, 0), id_str, font=font_bold)
    id_width = id_bbox[2] - id_bbox[0]
    draw.text(((width - id_width) / 2, 220), id_str, font=font_bold, fill=text_color)

    # 2. Render Centered Action Text below with good spacing
    wrapped_action = textwrap.wrap(action_text, width=22)
    y_text = 400
    for line in wrapped_action:
        line_bbox = draw.textbbox((0, 0), line, font=font_regular)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(((width - line_width) / 2, y_text), line, font=font_regular, fill=text_color)
        y_text += 75

    # 3. Render Footer perfectly on the bottom margin
    footer_text = "The Chicago Commons Independent Media for the Public Square"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
    footer_width = footer_bbox[2] - footer_bbox[0]
    
    # Positioned right at the bottom margin
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