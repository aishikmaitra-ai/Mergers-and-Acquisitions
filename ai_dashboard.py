import streamlit as st
import requests
import json
from groq import Groq
import re
import os
from io import StringIO
import pandas as pd
from dotenv import load_dotenv
import base64
from groqqer import groq_client

load_dotenv()

st.set_page_config(layout="wide")
# def set_bg_local(image_file):
#     with open(image_file, "rb") as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()

#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/png;base64,{encoded}");
#             background-size: cover;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# set_bg_local("sund_logo.png")

url="http://localhost:11434/api/generate"

data1=pd.read_csv("Rimi_Baltic_Infrastructure_Database.csv")
data2=pd.read_csv("Sailing_Group_Infrastructure_Database.csv")


st.title("AI Dashboard")
col1, col2 = st.columns(2)
st.markdown(
"""
**This is an AI Dashboard that supports Mergers and Acquisitions Based Work**

"""
)
# Data Import and Display
with col1:
    st.header("Data Display")
    cuss=st.selectbox("Select what you want:",["Rimi Baltic Table","Sailing Group Table"])
    if cuss=="Rimi Baltic Table":
        # with col1:
            #st.subheader("Data Display")
            st.dataframe(data1,use_container_width=True)
    elif cuss=="Sailing Group Table":
        #with col1:
            #st.subheader("")
            st.dataframe(data2,use_container_width=True)
# Ollama Section
def ollama_parse(df1,df2):

    #groq_client()
    n_df1 = len(df1)
    n_df2 = len(df2)
    n_total = n_df1 + n_df2

    prompt = f"""
You are a Senior Infrastructure Integration Analyst operating within a Decision Intelligence Framework.

SYSTEM FLOW:
1. Contextual Analysis (LLM-based extraction)
2. Scoring & Performance Evaluation
3. Strategic Infrastructure Simulation
4. Final Optimized Integration Output

C1 is the ACQUIRING company.
C2 is being ANNEXED.

** Data Input

== C1 (Acquirer) ==
{df1.to_csv(index=False)}

== C2 (Target) ==
{df2.to_csv(index=False)}

** Integration Logic

STEP 1 — Contextual Extraction:
- Understand operational capacity, automation maturity,
  distribution capability, energy efficiency, and IT strength.
- Identify comparative infrastructure advantages.

STEP 2 — Scoring Logic:
- For each numeric metric, treat higher value as stronger capability.
- Compute C2 average for each numeric metric.
- For C1 stores ONLY:
    If C2 average > C1 value → adopt C2 average.
    Else retain C1 value.
- For C2 stores:
    Copy all values exactly as-is.
    Do NOT modify or recompute.

STEP 3 — Simulation Rule:
- Ecommerce_Fulfillment_Center:
    If either company capability is "Yes" → final value is "Yes".

STEP 4 — Final Integration Table:
- ALL stores from both companies must appear.
- No omissions.
- No duplicates.
- Preserve operational coverage across all countries and cities.
- Ensure final structure reflects highest operational quality,
  strongest infrastructure capacity, and optimized performance profile.

**Output

- Output ONLY the final merged table.
- Format strictly as raw CSV.
- Wrap output inside <CSV> and </CSV> tags.
- No explanation.
- No markdown.
- No commentary.
- No decision logs.
- No text outside the tags.
- Exact columns (in this order):

Store_ID,
Country,
City,
Store_Format,
Warehouse_Capacity_Tons,
Distribution_Center,
Automation_Level_%,
POS_Systems_Count,
Ecommerce_Fulfillment_Center,
IT_Staff_Count,
Energy_Efficiency_Score

- Exactly {n_total} data rows.

Example format:

<CSV>
Store_ID,Country,City,...
RIMI-001,Latvia,Riga,...
</CSV>
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
            "num_predict": 2048
        }
    }

    response = requests.post(url, json=payload, timeout=None)
    response.raise_for_status()

    out = response.json().get("response", "").strip()

    if not out:
        raise RuntimeError("Model returned empty output")

    # Extract content between <CSV> tags
    
    match = re.search(r"<CSV>(.*?)</CSV>", out, re.DOTALL)
    if not match:
        print("RAW OUTPUT:\n", out)
        raise ValueError("Model did not return output in expected <CSV>...</CSV> format")

    csv_content = match.group(1).strip()
    df = pd.read_csv(StringIO(csv_content))

    # Validate
    expected_ids = set(df1["Store_ID"]).union(set(df2["Store_ID"]))
    returned_ids = set(df["Store_ID"])

    # 🔹 Add missing rows if LLM dropped any
    missing_ids = expected_ids - returned_ids

    if missing_ids:
        print("⚠ Missing rows detected:", missing_ids)

        for mid in missing_ids:
            if mid in df1["Store_ID"].values:
                row = df1[df1["Store_ID"] == mid]
            else:
                row = df2[df2["Store_ID"] == mid]

            df = pd.concat([df, row], ignore_index=True)

    # 🔹 Remove accidental duplicates
    df = df.drop_duplicates(subset=["Store_ID"])

    # 🔹 Final safety check
    if len(df) != n_total:
        raise ValueError(
            f"Final row correction failed. Got {len(df)}, expected {n_total}"
        )

    return df

#     n_df1=len(df1)
#     n_df2=len(df2)
#     n_total=n_df1+n_df2
# #     prompt=f"""
# # You are a Senior Infrastructure Integration Analyst overseeing the merger of Company C2 into Company C1.

