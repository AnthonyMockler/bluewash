from rembg import remove
from rembg import bg
human_session = bg.new_session("u2net_human_seg")
from PIL import Image,ImageEnhance,ImageOps
import streamlit as st
input_path = 'UN0353496.jpg'
#output_path = 'output.png'


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


st.title('Auto Bluewash')
upload = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if not upload:
    upload = input_path
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
