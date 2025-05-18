import csv
import os
from datetime import datetime
import pandas as pd

def read_schedule_data(excel_file):
    # Read Excel file, skipping first 3 rows
    df = pd.read_excel(excel_file, skiprows=3)
    
    # Get event names from the first row (4th row in Excel)
    events = df.columns[1:].tolist()  # Skip first column (school names)
    
    schools = []
    
    # Process each row (school)
    for _, row in df.iterrows():
        school_name = row[0]  # First column contains school name
        schedule = []
        
        # Process each event time for this school
        for event, time in zip(events, row[1:]):
            # Skip if event name is 'x' or time is 'x' or NaN
            if (str(event).lower() != 'x' and 
                pd.notna(time) and 
                str(time).lower() != 'x'):
                schedule.append({
                    'event_name': event,
                    'time': str(time)
                })
        
        schools.append({
            'name': school_name,
            'schedule': schedule
        })
    
    return schools

def generate_latex_document(school_name, schedule):
    # Create LaTeX document
    doc = []
    doc.append(r'\documentclass{article}')
    doc.append(r'\usepackage[utf8]{inputenc}')
    doc.append(r'\usepackage{polski}')
    doc.append(r'\usepackage{geometry}')
    doc.append(r'\geometry{a4paper, margin=1in}')
    doc.append(r'\begin{document}')
    
    # Title
    doc.append(r'\begin{center}')
    doc.append(r'\Large\textbf{Harmonogram RoboDay}')
    doc.append(f'\\large\\textbf{{{school_name}}}')
    doc.append(r'\end{center}')
    doc.append(r'\vspace{1cm}')
    
    # Schedule table
    doc.append(r'\begin{center}')
    doc.append(r'\begin{tabular}{|l|l|}')
    doc.append(r'\hline')
    doc.append(r'\textbf{Wydarzenie} & \textbf{Godzina} \\')
    doc.append(r'\hline')
    
    # Add schedule entries
    for event in schedule:
        doc.append(f'{event["event_name"]} & {event["time"]} \\\\')
        doc.append(r'\hline')
    
    doc.append(r'\end{tabular}')
    doc.append(r'\end{center}')
    
    doc.append(r'\end{document}')
    return '\n'.join(doc)

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Read schedule data
    schools = read_schedule_data('roboday.xlsx')
    
    # Generate LaTeX document for each school
    for school in schools:
        school_name = school['name'].split(',')[0]  # Get just the school name
        latex_content = generate_latex_document(school_name, school['schedule'])    
        
        # Save LaTeX file
        filename = f'output/{school_name.replace(" ", "_")}_schedule.tex'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f'Generated schedule for {school_name}')

if __name__ == '__main__':
    main()
