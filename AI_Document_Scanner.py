import streamlit as st
from PIL import Image
import json
import io
import base64
import pandas as pd
import cv2
import numpy as np
import easyocr
import re
from datetime import datetime

reader = easyocr.Reader(['en'])


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Transaction Scanner",
    page_icon="📄",
    layout="wide"
)


# -------------------------------
# Custom CSS Styling
# -------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size:40px;
        font-weight:bold;
        text-align:center;
    }

    .sub-title {
        font-size:20px;
        text-align:center;
        color:gray;
    }

    .box {
        padding:20px;
        border-radius:15px;
        border:1px solid #ddd;
        background-color:#fafafa;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# -------------------------------
# Application Header
# -------------------------------

st.markdown(
    "<div class='main-title'>📄 AI Transaction Scanner</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Scan GPay Transactions, Bills, Receipts and Documents using AI</div>",
    unsafe_allow_html=True
)


st.write("")


# -------------------------------
# Initialize Session Variables
# -------------------------------

if "scan_result" not in st.session_state:

    st.session_state.scan_result = None


if "image" not in st.session_state:

    st.session_state.image = None

        


# -------------------------------
# Sidebar Settings
# -------------------------------

with st.sidebar:

    st.header("⚙ Settings")

    st.write(
        """
        This AI Scanner can extract:

        ✔ Transaction ID

        ✔ Amount

        ✔ Date

        ✔ Time

        ✔ UPI ID

        ✔ Bank Details

        ✔ Merchant Name

        ✔ Reference Number

        ✔ Notes

        ✔ Bill Information

        """
    )


    st.divider()



    


# -------------------------------
# Main Upload Section
# -------------------------------


left, right = st.columns(2)



with left:

    st.subheader("📷 Scan Document")


    uploaded_file = st.file_uploader(
        "Upload Image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    camera_file = st.camera_input(
        "Capture Using Camera"
    )


    image = None


    if uploaded_file:

        image = Image.open(uploaded_file)

        st.session_state.image = image



    elif camera_file:

        image = Image.open(camera_file)

        st.session_state.image = image



    if image:

        st.image(
            image,
            caption="Selected Document",
            use_container_width=True
        )



with right:

    st.subheader("📊 Transaction Dashboard")


    if st.session_state.scan_result is None:

        st.info(
            "Scan a document to display extracted information"
        )

    else:

        st.success(
            "Document Processed Successfully"
        )


# -------------------------------
# Footer
# -------------------------------


st.divider()


st.caption(
    "Built using Python + Streamlit + OpenCV + EasyOCR"
)

# -------------------------------
# Image Preprocessing
# -------------------------------

def preprocess_image(image):

    # Convert PIL image to NumPy array
    image = np.array(image)

    # Convert RGB to OpenCV BGR format
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Make text clearer
    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return processed

def extract_text(image):

    result = reader.readtext(image)

    extracted_text = ""

    for item in result:
        extracted_text += item[1] + "\n"

    return extracted_text



# -------------------------------
# Scan Document Function
# -------------------------------



# -------------------------------
# Replace Temporary Scan Button
# -------------------------------


# -------------------------------
# Get Value Safely
# -------------------------------


def get_value(data, key):


    value = data.get(key)


    if value is None or value == "":


        return "Not Available"



    return value




# -------------------------------
# Format Extracted Information
# -------------------------------


def format_transaction_data(result):


    try:


        formatted = {



            "Transaction ID":

            get_value(
                result,
                "transaction_id"
            ),




            "Amount":

            get_value(
                result,
                "amount"
            ),




            "Date":

            get_value(
                result,
                "date"
            ),




            "Time":

            get_value(
                result,
                "time"
            ),




            "UPI ID":

            get_value(
                result,
                "upi_id"
            ),




            "Merchant":

            get_value(
                result,
                "merchant"
            ),




            "Bank":

            get_value(
                result,
                "bank"
            ),




            "Reference Number":

            get_value(
                result,
                "reference_no"
            ),




            "Payment Status":

            get_value(
                result,
                "status"
            ),




            "Payment Method":

            get_value(
                result,
                "payment_method"
            ),




            "Note":

            get_value(
                result,
                "note"
            ),




            "Invoice Number":

            get_value(
                result,
                "invoice_number"
            ),




            "GST Number":

            get_value(
                result,
                "gst_number"
            ),




            "Total Amount":

            get_value(
                result,
                "total"
            )

        }



        return formatted



    except Exception as error:


        return {


            "Error":

            str(error)

        }





# -------------------------------
# Display Dashboard
# -------------------------------


def display_dashboard(data):


    st.subheader(
        "📊 Extracted Document Details"
    )



    formatted_data = format_transaction_data(
        data
    )



    col1, col2 = st.columns(2)



    items = list(
        formatted_data.items()
    )



    half = len(items)//2



    with col1:


        for key,value in items[:half]:


            st.markdown(
                f"""
                <div class="box">

                <b>{key}</b>

                <br>

                {value}

                </div>
                """,

                unsafe_allow_html=True

            )



    with col2:


        for key,value in items[half:]:


            st.markdown(
                f"""
                <div class="box">

                <b>{key}</b>

                <br>

                {value}

                </div>
                """,

                unsafe_allow_html=True

            )





# -------------------------------
# Raw JSON Viewer
# -------------------------------


def show_raw_json(data):


    with st.expander(
        "View Complete AI Response"
    ):


        st.json(data)





# -------------------------------
# Download JSON File
# -------------------------------


def download_json(data):


    json_data = json.dumps(
        data,
        indent=4
    )


    return json_data





# -------------------------------
# Download CSV File
# -------------------------------


def download_csv(data):


    formatted = format_transaction_data(
        data
    )


    dataframe = pd.DataFrame(
        [formatted]
    )


    return dataframe.to_csv(
        index=False
    )




# -------------------------------
# Display Results Automatically
# -------------------------------


if (

    st.session_state.scan_result

    and

    "error"

    not

    in

    st.session_state.scan_result

):


    display_dashboard(
        st.session_state.scan_result
    )


    show_raw_json(
        st.session_state.scan_result
    )



    json_file = download_json(
        st.session_state.scan_result
    )


    csv_file = download_csv(
        st.session_state.scan_result
    )



    st.download_button(

        label="⬇ Download JSON",

        data=json_file,

        file_name="transaction_details.json",

        mime="application/json"

    )



    st.download_button(

        label="⬇ Download CSV",

        data=csv_file,

        file_name="transaction_details.csv",

        mime="text/csv"

    )

# -------------------------------
# Basic Document Validation
# -------------------------------


def validate_document(image):


    if image is None:


        return False



    try:


        width, height = image.size



        if width < 100 or height < 100:


            return False



        return True



    except:


        return False




# -------------------------------
# Create Demo Response
# (For Testing Without n8n)
# -------------------------------



# -------------------------------
# OCR Text Cleaner
# -------------------------------


def clean_text(text):


    if text is None:


        return ""



    replacements = {


        "\n\n":

        "\n",


        "  ":

        " "


    }



    for old,new in replacements.items():


        text=text.replace(
            old,
            new
        )



    return text.strip()




# -------------------------------
# Extract Possible Fields
# From OCR Text
# -------------------------------
def extract_basic_details(text):

    data = {}

    text = clean_text(text)

    # -----------------------
    # Amount
    # -----------------------
    amount = re.search(r"[₹rRsINR]+\s*([\d,]+(?:\.\d{2})?)", text, re.IGNORECASE)

    if amount:
        data["amount"] = "₹" + amount.group(1)

    # -----------------------
    # Status
    # -----------------------
    if "completed" in text.lower():
        data["status"] = "COMPLETED"

    elif "success" in text.lower():
        data["status"] = "SUCCESS"

    elif "failed" in text.lower():
        data["status"] = "FAILED"

    elif "pending" in text.lower():
        data["status"] = "PENDING"

    # -----------------------
    # Date
    # -----------------------
    date = re.search(
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}",
        text
    )

    if date:
        data["date"] = date.group()

    # -----------------------
    # Time
    # -----------------------
    time = re.search(
        r"\d{1,2}:\d{2}\s?(am|pm|AM|PM)",
        text
    )

    if time:
        data["time"] = time.group()

    # -----------------------
    # Bank
    # -----------------------
    bank = re.search(
        r"(Bank of [A-Za-z ]+|SBI|HDFC|ICICI|Axis|Canara|Indian Bank)",
        text,
        re.IGNORECASE
    )

    if bank:
        data["bank"] = bank.group()

    # -----------------------
    # UPI ID
    # -----------------------
    upis = re.findall(
        r"[A-Za-z0-9._-]+@[A-Za-z0-9]+",
        text
    )

    if len(upis) > 0:
        data["upi_id"] = upis[0]

    # -----------------------
    # Receiver
    # -----------------------
    receiver = re.search(
        r"To:\s*(.+)",
        text
    )

    if receiver:
        data["merchant"] = receiver.group(1).strip()

    # -----------------------
    # Sender
    # -----------------------
    sender = re.search(
        r"From:\s*(.+)",
        text
    )

    if sender:
        data["sender"] = sender.group(1).strip()

    # -----------------------
    # UPI Transaction ID
    # -----------------------
    txn = re.search(
        r"UPI transaction ID\s*([A-Za-z0-9]+)",
        text,
        re.IGNORECASE
    )

    if txn:
        data["transaction_id"] = txn.group(1)

    # -----------------------
    # Google Transaction ID
    # -----------------------
    google = re.search(
        r"Google transaction ID\s*([A-Za-z0-9_]+)",
        text,
        re.IGNORECASE
    )

    if google:
        data["google_transaction_id"] = google.group(1)

    # -----------------------
    # Payment Method
    # -----------------------
    if "upi" in text.lower():
        data["payment_method"] = "UPI"

    return data

