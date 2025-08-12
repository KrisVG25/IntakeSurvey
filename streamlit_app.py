import streamlit as st
import json

# --- Page Configuration ---
# Sets the title and layout of the page.
st.set_page_config(
    page_title="VG Intake Form",
    layout="wide"
)

# --- Welcome Screen ---
# Recreates the welcome screen from your Typeform.
st.image(
    "https://images.typeform.com/images/9GdDxLJcuvbz",
    width=200,
)
st.title("Internal Intake Tool")
st.markdown("""
*This is a testing version tool meant for internal use of Vista Grande employees to use for generating a CCA questionnaire.*

*If you are using this for a project, feedback on the quality and appropriateness of the resulting questionnaire would be greatly appreciated.*

Please send any you may have to Kristina, or document into the feedback area [here](https://docs.google.com/document/d/1nP_0AabzAs7lsI85FWhXyxuzzPH6mGvf-tLtJa5ykvs/edit?tab=t.e48co6y0d7g6#heading=h.2gou1iavuljp).
""")

st.divider()

# --- Data for Selectors ---
# Pre-defined lists for dropdowns and multi-select boxes.
regions = ["USA", "Canada", "Mexico", "UK"]
macro_categories = ["OTC & Wellness", "Personal Care & Beauty", "Food Storage", "Packaged Food & Drink", "Pet", "Cleaning"]
channels = [
    "Asian/Hispanic Markets", "Club (Costco，Sam’s Club，BJ’s)", "C-Store", "Delivery (Instacart)",
    "Dollar (Dollar General，Dollar Tree，Family Dollar)", "Drug (CVS，Rite Aid，Walgreen’s)", "Grocery",
    "Mass (Walmart，Target)", "Online General (Amazon)", "Online Grocery (Boxed，Peapod，Thrive，Freshdirect)",
    "Beauty", "Coffee Shops", "Farm & Feed", "Hardware", "Liquor", "Office Supply", "Online Pet", "Pet"
]
special_sections = [
    "Barriers - Question shoppers who did not purchase brand of interest in study",
    "Shopper Profile - Collect more background usage and purchase habits within the category",
    "Behavior and Attitudes - Directly ask what shoppers values in the category"
]
special_topics = [
    "Product Label Preferences – Factors attended to on product labels.",
    "Online Term Search – Understand what terms people use to shop for category online.",
    "Product Duration – How long the product is anticipated to last",
    "Skin Type Usage – Understand what skin types certain products are purchased for.",
    "Other Product Types – Understand what other product types would be purchased with certain products.",
    "Consumption Occasions – Understand what moments and occasions shoppers plan to consume their selected products.",
    "Diet or Nutrition History – Current and past adherence to various diets and nutrition plans.",
    "Medical Conditions – Profile any relevant health conditions for dietary or medical insights."
]

