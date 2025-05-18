import csv
import os
from datetime import datetime

def read_schedule_data(csv_file):
    schools = []
    headers = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Read headers (first row)
        headers = next(reader)[1:]  # Skip first empty cell
        
        # Read each school's schedule
        for row in reader:
            if not row:  # Skip empty rows
                continue
                
            school_name = row[0]
            events = []
            
            # Process each event time for this school
            for i, time in enumerate(row[1:], 1):
                if time != 'x':  # Skip events marked with 'x'
                    events.append((headers[i-1], time))
            
            # Sort events by time
            events.sort(key=lambda x: x[1])
            
            schools.append({
                'name': school_name,
                'schedule': events
            })
    
    return headers, schools

def generate_latex_document(school_name, schedule, headers):
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
    for event, time in schedule:
        doc.append(f'{event} & {time} \\\\')
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
    headers, schools = read_schedule_data('roboday.csv')
    
    # Generate LaTeX document for each school
    for school in schools:
        school_name = school['name'].split(',')[0]  # Get just the school name
        latex_content = generate_latex_document(school_name, school['schedule'], headers)
        
        # Save LaTeX file
        filename = f'output/{school_name.replace(" ", "_")}_schedule.tex'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f'Generated schedule for {school_name}')

if __name__ == '__main__':
    main()
