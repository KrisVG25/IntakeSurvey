import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="VG Intake Form",
    layout="wide"
)

# --- Initialize Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 0

# --- Navigation Functions ---
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# --- Helper functions for the dynamic list ---
def add_item(list_key):
    """Adds a new empty item to a dynamic list in session state."""
    st.session_state[list_key].append("")

def remove_item(list_key, index):
    """Removes an item from a dynamic list in session state."""
    st.session_state[list_key].pop(index)
    # Also remove the corresponding widget's state to prevent errors
    st.session_state.pop(f"{list_key}_{index}", None)


def dynamic_text_list(label, list_key):
    """Creates a UI for a dynamic list of text inputs."""
    st.markdown(f"**{label}**")
    
    # Initialize the list in session state if it doesn't exist
    if list_key not in st.session_state:
        st.session_state[list_key] = [""] # Start with one empty item

    # Display a text input for each item in the list
    for i, item in enumerate(st.session_state[list_key]):
        col1, col2 = st.columns([10, 1])
        with col1:
            # The key for each text_input must be unique
            current_value = st.text_input(
                f"Item {i+1}", 
                value=item, 
                key=f"{list_key}_{i}", 
                label_visibility="collapsed"
            )
            # Update the list in session state with the new value from the text input
            st.session_state[list_key][i] = current_value
        with col2:
            # Only show remove button if there's more than one item
            if len(st.session_state[list_key]) > 1:
                st.button("➖", key=f"remove_{list_key}_{i}", on_click=remove_item, args=(list_key, i))

    # Add button to append a new item
    st.button("➕ Add Item", key=f"add_{list_key}", on_click=add_item, args=(list_key,))
    st.write("---")


# ==============================================================================
# STEP 0: GENERAL PROJECT BACKGROUND (Unchanged)
# ==============================================================================
if st.session_state.step == 0:
    st.image("https://images.typeform.com/images/9GdDxLJcuvbz", width=200)
    st.title("Step 1: General Project Background")
    st.info("Let's start with the basics of your project.")

    st.text_input("Email", key="email", value=st.session_state.get("email", ""))
    st.text_input("Client Name (ex. Vital Farms)", key="client_name", value=st.session_state.get("client_name", ""))
    
    # Pre-select previous answers if they exist
    region_index = None
    if "region" in st.session_state:
        try:
            region_index = ["USA", "Canada", "Mexico", "UK"].index(st.session_state.region)
        except ValueError:
            region_index = None # Handle case where stored value is no longer in the list

    st.selectbox("Region", options=["USA", "Canada", "Mexico", "UK"], index=region_index, placeholder="Select a region...", key="region")
    st.selectbox("Macro-category", options=["OTC & Wellness", "Personal Care & Beauty", "Food Storage", "Packaged Food & Drink", "Pet", "Cleaning"], index=None, placeholder="Select a macro-category...", key="macro_category")

    st.radio("Number of subcategories to include in the study?", options=["1", "2", "3", "4"], key="num_subcategories", horizontal=True)
    
    if st.session_state.get("client_name") and st.session_state.get("region"):
        st.button("Next: Category Details", on_click=next_step, type="primary")
    else:
        st.warning("Please fill in Client Name and Region to continue.")


# ==============================================================================
# STEP 1: DYNAMIC CATEGORY INFORMATION (MODIFIED)
# ==============================================================================
elif st.session_state.step == 1:
    st.title("Step 2: Subcategory Information")
    st.info("Now, provide the details for each of the subcategories you selected.")

    num_categories = int(st.session_state.get("num_subcategories", 1))

    for i in range(num_categories):
        with st.expander(f"Details for Category {i + 1}", expanded=True):
            st.text_input(f"Category Name (ex. Butter)", key=f"cat_name_{i}")
            st.text_input(f"Sample Size (ex. 3,000)", key=f"cat_sample_{i}")
            
            # --- MODIFIED SECTION ---
            # Using the new dynamic_text_list function instead of st.text_area
            dynamic_text_list(
                label="What categories are needed to qualify? (ex. Butter, Oil, Margarine)",
                list_key=f"cat_qualify_{i}"
            )
            dynamic_text_list(
                label="Category Attribute List (ex. Brand, Type, Package Size)",
                list_key=f"cat_attributes_{i}"
            )
            # --- END MODIFIED SECTION ---

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Project Background", on_click=prev_step)
    with col2:
        st.button("Next: Study Settings", on_click=next_step, type="primary")

