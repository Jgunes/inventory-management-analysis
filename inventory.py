from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects
from fpdf import FPDF

INPUT_FILE = "inventory.xlsx"
OUTPUT_DIR = Path("output")
REPORT_DATE = datetime.today().strftime("%Y-%m-%d")


def read_inventory(file_path: str):
    df = pd.read_excel(file_path)

    df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce").fillna(0)
    df["Product"] = df["Product"].astype(str)

    return df


def analyze_inventory(df: pd.DataFrame):
    low_stock = df[df["Stock"] < 10]

    critical_count = len(low_stock)

    lowest_product = df.loc[df["Stock"].idxmin(), "Product"]
    lowest_stock = int(df["Stock"].min())

    total_products = len(df)
    average_stock = round(df["Stock"].mean(), 2)

    analysis = {
        "critical_count": critical_count,
        "lowest_product": lowest_product,
        "lowest_stock": lowest_stock,
        "total_products": total_products,
        "average_stock": average_stock,
    }

    return analysis


def create_neon_chart(df: pd.DataFrame):
    OUTPUT_DIR.mkdir(exist_ok=True)

    sorted_df = df.sort_values("Stock", ascending=False)

    neon_colors = [
        "#00F5FF",
        "#FF00FF",
        "#39FF14",
        "#FFD700",
        "#FF5F1F",
        "#8A2BE2",
        "#00FF99",
        "#FF1493",
    ]

    plt.figure(figsize=(14, 6), facecolor="#050816")

    ax = plt.gca()
    ax.set_facecolor("#050816")

    bars = plt.bar(
        sorted_df["Product"],
        sorted_df["Stock"],
        color=[neon_colors[i % len(neon_colors)] for i in range(len(sorted_df))],
        width=0.45
    )

    for bar in bars:
        bar.set_linewidth(0.8)

    for i, value in enumerate(sorted_df["Stock"]):
        plt.text(
            i,
            value + 1,
            str(int(value)),
            ha="center",
            fontsize=8,
            color="white"
        )

    title = plt.title(
        "Inventory Stock Analysis",
        fontsize=22,
        color="#00F5FF",
        pad=20,
        fontweight="bold"
    )

    title.set_path_effects([
        patheffects.withStroke(linewidth=6, foreground="#00F5FF33")
    ])

    plt.xlabel("Products", fontsize=12, color="white")
    plt.ylabel("Stock Quantity", fontsize=12, color="white")

    plt.xticks(rotation=30, ha="right", fontsize=8, color="white")
    plt.yticks(color="white")

    for spine in ax.spines.values():
        spine.set_color("#00F5FF")
        spine.set_linewidth(1)

    ax.grid(color="#1f2a44", linestyle="--", alpha=0.4)

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "inventory_neon_chart.png"

    plt.savefig(
        chart_path,
        dpi=300,
        facecolor="#050816",
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


class NeonPDF(FPDF):

    def header(self):
        self.set_fill_color(5, 8, 22)
        self.rect(0, 0, 210, 297, style="F")

        self.set_text_color(0, 245, 255)
        self.set_font("Arial", "B", 24)
        self.cell(0, 18, "INVENTORY MANAGEMENT REPORT", ln=True, align="C")

        self.set_text_color(180, 180, 180)
        self.set_font("Arial", "", 11)
        self.cell(0, 8, f"Automated Inventory Dashboard", ln=True, align="C")

        self.ln(8)


def export_neon_pdf(analysis: dict, chart_path: Path):
    pdf = NeonPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_text_color(255, 255, 255)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Executive Summary", ln=True)

    pdf.ln(2)

    pdf.set_font("Arial", "", 12)

    summary_text = (
        f"Total products tracked: {analysis['total_products']}\n"
        f"Average stock level: {analysis['average_stock']}\n"
        f"Critical stock products: {analysis['critical_count']}\n"
        f"Lowest stock product: {analysis['lowest_product']} "
        f"({analysis['lowest_stock']} units remaining)\n\n"
        "This inventory report was generated automatically using Python, "
        "Pandas, Matplotlib and FPDF."
    )

    pdf.multi_cell(0, 8, summary_text)

    pdf.ln(8)

    pdf.set_text_color(57, 255, 20)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Inventory Insights", ln=True)

    pdf.ln(2)

    pdf.set_text_color(230, 230, 230)
    pdf.set_font("Arial", "", 12)

    insight_text = (
        f"- {analysis['lowest_product']} currently has the lowest stock level.\n"
        "- Products below 10 units should be restocked immediately.\n"
        "- Monitoring stock trends helps avoid inventory shortages.\n"
        "- Automated reporting improves inventory planning efficiency."
    )

    pdf.multi_cell(0, 8, insight_text)

    pdf.ln(10)

    pdf.set_text_color(255, 0, 255)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Stock Visualization", ln=True)

    pdf.ln(5)

    pdf.image(str(chart_path), x=12, w=185)

    pdf.ln(100)

   
    pdf_path = OUTPUT_DIR / "inventory_neon_report.pdf"

    pdf.output(str(pdf_path))

    return pdf_path


def main():
    print("Starting Neon Inventory Reporting System...")

    df = read_inventory(INPUT_FILE)

    analysis = analyze_inventory(df)

    chart_path = create_neon_chart(df)

    pdf_path = export_neon_pdf(analysis, chart_path)

    print("Workflow completed successfully.")
    print(f"Chart created: {chart_path}")
    print(f"PDF report created: {pdf_path}")


if __name__ == "__main__":
    main()