# --- Form Definition ---
# Using st.form() allows users to fill everything out and submit once.
with st.form("vg_intake_form"):
    st.header("Project Details")
    
    # --- Project Background Section ---
    email = st.text_input(
        "Email",
        help="The resulting questionnaire from this form will be sent here."
    )

    st.subheader("General Project Background")
    client_name = st.text_input("Client Name (ex. Vital Farms)")
    
    # Using columns for a cleaner layout
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("Region", options=regions, index=None, placeholder="Select a region...")
    with col2:
        macro_category = st.selectbox(
            "Macro-category",
            options=macro_categories,
            help="The broader industry context of the category included",
            index=None,
            placeholder="Select a macro-category..."
        )

    num_subcategories = st.radio(
        "Number of subcategories",
        options=["1", "2", "3", "4"],
        help="Subcategory = a distinct qualification cell/shopping path/products with different attributes. *Current support only a max of 4",
        horizontal=True
    )

    # Conditionally show the Overall Study Category Name
    if num_subcategories and int(num_subcategories) > 1:
        overall_category_name = st.text_input(
            "Overall Study Category Name",
            help='You mentioned the study will include several subcategories. What will they all together be referred to? Ex. "Oral Care" - that covers toothbrushes & toothpaste'
        )
    else:
        overall_category_name = ""

    st.divider()

    # --- Conditional Subcategory Sections ---
    # These sections will appear based on the "Number of subcategories" selection.
    st.header("Subcategory Information")

    # This dictionary will hold the data for each subcategory
    category_data = {}

    # Category A (always visible if a number is selected)
    if num_subcategories:
        with st.expander("Category A Information", expanded=True):
            cat_a_name = st.text_input("Category Name (ex. Butter)", key="cat_a_name")
            cat_a_sample = st.text_input("Sample Size (ex. 3,000)", key="cat_a_sample")
            cat_a_qualify = st.text_area("What are the categories needed to have shopped to qualify for this category? (ex. Butter, Oil, Margarine)", key="cat_a_qualify")
            cat_a_attributes = st.text_area("Category Attribute List (ex. Brand, Type, Package Size, Flavor, Salt Level)", key="cat_a_attributes")
            category_data['A'] = {
                'name': cat_a_name, 'sample_size': cat_a_sample,
                'qualifiers': cat_a_qualify, 'attributes': cat_a_attributes
            }

    # Category B
    if num_subcategories and int(num_subcategories) >= 2:
        with st.expander("Category B Information", expanded=True):
            cat_b_name = st.text_input("Category Name (ex. Butter)", key="cat_b_name")
            cat_b_sample = st.text_input("Sample Size (ex. 3,000)", key="cat_b_sample")
            cat_b_qualify = st.text_area("What are the categories needed to have shopped to qualify for this category? (ex. Butter, Oil, Margarine)", key="cat_b_qualify")
            cat_b_attributes = st.text_area("Category Attribute List (ex. Brand, Type, Package Size, Flavor, Salt Level)", key="cat_b_attributes")
            category_data['B'] = {
                'name': cat_b_name, 'sample_size': cat_b_sample,
                'qualifiers': cat_b_qualify, 'attributes': cat_b_attributes
            }

    # Category C
    if num_subcategories and int(num_subcategories) >= 3:
        with st.expander("Category C Information", expanded=True):
            cat_c_name = st.text_input("Category Name (ex. Butter)", key="cat_c_name")
            cat_c_sample = st.text_input("Sample Size (ex. 3,000)", key="cat_c_sample")
            cat_c_qualify = st.text_area("What are the categories needed to have shopped to qualify for this category? (ex. Butter, Oil, Margarine)", key="cat_c_qualify")
            cat_c_attributes = st.text_area("Category Attribute List (ex. Brand, Type, Package Size, Flavor, Salt Level)", key="cat_c_attributes")
            category_data['C'] = {
                'name': cat_c_name, 'sample_size': cat_c_sample,
                'qualifiers': cat_c_qualify, 'attributes': cat_c_attributes
            }

    # Category D
    if num_subcategories and int(num_subcategories) == 4:
        with st.expander("Category D Information", expanded=True):
            cat_d_name = st.text_input("Category Name (ex. Butter)", key="cat_d_name")
            cat_d_sample = st.text_input("Sample Size (ex. 3,000)", key="cat_d_sample")
            cat_d_qualify = st.text_area("What are the categories needed to have shopped to qualify for this category? (ex. Butter, Oil, Margarine)", key="cat_d_qualify")
            cat_d_attributes = st.text_area("Category Attribute List (ex. Brand, Type, Package Size, Flavor, Salt Level)", key="cat_d_attributes")
            category_data['D'] = {
                'name': cat_d_name, 'sample_size': cat_d_sample,
                'qualifiers': cat_d_qualify, 'attributes': cat_d_attributes
            }

    st.divider()

    # --- Study Settings Section ---
    st.header("Study Settings")
    hispanic_screener = st.radio(
        "Study requires a hispanic/spanish language screener?",
        options=["Yes", "No"], index=None
    )
    
    included_channels = st.multiselect("Channels to Include", options=channels)
    
    included_sections = st.multiselect(
        "Special Sections to Include",
        options=special_sections,
        help="If selected, these sections will be added and initiated with their fundamental questions."
    )
    
    included_topics = st.multiselect("Special Question Topics to Include", options=special_topics)
    
    other_questions = st.text_area(
        "Describe any other specific business questions to address in the study, or skip.",
        help="Ex. Want to know about specific claims and concerns around the health of the dairy (antibiotics, grass fed, etc.)"
    )

    ai_suggestions = st.slider(
        "Adjust the amount of AI suggestions you would like inserted.",
        min_value=1,
        max_value=5,
        value=3,
        help="1 – Essentials Only (e.g. 5 suggestions added). 5 – Full Spectrum (e.g. 20 suggestions added)."
    )

    # --- Form Submission ---
    submitted = st.form_submit_button("Submit Intake Form")


# --- Post-Submission Logic ---
# This block runs only after the user clicks the "Submit" button.
if submitted:
    # Basic validation check
    if not client_name or not region or not macro_category or not num_subcategories:
        st.error("Please fill out all required fields in the 'General Project Background' section.")
    else:
        # Collect all data into a dictionary
        final_data = {
            "email": email,
            "client_name": client_name,
            "region": region,
            "macro_category": macro_category,
            "num_subcategories": int(num_subcategories) if num_subcategories else 0,
            "overall_category_name": overall_category_name,
            "subcategory_details": category_data,
            "study_settings": {
                "hispanic_screener": hispanic_screener,
                "included_channels": included_channels,
                "special_sections": included_sections,
                "special_topics": included_topics,
                "other_business_questions": other_questions,
                "ai_suggestion_level": ai_suggestions
            }
        }
        
        # Display a success message similar to the Typeform "Thank You" screen
        
        st.success("Thank you for completing the intake form!")
        st.balloons()
        st.info(f"The questionnaire will be sent to **{email}**. This may take up to 5 minutes.")

        # Display the collected data as a JSON object for verification
        st.subheader("Collected Form Data (as JSON)")
        st.json(final_data)