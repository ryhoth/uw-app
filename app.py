import streamlit as st
import pandas as pd

def main():
    st.title("Commercial Multifamily Underwriting")
    
    # Create Tabs for the entire roadmap
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Income", "Opex", "Capex", "Taxes", "Waterfall", "Summary"
    ])
    
    with tab1:
        st.subheader("Income Input")
        st.write("Manually enter unit types, square footage, and rent.")
        
        # Define columns for user input
        col1, col2, col3 = st.columns(3)
        
        with col1:
            unit_types = st.text_area("Unit Type", "Studio\n1-Bedroom\n2-Bedroom")
        with col2:
            unit_sf = st.text_area("Unit SF", "500\n700\n900")
        with col3:
            rent_per_sf = st.text_area("Rent per SF", "2.5\n2.2\n2.0")
        
        # Process input into a DataFrame
        unit_types = unit_types.split("\n")
        unit_sf = list(map(float, unit_sf.split("\n")))
        rent_per_sf = list(map(float, rent_per_sf.split("\n")))
        
        df_income = pd.DataFrame({
            "Unit Type": unit_types,
            "Unit SF": unit_sf,
            "Rent per SF": rent_per_sf,
            "Rent per Unit": [sf * rent for sf, rent in zip(unit_sf, rent_per_sf)]
        })
        
        # Display Table
        st.subheader("Income Breakdown")
        st.dataframe(df_income)
        
        # Summary Metrics
        st.subheader("Income Summary")
        st.metric(label="Total Units", value=len(df_income))
        st.metric(label="Total Revenue ($)", value=f"${df_income['Rent per Unit'].sum():,.2f}")
    
    with tab2:
        st.subheader("Opex Input")
        st.write("Operating expenses input coming soon.")
    
    with tab3:
        st.subheader("Capex Input")
        st.write("Capital expenditures input coming soon.")
    
    with tab4:
        st.subheader("Taxes Input")
        st.write("Tax calculations input coming soon.")
    
    with tab5:
        st.subheader("Waterfall Model")
        st.write("Investor waterfall calculations coming soon.")
    
    with tab6:
        st.subheader("Summary")
        st.write("Final underwriting summary coming soon.")
    
if __name__ == "__main__":
    main()
