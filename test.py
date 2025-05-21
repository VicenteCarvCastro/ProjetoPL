"""
Test module for the Pascal compiler
"""

import sys
from lex import lexer
from parser import parser
from CodeGenerator import CodeGenerator

def test_compiler(source_code, output_file="output.asm", verbose=True):
    """
    Test the compiler with given source code
    
    Args:
        source_code (str): Pascal source code
        output_file (str): Output assembly file path
        verbose (bool): Whether to print detailed output
    
    Returns:
        bool: True if compilation succeeded, False otherwise
    """
    try:
        if verbose:
            print("Starting parsing...")
        
        # Parse the source code
        parser.success = True
        ast = parser.parse(source_code, lexer=lexer)
        
        if not parser.success:
            print("Parsing failed")
            return False
        
        if verbose:
            print("Parsing completed")
            print("AST:", ast)
        
        # Generate assembly code
        if verbose:
            print("Generating assembly code...")
        
        generator = CodeGenerator()
        assembly_code = generator.generate(ast)
        
        # Write to output file
        with open(output_file, "w") as f:
            f.write(assembly_code)
        
        if verbose:
            print(f"Compilation successful! Output written to {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Compilation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test.py <input.pas> [output.asm]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.asm"
    
    try:
        with open(input_file, "r") as f:
            source_code = f.read()
        
        success = test_compiler(source_code, output_file)
        sys.exit(0 if success else 1)
        
    except FileNotFoundError:
        print(f"Could not open input file: {input_file}")
        sys.exit(1)