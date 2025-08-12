import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="VG Intake Form",
    layout="wide"
)

# --- Initialize Session State ---
# This is the magic that remembers which step we are on and stores data.
if 'step' not in st.session_state:
    st.session_state.step = 0

# --- Navigation Functions ---
def next_step():
    # To save the data from subcategory inputs, we process it before moving on.
    if st.session_state.step == 1:
        # Basic validation for step 1
        num_cats = int(st.session_state.get("num_subcategories", 0))
        for i in range(num_cats):
            if not st.session_state[f"cat_name_{i}"]:
                st.warning(f"Please enter a name for Category {i+1} before proceeding.")
                return # Stop the function if validation fails
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# --- Data for Selectors ---
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


# ==============================================================================
# STEP 0: GENERAL PROJECT BACKGROUND
# ==============================================================================
if st.session_state.step == 0:
    st.image("https://images.typeform.com/images/9GdDxLJcuvbz", width=200)
    st.title("Step 1: General Project Background")
    st.info("Let's start with the basics of your project.")

    st.text_input("Email", key="email")
    st.text_input("Client Name (ex. Vital Farms)", key="client_name")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Region", options=regions, index=None, placeholder="Select a region...", key="region")
    with col2:
        st.selectbox("Macro-category", options=macro_categories, index=None, placeholder="Select a macro-category...", key="macro_category")

    st.radio(
        "Number of subcategories to include in the study?",
        options=["1", "2", "3", "4"],
        key="num_subcategories",
        horizontal=True
    )
    
    # Basic validation before allowing user to proceed
    if st.session_state.get("client_name") and st.session_state.get("region"):
        st.button("Next: Category Details", on_click=next_step, type="primary")
    else:
        st.warning("Please fill in Client Name and Region to continue.")

# ==============================================================================
# STEP 1: DYNAMIC CATEGORY INFORMATION
# ==============================================================================
elif st.session_state.step == 1:
    st.title("Step 2: Subcategory Information")
    st.info("Now, provide the details for each of the subcategories you selected.")

    # Get the number of categories from the previous step. Default to 1 if not set.
    num_categories = int(st.session_state.get("num_subcategories", 1))

    # This loop dynamically creates the input fields.
    for i in range(num_categories):
        with st.expander(f"Details for Category {i + 1}", expanded=True):
            st.text_input(f"Category Name (ex. Butter)", key=f"cat_name_{i}")
            st.text_input(f"Sample Size (ex. 3,000)", key=f"cat_sample_{i}")
            st.text_area(f"What are the categories needed to have shopped to qualify for this category?", key=f"cat_qualify_{i}", help="Ex. Butter, Oil, Margarine")
            st.text_area(f"Category Attribute List", key=f"cat_attributes_{i}", help="Ex. If the category is Bacon, you might put: Brand, Type, Package Size, Flavor, Salt Level")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Project Background", on_click=prev_step)
    with col2:
        st.button("Next: Study Settings", on_click=next_step, type="primary")

# ==============================================================================
# STEP 2: STUDY SETTINGS
# ==============================================================================
elif st.session_state.step == 2:
    st.title("Step 3: Study Settings")
    st.info("Finally, let's configure the specific content of the study.")

    st.radio("Study requires a hispanic/spanish language screener?", options=["Yes", "No"], index=None, key="hispanic_screener")
    st.multiselect("Channels to Include", options=channels, key="included_channels")
    st.multiselect("Special Sections to Include", options=special_sections, key="included_sections")
    st.multiselect("Special Question Topics to Include", options=special_topics, key="included_topics")
    st.text_area("Describe any other specific business questions to address in the study, or skip.", key="other_questions")
    st.slider("Adjust the amount of AI suggestions you would like inserted.", min_value=1, max_value=5, value=3, key="ai_suggestions")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Category Details", on_click=prev_step)
    with col2:
        st.button("Next: Review & Submit", on_click=next_step, type="primary")

# ==============================================================================
# STEP 3: REVIEW AND SUBMIT
# ==============================================================================
elif st.session_state.step == 3:
    st.title("Step 4: Review and Submit")
    st.success("You're all done! Please review your answers below before submitting.")
    
    # --- Collect all the data from session_state ---
    final_data = {
        "email": st.session_state.get("email"),
        "client_name": st.session_state.get("client_name"),
        "region": st.session_state.get("region"),
        "macro_category": st.session_state.get("macro_category"),
        "num_subcategories": int(st.session_state.get("num_subcategories", 0)),
        "subcategory_details": [],
        "study_settings": {
            "hispanic_screener": st.session_state.get("hispanic_screener"),
            "included_channels": st.session_state.get("included_channels"),
            "special_sections": st.session_state.get("special_sections"),
            "special_topics": st.session_state.get("included_topics"),
            "other_business_questions": st.session_state.get("other_questions"),
            "ai_suggestion_level": st.session_state.get("ai_suggestions")
        }
    }

    # Loop to gather the dynamic category data
    num_cats = int(st.session_state.get("num_subcategories", 0))
    for i in range(num_cats):
        category_info = {
            "name": st.session_state.get(f"cat_name_{i}"),
            "sample_size": st.session_state.get(f"cat_sample_{i}"),
            "qualifiers": st.session_state.get(f"cat_qualify_{i}"),
            "attributes": st.session_state.get(f"cat_attributes_{i}")
        }
        final_data["subcategory_details"].append(category_info)

    # Display the collected data for review
    st.json(final_data)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Study Settings", on_click=prev_step)
    with col2:
        if st.button("Submit Form", type="primary"):
            st.balloons()
            st.success("Form submitted successfully! Thank you.")
            # Here you would add the logic to send an email, save to a database, etc.
            # For now, we just show a success message.
