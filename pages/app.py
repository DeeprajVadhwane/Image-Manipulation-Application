import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io

st.title("Image Processing App")

def load_image(image_file):
    try:
        img = Image.open(image_file)
        return img
    except Exception as e:
        st.error(f"Error: {e}")
        st.error("Please provide an image in a supported format (png, jpg, jpeg).")
        return None
    
# Image Enhancement Section
st.markdown("## Image Enhancement")
st.sidebar.markdown("Choose an enhancement option:")

image_file_enhance = st.file_uploader("Upload Image for Enhancement", type=["png", "jpg", "jpeg"])

if image_file_enhance is not None:
    number_contrast = st.sidebar.number_input('Contrast Enhancement Factor', min_value=0.0, max_value=2.0, value=1.0)
    original_image_enhance = load_image(image_file_enhance)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(original_image_enhance)
    enhanced_image = enhancer.enhance(number_contrast)

    # Display the original and enhanced images
    st.image([original_image_enhance, enhanced_image], caption=['Original Image', 'Contrast Enhanced Image'], use_column_width=True)

    # Download Button for Enhanced Image
    if st.button("Download Enhanced Image"):
        enhanced_image_bytes = io.BytesIO()
        enhanced_image.save(enhanced_image_bytes, format='PNG')
        st.download_button(
            label="Download Enhanced Image",
            data=enhanced_image_bytes.getvalue(),
            file_name="enhanced_image.png",
            mime="image/png"
        )

# Image Cropping Section
st.markdown("## Image Cropping")
st.sidebar.markdown("Choose the crop parameters:")

image_file_crop = st.file_uploader("Upload Image for Cropping", type=["jpg", "jpeg", "png"])

if image_file_crop is not None:
    original_image_crop = Image.open(image_file_crop)
    
    crop_left = st.sidebar.number_input("Left", value=0, min_value=0, max_value=original_image_crop.width - 1, step=1)
    crop_top = st.sidebar.number_input("Top", value=0, min_value=0, max_value=original_image_crop.height - 1, step=1)
    crop_right = st.sidebar.number_input("Right", value=original_image_crop.width, min_value=crop_left + 1, max_value=original_image_crop.width, step=1)
    crop_bottom = st.sidebar.number_input("Bottom", value=original_image_crop.height, min_value=crop_top + 1, max_value=original_image_crop.height, step=1)

    # Crop the image
    cropped_image = original_image_crop.crop((crop_left, crop_top, crop_right, crop_bottom))
    st.image(cropped_image, caption="Cropped Image", use_column_width=True)

    # Download Button for Cropped Image
    if st.button("Download Cropped Image"):
        cropped_image_bytes = io.BytesIO()
        cropped_image.save(cropped_image_bytes, format='PNG')
        st.download_button(
            label="Download Cropped Image",
            data=cropped_image_bytes.getvalue(),
            file_name="cropped_image.png",
            mime="image/png"
        )

# Image Filtering Section
st.markdown("Image Filtering")
st.sidebar.markdown("Choose a filter option:")

image_file_filter = st.file_uploader("Upload Image for Filtering", type=["png","jpg","jpeg"])

if image_file_filter is not None:
    filter_option = st.sidebar.selectbox(
        "Filter:",
        ("blur", "contour", "emboss", "FIND_EDGES"),
        index=None, placeholder="Select Filter method...",
    )

    original_image_filter = load_image(image_file_filter)

    if filter_option == "blur":
        filtered_image = original_image_filter.filter(ImageFilter.BLUR)
        st.image([original_image_filter,filtered_image ], caption=['Original Image',"filtered_image"], use_column_width=True)
    
    elif filter_option == "contour":
        filtered_image = original_image_filter.filter(ImageFilter.CONTOUR)
        st.image([original_image_filter,filtered_image ], caption=['Original Image',"filtered_image"], use_column_width=True)
        
    
    elif filter_option == "FIND_EDGES":
        filtered_image = original_image_filter.filter(ImageFilter.FIND_EDGES)
        st.image([original_image_filter,filtered_image ], caption=['Original Image',"filtered_image"], use_column_width=True)
        
    
    elif filter_option == "emboss":
        filtered_image = original_image_filter.filter(ImageFilter.EMBOSS)
        st.image([original_image_filter,filtered_image ], caption=['Original Image',"filtered_image"], use_column_width=True)

    # Download Button for Filtered Image
    if st.button("Download Filtered Image"):
        filtered_image_bytes = io.BytesIO()
        filtered_image.save(filtered_image_bytes, format='PNG')
        st.download_button(
            label="Download Filtered Image",
            data=filtered_image_bytes.getvalue(),
            file_name=f"filtered_{filter_option.lower()}_image.png",
            mime="image/png"
        )
