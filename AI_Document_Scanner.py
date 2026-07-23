import streamlit as st
from PIL import Image
import requests
import json
import io
import base64
import pandas as pd
from datetime import datetime


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


    webhook_url = st.text_input(
        "Enter n8n Webhook URL",
        placeholder="https://your-n8n-url/webhook/scanner"
    )


    st.session_state.webhook = webhook_url



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
# Scan Button
# -------------------------------


if st.session_state.image:


    if st.button(
        "🔍 Scan Document",
        use_container_width=True
    ):


        with st.spinner(
            "AI is analyzing the document..."
        ):


            # Function will be added
            # in next parts

            st.session_state.scan_result = {

                "status":
                "Waiting for n8n connection"

            }


        st.success(
            "Scanning Completed"
        )



# -------------------------------
# Footer
# -------------------------------


st.divider()


st.caption(
    "Built using Python + Streamlit + n8n + AI OCR"
)

# -------------------------------
# Convert Image Into Base64
# -------------------------------

def image_to_base64(image):

    try:

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="PNG"
        )

        image_bytes = buffer.getvalue()


        encoded_image = base64.b64encode(
            image_bytes
        ).decode(
            "utf-8"
        )


        return encoded_image


    except Exception as error:


        st.error(
            f"Image conversion error: {error}"
        )

        return None




# -------------------------------
# Send Image To n8n Webhook
# -------------------------------


def send_to_n8n(image, webhook_url):


    if webhook_url == "":


        return {

            "error":
            "Please enter n8n webhook URL"

        }



    try:


        encoded_image = image_to_base64(
            image
        )


        if encoded_image is None:


            return {

                "error":
                "Unable to process image"

            }



        payload = {


            "file_name":
            "document.png",



            "image":

            encoded_image,



            "timestamp":

            str(datetime.now())

        }



        response = requests.post(


            webhook_url,


            json=payload,


            timeout=60

        )



        if response.status_code == 200:



            result = response.json()


            return result



        else:



            return {


                "error":

                f"n8n Error {response.status_code}"

            }



    except requests.exceptions.Timeout:



        return {


            "error":

            "n8n server timeout"

        }




    except Exception as error:



        return {


            "error":

            str(error)

        }




# -------------------------------
# Scan Document Function
# -------------------------------


def scan_document(image):


    webhook = st.session_state.get(
        "webhook",
        ""
    )


    result = send_to_n8n(

        image,

        webhook

    )



    return result





# -------------------------------
# Replace Temporary Scan Button
# -------------------------------

if (

    st.session_state.image

    and

    st.session_state.scan_result

    and

    st.session_state.scan_result.get("status")

    ==

    "Waiting for n8n connection"

):


    pass

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


def demo_scan_result():


    return {


        "transaction_id":

        "TID98473829384",



        "amount":

        "₹2500",



        "date":

        "21-07-2026",



        "time":

        "08:45 PM",



        "upi_id":

        "example@upi",



        "merchant":

        "Amazon Shopping",



        "bank":

        "State Bank Of India",



        "reference_no":

        "847392847392",



        "status":

        "SUCCESS",



        "payment_method":

        "UPI",



        "note":

        "Online Purchase",



        "invoice_number":

        "INV123456",



        "gst_number":

        "33ABCDE1234F1Z5",



        "total":

        "₹2500"



    }




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



    lines = text.split("\n")



    for line in lines:



        lower = line.lower()



        if "amount" in lower:


            data["amount"] = line



        elif "transaction" in lower:


            data["transaction_id"] = line



        elif "date" in lower:


            data["date"] = line



        elif "time" in lower:


            data["time"] = line



        elif "upi" in lower:


            data["upi_id"] = line



        elif "bank" in lower:


            data["bank"] = line



        elif "note" in lower:


            data["note"] = line




    return data





# -------------------------------
# Safe Scan Controller
# -------------------------------


def process_document(image):


    if not validate_document(image):


        return {


            "error":

            "Invalid document image"

        }



    try:


        webhook = st.session_state.get(
            "webhook",
            ""
        )



        # If user has not added n8n URL
        # use demo mode


        if webhook == "":


            return demo_scan_result()



        else:


            return scan_document(
                image
            )



    except Exception as error:


        return {


            "error":

            str(error)

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


def process_n8n_response(response):


    try:


        if isinstance(response, dict):


            return response



        data = json.loads(
            response
        )


        return data



    except Exception:


        return {


            "error":

            "Invalid response received from AI"

        }





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

✅ n8n Automation Support

✅ Transaction Dashboard

✅ JSON Export

✅ CSV Export

✅ Camera Scanning


Technology Used:

Python | Streamlit | n8n | OCR | AI


"""

)