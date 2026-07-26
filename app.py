import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os


# -----------------------------------
# Load Dataset
# -----------------------------------

@st.cache_data
def load_data():
    return pd.read_excel("198 Nonviolent Revolutionary Actions.xlsx")


df = load_data()


# -----------------------------------
# Font Loader
# -----------------------------------

def get_font(size, bold=False):

    font_candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]

    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass

    return ImageFont.load_default()



# -----------------------------------
# Find Best Font Size
# -----------------------------------

def fit_font(draw, text, max_width, max_size, min_size):

    for size in range(max_size, min_size, -5):

        font = get_font(size, bold=True)

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            return font

    return get_font(min_size, bold=True)



# -----------------------------------
# Generate Card
# -----------------------------------

def generate_card():

    action_id = random.randint(1, 198)

    row = df[df["ID"] == action_id]


    if not row.empty:
        action = str(row["Action"].values[0])
    else:
        action = "Unknown Action"


    width = 1080
    height = 1080


    bg_color = "#F9F9F7"
    text_color = "#111111"
    footer_color = "#555555"


    image = Image.new(
        "RGB",
        (width, height),
        bg_color
    )


    draw = ImageDraw.Draw(image)



    # -----------------------------------
    # HUGE ACTION NUMBER
    # -----------------------------------

    number_font = get_font(
        300,
        bold=True
    )


    number_text = f"#{action_id}"


    bbox = draw.textbbox(
        (0,0),
        number_text,
        font=number_font
    )


    number_width = bbox[2]-bbox[0]


    draw.text(
        (
            (width-number_width)/2,
            40
        ),
        number_text,
        font=number_font,
        fill=text_color
    )



    # -----------------------------------
    # HUGE ACTION TEXT
    # -----------------------------------

    words = action.split()


    lines = []
    current = ""


    for word in words:

        test = current + " " + word

        if len(test) <= 18:
            current = test.strip()

        else:
            lines.append(current)
            current = word


    if current:
        lines.append(current)



    # Try large font sizes until it fits

    for size in range(170, 60, -5):

        action_font = get_font(
            size,
            bold=True
        )


        fits = True


        for line in lines:

            bbox = draw.textbbox(
                (0,0),
                line,
                font=action_font
            )

            if bbox[2]-bbox[0] > 900:
                fits = False


        if fits:
            break



    line_height = size + 20


    total_height = (
        len(lines)
        *
        line_height
    )


    y = (
        520
        -
        total_height/2
    )


    for line in lines:

        bbox = draw.textbbox(
            (0,0),
            line,
            font=action_font
        )


        line_width = bbox[2]-bbox[0]


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



    # -----------------------------------
    # Footer
    # -----------------------------------

    footer_font = get_font(
        30,
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


    footer_width = bbox[2]-bbox[0]


    draw.text(
        (
            (width-footer_width)/2,
            height-80
        ),
        footer,
        font=footer_font,
        fill=footer_color
    )


    return image, action_id, action



# -----------------------------------
# Streamlit Interface
# -----------------------------------

st.set_page_config(
    page_title="198 Actions Generator",
    layout="wide"
)


st.title(
    "The Chicago Commons: 198 Nonviolent Actions Card Generator"
)


st.write(
    "Generate minimalist social media cards from the 198 nonviolent actions dataset."
)



if st.button("Generate Random Card"):


    img, action_id, action = generate_card()


    left, center, right = st.columns(
        [1,4,1]
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
        label="Download Card PNG",
        data=buffer.getvalue(),
        file_name=f"action_{action_id}_card.png",
        mime="image/png"
    )
