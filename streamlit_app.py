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
    if len(st.session_state[list_key]) > 1:
        st.session_state[list_key].pop(index)
        # Clean up the corresponding widget's state from session_state
        for i in range(len(st.session_state[list_key]), len(st.session_state[list_key]) + 2):
            st.session_state.pop(f"{list_key}_{i}", None)


def dynamic_text_list(label, list_key):
    """Creates a UI for a dynamic list of text inputs."""
    st.markdown(f"**{label}**")
    
    if list_key not in st.session_state:
        st.session_state[list_key] = [""] 

    # This loop synchronizes the widget values back to our list on each rerun
    for i in range(len(st.session_state[list_key])):
        st.session_state[list_key][i] = st.session_state.get(f"{list_key}_{i}", "")

    # This loop displays the actual widgets
    for i, item in enumerate(st.session_state[list_key]):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.text_input(
                f"Item {i+1}", 
                value=item, 
                key=f"{list_key}_{i}", 
                label_visibility="collapsed"
            )
        with col2:
            if len(st.session_state[list_key]) > 1:
                st.button("➖", key=f"remove_{list_key}_{i}", on_click=remove_item, args=(list_key, i))

    st.button("➕ Add Item", key=f"add_{list_key}", on_click=add_item, args=(list_key,))
    

# ==============================================================================
# STEP 0: GENERAL PROJECT BACKGROUND (Unchanged)
# ==============================================================================
if st.session_state.step == 0:
    st.image("https://images.typeform.com/images/9GdDxLJcuvbz", width=200)
    st.title("Step 1: General Project Background")
    st.info("Let's start with the basics of your project.")

    st.text_input("Email", key="email")
    st.text_input("Client Name (ex. Vital Farms)", key="client_name")
    
    st.selectbox("Region", options=["USA", "Canada", "Mexico", "UK"], index=None, placeholder="Select a region...", key="region")
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
        # We add a clear separator and header for each category section
        st.markdown("---")
        category_name = st.session_state.get(f"cat_name_{i}", f"Category {i+1}")
        header_text = f"**{category_name}**" if category_name != f"Category {i+1}" else f"**Category {i+1}**"
        
        # This toggle controls the visibility of the container and saves its state
        is_expanded = st.toggle(
            header_text, 
            key=f"expander_state_{i}", 
            value=st.session_state.get(f"expander_state_{i}", True) # Default to True
        )
        
        # If the toggle is on, show the container with the input fields
        if is_expanded:
            with st.container(border=True):
                st.text_input("Category Name (ex. Butter)", key=f"cat_name_{i}")
                st.text_input("Sample Size (ex. 3,000)", key=f"cat_sample_{i}")
                
                st.markdown("---")
                
                dynamic_text_list(
                    label="What categories are needed to qualify? (ex. Butter, Oil, Margarine)",
                    list_key=f"cat_qualify_{i}"
                )
                
                st.markdown("---")
                
                dynamic_text_list(
                    label="Category Attribute List (ex. Brand, Type, Package Size)",
                    list_key=f"cat_attributes_{i}"
                )

    st.markdown("---")
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
# STEP 3: REVIEW AND SUBMIT (Unchanged)
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
        qualifiers_list = [q for q in st.session_state.get(f"cat_qualify_{i}", []) if q]
        attributes_list = [a for a in st.session_state.get(f"cat_attributes_{i}", []) if a]
        
        category_info = {
            "name": st.session_state.get(f"cat_name_{i}"),
            "sample_size": st.session_state.get(f"cat_sample_{i}"),
            "qualifiers": qualifiers_list,
            "attributes": attributes_list
        }
        final_data["subcategory_details"].append(category_info)

    st.json(final_data)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back: Study Settings", on_click=prev_step)
    with col2:
        if st.button("Submit Form", type="primary"):
            st.balloons()
            st.success("Form submitted successfully! Thank you.")
