import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import re
from groqqer import groq_client
from database_comp import data_loader,compare,extract_schema

st.title("Audit Automated Part")
files = st.file_uploader(
"Drop your files here",
type=["csv", "xlsx","pdf","docx"],
accept_multiple_files=True
)
df1,df2=None,None
cuss=st.selectbox("Output Type",["Structured","Unstructured"])
if cuss=="Structured":

# with open("india_infra_store_mapping.xlsx","rb") as f:
#     df1=pd.read_excel(f)
# # india_infra_store_mapping.xlsx
# query=st.text_input("Enter your query:")
# for file in files:
#     name = file.name.lower()

#     if name.endswith(".csv"):
#         df2 = pd.read_csv(file, encoding="utf-8", encoding_errors="ignore")

#     elif name.endswith((".xlsx", ".xls")):
#         df2 = pd.read_excel(file)
    

# #df1,df2=data_loader(file1,file2)
# if st.button("Process with AI",type="primary"):

#     our_schema,target_schema=extract_schema(df1),extract_schema(df2)

#     comparison=compare(our_schema,target_schema)

#     prompt=f"""
#     You are a database integration expert.

#     Your task is to do schema comparison between two ERP databases.

#     Based on the differences:
#     1. Estimate integration complexity (1-10)
#     2. Assess the schemas of both and create an expected target schema and follow these rules:
#     - If {our_schema} better than {target_schema} consider integrating their functionalities into our system
#     - If {our_schema} weaker than {target_schema} consider integrating our functionalities into their system
#     - If both the schemas go different ways ask an integration expert to handle it
#     3. Generate gap reports if any and give ideas how to implement
#     4. If analytics or plots are needed, return ONLY valid Python code.
#     Rules:
#     - Do not write explanations
#     - Do not include markdown
#     - Do not include ```python
#     - Only output executable Python code
#     - Use streamlit (st.pyplot, st.line_chart, st.bar_chart) for plots
#     5. You must always include at least two analytical visualizations(preferably histogram and line chart) when comparing datasets.
#     6. You may ONLY use the following libraries:
#         - pandas
#         - matplotlib
#         - seaborn
#         - numpy
#         - streamlit
#         Do NOT import any other libraries.
#     6. If a visualization is useful, generate Python code wrapped in:

#     <GRAPH>
#     # python code
#     </GRAPH>
#     - All other explanations should remain normal text.
#     7. Explain reasoning and display analytics like correlation,line charts,histograms as proof of your predictions 

#     Databases given:
#     Table-Our_Schema:{our_schema},
#     Table-Target_Schema:{target_schema}

#     Output Section:

#     *Acquirer Details:*
#     - Our_Schema Detailed Analysis

#     *Target Details:*
#     - Target_Schema Detailed Analysis

#     *Merged Analysis and Explanations*
#     - Merged Table with valid explanations

#     *Plots*
#     - Plots to support your judgement

#     *Gap Report and Inference*
#     - Generate a gap report with adequate proof of how and why merging should be done the way u suggest

#     *Complexity Score*
#     - Finally generate a complexity score based on the entire comparison

