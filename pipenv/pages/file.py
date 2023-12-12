import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io

def load_image(image_file):
    try:
        img = Image.open(image_file)
        return img
    except Exception as e:
        st.error(f"Error: {e}")
        st.error("Please provide an image in a supported format (png, jpg, jpeg).")
        return None

def enhance_image(original_image, contrast_factor):
    enhancer = ImageEnhance.Contrast(original_image)
    enhanced_image = enhancer.enhance(contrast_factor)
    return enhanced_image

def crop_image(original_image, left, top, right, bottom):  
    cropped_image = original_image.crop((left, top, right, bottom))
    return cropped_image

# def compress_img(original_image, target_width, target_height):
#     # Calculate new dimensions while preserving aspect ratio
#     aspect_ratio = original_image.width / original_image.height
    
#     if aspect_ratio >= 1:
#         new_width = target_width
#         new_height = int(target_width / aspect_ratio)
#     else:
#         new_height = target_height
#         new_width = int(target_height * aspect_ratio)

#     # Resize the image
#     resized_image = original_image.resize((new_width, new_height))

#     return resized_image

def apply_filter(original_image, filter_option):
    st.text(f"Applying {filter_option} filter")
    
    if filter_option == "original":
        return original_image
    elif filter_option == "blur":
        return original_image.filter(ImageFilter.BLUR)
    elif filter_option == "contour":
        return original_image.filter(ImageFilter.CONTOUR)
    elif filter_option == "emboss":
        return original_image.filter(ImageFilter.EMBOSS)
    elif filter_option == "FIND_EDGES":
        return original_image.filter(ImageFilter.FIND_EDGES)
    
def flipping(original_image,filter):
    if filter =="original":
        return original_image
    elif filter == "FLIP_LEFT_RIGHT":
        return original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif filter == "FLIP_TOP_BOTTOM":
        return original_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif filter == "TRANSPOSE":
        return original_image.transpose(Image.Transpose.TRANSPOSE)

def main():
    st.title("Image Processing App")

    # Main page options for user input
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if image_file:
        original_image = load_image(image_file)

        st.image(original_image, caption='Original Image', use_column_width=True)
        
        st.subheader("Enchncement")
        number_contrast = st.slider('Contrast Enhancement Factor', min_value=0.0, max_value=2.0, value=1.0)
        st.subheader("Select Crop ")
        crop_left = st.slider("Left", value=0, min_value=0, max_value=original_image.width - 1, step=1)
        crop_top = st.slider("Top", value=0, min_value=0, max_value=original_image.height - 1, step=1)
        crop_right = st.slider("Right", value=original_image.width, min_value=crop_left + 1, max_value=original_image.width, step=1)
        crop_bottom = st.slider("Bottom", value=original_image.height, min_value=crop_top + 1, max_value=original_image.height, step=1)
        
        st.subheader("Filtering an image")
        filter_option = st.selectbox(
            "Filter:",
            ("original", "blur", "contour", "emboss", "FIND_EDGES"),
            help="Select Filter method"
        )
        st.subheader("Flipping an image")
        filter= st.selectbox(
            "Flipping:",
            ("original","FLIP_LEFT_RIGHT", "FLIP_TOP_BOTTOM", "TRANSPOSE"),
            help="Select Filter method"
        )
        
        # Update the displayed image in real-time
        
        enhanced_image = enhance_image(original_image, number_contrast)
        cropped_image = crop_image(enhanced_image, crop_left, crop_top, crop_right, crop_bottom)
        # resized_image = compress_img(cropped_image, edge_1, edge_2)
        filtered_image = apply_filter(cropped_image, filter_option)
        flip=flipping(filtered_image,filter)
        
        st.image(flip, caption=f'Filtered Image')

        if st.button("Download Processed Image"):
            # Download button for the final processed image
            processed_image_bytes = io.BytesIO()
            filtered_image.save(processed_image_bytes, format='PNG')
            st.download_button(
                label="Download Processed Image",
                data=processed_image_bytes.getvalue(),
                file_name="processed_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
