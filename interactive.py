from rembg import remove
from rembg import bg
human_session = bg.new_session("u2net_human_seg")
from PIL import Image,ImageEnhance,ImageOps
import streamlit as st


st.title('Auto Bluewash')
upload = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if upload is not None:
    input = Image.open(upload)

    #Make alpha channel
    original = Image.new('RGBA', input.size)
    original.paste(input)

    #Remove BG with u2net_human_seg
    with st.sidebar:
        tint = st.slider('Tint', 0, 255, 141)
        contrast = st.slider('Contrast', 0.0, 2.0, 1.2)
        brightness = st.slider('Brightness', 0.0, 2.0, 0.6)
        alpha_blend = st.slider('Edge blur',0,40,20)
    output = remove(input,alpha_matting=True,session=human_session,post_process_mask=True, alpha_matting_erode_size=alpha_blend)
    background = Image.new('RGBA', input.size, (0,174,239,tint))
    blend = Image.alpha_composite(background, output)

    original = ImageOps.grayscale(original)
    
    
    #Apply contrast + brightnessadjustments
    contrast_enhancer = ImageEnhance.Contrast(original)
    brightness_enhancer = ImageEnhance.Brightness(original)
    original = contrast_enhancer.enhance(contrast)
    original = brightness_enhancer.enhance(brightness)
    original = original.convert('RGBA')
    original.alpha_composite(blend)
    st.image(original)