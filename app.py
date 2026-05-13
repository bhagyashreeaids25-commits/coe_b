import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from io import BytesIO

# Page settings
st.set_page_config(
    page_title="Adobe Scan Style PDF Converter",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Adobe Scan Style Image to PDF Converter")
st.write(
    "Upload an image, convert it into a clean black & white scanned PDF, and download it."
)

# Upload image
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    # Display original image
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Convert button
    if st.button("Convert to Scanned PDF"):

        # Step 1: Convert to grayscale
        gray = ImageOps.grayscale(image)

        # Step 2: Increase sharpness
        sharp = ImageEnhance.Sharpness(gray)
        gray = sharp.enhance(2.5)

        # Step 3: Increase contrast
        contrast = ImageEnhance.Contrast(gray)
        gray = contrast.enhance(2)

        # Step 4: Reduce noise
        gray = gray.filter(ImageFilter.MedianFilter(size=3))

        # Step 5: Convert to pure black & white
        bw = gray.point(lambda x: 0 if x < 140 else 255, '1')

        # Preview processed image
        st.subheader("Scanned Preview")
        st.image(bw, use_container_width=True)

        # Convert to PDF
        pdf_buffer = BytesIO()

        pdf_image = bw.convert("RGB")
        pdf_image.save(pdf_buffer, format="PDF")

        pdf_buffer.seek(0)

        st.success("PDF created successfully!")

        # Download button
        st.download_button(
            label="⬇ Download PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Live Adobe Scan Style PDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Live Adobe Scan Style PDF Converter")

st.write(
    "Capture an image live from camera or upload one, "
    "convert it into a clean black & white scanned PDF, "
    "and download it."
)

# ---------------- IMAGE INPUT ----------------
option = st.radio(
    "Choose Input Method",
    ["📷 Use Camera", "🖼 Upload Image"]
)

image = None

# Live Camera Capture
if option == "📷 Use Camera":
    captured_image = st.camera_input("Take a Picture")

    if captured_image is not None:
        image = Image.open(captured_image)

# File Upload
else:
    uploaded_file = st.file_uploader(
        "Upload an Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# ---------------- PROCESS IMAGE ----------------
if image is not None:

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scanned PDF"):

        # Convert to grayscale
        gray = ImageOps.grayscale(image)

        # Enhance sharpness
        sharp = ImageEnhance.Sharpness(gray)
        gray = sharp.enhance(2.5)

        # Enhance contrast
        contrast = ImageEnhance.Contrast(gray)
        gray = contrast.enhance(2)

        # Noise reduction
        gray = gray.filter(ImageFilter.MedianFilter(size=3))

        # Convert to black & white threshold
        bw = gray.point(lambda x: 0 if x < 140 else 255, '1')

        st.subheader("Scanned Preview")
        st.image(bw, use_container_width=True)

        # ---------------- PDF GENERATION ----------------
        pdf_buffer = BytesIO()

        pdf_image = bw.convert("RGB")

        pdf_image.save(pdf_buffer, format="PDF")

        pdf_buffer.seek(0)

        st.success("PDF created successfully!")

        # ---------------- DOWNLOAD BUTTON ----------------
        st.download_button(
            label="⬇ Download Scanned PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
