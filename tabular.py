# Create two CSV infrastructure databases using pandas
import pandas as pd

# ----------------------------
# RIMI BALTIC INFRA DATABASE
# ----------------------------
rimi_data = {
    "Store_ID": ["RIMI-001", "RIMI-002", "RIMI-003", "RIMI-004"],
    "Country": ["Latvia", "Estonia", "Lithuania", "Latvia"],
    "City": ["Riga", "Tallinn", "Vilnius", "Daugavpils"],
    "Store_Format": ["Hypermarket", "Supermarket", "Mini", "Express"],
    "Warehouse_Capacity_Tons": [12000, 8000, 5000, 3000],
    "Distribution_Center": ["Riga DC", "Tallinn DC", "Vilnius DC", "Riga DC"],
    "Automation_Level_%": [75, 68, 60, 55],
    "POS_Systems_Count": [45, 30, 18, 12],
    "Ecommerce_Fulfillment_Center": ["Yes", "Yes", "No", "No"],
    "IT_Staff_Count": [120, 90, 65, 40],
    "Energy_Efficiency_Score": [72, 70, 66, 63]
}

rimi_df = pd.DataFrame(rimi_data)
rimi_path = "Rimi_Baltic_Infrastructure_Database.csv"
rimi_df.to_csv(rimi_path, index=False)


# ----------------------------
# SALLING GROUP INFRA DATABASE
# ----------------------------
sailing_data = {
    "Store_ID": ["SALL-101", "SALL-102", "SALL-103", "SALL-104"],
    "Country": ["Denmark", "Denmark", "Germany", "Poland"],
    "City": ["Aarhus", "Copenhagen", "Hamburg", "Warsaw"],
    "Store_Format": ["Bilka", "føtex", "Netto", "Netto"],
    "Warehouse_Capacity_Tons": [25000, 18000, 15000, 13000],
    "Distribution_Center": ["Aarhus Mega DC", "Copenhagen DC", "Hamburg DC", "Warsaw DC"],
    "Automation_Level_%": [88, 82, 78, 74],
    "POS_Systems_Count": [110, 85, 70, 65],
    "Ecommerce_Fulfillment_Center": ["Yes", "Yes", "Yes", "Yes"],
    "IT_Staff_Count": [420, 350, 280, 260],
    "Energy_Efficiency_Score": [85, 83, 80, 77]
}

sailing_df = pd.DataFrame(sailing_data)
sailing_path = "Sailing_Group_Infrastructure_Database.csv"
sailing_df.to_csv(sailing_path, index=False)

rimi_path, sailing_path