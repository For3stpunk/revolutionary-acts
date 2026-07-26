import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os


# -----------------------------------------
# Streamlit Configuration
# -----------------------------------------

st.set_page_config(
    page_title="198 Nonviolent Revolutionary Actions",
    layout="wide"
)


# -----------------------------------------
# Load Dataset
# -----------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel(
        "198 Nonviolent Revolutionary Actions.xlsx"
    )


df = load_data()



# -----------------------------------------
# Font Loader
# Uses repository fonts folder
# -----------------------------------------

def get_font(size, bold=False):

    if bold:
        font_path = "fonts/DejaVuSans-Bold.ttf"
    else:
        font_path = "fonts/DejaVuSans.ttf"


    if not os.path.exists(font_path):
        raise FileNotFoundError(
            f"Missing font file: {font_path}"
        )


    return ImageFont.truetype(
        font_path,
        size
    )



# -----------------------------------------
# Generate Card
# -----------------------------------------

def generate_card():

    action_id = random.randint(
        1,
        198
    )


    row = df[
        df["ID"] == action_id
    ]


    if not row.empty:
        action = str(
            row["Action"].values[0]
        )
    else:
        action = "Unknown Action"



    width = 1080
    height = 1080


    bg_color = "#F9F9F7"
    text_color = "#111111"
    footer_color = "#555555"



    image = Image.new(
        "RGB",
        (
            width,
            height
        ),
        bg_color
    )


    draw = ImageDraw.Draw(
        image
    )



    # ---------------------------------
    # Large Action Number
    # ---------------------------------

    number_font = get_font(
        260,
        bold=True
    )


    number_text = f"#{action_id}"


    bbox = draw.textbbox(
        (0, 0),
        number_text,
        font=number_font
    )


    number_width = (
        bbox[2]
        -
        bbox[0]
    )


    draw.text(
        (
            (width - number_width) / 2,
            50
        ),
        number_text,
        font=number_font,
        fill=text_color
    )



    # ---------------------------------
    # Large Centered Action Text
    # ---------------------------------

    wrapped_text = textwrap.wrap(
        action,
        width=15
    )


    font_size = 150


    while font_size >= 60:

        action_font = get_font(
            font_size,
            bold=True
        )


        fits = True


        for line in wrapped_text:

            bbox = draw.textbbox(
                (0, 0),
                line,
                font=action_font
            )


            line_width = (
                bbox[2]
                -
                bbox[0]
            )


            if line_width > 900:
                fits = False
                break


        if fits:
            break


        font_size -= 5



    line_height = font_size + 25


    total_height = (
        len(wrapped_text)
        *
        line_height
    )


    y_position = (
        560
        -
        total_height / 2
    )



    for line in wrapped_text:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=action_font
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
            font=action_font,
            fill=text_color
        )


        y_position += line_height



    # ---------------------------------
    # Footer
    # ---------------------------------

    footer_font = get_font(
        28,
        bold=False
    )


    footer_text = (
        "The Chicago Commons Independent "
        "Media for the Public Square"
    )


    bbox = draw.textbbox(
        (0, 0),
        footer_text,
        font=footer_font
    )


    footer_width = (
        bbox[2]
        -
        bbox[0]
    )


    draw.text(
        (
            (width - footer_width) / 2,
            height - 80
        ),
        footer_text,
        font=footer_font,
        fill=footer_color
    )


    return image, action_id, action



# -----------------------------------------
# Streamlit Interface
# -----------------------------------------

st.title(
    "The Chicago Commons: 198 Actions Card Generator"
)


st.write(
    "Generate minimalist social media cards based on "
    "the 198 Nonviolent Revolutionary Actions dataset."
)



if st.button(
    "Generate Random Card"
):

    img, action_id, action = generate_card()


    left, center, right = st.columns(
        [1, 4, 1]
    )


    with center:

        st.image(
            img,
            width=850,
            caption=f"Action #{action_id}: {action}"
        )


    buffer = io.BytesIO()


    img.save(
        buffer,
        format="PNG"
    )


    st.download_button(
        label="Download Card (PNG)",
        data=buffer.getvalue(),
        file_name=f"action_{action_id}_card.png",
        mime="image/png"
    )
