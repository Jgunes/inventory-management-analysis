import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

dF=pd.read_excel("Inventory/inventory.xlsx")

low_stock= dF[dF["Stock"]<10]

critical_count=len(low_stock)

lowest_product=dF.loc[dF["Stock"].idxmin(),"Product"]
lowest_stock=dF["Stock"].min()

plt.figure(figsize=(10,5))

dF.sort_values("Stock").plot(
    kind="bar",
    x="Product",
    y="Stock",
    color="orange",
    legend=False

)

plt.title("Inventory Stock Levels")
plt.xlabel("Products")
plt.ylabel("Stock Quantity")

plt.tight_layout()

plt.savefig("inventory_chart.png")
plt.close()

pdf=FPDF()
pdf.add_page()

pdf.set_font("Arial","B", 16)
pdf.cell(
    0,
    10,
    "Inventory Management Report", 
    ln=True
    
)

pdf.ln(10)

pdf.set_font("Arial","",12)
pdf.cell(
    0,
    10,
    f"Lowest Stock Product:{lowest_product}",
    ln=True

)

pdf.cell(
    0,
    10,
    f"Lowest Stock Quantity:{lowest_stock}",
    ln=True

)

pdf.cell(
    0,
    10,
    f"Critical Stock Products:{critical_count}",
    ln=True

)

pdf.ln(10)

pdf.image("inventory_chart.png",w=180)

pdf.ln(10)

pdf.multi_cell(
    0,
    10,
    f"{lowest_product} currently has the lowest stock level.\n"
    "Products with stock below 10 should be restocked immediately"
    "to avoid inventory shortages." 

)

pdf.output("inventory_report.pdf")

print("Inventory report generated successfully.")