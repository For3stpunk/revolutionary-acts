import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os


# -----------------------------------------
# Page Configuration
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
# Font Loader (Streamlit Cloud Compatible)
# -----------------------------------------

def get_font(size, bold=False):

    fonts = [

        # Streamlit Cloud / Linux
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),

        (
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        ),

        (
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
            if bold
            else "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        ),

        # Windows fallback
        (
            r"C:\Windows\Fonts\arialbd.ttf"
            if bold
            else r"C:\Windows\Fonts\arial.ttf"
        )
    ]


    for font_path in fonts:

        if os.path.exists(font_path):

            return ImageFont.truetype(
                font_path,
                size
            )


    # Never use PIL default font
    # because it is tiny
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
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
    # Action Number
    # ---------------------------------

    number_font = get_font(
        260,
        bold=True
    )


    number = f"#{action_id}"


    bbox = draw.textbbox(
        (0,0),
        number,
        font=number_font
    )


    number_width = (
        bbox[2]
        -
        bbox[0]
    )


    draw.text(
        (
            (width-number_width)/2,
            40
        ),
        number,
        font=number_font,
        fill=text_color
    )



    # ---------------------------------
    # Action Text
    # ---------------------------------

    wrapped = textwrap.wrap(
        action,
        width=14
    )


    # Start very large
    action_size = 150


    while action_size > 60:

        action_font = get_font(
            action_size,
            bold=True
        )


        fits = True


        for line in wrapped:

            bbox = draw.textbbox(
                (0,0),
                line,
                font=action_font
            )


            if (
                bbox[2]
                -
                bbox[0]
                >
                900
            ):

                fits = False



        if fits:

            break


        action_size -= 5



    line_height = action_size + 20


    total_height = (
        len(wrapped)
        *
        line_height
    )


    y = (
        540
        -
        total_height / 2
    )



    for line in wrapped:

        bbox = draw.textbbox(
            (0,0),
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
                (width-line_width)/2,
                y
            ),
            line,
            font=action_font,
            fill=text_color
        )


        y += line_height



    # ---------------------------------
    # Footer
    # ---------------------------------

    footer_font = get_font(
        28,
        bold=False
    )


    footer = (
        "The Chicago Commons Independent "
        "Media for the Public Square"
    )


    bbox = draw.textbbox(
        (0,0),
        footer,
        font=footer_font
    )


    footer_width = (
        bbox[2]
        -
        bbox[0]
    )


    draw.text(
        (
            (width-footer_width)/2,
            height-70
        ),
        footer,
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
    "Generate minimalist social media cards based on the "
    "198 Nonviolent Revolutionary Actions dataset."
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