# -------------------------------
# Safe Scan Controller
# -------------------------------


def process_document(image):

    if not validate_document(image):

        return {
            "error": "Invalid document image"
        }

    try:

        # Step 1 - Clean image using OpenCV
        processed_image = preprocess_image(image)

        # Step 2 - Read text using EasyOCR
        extracted_text = extract_text(processed_image)

        print("\n===== OCR TEXT =====")
        print(extracted_text)

        st.text_area(
            "OCR Output",
            extracted_text,
            height=300
        )
        # Step 3 - Extract useful information
        result = extract_basic_details(extracted_text)

        return result

    except Exception as error:

        return {
            "error": str(error)
        }


# -------------------------------
# Replace Scan Button Logic
# -------------------------------


if st.session_state.image:


    if st.button(
        "🚀 Process With AI",
        use_container_width=True
    ):


        with st.spinner(
            "Reading document using AI..."
        ):


            result = process_document(
                st.session_state.image
            )



            st.session_state.scan_result = result



        st.success(
            "Document processed successfully!"
        )

# -------------------------------
# Improve n8n Response Formatting
# -------------------------------



# -------------------------------
# Application Status Panel
# -------------------------------


with st.sidebar:


    st.divider()


    st.subheader(
        "System Status"
    )


    if st.session_state.image:


        st.success(
            "Image Loaded"
        )


    else:


        st.warning(
            "Waiting For Image"
        )



    if st.session_state.scan_result:


        st.success(
            "AI Processing Completed"
        )


    else:


        st.info(
            "No Scan Available"
        )





