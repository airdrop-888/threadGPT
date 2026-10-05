"""
Create a pre-formatted Excel template for scheduling
Run this to generate schedule_template.xlsx with colors and formatting
"""

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    
    print("Creating formatted Excel template...")
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"
    
    # Headers
    headers = ['date', 'time', 'content', 'media', 'hashtags']
    ws.append(headers)
    
    # Format header row
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Add example data
    examples = [
        ['2024-10-07', '09:00', 'Good morning! Starting the week strong!', '', 'motivation monday'],
        ['2024-10-07', '19:00', 'Evening update: Progress over perfection!', '', 'motivation'],
        ['2024-10-08', '12:00', 'Lunch break tips: Stay productive!', '', 'productivity'],
    ]
    
    for row in examples:
        ws.append(row)
    
    # Set column widths
    ws.column_dimensions['A'].width = 12  # date
    ws.column_dimensions['B'].width = 8   # time
    ws.column_dimensions['C'].width = 50  # content
    ws.column_dimensions['D'].width = 20  # media
    ws.column_dimensions['E'].width = 20  # hashtags
    
    # Wrap text for content column
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    
    # Freeze header row
    ws.freeze_panes = 'A2'
    
    # Save
    filename = 'schedule_template.xlsx'
    wb.save(filename)
    
    print(f"✓ Created: {filename}")
    print("\nOpen this file in Excel:")
    print("- Header is blue with white text")
    print("- Columns are sized properly")
    print("- Content wraps automatically")
    print("- Header row is frozen")
    print("\nJust fill in your content and Save As CSV!")
    
except ImportError:
    print("openpyxl not installed.")
    print("\nTo create formatted Excel templates:")
    print("  pip install openpyxl")
    print("\nOr just use schedule.example.csv and format manually in Excel!")
    print("See EXCEL_TEMPLATE_GUIDE.md for formatting instructions.")