# ==============================================================================
# STEP 2: STUDY SETTINGS (Unchanged)
# ==============================================================================
elif st.session_state.step == 2:
    st.title("Step 3: Study Settings")
    st.info("Finally, let's configure the specific content of the study.")

    st.radio("Study requires a hispanic/spanish language screener?", options=["Yes", "No"], index=None, key="hispanic_screener")
    st.multiselect("Channels to Include", options=["Asian/Hispanic Markets", "Club (Costco，Sam’s Club，BJ’s)", "C-Store", "Delivery (Instacart)", "Dollar (Dollar General，Dollar Tree，Family Dollar)", "Drug (CVS，Rite Aid，Walgreen’s)", "Grocery", "Mass (Walmart，Target)", "Online General (Amazon)", "Online Grocery (Boxed，Peapod，Thrive，Freshdirect)", "Beauty", "Coffee Shops", "Farm & Feed", "Hardware", "Liquor", "Office Supply", "Online Pet", "Pet"], key="included_channels")
    st.multiselect("Special Sections to Include", options=["Barriers - Question shoppers who did not purchase brand of interest in study", "Shopper Profile - Collect more background usage and purchase habits within the category", "Behavior and Attitudes - Directly ask what shoppers values in the category"], key="included_sections")
    st.multiselect("Special Question Topics to Include", options=["Product Label Preferences – Factors attended to on product labels.", "Online Term Search – Understand what terms people use to shop for category online.", "Product Duration – How long the product is anticipated to last", "Skin Type Usage – Understand what skin types certain products are purchased for.", "Other Product Types – Understand what other product types would be purchased with certain products.", "Consumption Occasions – Understand what moments and occasions shoppers plan to consume their selected products.", "Diet or Nutrition History – Current and past adherence to various diets and nutrition plans.", "Medical Conditions – Profile any relevant health conditions for dietary or medical insights."], key="included_topics")
    st.text_area("Describe any other specific business questions to address in the study, or skip.", key="other_questions")
    st.slider("Adjust the amount of AI suggestions you would like inserted.", min_value=1, max_value=5, value=3, key="ai_suggestions")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Category Details", on_click=prev_step)
    with col2:
        st.button("Next: Review & Submit", on_click=next_step, type="primary")

# ==============================================================================
# STEP 3: REVIEW AND SUBMIT (MODIFIED)
# ==============================================================================
elif st.session_state.step == 3:
    st.title("Step 4: Review and Submit")
    st.success("You're all done! Please review your answers below before submitting.")
    
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
            "special_topics": st.session_state.get("special_topics"),
            "other_business_questions": st.session_state.get("other_questions"),
            "ai_suggestion_level": st.session_state.get("ai_suggestions")
        }
    }

    num_cats = int(st.session_state.get("num_subcategories", 0))
    for i in range(num_cats):
        # --- MODIFIED SECTION ---
        # Get the list of qualifiers, filtering out any empty strings
        qualifiers_list = [q for q in st.session_state.get(f"cat_qualify_{i}", []) if q]
        # Get the list of attributes, filtering out any empty strings
        attributes_list = [a for a in st.session_state.get(f"cat_attributes_{i}", []) if a]
        
        category_info = {
            "name": st.session_state.get(f"cat_name_{i}"),
            "sample_size": st.session_state.get(f"cat_sample_{i}"),
            "qualifiers": qualifiers_list, # This is now a clean list
            "attributes": attributes_list  # This is also a clean list
        }
        final_data["subcategory_details"].append(category_info)
        # --- END MODIFIED SECTION ---

    st.json(final_data)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Study Settings", on_click=prev_step)
    with col2:
        if st.button("Submit Form", type="primary"):
            st.balloons()
            st.success("Form submitted successfully! Thank you.")
