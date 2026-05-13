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
import streamlit as st
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Adobe Scan Style PDF Converter",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Document Scanner")

st.write(
    "Upload an image and convert it into a clean scanned PDF "
    "similar to Adobe Scan."
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg", "webp"]
)

# ---------------- IMAGE PROCESSING FUNCTION ----------------
def scan_document(pil_image):

    # Convert PIL image to OpenCV format
    image = np.array(pil_image)

    # Convert RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Resize for better processing
    ratio = image.shape[0] / 500.0
    orig = image.copy()

    height = 500
    resized = cv2.resize(
        image,
        (int(image.shape[1] / ratio), height)
    )

    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Blur to remove noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edged = cv2.Canny(gray, 75, 200)

    # Find contours
    contours, _ = cv2.findContours(
        edged.copy(),
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    screen_contour = None

    # Detect document edges
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            screen_contour = approx
            break

    # If no document detected
    if screen_contour is None:
        processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        # Warp perspective
        pts = screen_contour.reshape(4, 2) * ratio

        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        (tl, tr, br, bl) = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)

        warped = cv2.warpPerspective(
            orig,
            M,
            (maxWidth, maxHeight)
        )

        # Convert to grayscale
        processed = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    # Adaptive threshold for Adobe Scan effect
    processed = cv2.adaptiveThreshold(
        processed,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return Image.fromarray(processed)

# ---------------- MAIN APP ----------------
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scanned PDF"):

        scanned = scan_document(image)

        st.subheader("Scanned Preview")
        st.image(scanned, use_container_width=True)

        # Convert to PDF
        pdf_buffer = BytesIO()

        pdf_image = scanned.convert("RGB")

        pdf_image.save(pdf_buffer, format="PDF")

        pdf_buffer.seek(0)

        st.success("PDF created successfully!")

        # Download button
        st.download_button(
            label="⬇ Download Scanned PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