# # CONTEXT:
# # C1 is the acquiring company. C2 is being annexed. The goal is to absorb only those 
# # assets, capabilities, and resources from C2 that offer a clear advantage over C1's 
# # existing infrastructure — not a simple union of both.

# # TASKS:
# # 1. Analyze both infrastructure databases in detail across all parameters.

# # 2. For each metric/feature, benchmark C2 against C1:
# #    - If C2 is SUPERIOR → adopt C2's value/system for that attribute.
# #    - If C1 is SUPERIOR → retain C1's existing value/system.
# #    - If EQUAL → retain C1's as the default (acquirer takes precedence).

# # 3. Identify which C2 locations, distribution centers, or facilities add geographic 
# #    or operational value not already covered by C1 — include only those.

# # 4. Build a final Merged Infrastructure Table that reflects:
# #    - Best-in-class Automation Level
# #    - Highest Energy Efficiency
# #    - Strongest IT & Human Resources
# #    - Optimal Warehouse Capacity per region
# #    - Superior POS and Ecommerce capabilities
# #    - No redundant or underperforming assets

# # 5. For every decision made, provide a brief justification 
# #    (e.g., "Adopted C2's automation level of 88% vs C1's 75% — C2 superior").

# # 6. The final table should represent a leaner, stronger, consolidated entity — 
# #    not a bloated combination of both

# # IMPORTANT OUTPUT RULES:

# # - Return ONLY raw CSV.
# # - No explanation.
# # - No markdown.
# # - No backticks.
# # - No commentary.
# # - First row must be column headers.
# # - Output must start directly with column names.
# # - Output must not be empty.
# # - Every column must contain values.

# # Database of S1 (CSV format):
# # {df1.to_csv(index=False)}

# # Database of S2 (CSV format):
# # {df2.to_csv(index=False)}
# # """
#     prompt=f"""
# You are a Senior Infrastructure Integration Analyst. C1 is the ACQUIRING company. C2 is being ANNEXED.

# DATA:
# == C1 (Acquirer) ==
# {df1.to_csv(index=False)}

# == C2 (Target) ==
# {df2.to_csv(index=False)}

# RULES:
# - ALL stores from both companies must appear in the final table. No omissions, no duplicates.
# - For C1 stores ONLY: compute C2's average for each numeric metric. If C2 avg > C1 value → adopt C2 avg. Else keep C1.
# - For C2 stores: copy every value exactly as-is. Do NOT compute averages or modify any values.
# - Ecommerce_Fulfillment_Center: if either is "Yes" → final value is "Yes".

# OUTPUT INSTRUCTIONS:
# - Output the merged table ONLY as a CSV block inside <CSV> and </CSV> tags.
# - No explanation, no decision log, no markdown, no extra text outside the tags.
# - Exact columns: Store_ID,Country,City,Store_Format,Warehouse_Capacity_Tons,Distribution_Center,Automation_Level_%,POS_Systems_Count,Ecommerce_Fulfillment_Center,IT_Staff_Count,Energy_Efficiency_Score
# - Exactly {n_total} data rows.

# Example format:
# <CSV>
# Store_ID,Country,...
# RIMI-001,Latvia,...
# </CSV>
# """
#     payload={
#         "model":"llama3",
#         "prompt":prompt,
#         "stream":False,
#         "options":{
#             "temperature":0.0,
#             "top_p":0.9,
#             "num_predict": 2048
#         }

#     }

#     response=requests.post(url,json=payload,timeout=None)
#     response.raise_for_status()

#     result=response.json()

#     # out=result.get("response","").strip()
#     # if not out:
#     #     raise RuntimeError("Model returned empty output")
#     # out = out.replace("```", "").strip()