#     *Additional Information(Optional)*
#     - If {query} asks something else of you please generate that information here
#     """
#     response=groq_client(query,prompt)


    with open("india_infra_store_mapping.xlsx","rb") as f:
        df1=pd.read_excel(f)
        df1.columns = df1.columns.str.lower().str.strip()
    # india_infra_store_mapping.xlsx
    query=st.text_input("Enter your query:")
    for file in files:
        name = file.name.lower()

        if name.endswith(".csv"):
            df2 = pd.read_csv(file, encoding="utf-8", encoding_errors="ignore")

        elif name.endswith((".xlsx", ".xls")):
            df2 = pd.read_excel(file)
    
        

    #df1,df2=data_loader(file1,file2)
    if st.button("Process with AI",type="primary"):
        if df1 is not None and df2 is not None:

            our_schema,target_schema=extract_schema(df1),extract_schema(df2)

            #comparison=compare(our_schema,target_schema)

            prompt=f"""
            You are a database integration expert.

            Your task is to do schema comparison between two ERP database schemas.

            Based on the differences:
            1. Estimate integration complexity (1-10)
            2. Assess the schemas of both and create an expected target schema and follow these rules:
            - If {our_schema} better than {target_schema} consider integrating their functionalities into our system
            - If {our_schema} weaker than {target_schema} consider integrating our functionalities into their system
            - If both the schemas go different ways ask an integration expert to handle it
            3.{df1} and {df2} are already in memory. NEVER use pd.read_csv(), 
              pd.read_excel(), or any file reading. Use df1 and df2 directly.
            3. Generate gap reports if any and give ideas how to implement
            4. If analytics or plots are needed, return ONLY valid Python code.
            Rules:
            - Do not write explanations
            - Do not include markdown
            - Do not include ```python
            - Only output executable Python code
            - Use streamlit (st.pyplot, st.line_chart, st.bar_chart) for plots

            5. You must always include at least two analytical visualizations
               (preferably histogram and line chart) when comparing datasets.
               - Line Chart: use related numeric columns from {df1} (acquirer) and {df2}(target)[in the plot one line corresponds to acquirer and one line corresponds to target]
               - Correlation Matrix: use numeric columns from {df1} and {df2} (target)[one column of acquirer and one related column of target that helps u reach the conclusion]
            6. The plots should be comparible for e.g line chart consists of {our_schema} vs {target_schema}
                You may ONLY use the following libraries:
                - pandas
                - matplotlib
                - seaborn
                - numpy
                - streamlit
                Do NOT import any other libraries.
            7. If a visualization is useful, generate Python code wrapped in:

            <GRAPH>
            # python code
            </GRAPH>
            - All other explanations should remain normal text.
            8. Explain reasoning and display analytics like correlation,line charts,histograms as proof of your predictions 

            Databases given:
            Table-Acquirer Sample:{df1.head(5).to_string()}
            Table-Merger Sample:{df2.head(5).to_string()}

            Schemas given:
            Table-Acquirer_Schema:{our_schema},
            Table-Target_Schema:{target_schema}

            Output Section:

            *Acquirer Details:*
            - Our_Schema Detailed Analysis

            *Target Details:*
            - Target_Schema Detailed Analysis

            *Merged Analysis and Explanations*
            - Merged Table with valid explanations

            *Plots*
            - Plots to support your judgement

            *Gap Report and Inference*
            - Generate a gap report with adequate proof of how and why merging should be done the way u suggest

            *Complexity Score*
            - Finally generate a complexity score based on the entire comparison

            *Additional Information(Optional)*
            - If {query} asks something else of you please generate that information here
            """
            response=groq_client(query,prompt)
#part 1

            # 4. If analytics or plots are needed, return ONLY valid Python code.
            # Rules:
            # - Do not write explanations
            # - Do not include markdown
            # - Do not include ```python
            # - Only output executable Python code
            # - Use streamlit (st.pyplot, st.line_chart, st.bar_chart) for plots

    # with st.expander("Document Checker"):
    #     st.code(response)
    #     exec(response)
#part 2
    # with st.expander("Document Comparison:"):

    #     parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

    #     for i, part in enumerate(parts):

    #         if i % 2 == 0:
    #             # normal text
    #             st.write(part)

    #         else:
    #             fig, ax = plt.subplots(figsize=(18,6))
    #             # graph code
    #             exec(part, {
    #                 "df1": df1,
    #                 "df2": df2,
    #                 "pd": pd,
    #                 "plt": plt,
    #                 "st": st
    #             })
#part 3
    # with st.expander("Document Comparison:"):

    #     parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

    #     safe_env = {
    #         "df1": df1,
    #         "df2": df2,
    #         "pd": pd,
    #         "plt": plt,
    #         "st": st
    #     }

    #     for i, part in enumerate(parts):

    #         part = part.strip()

    #         if i % 2 == 0:
    #             if part:
    #                 st.write(part)

    #         else:
    #             try:
    #                 exec(part, safe_env)
    #                 fig = plt.gcf()
    #                 if fig.get_axes():
    #                     st.pyplot(fig)
    #                     plt.clf()

    #             except Exception as e:
    #                 st.error(f"Graph generation failed: {e}")
