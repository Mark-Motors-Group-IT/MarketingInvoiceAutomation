# Mark Motors Group - Marketing Invoice Automation

This application streamlines reviewing, stamping, and organizing Marketing receipt and invoice PDFs. It automatically assigns accounting details, stamps the invoice with GL codes and descriptions, and moves files into the correct dealership network folders.

## How to Run
1. Double-click **`RunMarketingStamper.bat`** (it will handle Python virtual environment and dependencies setup automatically).
2. A window will appear. Select the **Invoice Month** from the network folder (`J:\Accounting Marketing\2026`) and click **Open**.

## Folder Structure
For the selected month (e.g., `J:\Accounting Marketing\2026\09_September`), the app expects/creates:
- **`Pending\`**: Drop raw invoice PDFs here.
- **`Original\`**: Unstamped original invoices are automatically archived here.
- **`Locations\`**: Stamped and renamed invoices are automatically saved inside their corresponding dealership subfolders:
  - `Alfa-Mas`
  - `Audi City Ottawa`
  - `Audi Ottawa`
  - `Audi West Ottawa`
  - `Cornwall Centre Volkswagen`
  - `INEOS`
  - `JLR`
  - `Mercedes-Benz`
  - `MMG`
  - `Porsche`
  - `Split`
  - `Volkswagen de l'Outaouais`

## How to Use
1. **View PDF**: Scroll through the invoice preview on the left.
2. **Fill Details**: Select the **Location**, **Account**, and **Source**. The GL Code and Description will auto-populate based on the marketing matrix.
3. **Rename Option**: Customize the **Charge Description (Filename)** if needed. The output file is saved as `[YYYY-MM-DD] - [Charge Description].pdf`.
4. **Process**: Click **✓ Process & Next** to stamp the PDF, file it into the location folder, archive the original, and load the next invoice.
