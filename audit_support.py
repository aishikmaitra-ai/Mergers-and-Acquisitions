import requests

url = "http://localhost:11434/api/generate"

def summarize(file):
    prompt = f"""
    You are a Senior Infrastructure Integration Analyst operating within a Decision Intelligence Framework.

    SYSTEM FLOW:
    1. Contextual Analysis (LLM-based extraction)
    2. Scoring & Performance Evaluation
    3. Strategic Infrastructure Simulation
    4. Final Optimized Integration Output

    C1 is AMERICA SOLUTIONS — the ACQUIRING company.
    C2 is the TARGET company being annexed.
    C2 can be ANY company — retail, logistics, warehouse, or mixed operations.

    ** C1 (America Solutions) Fixed Infrastructure Data

    The following is America Solutions' actual store and facility network.
    This data is fixed and must always be included in the final output as-is,
    subject only to the scoring upgrades defined in STEP 2.

    Store_ID,Country,City,Store_Format,Warehouse_Capacity_Tons,Distribution_Center,Automation_Level_%,POS_Systems_Count,Ecommerce_Fulfillment_Center,IT_Staff_Count,Energy_Efficiency_Score
    AS-001,USA,New York,Hypermarket,18000,NYC-DC,88,72,Yes,180,91
    AS-002,USA,Los Angeles,Hypermarket,17000,LA-DC,86,68,Yes,170,90
    AS-003,USA,Chicago,Supermarket,11000,CHI-DC,80,45,Yes,130,87
    AS-004,USA,Houston,Supermarket,10500,HOU-DC,78,42,Yes,120,85
    AS-005,USA,Phoenix,Mini,5500,PHX-DC,74,22,Yes,75,83
    AS-006,USA,Philadelphia,Supermarket,10000,PHL-DC,76,40,Yes,115,84
    AS-007,USA,San Antonio,Mini,4800,SA-DC,72,19,Yes,65,81
    AS-008,USA,Dallas,Hypermarket,16000,DAL-DC,84,65,Yes,160,89
    AS-009,Canada,Toronto,Supermarket,9500,TOR-DC,79,38,Yes,110,86
    AS-010,Canada,Vancouver,Mini,4500,VAN-DC,73,18,Yes,62,82

    ** C2 (Target Company) Raw Data — Extracted from uploaded file(s)

    The following content was extracted from all uploaded files belonging to the target company.
    Files may originate from CSV, XLSX, JSON, TXT, PDF, or DOCX format.
    Content may be structured (tabular) or unstructured (reports, IT profiles, supply chain docs etc.).

    Your job:
    - Intelligently parse and interpret ALL files regardless of format or industry.
    - Extract all store/facility/warehouse records across all files.
    - If supplementary files exist (IT profiles, supply chain KPIs, energy reports, fleet data etc.),
    use that data to ENRICH the corresponding store records — do not treat them as separate new rows.
    - Detect the schema of C2 automatically and map columns to C1 using context and semantics.
    Examples of mappings:
        Store_ID / Facility_ID / Site_ID → Store_ID
        Warehouse_Capacity_Tons / Storage_Capacity / Floor_Area → Warehouse_Capacity_Tons
        POS_Systems_Count / Checkout_Lanes / Till_Count → POS_Systems_Count
        Distribution_Center / Distribution_Hub / DC_Name → Distribution_Center
        Automation_Level_% / Automation_Score / Process_Automation → Automation_Level_%
        Ecommerce_Fulfillment_Center / Online_Fulfillment / Click_Collect → Ecommerce_Fulfillment_Center
    - If a value cannot be determined from any uploaded file, use "N/A".

    {combined_content}

    ** Integration Logic

    STEP 1 — Contextual Extraction:
    - Parse ALL C2 data regardless of format, structure, or industry.
    - Understand store/facility capacity, automation maturity, distribution capability,
    ecommerce readiness, IT strength, and energy efficiency.
    - Cross-reference supplementary files to enrich store-level records.
    - Identify comparative advantages between C1 and C2.

    STEP 2 — Scoring Logic:
    - For each numeric metric, treat higher value as stronger capability.
    - Compute C2 average for each numeric metric.
    - For C1 (America Solutions) stores ONLY:
        If C2 average > C1 value → adopt C2 average.
        Else retain C1 value.
    - For C2 stores:
        Copy all values exactly as-is.
        Do NOT modify or recompute.

    STEP 3 — Simulation Rule:
    - Ecommerce_Fulfillment_Center and any Yes/No capability field:
        If either company capability is "Yes" → final value is "Yes".

    STEP 4 — Final Integration Table:
    - ALL stores from BOTH companies must appear.
    - No omissions. No duplicates.
    - Preserve all countries and cities.
    - Reflect highest operational quality and strongest infrastructure.
    - Use best-fit column mapping for any mismatched C2 columns.
    - Fill truly missing values with "N/A".

    ** Output

    - Output ONLY the final merged table.
    - Format strictly as raw CSV.
    - Wrap output inside <CSV> and </CSV> tags.
    - No explanation. No markdown. No commentary. No decision logs.
    - No text outside the tags.
    - Exact columns (in this order):

    Store_ID,Country,City,Store_Format,Warehouse_Capacity_Tons,Distribution_Center,Automation_Level_%,POS_Systems_Count,Ecommerce_Fulfillment_Center,IT_Staff_Count,Energy_Efficiency_Score

    Example format:

    <CSV>
    Store_ID,Country,City,...
    AS-001,USA,New York,...
    RIMI-001,Latvia,Riga,...
    </CSV>
    """
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9
        }
    }

    # Send request to Ollama
    response = requests.post(url, json=payload, timeout=None)
    response.raise_for_status()


    result = response.json()

    summary = result.get("response", "").strip()

    if not summary:
        raise RuntimeError("Model returned an empty response")
    return summary