import streamlit as st
import io
import json
import requests
import pandas as pd
# from dashboard import uploaded_files
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_KEY")
url="http://"

uploaded_files = st.session_state.get("uploaded_files", [])

st.title("Welcome to the ERP Auditing Page!")

if "uploaded_files" in st.session_state:
    files = st.session_state["uploaded_files"]

    st.write("### Uploaded Files")

    cols = st.columns(len(files))   # create columns equal to number of files

    for col, file in zip(cols, files):
        with col:
            st.info(file.name)

else:
    st.warning("Upload a file first.")

# def groq_client(query,prompt):
#     client = Groq(api_key=api_key)

#     completion = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[
#             {"role": "system", "content": prompt},
#             {"role": "user", "content": query}
#         ],
#         temperature=0.7,
#     )

#     return completion.choices[0].message.content

def groq_client(query, prompt):
    client = Groq(api_key=api_key)

    structured_prompt = prompt + """
    
You MUST respond with a valid JSON object and nothing else. No preamble, no explanation, no markdown backticks.
The JSON must follow this exact structure:
{
    "table1": "| Col1 | Col2 |\\n|------|------|\\n| val  | val  |",
    "table2": "| Col1 | Col2 |\\n|------|------|\\n| val  | val  |",
    "summary": "Your summary text here."
}
- table1 and table2 must be valid markdown tables as a single string (use \\n for newlines)
- summary must be a concise plain text summary
"""

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": structured_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.7,
    )

    raw = completion.choices[0].message.content

    try:
        # Strip accidental markdown fences if model misbehaves
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(clean)

        return {
            "table1": parsed.get("table1", ""),
            "table2": parsed.get("table2", ""),
            "summary": parsed.get("summary", "")
        }

    except json.JSONDecodeError as e:
        return {
            "table1": "",
            "table2": "",
            "summary": "",
            "error": f"Failed to parse response: {str(e)}",
            "raw": raw
        }


