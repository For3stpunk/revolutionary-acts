import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os


# -------------------------
# Load Dataset
# -------------------------

@st.cache_data
def load_data():
    return pd.read_excel("198 Nonviolent Revolutionary Actions.xlsx")


df = load_data()


# -------------------------
# Font Loader
# -------------------------

def get_font(size, bold=False):
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",

        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",

        r"C:\Windows\Fonts\arialbd.ttf"
        if bold else r"C:\Windows\Fonts\arial.ttf",

        "/Library/Fonts/Arial Bold.ttf"
        if bold else "/Library/Fonts/Arial.ttf",
    ]

    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    return ImageFont.load_default()


# -------------------------
# Generate Card
# -------------------------

def generate_card():

    # Pick random action
    uuid = random.randint(1, 198)

    row = df[df["ID"] == uuid]

    if not row.empty:
        action_text = row["Action"].values[0]
    else:
        action_text = "Unknown Action"


    # Canvas
    width = 1080
    height = 1080

    bg_color = "#F9F9F7"
    text_color = "#1A1A1A"
    accent_color = "#555555"


    image = Image.new(
        "RGB",
        (width, height),
        bg_color
    )

    draw = ImageDraw.Draw(image)


    # Fonts
    font_id = get_font(
        220,
        bold=True
    )

    font_action = get_font(
        105,
        bold=True
    )

    font_footer = get_font(
        28,
        bold=False
    )


    # -------------------------
    # Action Number
    # -------------------------

    id_text = f"#{uuid}"

    id_bbox = draw.textbbox(
        (0, 0),
        id_text,
        font=font_id
    )

    id_width = id_bbox[2] - id_bbox[0]

    draw.text(
        (
            (width - id_width) / 2,
            80
        ),
        id_text,
        font=font_id,
        fill=text_color
    )


    # -------------------------
    # Action Text
    # -------------------------

    # Wrap text
    wrapped_action = textwrap.wrap(
        action_text,
        width=13
    )


    line_height = 125

    total_height = (
        len(wrapped_action)
        *
        line_height
    )


    y_position = (
        height / 2
        -
        total_height / 2
        -
        20
    )


    for line in wrapped_action:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font_action
        )

        line_width = (
            bbox[2]
            -
            bbox[0]
        )


        draw.text(
            (
                (width - line_width) / 2,
                y_position
            ),
            line,
            font=font_action,
            fill=text_color
        )


        y_position += line_height



    # -------------------------
    # Footer
    # -------------------------

    footer = (
        "The Chicago Commons Independent "
        "Media for the Public Square"
    )


    footer_bbox = draw.textbbox(
        (0, 0),
        footer,
        font=font_footer
    )


    footer_width = (
        footer_bbox[2]
        -
        footer_bbox[0]
    )


    draw.text(
        (
            (width - footer_width) / 2,
            height - 75
        ),
        footer,
        font=font_footer,
        fill=accent_color
    )


    return image, uuid, action_text



# -------------------------
# Streamlit App
# -------------------------

st.set_page_config(
    page_title="198 Nonviolent Actions Generator",
    layout="wide"
)


st.title(
    "The Chicago Commons: 198 Actions Card Generator"
)


st.write(
    "Generate minimalist social media cards based on the "
    "198 Nonviolent Revolutionary Actions dataset."
)



if st.button("Generate Random Card"):

    img, uuid, action = generate_card()


    # Center image
    col1, col2, col3 = st.columns(
        [1, 3, 1]
    )


    with col2:

        st.image(
            img,
            caption=f"Action #{uuid}: {action}",
            use_container_width=True
        )


    # Download button

    buffer = io.BytesIO()

    img.save(
        buffer,
        format="PNG"
    )


    st.download_button(
        label="Download Card (PNG)",
        data=buffer.getvalue(),
        file_name=f"action_{uuid}_card.png",
        mime="image/png"
    )
