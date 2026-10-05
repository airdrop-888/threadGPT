"""
Create a pre-formatted Excel template for scheduling
Run this to generate schedule_template.xlsx with colors and formatting
"""

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    
    print("="*60)
    print("ThreadsGPT - Excel Template Generator")
    print("="*60)
    print("\nCreating formatted Excel template...")
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Posts Schedule"
    
    # Headers with format hints
    headers = [
        'date\n(YYYY-MM-DD)',   # e.g. 2024-10-07
        'time\n(HH:MM)',        # e.g. 19:00
        'content',
        'media\n(images/foto.jpg)',
        'hashtags\n(space separated)'
    ]
    ws.append(headers)
    
    # Format header row - Professional blue theme
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12, name='Calibri')
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Border style
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    
    # Add example data with formatting
    examples = [
        ['2024-10-07', '09:00', 'Good morning! Starting the week with positive energy!', '', 'motivation monday'],
        ['2024-10-07', '12:00', 'Lunch break thoughts: Always keep learning and growing', '', ''],
        ['2024-10-07', '19:00', 'Evening reminder: Small progress is still progress!', '', 'motivation'],
        ['2024-10-08', '09:00', 'Tech Tuesday: AI is changing everything! What do you think?', 'image.jpg', 'AI tech'],
        ['2024-10-08', '12:00', 'Quick tip: Automate repetitive tasks to save time', '', 'productivity'],
        ['2024-10-09', '09:00', 'Wednesday wisdom: Consistency beats perfection', '', 'wisdom'],
        ['2024-10-10', '09:00', 'Throwback Thursday: Remember when we started?', '', 'throwback'],
        ['2024-10-11', '09:00', 'Friday motivation: Finish strong!', '', 'friday motivation'],
    ]
    
    for row in examples:
        ws.append(row)
    
    # Set column widths for better readability
    ws.column_dimensions['A'].width = 13  # date
    ws.column_dimensions['B'].width = 8   # time
    ws.column_dimensions['C'].width = 55  # content (wider for better reading)
    ws.column_dimensions['D'].width = 20  # media
    ws.column_dimensions['E'].width = 25  # hashtags
    
    # Format data rows
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = thin_border
            
            # Center align date and time columns
            if cell.column in [1, 2]:  # A and B columns
                cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Set row heights
    ws.row_dimensions[1].height = 42  # Header taller so format hint is visible
    for row_num in range(2, ws.max_row + 1):
        ws.row_dimensions[row_num].height = 30  # Data rows

    # Data Validation: time column (B) - dropdown of common times
    from openpyxl.worksheet.datavalidation import DataValidation
    time_dv = DataValidation(
        type="list",
        formula1='"06:00,07:00,08:00,09:00,10:00,11:00,12:00,13:00,14:00,15:00,16:00,17:00,18:00,19:00,20:00,21:00,22:00,23:00"',
        allow_blank=True,
        showDropDown=False,
        showErrorMessage=True,
        errorTitle='Format Salah',
        error='Gunakan format HH:MM (contoh: 19:00)',
        showInputMessage=True,
        promptTitle='Format Waktu',
        prompt='Pilih dari dropdown atau ketik HH:MM (24 jam)\nContoh: 09:00, 19:00'
    )
    ws.add_data_validation(time_dv)
    time_dv.sqref = 'B2:B1000'

    # Data Validation: date column (A) - show format hint
    date_dv = DataValidation(
        type="date",
        allow_blank=True,
        showErrorMessage=True,
        errorTitle='Format Salah',
        error='Gunakan format YYYY-MM-DD (contoh: 2024-10-07)',
        showInputMessage=True,
        promptTitle='Format Tanggal',
        prompt='Ketik tanggal dengan format:\nYYYY-MM-DD\nContoh: 2024-10-07'
    )
    ws.add_data_validation(date_dv)
    date_dv.sqref = 'A2:A1000'
    
    # Freeze header row
    ws.freeze_panes = 'A2'
    
    # Add instruction sheet
    ws_instructions = wb.create_sheet("Instructions")
    ws_instructions.column_dimensions['A'].width = 80
    
    instructions_text = [
        ["ThreadsGPT - Schedule Template Instructions"],
        [""],
        ["HOW TO USE:"],
        ["1. Fill in your posts in the 'Posts Schedule' sheet"],
        ["2. Save this file (keep as .xlsx)"],
        ["3. Run: python bulk_schedule.py schedule_template.xlsx"],
        [""],
        ["COLUMN GUIDE:"],
        ["- date: Use format YYYY-MM-DD (e.g., 2024-10-07)"],
        ["- time: Use format HH:MM in 24-hour (e.g., 19:00 for 7 PM)"],
        ["- content: Your post text (up to 500 characters)"],
        ["- media: Filename or path to image/video (optional)"],
        ["- hashtags: Space-separated hashtags without # (optional)"],
        [""],
        ["TIPS:"],
        ["- Best posting times: 09:00, 12:00, 19:00, 21:00"],
        ["- Keep content between 100-280 characters for best engagement"],
        ["- Use 1-3 relevant hashtags per post"],
        ["- Add emojis in content for better engagement"],
        [""],
        ["FORMATTING:"],
        ["- You can add more rows as needed"],
        ["- You can use Excel formulas (e.g., =A2+1 for next day)"],
        ["- Sort and filter your posts as needed"],
        ["- Color code rows: Green=ready, Yellow=review, Red=draft"],
    ]
    
    for row in instructions_text:
        ws_instructions.append(row)
    
    # Format instructions
    for cell in ws_instructions['A']:
        if cell.value and cell.value.isupper() and ":" in str(cell.value):
            cell.font = Font(bold=True, size=12, color="4472C4")
        else:
            cell.font = Font(size=11)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    
    # Save
    filename = 'schedule_template.xlsx'
    wb.save(filename)
    
    print(f"\n[OK] Created: {filename}")
    print("\n" + "="*60)
    print("Template Features:")
    print("="*60)
    print("- Blue header with white text")
    print("- Columns sized for easy reading")
    print("- Text wrapping enabled")
    print("- Borders for clarity")
    print("- Header row frozen")
    print("- 8 example posts included")
    print("- Instructions sheet included")
    print("\n" + "="*60)
    print("How to Use:")
    print("="*60)
    print("1. Open schedule_template.xlsx in Excel")
    print("2. Edit/add your content (keep format!)")
    print("3. Save the file")
    print("4. Run: python bulk_schedule.py schedule_template.xlsx")
    print("\nTIP: You can also 'Save As' with a new name to keep template!")
    
except ImportError:
    print("\n[ERROR] openpyxl not installed!")
    print("\nTo create formatted Excel templates:")
    print("  pip install openpyxl")
    print("\nOr just use schedule.example.csv and format manually in Excel!")
except Exception as e:
    print(f"\n[ERROR] Failed to create template: {e}")