#     # try:
#     #     df = pd.read_csv(StringIO(out))
#     # except Exception:
#     #     print("RAW OUTPUT:\n", out)
#     #     raise ValueError("Model did not return valid CSV table format")
    
#     # return df   
#     out = result.get("response", "").strip()

#     if not out:
#         raise RuntimeError("Model returned empty output")

#     # Remove markdown backticks if present
#     out = out.replace("```", "").strip()

#     # 🔥 Case 1: Markdown table (| column | column |)
#     if "|" in out:
#         try:
#             df = pd.read_csv(StringIO(out), sep="|", engine="python")
#             df = df.dropna(axis=1, how="all")  # remove empty columns
#         except:
#             df = None

#     # 🔥 Case 2: Comma-separated content
#     elif "," in out:
#         try:
#             df = pd.read_csv(StringIO(out))
#         except:
#             df = None

#     # 🔥 Case 3: Plain text → Auto structure
#     else:
#         lines = [line.strip() for line in out.split("\n") if line.strip()]
#         df = pd.DataFrame({"Merged Structure Summary": lines})
#     return df



api_key = os.getenv("GROQ_KEY")

if not api_key:
    st.error("GROQ_KEY not found in .env file")
    st.stop()

def groq_client(query):
  client = Groq(api_key=api_key)

  #st.title("What is Mergers and Acquisitions?")

  completion = client.chat.completions.create(
      model="openai/gpt-oss-120b",  # safer default model
      messages=[
          {"role": "user",
          "content": query}
      ],
      temperature=0.7,
  )

  #st.subheader("The Answer is:")
  return completion.choices[0].message.content

def groq_client_adv(user_prompt, system_prompt=None, temperature=0.7):
    
    client = Groq(api_key=api_key)

    messages = []

    # Optional system instruction
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    # User query
    messages.append({
        "role": "user",
        "content": user_prompt
    })

    completion = client.chat.completions.create(
        model="llama3-8b-8192",   # safer supported model
        messages=messages,
        temperature=temperature,
    )

    return completion.choices[0].message.content
def sys(file):
    system_prompt =f"""
You are a Senior Infrastructure Integration Analyst operating within a Decision Intelligence Framework.

SYSTEM FLOW:
1. Contextual Analysis (LLM-based extraction)
2. Scoring & Performance Evaluation
3. Strategic Infrastructure Simulation
4. Final Optimized Integration Output

C1 is the ACQUIRING company.
C2 is being ANNEXED.

** Data Input

== C1 (Acquirer) ==
{df1.to_csv(index=False)}

== C2 (Target) ==
{df2.to_csv(index=False)}

** Integration Logic

STEP 1 — Contextual Extraction:
- Understand operational capacity, automation maturity,
  distribution capability, energy efficiency, and IT strength.
- Identify comparative infrastructure advantages.

STEP 2 — Scoring Logic:
- For each numeric metric, treat higher value as stronger capability.
- Compute C2 average for each numeric metric.
- For C1 stores ONLY:
    If C2 average > C1 value → adopt C2 average.
    Else retain C1 value.
- For C2 stores:
    Copy all values exactly as-is.
    Do NOT modify or recompute.

STEP 3 — Simulation Rule:
- Ecommerce_Fulfillment_Center:
    If either company capability is "Yes" → final value is "Yes".

STEP 4 — Final Integration Table:
- ALL stores from both companies must appear.
- No omissions.
- No duplicates.
- Preserve operational coverage across all countries and cities.
- Ensure final structure reflects highest operational quality,
  strongest infrastructure capacity, and optimized performance profile.

**Output

- Output ONLY the final merged table.
- Format strictly as raw CSV.
- Wrap output inside <CSV> and </CSV> tags.
- No explanation.
- No markdown.
- No commentary.
- No decision logs.
- No text outside the tags.
- Exact columns (in this order):

Store_ID,
Country,
City,
Store_Format,
Warehouse_Capacity_Tons,
Distribution_Center,
Automation_Level_%,
POS_Systems_Count,
Ecommerce_Fulfillment_Center,
IT_Staff_Count,
Energy_Efficiency_Score

- Exactly {n_total} data rows.

Example format:

<CSV>
Store_ID,Country,City,...
RIMI-001,Latvia,Riga,...
</CSV>
"""

user_prompt = """
Merge the following datasets...
"""

response = groq_client(user_prompt, system_prompt)
print(response)

if st.button("Process for Merge",type="primary"):
    with col2:
        st.header("Merged database")
        data3=ollama_parse(data2,data1)
        st.dataframe(data3)