# part 4
    # with st.expander("Document Comparison:"):

    #     parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

    #     safe_env = {
    #         "df1": df1,
    #         "df2": df2,
    #         "pd": pd,
    #         "plt": plt,
    #         "st": st
    #     }
    #     plt.close('all')

    #     for i, part in enumerate(parts):

    #         part = part.strip()

    #         if i % 2 == 0:
    #             if part:
    #                 st.write(part)

    #         else:
    #             try:
    #                 # Track figure count before execution
    #                 before = len(plt.get_fignums())

    #                 exec(part, safe_env)

    #                 after = len(plt.get_fignums())

    #                 # If AI didn't render the figure
    #                 if after > before:
    #                     fig = plt.gcf()
    #                     st.pyplot(fig)
    #                     plt.close(fig)

    #             except Exception as e:
    #                 st.error(f"Graph generation failed: {e}")
#part 5
    # with st.expander("Document Comparison:"):

    #     parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

    #     safe_env = {
    #         "df1": df1,
    #         "df2": df2,
    #         "pd": pd,
    #         "plt": plt,
    #         "st": st
    #     }
    #     plt.close('all')

    #     for i, part in enumerate(parts):

    #         part = part.strip()

    #         if i % 2 == 0:
    #             if part:
    #                 st.write(part)

    #         else:
    #             try:
    #                 # Track figure count before execution
    #                 before = len(plt.get_fignums())

    #                 exec(part, safe_env)

    #                 after = len(plt.get_fignums())

    #                 # If AI didn't render the figure
    #                 if after > before:
    #                     fig = plt.gcf()
    #                     st.pyplot(fig)
    #                     plt.close(fig)

    #             except Exception as e:
    #                 st.error(f"Graph generation failed: {e}")
            with st.expander("Document Comparison:"):

                parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

                safe_env = {
                    "our_schema": our_schema,
                    "target_schema": target_schema,
                    "df1":df1,
                    "df2":df2,
                    "pd": pd,
                    "plt": plt,
                    "st": st
                }

                for i, part in enumerate(parts):

                    part = part.strip()

                    if i % 2 == 0:
                        if part:
                            st.write(part)

                    else:
                        try:
                            exec(part, safe_env)
                            fig = plt.gcf()
                            if fig.get_axes():
                                st.pyplot(fig)
                            plt.close('all')

                        except Exception as e:
                            st.error(f"Graph generation failed: {e}")
