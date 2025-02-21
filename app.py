import streamlit as st
import pandas as pd

def calculate_monthly_revenue(unit_count, rent_per_unit):
    return unit_count * rent_per_unit

def calculate_annual_revenue(monthly_revenue):
    return monthly_revenue * 12

def calculate_unit_mix(unit_count, total_units):
    return (unit_count / total_units) * 100 if total_units > 0 else 0

def calculate_bed_mix(num_beds, unit_count, total_beds):
    return (num_beds * unit_count / total_beds) * 100 if total_beds > 0 else 0

def main():
    st.set_page_config(layout="wide")  # Expands to use full screen width
    
    st.title("Ryan's Commercial Real Estate Underwriting App")
    
    # Initialize session state variables if they don't exist
    if "total_units" not in st.session_state:
        st.session_state.total_units = 0
    if "total_beds" not in st.session_state:
        st.session_state.total_beds = 0
    if "total_affordable_units" not in st.session_state:
        st.session_state.total_affordable_units = 0
    
    # Create Tabs for the entire roadmap
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Income", "Opex", "Capex", "Taxes", "Waterfall", "Summary"
    ])
    
    with tab1:
        # Fixed Output Section at the top
        st.subheader("Income Breakdown")
        
        # A. Multifamily Income Section
        st.markdown("### A. Multifamily Income")
        multifamily_enabled = st.checkbox("Enable Multifamily Revenue", value=True)
        if multifamily_enabled:
            # I. Multifamily Income Breakdown
            st.markdown("#### I. Multifamily Income Breakdown")
            num_units = st.number_input("Number of Unit Types", min_value=1, value=3, step=1, label_visibility="collapsed")
            
            unit_data = []
            st.session_state.total_units = 0  # Reset total units
            st.session_state.total_beds = 0  # Reset total beds
            st.session_state.total_affordable_units = 0  # Reset total affordable units
            
            for i in range(num_units):
                with st.container():
                    # Use letters (A, B, C, etc.) for unit type placeholders
                    unit_type_placeholder = chr(65 + i)  # 65 is ASCII for 'A'
                    st.markdown(f"##### a. Unit Type {unit_type_placeholder}")
                    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
                    with col1:
                        unit_type = st.text_input(f"Unit Type {unit_type_placeholder}", value=unit_type_placeholder, key=f"unit_type_{i}")
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
                    with col8:
                        num_beds = st.number_input(f"Number of Beds {unit_type}", min_value=0, step=1, value=1, key=f"num_beds_{i}")
                    
                    total_monthly_revenue = calculate_monthly_revenue(unit_count, rent_per_unit)
                    total_annual_revenue = calculate_annual_revenue(total_monthly_revenue)
                    
                    # Add to total units and beds for mix calculations
                    st.session_state.total_units += unit_count
                    st.session_state.total_beds += num_beds * unit_count
                    
                    # Append unit data (unit mix and bed mix will be calculated later)
                    unit_data.append([unit_type, bedrooms, bathrooms, unit_sf, rent_per_sf, rent_per_unit, unit_count, num_beds, total_monthly_revenue, total_annual_revenue])
                    
                    is_affordable = st.checkbox(f"Affordable {unit_type}", key=f"affordable_{i}")
                    
                    if is_affordable:
                        with st.container():
                            st.markdown(f"##### b. Affordable Version of {unit_type}")
                            col9, col10, col11 = st.columns([1, 1, 1])
                            with col9:
                                affordable_units = st.number_input(f"Affordable Units for {unit_type}", min_value=1, max_value=unit_count, step=1, value=unit_count, key=f"aff_units_{i}")
                            with col10:
                                mfi_percentage = st.number_input(f"% MFI for {unit_type}", min_value=0, max_value=100, step=1, value=60, key=f"mfi_{i}")
                            with col11:
                                mfi_value = st.number_input(f"MFI Value for {unit_type}", min_value=0, step=1000, value=50000, key=f"mfi_value_{i}")
                            
                            affordable_rent_per_unit = (mfi_value * (mfi_percentage / 100)) / 12
                            affordable_total_monthly_revenue = calculate_monthly_revenue(affordable_units, affordable_rent_per_unit)
                            affordable_total_annual_revenue = calculate_annual_revenue(affordable_total_monthly_revenue)
                            
                            # Add to total affordable units
                            st.session_state.total_affordable_units += affordable_units
                            
                            # Append affordable unit data
                            unit_data.append([f"{unit_type} (Affordable)", bedrooms, bathrooms, unit_sf, rent_per_sf, affordable_rent_per_unit, affordable_units, num_beds, affordable_total_monthly_revenue, affordable_total_annual_revenue])
            
            # Create DataFrame for Multifamily Revenue
            df_multifamily = pd.DataFrame(unit_data, columns=[
                "Unit Type", "Bedrooms", "Bathrooms", "Unit SF", "Rent per SF", "Rent per Unit",
                "Unit Count", "Number of Beds", "Total Monthly Revenue", "Total Annual Revenue"
            ])
            
            # Calculate Unit Mix % and Bed Mix %
            df_multifamily["Unit Mix %"] = df_multifamily["Unit Count"].apply(lambda x: calculate_unit_mix(x, st.session_state.total_units))
            df_multifamily["Bed Mix %"] = df_multifamily.apply(lambda row: calculate_bed_mix(row["Number of Beds"], row["Unit Count"], st.session_state.total_beds), axis=1)
            
            # Move "Unit Mix %" and "Bed Mix %" columns next to "Unit Type"
            cols = df_multifamily.columns.tolist()
            cols = cols[:1] + [cols[-2], cols[-1]] + cols[1:-2]  # Reorder columns
            df_multifamily = df_multifamily[cols]
            
            # Append summary row at the bottom
            summary_row = pd.DataFrame({
                "Unit Type": ["TOTAL / AVERAGE"],
                "Unit Mix %": ["-"],
                "Bed Mix %": ["-"],
                "Bedrooms": ["-"],
                "Bathrooms": ["-"],
                "Unit SF": [df_multifamily["Unit SF"].mean()],
                "Rent per SF": [df_multifamily["Rent per SF"].mean()],
                "Rent per Unit": [df_multifamily["Rent per Unit"].mean()],
                "Unit Count": [df_multifamily["Unit Count"].sum()],
                "Number of Beds": [df_multifamily["Number of Beds"].sum()],
                "Total Monthly Revenue": [df_multifamily["Total Monthly Revenue"].sum()],
                "Total Annual Revenue": [df_multifamily["Total Annual Revenue"].sum()]
            })
            df_multifamily = pd.concat([df_multifamily, summary_row], ignore_index=True)
            
            # Format columns
            df_multifamily["Unit SF"] = df_multifamily["Unit SF"].apply(lambda x: f'{int(x):,}' if isinstance(x, (int, float)) else x)  # No decimals
            df_multifamily["Rent per SF"] = df_multifamily["Rent per SF"].apply(lambda x: f'$ {x:.2f}')
            df_multifamily["Rent per Unit"] = df_multifamily["Rent per Unit"].apply(lambda x: f'$ {x:,.0f}')
            df_multifamily["Total Monthly Revenue"] = df_multifamily["Total Monthly Revenue"].apply(lambda x: f'$ {x:,.0f}')
            df_multifamily["Total Annual Revenue"] = df_multifamily["Total Annual Revenue"].apply(lambda x: f'$ {x:,.0f}')
            df_multifamily["Unit Mix %"] = df_multifamily["Unit Mix %"].apply(lambda x: f'{x:.1f}%' if isinstance(x, (int, float)) else x)
            df_multifamily["Bed Mix %"] = df_multifamily["Bed Mix %"].apply(lambda x: f'{x:.1f}%' if isinstance(x, (int, float)) else x)
            
            # Format summary row differently
            df_multifamily.iloc[-1, df_multifamily.columns.get_loc("Unit Type")] = "TOTAL / AVERAGE"  # No bold text
            for col in ["Unit SF", "Rent per SF", "Rent per Unit", "Unit Count", "Number of Beds", "Total Monthly Revenue", "Total Annual Revenue"]:
                df_multifamily.iloc[-1, df_multifamily.columns.get_loc(col)] = f'{df_multifamily.iloc[-1][col]}'  # No bold text
            
            # Display Multifamily Income Breakdown Table
            st.markdown("---")  # Line separator for clarity
            st.dataframe(
                df_multifamily.style.apply(
                    lambda x: ["background: lightgray; font-weight: bold" if x.name == len(df_multifamily)-1 else "" for i in x],
                    axis=1
                ),
                use_container_width=True
            )
            st.markdown("---")  # Line separator for clarity
            
            # II. Affordable Metrics (Nested under Multifamily Income Section)
            st.markdown("#### II. Affordable Metrics")
            affordable_pct = st.number_input("Affordable %", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
            affordable_req = (affordable_pct / 100) * st.session_state.total_units
            affordable_planned = st.session_state.total_affordable_units
            satisfied_requirement = affordable_planned >= affordable_req
            
            st.write(f"Affordable Requirement: {affordable_req:.0f}")
            st.write(f"Affordable Planned: {affordable_planned}")
            st.write(f"Satisfied Requirement: {satisfied_requirement}")
        
        # B. Retail Revenue Section
        st.markdown("### B. Retail Revenue")
        retail_enabled = st.checkbox("Enable Retail Revenue", value=True)
        if retail_enabled:
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
            with col1:
                retail_sf = st.number_input("Retail Square Footage", min_value=0, value=1000, step=100)
            with col2:
                retail_rent_psf = st.number_input("Retail Rent per SF", min_value=0.0, value=2.5, step=0.1)
            with col3:
                retail_parking_spaces = st.number_input("Retail Parking Spaces", min_value=0, value=10, step=1)
            with col4:
                retail_parking_fee = st.number_input("Retail Parking Fee", min_value=0.0, value=50.0, step=5.0)
            
            retail_annual_revenue = retail_sf * retail_rent_psf * 12
            retail_parking_revenue = retail_parking_spaces * retail_parking_fee * 12
            
            st.write(f"Retail Annual Revenue: ${retail_annual_revenue:,.2f}")
            st.write(f"Retail Parking Revenue: ${retail_parking_revenue:,.2f}")
        
        # C. Office Revenue Section
        st.markdown("### C. Office Revenue")
        office_enabled = st.checkbox("Enable Office Revenue", value=True)
        if office_enabled:
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
            with col1:
                office_sf = st.number_input("Office Square Footage", min_value=0, value=2000, step=100)
            with col2:
                office_rent_psf = st.number_input("Office Rent per SF", min_value=0.0, value=3.0, step=0.1)
            with col3:
                office_parking_spaces = st.number_input("Office Parking Spaces", min_value=0, value=20, step=1)
            with col4:
                office_parking_fee = st.number_input("Office Parking Fee", min_value=0.0, value=75.0, step=5.0)
            
            office_annual_revenue = office_sf * office_rent_psf * 12
            office_parking_revenue = office_parking_spaces * office_parking_fee * 12
            
            st.write(f"Office Annual Revenue: ${office_annual_revenue:,.2f}")
            st.write(f"Office Parking Revenue: ${office_parking_revenue:,.2f}")
        
        # D. Hotel Revenue Section
        st.markdown("### D. Hotel Revenue")
        hotel_enabled = st.checkbox("Enable Hotel Revenue", value=True)
        if hotel_enabled:
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
            with col1:
                hotel_rooms = st.number_input("Hotel Rooms", min_value=0, value=50, step=1)
            with col2:
                hotel_room_rate = st.number_input("Hotel Room Rate", min_value=0.0, value=150.0, step=5.0)
            with col3:
                hotel_occupancy_rate = st.number_input("Hotel Occupancy Rate (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
            with col4:
                hotel_parking_spaces = st.number_input("Hotel Parking Spaces", min_value=0, value=30, step=1)
            
            hotel_annual_revenue = hotel_rooms * hotel_room_rate * (hotel_occupancy_rate / 100) * 365
            hotel_parking_revenue = hotel_parking_spaces * 50 * 12  # Assuming $50 per parking space per month
            
            st.write(f"Hotel Annual Revenue: ${hotel_annual_revenue:,.2f}")
            st.write(f"Hotel Parking Revenue: ${hotel_parking_revenue:,.2f}")
    
if __name__ == "__main__":
    main()