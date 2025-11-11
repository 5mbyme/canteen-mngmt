import os
import re
from collections import Counter
import math


# Define operators and keywords for JavaScript/React-like code
JS_OPERATORS = set([
    "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", ">", "<", ">=", "<=", 
    "&&", "||", "!", "++", "--", "?", ":", "::", ".", ",", ";", "(", ")", "{", "}", "[", "]",
    "=>"
])


JS_KEYWORDS = set([
    "if", "else", "for", "while", "switch", "case", "break", "continue",
    "function", "return", "const", "let", "var", "class", "new",
    "try", "catch", "finally", "throw", "async", "await", "import", "from", "export"
])


# Regex patterns
PATTERN_IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
PATTERN_FUNCTION_CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
PATTERN_STRING_LITERAL = re.compile(r"\".*?\"|'.*?'")
PATTERN_COMMENT = re.compile(r"\/\*.*?\*\/|\/\/.*?$", re.DOTALL | re.MULTILINE)


def parse_code(content):
    content_no_comments = PATTERN_COMMENT.sub("", content)
    content_no_strings = PATTERN_STRING_LITERAL.sub("", content_no_comments)
    func_calls = PATTERN_FUNCTION_CALL.findall(content_no_strings)
    
    operators = list(func_calls)
    for kw in JS_KEYWORDS:
        operators.extend(re.findall(r"\b" + re.escape(kw) + r"\b", content_no_strings))
    for op in JS_OPERATORS:
        operators.extend(re.findall(re.escape(op), content_no_strings))
    
    identifiers = PATTERN_IDENTIFIER.findall(content_no_strings)
    operands = [id for id in identifiers if id not in JS_KEYWORDS and id not in func_calls]
    
    return operators, operands


def scan_specific_files(dir_path):
    """Scan only the specific source files, ignore node_modules and other folders"""
    all_operators = []
    all_operands = []
    
    # List of specific files to scan
    source_files = [
        "src/App.css",
        "src/App.js",
        "src/App.test.js",
        "src/AuthContext.js",
        "src/firebase.js",
        "src/index.css",
        "src/index.js",
        "src/AdminPanel/AddProduct.js",
        "src/AdminPanel/AdminPanel.js",
        "src/AdminPanel/BestSellersComponent.js",
        "src/AdminPanel/ChartComponent.js",
        "src/AdminPanel/OrderHistory.js",
        "src/AdminPanel/SummaryComponent.js",
        "src/AdminPanel/UpdateQuantity.js",
        "src/Auth/Login.js",
        "src/Auth/SignUp.js",
        "src/Components/CartModal.css",
        "src/Components/CartModal.js",
        "src/Components/Footer.js",
        "src/Components/Home.js",
        "src/Components/UserOrderHistory.js",
        "src/Components/ProductDetailModal.js",
        "src/Components/ProductList.js",
        "src/Components/ProductList.css",
        "src/hooks/useAdmin.js",
        "src/hooks/useProducts.js",
        "tests/App.test.js",
        "tests/AuthContext.test.js",
        "tests/functional-test.js"
    ]
    
    for file_path in source_files:
        full_path = os.path.join(dir_path, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8", errors='ignore') as f:
                    content = f.read()
                    ops, oprs = parse_code(content)
                    all_operators.extend(ops)
                    all_operands.extend(oprs)
                    print(f"✓ Scanned: {file_path}")
            except Exception as e:
                print(f"✗ Error reading {file_path}: {e}")
        else:
            print(f"⚠ File not found: {file_path}")
    
    return all_operators, all_operands


def calculate_halstead_metrics(operators, operands):
    unique_operators = set(operators)
    unique_operands = set(operands)
    
    n1 = len(unique_operators)
    n2 = len(unique_operands)
    N1 = len(operators)
    N2 = len(operands)
    
    vocabulary = n1 + n2
    length = N1 + N2
    
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = difficulty * volume
    time_sec = effort / 18
    estimated_bugs = (volume ** (2/3)) / 3000 if volume > 0 else 0
    
    return {
        'Unique Operators (n1)': n1,
        'Unique Operands (n2)': n2,
        'Total Operators (N1)': N1,
        'Total Operands (N2)': N2,
        'Program Vocabulary': vocabulary,
        'Program Length': length,
        'Volume': volume,
        'Difficulty': difficulty,
        'Effort': effort,
        'Time (seconds)': time_sec,
        'Estimated Bugs': estimated_bugs
    }


def print_metrics(metrics):
    print("\n===== Halstead Metrics Report =====\n")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    print("\n==================================\n")


def main():
    project_root = '.'  # Change if needed
    print(f"Scanning specific source files from: {os.path.abspath(project_root)}\n")
    operators, operands = scan_specific_files(project_root)
    
    if operators or operands:
        print(f"\nTotal operator occurrences found: {len(operators)}")
        print(f"Total operand occurrences found: {len(operands)}")
        
        metrics = calculate_halstead_metrics(operators, operands)
        print_metrics(metrics)
    else:
        print("No code found to analyze!")


if __name__ == "__main__":
    main()
