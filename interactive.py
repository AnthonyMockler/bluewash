from rembg import remove
from rembg import bg
human_session = bg.new_session("u2net_human_seg")
from PIL import Image,ImageEnhance,ImageOps
import streamlit as st


st.title('Auto Bluewash')
upload = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if upload is not None:
    input = Image.open(upload)
    original = Image.new('RGBA', input.size)
    original.paste(input)
    output = remove(input,alpha_matting=True,session=human_session)
    with st.sidebar:
        tint = st.slider('Tint', 0, 255, 141)
    background = Image.new('RGBA', input.size, (0,174,239,tint))

    blend = Image.alpha_composite(background, output)

    original = ImageOps.grayscale(original)
    enhancer = ImageEnhance.Contrast(original)
    with st.sidebar:
        factor = st.slider('Contrast', 0.0, 2.0, 1.2)
    original = enhancer.enhance(factor)

    enhancer = ImageEnhance.Brightness(original)
    with st.sidebar:
        factor = st.slider('Brightness', 0.0, 2.0, 0.6)
    original = enhancer.enhance(factor)

    original = original.convert('RGBA')
    original.alpha_composite(blend)
    st.image(original)
