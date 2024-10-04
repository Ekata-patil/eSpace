import pandas as pd
import json
import matplotlib.pyplot as plt
from fpdf import FPDF

# Load the JSON data from the files
with open("/home/ec2-user/python/result.json", "r") as result_file:
    result_data = json.load(result_file)

with open("/home/ec2-user/python/SRE CHAOS SUMMARY REPORT.json", "r") as sre_file:
    sre_data = json.load(sre_file)

# Create a dataframe for result.json data
result_df = pd.DataFrame(result_data)

# Create a dataframe for SRE CHAOS SUMMARY REPORT.json data
sre_df = pd.DataFrame(sre_data)

# Generate Pie Chart from the 'Results' field in result.json
result_counts = result_df.groupby('Experiment')['Results'].count()
plt.figure(figsize=(6, 6))  # Ensure square figure for the pie chart
plt.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', 
        colors=['#ff6666', '#66b3ff', '#99ff99'], startangle=90)

plt.title('WEB', fontweight='bold')

# Position the legend to the upper right outside the pie chart
plt.legend(result_counts.index, title="Experiment", loc="upper left", bbox_to_anchor=(1, 1))

# Ensure the pie chart is a perfect circle
plt.axis('equal')

# Save the pie chart as an image
plt.savefig('/home/ec2-user/python/pie_chart.png', bbox_inches="tight")
plt.close()

# Generate PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SRE CHAOS SUMMARY REPORT', 0, 1, 'C')
        self.ln(10)

    def add_table(self, sre_data):
        self.set_font('Arial', 'B', 12)
        # Set table columns (Key-Value like structure)
        for row in sre_data:
            self.cell(90, 10, row["Requirments"], 1, 0, 'L')
            self.set_font('Arial', '', 12)
            self.cell(90, 10, row["Details"], 1, 1, 'L')
            self.set_font('Arial', 'B', 12)

    def add_results_heading(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chaos Test Results:', 0, 1)
        self.ln(10)

    def add_pie_chart(self):
        # Ensure the image has equal width and height to maintain circular shape
        self.image('/home/ec2-user/python/pie_chart.png', x=50, y=None, w=120, h=120)

# Create PDF
pdf = PDF()

# Add a page and the report title
pdf.add_page()

# Add the SRE Chaos Summary table
pdf.add_table(sre_data)

# Add the results section heading and pie chart
pdf.add_page()  # Create a new page for the results
pdf.add_results_heading()
pdf.add_pie_chart()

# Save the PDF
pdf_output_path = '/home/ec2-user/python/Chaos_SRE_Report_Full.pdf'
pdf.output(pdf_output_path)

print(f"PDF report saved as {pdf_output_path}")

