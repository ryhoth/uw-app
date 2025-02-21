import streamlit as st
import pandas as pd

def main():
    st.set_page_config(layout="wide")  # Expands to use full screen width
    
    st.title("Ryan's Commercial Multifamily Underwriting")
    
    # Create Tabs for the entire roadmap
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Income", "Opex", "Capex", "Taxes", "Waterfall", "Summary"
    ])
    
    with tab1:
        # Fixed Output Section at the top
        st.subheader("Income Breakdown")
        output_container = st.container()
        
        # Scrollable Input Section
        with st.container():
            st.subheader("Income Input")
            st.write("Manually enter unit types, square footage, rent details, bedrooms, bathrooms, and unit counts.")
            
            num_units = st.number_input("Number of Unit Types", min_value=1, value=3, step=1, label_visibility="collapsed")
            
            unit_data = []
            for i in range(num_units):
                with st.container():
                    st.markdown(f"### Unit Type {i+1}")
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1, 1, 1, 1, 1, 1])
                    with col1:
                        unit_type = st.text_input(f"Unit Type {i+1}", value=f"{i+1}", key=f"unit_type_{i}")
                    with col2:
                        bedrooms = st.number_input(f"Bedrooms {unit_type}", min_value=0, step=1, value=1, key=f"bedrooms_{i}")
                    with col3:
                        bathrooms = st.number_input(f"Bathrooms {unit_type}", min_value=1, step=1, value=1, key=f"bathrooms_{i}")
                    with col4:
                        unit_sf = st.number_input(f"Unit SF {unit_type}", min_value=100, step=50, value=500, key=f"unit_sf_{i}")
                    
                    with col5:
                        rent_option = st.radio(f"Rent Input Type for {unit_type}", ["Per SF", "Per Unit"], key=f"rent_option_{i}")
                    with col6:
                        if rent_option == "Per SF":
                            rent_per_sf = st.number_input(f"Rent per SF {unit_type}", min_value=0.0, step=0.1, value=2.5, key=f"rent_per_sf_{i}")
                            rent_per_unit = unit_sf * rent_per_sf
                        else:
                            rent_per_unit = st.number_input(f"Rent per Unit {unit_type}", min_value=0.0, step=10.0, value=1000.0, key=f"rent_per_unit_{i}")
                            rent_per_sf = rent_per_unit / unit_sf
                    with col7:
                        unit_count = st.number_input(f"Unit Count {unit_type}", min_value=1, step=1, value=10, key=f"unit_count_{i}")
                    
                    total_monthly_revenue = rent_per_unit * unit_count
                    total_annual_revenue = total_monthly_revenue * 12
                    
                    # Calculate unit mix percentage
                    unit_mix_pct = (unit_count / num_units) * 100
                    
                    unit_data.append([unit_type, bedrooms, bathrooms, unit_sf, rent_per_sf, rent_per_unit, unit_count, total_monthly_revenue, total_annual_revenue, unit_mix_pct])
                    
                    is_affordable = st.checkbox(f"Affordable {unit_type}", key=f"affordable_{i}")
                    
                    if is_affordable:
                        with st.container():
                            st.markdown(f"#### Affordable Version of {unit_type}")
                            col8, col9, col10 = st.columns([1, 1, 1])
                            with col8:
                                affordable_units = st.number_input(f"Affordable Units for {unit_type}", min_value=1, max_value=unit_count, step=1, value=unit_count, key=f"aff_units_{i}")
                            with col9:
                                mfi_percentage = st.number_input(f"% MFI for {unit_type}", min_value=0, max_value=100, step=1, value=60, key=f"mfi_{i}")
                            with col10:
                                mfi_value = st.number_input(f"MFI Value for {unit_type}", min_value=0, step=1000, value=50000, key=f"mfi_value_{i}")
                            
                            affordable_rent_per_unit = (mfi_value * (mfi_percentage / 100)) / 12
                            affordable_total_monthly_revenue = affordable_units * affordable_rent_per_unit
                            affordable_total_annual_revenue = affordable_total_monthly_revenue * 12
                            
                            # Calculate affordable unit mix percentage
                            affordable_unit_mix_pct = (affordable_units / num_units) * 100
                            
                            unit_data.append([f"{unit_type} (Affordable)", bedrooms, bathrooms, unit_sf, rent_per_sf, affordable_rent_per_unit, affordable_units, affordable_total_monthly_revenue, affordable_total_annual_revenue, affordable_unit_mix_pct])
            
            # Create DataFrame
            df_income = pd.DataFrame(unit_data, columns=[
                "Unit Type", "Bedrooms", "Bathrooms", "Unit SF", "Rent per SF", "Rent per Unit",
                "Unit Count", "Total Monthly Revenue", "Total Annual Revenue", "Unit Mix %"
            ])
            
            # Append summary row at the bottom
            summary_row = pd.DataFrame({
                "Unit Type": ["TOTAL / AVERAGE"],
                "Bedrooms": ["-"],
                "Bathrooms": ["-"],
                "Unit SF": [df_income["Unit SF"].mean()],
                "Rent per SF": [df_income["Rent per SF"].mean()],
                "Rent per Unit": [df_income["Rent per Unit"].mean()],
                "Unit Count": [df_income["Unit Count"].sum()],
                "Total Monthly Revenue": [df_income["Total Monthly Revenue"].sum()],
                "Total Annual Revenue": [df_income["Total Annual Revenue"].sum()],
                "Unit Mix %": ["-"]
            })
            df_income = pd.concat([df_income, summary_row], ignore_index=True)
            
            # Format columns
            df_income["Rent per SF"] = df_income["Rent per SF"].apply(lambda x: f'$ {x:.2f}')
            df_income["Rent per Unit"] = df_income["Rent per Unit"].apply(lambda x: f'$ {x:,.0f}')
            df_income["Unit Mix %"] = df_income["Unit Mix %"].apply(lambda x: f'{x:.1f}%' if isinstance(x, (int, float)) else x)
        
        # Update Output Section
        with output_container:
            st.markdown("---")  # Line separator for clarity
            st.dataframe(df_income, use_container_width=True)
            st.markdown("---")  # Line separator for clarity
    
if __name__ == "__main__":
    main()