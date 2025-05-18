import os
import subprocess
import shutil
from pathlib import Path

def compile_tex_files():
    # Get the output directory path
    output_dir = Path('output')
    pdf_dir = Path('pdf')
    
    # Check if output directory exists
    if not output_dir.exists():
        print("Error: output directory not found!")
        return
    
    # Create pdf directory if it doesn't exist
    pdf_dir.mkdir(exist_ok=True)
    
    # Get all .tex files in the output directory
    tex_files = list(output_dir.glob('*.tex'))
    
    if not tex_files:
        print("No .tex files found in the output directory!")
        return
    
    print(f"Found {len(tex_files)} .tex files to compile...")
    
    # Compile each .tex file
    for tex_file in tex_files:
        print(f"\nCompiling {tex_file.name}...")
        try:
            # Run pdflatex twice to ensure proper compilation of references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', 
                     '-interaction=nonstopmode',
                     '-output-directory=output',
                     str(tex_file)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"Error compiling {tex_file.name}:")
                    print(result.stderr)
                    break
            
            # Move the PDF to the pdf directory
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists():
                shutil.move(str(pdf_file), str(pdf_dir / pdf_file.name))
                print(f"Moved {pdf_file.name} to pdf directory")
            
            # Clean up auxiliary files
            aux_file = tex_file.with_suffix('.aux')
            log_file = tex_file.with_suffix('.log')
            if aux_file.exists():
                aux_file.unlink()
            if log_file.exists():
                log_file.unlink()
                
            print(f"Successfully compiled {tex_file.name}")
            
        except Exception as e:
            print(f"Error processing {tex_file.name}: {str(e)}")
    
    print("\nCompilation complete! All PDFs have been moved to the pdf directory.")

if __name__ == '__main__':
    compile_tex_files()