# -------------------------------
# Recent Scan Information
# -------------------------------


if st.session_state.scan_result:


    st.divider()


    st.subheader(
        "📌 Scan Summary"
    )



    summary_col1, summary_col2, summary_col3 = st.columns(3)



    result = st.session_state.scan_result



    with summary_col1:


        st.metric(

            "Amount",

            result.get(
                "amount",
                "N/A"
            )

        )



    with summary_col2:


        st.metric(

            "Status",

            result.get(
                "status",
                "N/A"
            )

        )



    with summary_col3:


        st.metric(

            "Payment",

            result.get(
                "payment_method",
                "N/A"
            )

        )






# -------------------------------
# Clear Button
# -------------------------------


if st.session_state.scan_result:


    if st.button(
        "🗑 Clear Scan",
        use_container_width=True
    ):


        st.session_state.scan_result = None

        st.session_state.image = None


        st.rerun()






# -------------------------------
# Final Information
# -------------------------------


st.divider()


st.markdown(

"""
### 🚀 AI Transaction Scanner

Features:

✅ Scan GPay Screenshots

✅ Scan Bills and Receipts

✅ AI Based Data Extraction

✅ OpenCV Image Enhancement

✅ Transaction Dashboard

✅ JSON Export

✅ CSV Export

✅ Camera Scanning


Technology Used:

Python | Streamlit | OpenCV | EasyOCR

"""

)