else:
    with open("india_infra_store_mapping.xlsx","rb") as f:
        df1=pd.read_excel(f)
        df1.columns = df1.columns.str.lower().str.strip()
    # india_infra_store_mapping.xlsx
    query=st.text_input("Enter your query:")
    if st.button("Process with AI",type="primary"):

        # for file in files:
        # name = file.name.lower()

        # if name.endswith(".csv"):
        #     df2 = pd.read_csv(file, encoding="utf-8", encoding_errors="ignore")

        # elif name.endswith((".xlsx", ".xls")):
        #     df2 = pd.read_excel(file)
        

    #df1,df2=data_loader(file1,file2)
    

        our_schema=extract_schema(df1)       

        # Extract raw content from uploaded files
        file_contents = ""
        for file in files:
            name = file.name.lower()
            if name.endswith(".pdf"):
                import pdfplumber
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        file_contents += page.extract_text() or ""
            elif name.endswith(".docx"):
                import docx
                doc = docx.Document(file)
                for para in doc.paragraphs:
                    file_contents += para.text + "\n"
            elif name.endswith(".csv"):
                file_contents += pd.read_csv(file).to_string()
            elif name.endswith((".xlsx", ".xls")):
                file_contents += pd.read_excel(file).to_string()

    # comparison=compare(our_schema,target_schema)

        # prompt=f"""
        # You are a database integration expert.

        # Your task is to do schema comparison between two ERP databases.

        # Based on the differences:
        # 1. Estimate integration complexity (1-10)
        # 2. The user has provided {files} — one or more files (.pdf, .xlsx, .docx, or other formats) 
        # that collectively describe the target company's database or data system.
        # All provided files refer to the same target company.

        # - Parse and extract all structured or semi-structured content from each file.
        # - Identify fields, data types, sample values, and nullability across all files.
        # - Merge extracted fields into a single unified target schema 
        #     (if multiple files are provided, treat them as complementary — not conflicting).
        # - Resolve any naming inconsistencies across files by standardizing to snake_case.
        # 3. Assess the schemas of both and create an expected target schema and follow these rules:
        # - If {our_schema} better than schema of the {files} consider integrating their functionalities into our system
        # - If {our_schema} weaker than chema of the {files} consider integrating our functionalities into their system
        # - If both the schemas go different ways ask an integration expert to handle it
        # 4. Generate gap reports if any and give ideas how to implement
        # 5. If analytics or plots are needed, return ONLY valid Python code.
        # Rules:
        # - Do not write explanations
        # - Do not include markdown
        # - Do not include ```python
        # - Only output executable Python code
        # - Use streamlit (st.pyplot, st.line_chart, st.bar_chart) for plots
        # 6. You must always include at least two analytical visualizations(preferably histogram and line chart) when comparing datasets.
        # 7. You may ONLY use the following libraries:
        #     - pandas
        #     - matplotlib
        #     - seaborn
        #     - numpy
        #     - streamlit
        #     Do NOT import any other libraries.
        # 8. If a visualization is useful, generate Python code wrapped in:

        # <GRAPH>
        # # python code
        # </GRAPH>
        # - All other explanations should remain normal text.
        # 9. Explain reasoning and display analytics like correlation,line charts,histograms as proof of your predictions 

        # Databases given:
        # Table-Our_Schema:{our_schema},
        # Table-Target_Schema:schema of {files}

        # Output Section:

        # *Acquirer Details:*
        # - Our_Schema Detailed Analysis

        # *Target Details:*
        # - Target_Schema Detailed A
        #             -+****nalysis

        # *Merged Analysis and Explanations*
        # - Merged Table with valid explanations

        # *Plots*
        # - Plots to support your judgement

        # *Gap Report and Inference*
        # - Generate a gap report with adequate proof of how and why merging should be done the way u suggest

        # *Complexity Score*
        # - Finally generate a complexity score based on the entire comparison

        # *Additional Information(Optional)*
        # - If {query} asks something else of you please generate that information here
        # """
        prompt = f"""
        You are a database integration expert.

        You will be given:
        1. The acquirer's schema (already extracted)
        2. Raw content from one or more target company files

        Your tasks in order:

        STEP 1 - Extract Target Schema:
        - Read the raw file contents provided below
        - Identify all fields, data types, sample values and nullability
        - If multiple files are provided, treat them as complementary and merge into one unified target schema
        - Standardize all field names to snake_case
        - Output the unified target schema as:
        Field_Name | Data_Type | Nullable | Source_File | Notes

        STEP 2 - Compare schemas and:
        - Estimate integration complexity (1-10)
        - If acquirer schema is stronger, integrate target functionalities into acquirer
        - If target schema is stronger, integrate acquirer functionalities into target
        - If both go different directions, flag for integration expert

        STEP 3 - Gap Report:
        - List all gaps with implementation suggestions

        STEP 4 - Visualizations:
        - df1 (acquirer) is already in memory as a pandas DataFrame
        - Use df1 ONLY for all plots — do NOT read any file from disk
        - NEVER use pd.read_csv(), pd.read_excel(), or any file reading
        - Wrap ALL plot code in <GRAPH></GRAPH> tags
        - Use only: pandas, matplotlib, seaborn, numpy, streamlit
        - Use st.pyplot() to render all plots

        Acquirer Schema:
        {our_schema.to_string()}

        Acquirer Sample Data:
        {df1.head(20).to_string()}

        Target Raw File Contents:
        {file_contents}

        Output Section:
        *Acquirer Details:* - Our_Schema Detailed Analysis
        *Target Details:* - Target_Schema Detailed Analysis
        *Merged Analysis and Explanations*
        *Plots*
        *Gap Report and Inference*
        *Complexity Score*
        *Additional Information(Optional)* - {query}
        """
        response=groq_client(query,prompt)
        with st.expander("Document Comparison:"):

            parts = re.split(r"<GRAPH>(.*?)</GRAPH>", response, flags=re.S)

            safe_env = {
                "df1": df1,
                "pd": pd,
                "plt": plt,
                "st": st
            }

            for i, part in enumerate(parts):

                part = part.strip()

                if i % 2 == 0:
                    if part:
                        st.markdown(part)

                else:
                    try:
                        exec(part, safe_env)
                        fig=plt.gcf()
                        if fig.get_axes():
                            st.pyplot(fig)
                        plt.close('all')
                    except Exception as e:
                        st.error(f"Graph generation failed: {e}")  