load_text=st.text_area("Enter your text here:")
if st.button("Load"):
    if load_text:

        all_content=[]
        for selected_file in uploaded_files:

            name = selected_file.name.lower()
            raw = selected_file.read()

            # CSV
            if name.endswith(".csv"):
                try:
                    content = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig").to_csv(index=False)
                except Exception:
                    try:
                        content = pd.read_csv(io.BytesIO(raw), encoding="latin1").to_csv(index=False)
                    except Exception:
                        content = raw.decode("utf-8", errors="ignore")

            # Excel
            elif name.endswith((".xlsx", ".xls")):
                try:
                    content = pd.read_excel(io.BytesIO(raw)).to_csv(index=False)
                except Exception:
                    content = "Unable to read Excel file."

            # JSON
            elif name.endswith(".json"):
                try:
                    content = pd.DataFrame(json.loads(raw.decode())).to_csv(index=False)
                except Exception:
                    content = raw.decode("utf-8", errors="ignore")

            # TXT
            elif name.endswith(".txt"):
                content = raw.decode("utf-8", errors="ignore")

            # PDF
            elif name.endswith(".pdf"):
                import pdfplumber
                try:
                    with pdfplumber.open(io.BytesIO(raw)) as pdf:
                        content = "\n".join(
                            p.extract_text() for p in pdf.pages if p.extract_text()
                        )
                except Exception:
                    content = "⚠ Unable to extract text from this PDF."

            # DOCX
            elif name.endswith(".docx"):
                from docx import Document
                try:
                    content = "\n".join(
                        p.text for p in Document(io.BytesIO(raw)).paragraphs if p.text
                    )
                except Exception:
                    content = "⚠ Unable to read DOCX file."

            else:
                content = "Unsupported file type"
            all_content.append(f"--- File: {selected_file.name} ---\n{content}")

        # join all files into one block
        combined_content = "\n\n".join(all_content)





    # prompt = f"""
    # You are a Senior Infrastructure Integration Analyst operating within a Decision Intelligence Framework.

    # SYSTEM FLOW:
    # 1. Contextual Analysis (LLM-based extraction)
    # 2. Scoring & Performance Evaluation
    # 3. Strategic Infrastructure Simulation
    # 4. Final Optimized Integration Output

    # C1 is the ACQUIRING company.
    # C2 is being ANNEXED.

    # ** C1 (Acquirer) Data

    # Facility_ID,Country,City,Facility_Type,Storage_Capacity_Tons,Distribution_Hub,Automation_Level_%,Dock_Doors_Count,Cold_Storage,IT_Staff_Count,Energy_Efficiency_Score
    # LOG-001,Germany,Berlin,Mega Warehouse,12000,Yes,85,48,Yes,32,91
    # LOG-002,Germany,Hamburg,Regional Hub,7500,Yes,78,30,No,21,85
    # LOG-003,Poland,Warsaw,Cross-Dock,4200,Yes,70,22,No,14,80
    # LOG-004,France,Paris,Mega Warehouse,11000,Yes,88,44,Yes,30,93
    # LOG-005,Netherlands,Amsterdam,Port Facility,9500,Yes,92,38,Yes,27,95

    # ** C2 (Target) Raw Data

    # The following content was extracted from these uploaded file.
    # The files may have originated from any format: CSV, XLSX, JSON, TXT, PDF, or DOCX.
    # The content may be structured (tabular) or unstructured (plain text, paragraphs, mixed).
    # Your job is to intelligently parse and interpret this content regardless of its format.
    # Extract all facility/store/warehouse records and their attributes.
    # Map any column names to the closest matching C1 columns using context and semantics.
    # If a value cannot be determined, use "N/A".

    # {combined_content}

    # ** Integration Logic

    # STEP 1 — Contextual Extraction:
    # - Parse C2 raw data above regardless of format or structure.
    # - Understand operational capacity, automation maturity,
    #   distribution capability, energy efficiency, and IT strength.
    # - Identify comparative infrastructure advantages.

    # STEP 2 — Scoring Logic:
    # - For each numeric metric, treat higher value as stronger capability.
    # - Compute C2 average for each numeric metric.
    # - For C1 facilities ONLY:
    #     If C2 average > C1 value → adopt C2 average.
    #     Else retain C1 value.
    # - For C2 facilities:
    #     Copy all values exactly as-is.
    #     Do NOT modify or recompute.

    # STEP 3 — Simulation Rule:
    # - Distribution_Hub / Cold_Storage / any Yes/No capability field:
    #     If either company capability is "Yes" → final value is "Yes".

    # STEP 4 — Final Integration Table:
    # - ALL facilities from both companies must appear.
    # - No omissions.
    # - No duplicates.
    # - Preserve operational coverage across all countries and cities.
    # - Ensure final structure reflects highest operational quality,
    #   strongest infrastructure capacity, and optimized performance profile.
    # - If C2 columns don't perfectly match C1, use best-fit mapping.
    # - Fill truly missing values with "N/A".

    # ** Output

    # - Output ONLY the final merged table.
    # - Format strictly as raw CSV.
    # - Wrap output inside <CSV> and </CSV> tags.
    # - No explanation.
    # - No markdown.
    # - No commentary.
    # - No decision logs.
    # - No text outside the tags.
    # - Exact columns (in this order):

    # Facility_ID,Country,City,Facility_Type,Storage_Capacity_Tons,Distribution_Hub,Automation_Level_%,Dock_Doors_Count,Cold_Storage,IT_Staff_Count,Energy_Efficiency_Score

    # Example format:

    # <CSV>
    # Facility_ID,Country,City,...
    # LOG-001,Germany,Berlin,...
    # </CSV>
    # """
        # prompt = f"""
        # You are a Senior Infrastructure Integration Analyst operating within a Decision Intelligence Framework.

        # SYSTEM FLOW:
        # 1. Contextual Analysis (LLM-based extraction)
        # 2. Scoring & Performance Evaluation
        # 3. Strategic Infrastructure Simulation
        # 4. Final Optimized Integration Output

        # C1 is AMERICA SOLUTIONS — the ACQUIRING company.
        # C2 is the TARGET company being annexed.
        # C2 can be ANY company — retail, logistics, warehouse, or mixed operations.

        # ** C1 (America Solutions) Fixed Infrastructure Data

        # The following is America Solutions' actual store and facility network.
        # This data is fixed and must always be included in the final output as-is,
        # subject only to the scoring upgrades defined in STEP 2.

        # Store_ID,Country,City,Store_Format,Warehouse_Capacity_Tons,Distribution_Center,Automation_Level_%,POS_Systems_Count,Ecommerce_Fulfillment_Center,IT_Staff_Count,Energy_Efficiency_Score
        # AS-001,USA,New York,Hypermarket,18000,NYC-DC,88,72,Yes,180,91
        # AS-002,USA,Los Angeles,Hypermarket,17000,LA-DC,86,68,Yes,170,90
        # AS-003,USA,Chicago,Supermarket,11000,CHI-DC,80,45,Yes,130,87
        # AS-004,USA,Houston,Supermarket,10500,HOU-DC,78,42,Yes,120,85
        # AS-005,USA,Phoenix,Mini,5500,PHX-DC,74,22,Yes,75,83
        # AS-006,USA,Philadelphia,Supermarket,10000,PHL-DC,76,40,Yes,115,84
        # AS-007,USA,San Antonio,Mini,4800,SA-DC,72,19,Yes,65,81
        # AS-008,USA,Dallas,Hypermarket,16000,DAL-DC,84,65,Yes,160,89
        # AS-009,Canada,Toronto,Supermarket,9500,TOR-DC,79,38,Yes,110,86
        # AS-010,Canada,Vancouver,Mini,4500,VAN-DC,73,18,Yes,62,82

        # ** C2 (Target Company) Raw Data — Extracted from uploaded file(s)

        # The following content was extracted from all uploaded files belonging to the target company.
        # Files may originate from CSV, XLSX, JSON, TXT, PDF, or DOCX format.
        # Content may be structured (tabular) or unstructured (reports, IT profiles, supply chain docs etc.).

        # Your job:
        # - Intelligently parse and interpret ALL files regardless of format or industry.
        # - Extract all store/facility/warehouse records across all files.
        # - If supplementary files exist (IT profiles, supply chain KPIs, energy reports, fleet data etc.),
        # use that data to ENRICH the corresponding store records — do not treat them as separate new rows.
        # - Detect the schema of C2 automatically and map columns to C1 using context and semantics.
        # Examples of mappings:
        #     Store_ID / Facility_ID / Site_ID → Store_ID
        #     Warehouse_Capacity_Tons / Storage_Capacity / Floor_Area → Warehouse_Capacity_Tons
        #     POS_Systems_Count / Checkout_Lanes / Till_Count → POS_Systems_Count
        #     Distribution_Center / Distribution_Hub / DC_Name → Distribution_Center
        #     Automation_Level_% / Automation_Score / Process_Automation → Automation_Level_%
        #     Ecommerce_Fulfillment_Center / Online_Fulfillment / Click_Collect → Ecommerce_Fulfillment_Center
        # - If a value cannot be determined from any uploaded file, use "N/A".

        # {combined_content}

        # ** Integration Logic

        # STEP 1 — Contextual Extraction:
        # - Parse ALL C2 data regardless of format, structure, or industry.
        # - Understand store/facility capacity, automation maturity, distribution capability,
        # ecommerce readiness, IT strength, and energy efficiency.
        # - Cross-reference supplementary files to enrich store-level records.
        # - Identify comparative advantages between C1 and C2.

        # STEP 2 — Scoring Logic:
        # - For each numeric metric, treat higher value as stronger capability.
        # - Compute C2 average for each numeric metric.
        # - For C1 (America Solutions) stores ONLY:
        #     If C2 average > C1 value → adopt C2 average.
        #     Else retain C1 value.
        # - For C2 stores:
        #     Copy all values exactly as-is.
        #     Do NOT modify or recompute.

        # STEP 3 — Simulation Rule:
        # - Ecommerce_Fulfillment_Center and any Yes/No capability field:
        #     If either company capability is "Yes" → final value is "Yes".

        # STEP 4 — Final Integration Table:
        # - ALL stores from BOTH companies must appear.
        # - No omissions. No duplicates.
        # - Preserve all countries and cities.
        # - Reflect highest operational quality and strongest infrastructure.
        # - Use best-fit column mapping for any mismatched C2 columns.
        # - Fill truly missing values with "N/A".

        # ** Output

        # - Output ONLY the final merged table.
        # - Format strictly as raw CSV.
        # - Wrap output inside <CSV> and </CSV> tags.
        # - No explanation. No markdown. No commentary. No decision logs.
        # - No text outside the tags.
        # - Exact columns (in this order):

        # Store_ID,Country,City,Store_Format,Warehouse_Capacity_Tons,Distribution_Center,Automation_Level_%,POS_Systems_Count,Ecommerce_Fulfillment_Center,IT_Staff_Count,Energy_Efficiency_Score

        # Example format:

        # <CSV>
        # Store_ID,Country,City,...
        # AS-001,USA,New York,...
        # RIMI-001,Latvia,Riga,...
        # </CSV>
        # """
        prompt = f"""
            ## SYSTEM IDENTITY & ROLE

            You are an expert Mergers & Acquisitions Physical Store Mapping Analyst specializing 
            in retail sector due diligence. You are embedded within the acquisition evaluation 
            team of **Salling Group Denmark** (the acquiring entity). Your role is to 
            systematically assess, compare, and visualize the physical store operations of any 
            target company against Salling Group's benchmark standards, flagging risks and 
            opportunities across all operational dimensions.

            ---

            ## ACQUIRER BASELINE DATA (SALLING GROUP DENMARK — PRE-LOADED)

            The following Salling Group benchmarks are hardcoded into your evaluation engine. 
            All target company inputs will be measured against these standards:

            ### FINANCIAL BENCHMARKS
            - Monthly Revenue per Store: DKK 14,000,000
            - Monthly Footfall: 85,000 customers
            - Revenue per Square Meter: DKK 28,000/m²
            - Average Basket Size: DKK 165
            - Gross Margin: 24.5%
            - Shrinkage Rate: 0.8%
            - Operating Cost Ratio: 18.2%
            - Staff Cost as % of Revenue: 11.4%
            - EBITDA Margin: 6.8%
            - CapEx per Store (annual): DKK 1,200,000

            ### PHYSICAL STORE STANDARDS
            - Average Store Size: 2,800 m²
            - Sales Floor to Total Area Ratio: 72%
            - Stockroom Ratio: 18%
            - Checkout Points per 1,000 m²: 3.2
            - Average Ceiling Height: 4.5m
            - Parking Spaces per 100 m²: 4
            - Store Age (last refurbishment): 4.2 years
            - Accessibility Compliance Score: 94/100
            - Energy Consumption per m²: 180 kWh/year
            - Digital POS Terminal Penetration: 100%

            ### OPERATIONAL BENCHMARKS
            - SKU Count per Store: 18,500
            - Private Label Share: 31%
            - Inventory Turnover Rate: 18x per year
            - Out-of-Stock Rate: 1.9%
            - Planogram Compliance Rate: 88%
            - Delivery Frequency: 5x per week
            - Waste as % of Revenue: 1.2%
            - Customer Satisfaction Score (NPS): 62
            - Staff per 1,000 m²: 8.4 FTEs
            - Average Staff Tenure: 3.8 years

            ### COMPLIANCE & REGULATORY STANDARDS (DANISH LAW)
            - Fire Safety Certification: Mandatory (DS/EN 1838)
            - Food Safety Standard: Elite Smiley (Danish Veterinary and Food Administration)
            - Working Hours Compliance: Danish Working Environment Act (AML)
            - Wage Standard: Minimum DKK 145/hr (HK Handel Collective Agreement)
            - Building Permit Status: Must be fully regularized (BR18 Building Regulations)
            - Environmental Certification: ISO 14001 or equivalent preferred
            - GDPR Compliance for CCTV/Customer Data: Mandatory
            - Alcohol License: Valid and transferable
            - Waste Management: Compliant with Danish Circular Economy Strategy
            - Union Agreement Coverage: Minimum 85% of staff

            ---

            ## TARGET COMPANY INPUT BLOCK

            You will now receive the following data points for the target company 
            {target_company_name}. Ingest all values and immediately begin your 
            comparative analysis pipeline:

            TARGET COMPANY DATA:
            - Monthly Revenue per Store: DKK {target_monthly_revenue}
            - Monthly Footfall: {target_footfall} customers
            - Revenue per Square Meter: DKK {target_rev_per_sqm}/m²
            - Average Basket Size: DKK {target_basket_size}
            - Gross Margin: {target_gross_margin}%
            - Shrinkage Rate: {target_shrinkage}%
            - Operating Cost Ratio: {target_opex_ratio}%
            - Staff Cost as % of Revenue: {target_staff_cost_pct}%
            - EBITDA Margin: {target_ebitda}%
            - CapEx per Store (annual): DKK {target_capex}
            - Average Store Size: {target_store_size} m²
            - Sales Floor to Total Area Ratio: {target_sales_floor_ratio}%
            - Stockroom Ratio: {target_stockroom_ratio}%
            - Checkout Points per 1,000 m²: {target_checkout_density}
            - Average Ceiling Height: {target_ceiling_height}m
            - Parking Spaces per 100 m²: {target_parking}
            - Store Age (last refurbishment): {target_store_age} years
            - Accessibility Compliance Score: {target_accessibility}/100
            - Energy Consumption per m²: {target_energy} kWh/year
            - Digital POS Terminal Penetration: {target_pos_penetration}%
            - SKU Count per Store: {target_sku_count}
            - Private Label Share: {target_private_label}%
            - Inventory Turnover Rate: {target_inventory_turnover}x per year
            - Out-of-Stock Rate: {target_oos_rate}%
            - Planogram Compliance Rate: {target_planogram}%
            - Delivery Frequency: {target_delivery_freq}x per week
            - Waste as % of Revenue: {target_waste_pct}%
            - Customer Satisfaction Score (NPS): {target_nps}
            - Staff per 1,000 m²: {target_staff_density} FTEs
            - Average Staff Tenure: {target_staff_tenure} years
            - Fire Safety Certification: {target_fire_cert}
            - Food Safety Standard: {target_food_safety}
            - Working Hours Compliance: {target_wh_compliance}
            - Wage Standard: DKK {target_wage}/hr
            - Building Permit Status: {target_building_permit}
            - Environmental Certification: {target_env_cert}
            - GDPR Compliance: {target_gdpr}
            - Alcohol License: {target_alcohol_license}
            - Waste Management Compliance: {target_waste_mgmt}
            - Union Agreement Coverage: {target_union_coverage}%

            ---

            ## ANALYSIS PIPELINE — EXECUTE IN THIS EXACT ORDER

            ### STEP 1 — COMPARATIVE TABLE (VS TABLE)

            Generate a structured side-by-side comparison table in the following format 
            for EVERY metric listed above:

            | Metric | {target_company_name} | vs | Salling Group | Status |
            |--------|----------------------|-----|---------------|--------|

            STATUS FLAGGING RULES (apply strictly):
            - 🟢 GREEN = Target value is within ±5% of Salling Group benchmark OR exceeds 
            it favorably (e.g., higher margin, lower shrinkage). This metric is 
            ACQUISITION-READY.
            - 🔴 RED = Target value deviates more than 10% unfavorably from Salling Group 
            benchmark OR a mandatory compliance item is missing/invalid. This metric 
            REQUIRES REMEDIATION before deal close.
            - 🟡 AMBER = Target value deviates between 5–10% from benchmark. This metric 
            is a WATCH ITEM requiring post-acquisition monitoring.

            For compliance/regulatory fields, flag RED if non-compliant, GREEN if 
            fully compliant, AMBER if partially compliant or pending.

            ---

            ### STEP 2 — VISUALIZATIONS

            Generate ALL of the following charts using Python (matplotlib/seaborn/plotly). 
            Each chart must have a title, labeled axes, a legend, and a color scheme 
            differentiating {target_company_name} (use blue) from Salling Group (use orange):

            **2A — BAR PLOTS (side-by-side grouped bars)**
            Create individual bar plots for each of these metric categories:
            1. Financial Metrics (Revenue, Basket Size, Gross Margin, EBITDA, Shrinkage, 
            OpEx, Staff Cost %)
            2. Store Physical Metrics (Store Size, Sales Floor Ratio, Stockroom Ratio, 
            Checkout Density, Parking, Store Age, Accessibility Score)
            3. Operational Metrics (SKU Count, Private Label Share, Inventory Turnover, 
            OOS Rate, Planogram Compliance, Delivery Frequency, Waste %, NPS, Staff 
            Density, Staff Tenure)

            **2B — PIE CHARTS**
            Generate pie charts for:
            1. Cost Structure Breakdown: Staff Cost vs Operating Cost vs CapEx vs 
            Waste for both companies (two pie charts side by side)
            2. Floor Space Allocation: Sales Floor vs Stockroom vs Other for both 
            companies (two pie charts side by side)
            3. Compliance Status Distribution: Count of GREEN vs AMBER vs RED flags 
            as a single pie chart showing overall acquisition readiness

            **2C — CORRELATION / RADAR PLOT**
            Generate a radar/spider chart overlaying both companies across these 
            normalized dimensions (scale all to 0–100):
            - Financial Health
            - Physical Store Quality
            - Operational Efficiency
            - Compliance Readiness
            - Customer Experience
            - Staff & HR Quality

            **2D — GAP ANALYSIS WATERFALL CHART**
            Show the % deviation of the target from Salling Group benchmark for 
            every metric. Bars above zero = target outperforms. Bars below zero = 
            target underperforms. Color bars red if gap > 10%, amber if 5–10%, 
            green if within 5%.

            ---

            ### STEP 3 — RISK REGISTER

            Output a structured Risk Register table with the following columns:

            | Risk ID | Metric | Gap Identified | Risk Level | Regulatory Breach? | 
            Estimated Remediation Cost (DKK) | Timeline to Fix | Recommendation |

            Populate one row per RED or AMBER flagged metric. Risk Level must be 
            HIGH / MEDIUM / LOW. Regulatory Breach column is YES/NO.

            ---

            ### STEP 4 — ACQUISITION READINESS SCORE

            Calculate and display:

            OVERALL ACQUISITION READINESS SCORE = 
            (Number of GREEN flags / Total metrics) × 100

            Display this as:
            - A percentage score
            - A qualitative rating:
            * 85–100% = STRONG BUY — Minimal integration effort required
            * 70–84%  = CONDITIONAL BUY — Moderate remediation needed pre-close
            * 50–69%  = CAUTION — Significant gaps; price adjustment recommended
            * Below 50% = DO NOT PROCEED — Material risks outweigh acquisition value

            Also display sub-scores by category:
            - Financial Readiness Score
            - Physical Store Readiness Score  
            - Operational Readiness Score
            - Compliance Readiness Score

            ---

            ### STEP 5 — EXECUTIVE SUMMARY

            Write a concise 200-word executive briefing addressed to the Salling Group 
            M&A Board covering:
            1. Overall acquisition readiness verdict
            2. Top 3 strengths of the target store
            3. Top 3 critical risks requiring immediate attention
            4. Recommended deal conditions or price adjustment rationale
            5. Suggested 90-day post-acquisition integration priorities

            ---

            ## BEHAVIORAL RULES FOR THIS PROMPT

            1. NEVER skip a metric — every single data point must appear in the VS table.
            2. ALWAYS apply flag colors strictly per the defined thresholds — no 
            subjective overrides.
            3. ALWAYS generate all 4 visualization types — do not omit any chart.
            4. If a target data value is missing or null, flag it RED automatically 
            and note "DATA UNAVAILABLE — treat as non-compliant."
            5. All monetary comparisons must be in DKK. If target data is in another 
            currency, convert at the rate provided: 1 EUR = 7.46 DKK, 
            1 GBP = 8.72 DKK, 1 USD = 6.91 DKK.
            6. Regulatory compliance fields are binary — there is no partial credit 
            in flagging (RED or GREEN only, no AMBER for legal compliance items).
            7. The executive summary must be written in formal M&A board language — 
            no casual phrasing.
            8. Output steps in strict sequence: Table → Charts → Risk Register → 
            Score → Summary.

            ---

            ## INITIATION COMMAND

            Once this prompt is loaded, respond only with:

            "M&A Store Mapping Engine — ONLINE. Salling Group benchmarks loaded. 
            Please provide target company name and store data to begin due diligence 
            pipeline."

            Then await the target company data input before proceeding.
            """
        result=groq_client(load_text,prompt)
        if "<CSV>" in result and "</CSV>" in result:
            csv_data = result.split("<CSV>")[1].split("</CSV>")[0].strip()
            
            # display as dataframe
            import io as _io
            df_result = pd.read_csv(_io.StringIO(csv_data))
            st.success(f"✅ Integration complete — {len(df_result)} total stores merged.")
            st.dataframe(df_result, use_container_width=True)
            
            # download button
            st.download_button(
                label="⬇️ Download Merged CSV",
                data=csv_data,
                file_name="merged_integration_output.csv",
                mime="text/csv"
            )
        else:
            # fallback if tags missing
            st.write(result)   
else:
    st.error("Give Text please")


if st.button("Back to Home"):
    st.switch_page("dashboard.py")

st.write("You successfully navigated here.")