import os
import re

# List of specific files to scan
SOURCE_FILES = [
    "src/App.css",
    "src/App.js",
    "src/App.test.js",
    "src/AuthContext.js",
    "src/firebase.js",
    "src/index.css",
    "src/index.js",
    "src/logo.svg",
    "src/reportWebVitals.js",
    "src/setupTests.js",
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

def count_lines_of_code_and_metrics(content):
    lines = content.split('\n')
    loc = 0
    comment_lines = 0
    blank_lines = 0
    in_multiline_comment = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
            continue
        if "/*" in stripped:
            in_multiline_comment = True
            comment_lines += 1
        if "*/" in stripped:
            in_multiline_comment = False
            comment_lines += 1
            continue
        if in_multiline_comment:
            comment_lines += 1
            continue
        if stripped.startswith("//"):
            comment_lines += 1
            continue
        loc += 1
    classes = len(re.findall(r"\bclass\s+[A-Za-z_][A-Za-z0-9_]*", content))
    functions = len(re.findall(r"\bfunction\s+[A-Za-z_][A-Za-z0-9_]*|\([^)]*\)\s*=>", content))
    return loc, comment_lines, blank_lines, classes, functions

def calculate_live_variables(content):
    declared_vars = set()
    var_patterns = [
        r"\bconst\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\blet\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"\bvar\s+([A-Za-z_][A-Za-z0-9_]*)"
    ]
    for pattern in var_patterns:
        matches = re.findall(pattern, content)
        declared_vars.update(matches)
    used_patterns = [
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*[+\-*/=<>!&|]",
        r"return\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"console\.log\(([A-Za-z_][A-Za-z0-9_]*)"
    ]
    used_vars = set()
    for pattern in used_patterns:
        matches = re.findall(pattern, content)
        used_vars.update(matches)
    live_vars = declared_vars & used_vars
    return len(live_vars)

def calculate_information_flow(content):
    function_calls = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", content)
    fan_out = len(set(function_calls))
    function_defs = re.findall(r"\bfunction\s+([A-Za-z_][A-Za-z0-9_]*)", content)
    arrow_funcs = re.findall(r"\bconst\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(.*?\)\s*=>", content)
    fan_in = len(set(function_defs) | set(arrow_funcs))
    info_flow_metric = fan_in * fan_out if fan_in > 0 and fan_out > 0 else max(fan_in, fan_out)
    return fan_in, fan_out, info_flow_metric

def scan_specific_files(dir_path):
    metrics_size = []
    metrics_live_vars = []
    metrics_info_flow = []
    for file_path in SOURCE_FILES:
        full_path = os.path.join(dir_path, file_path)
        # Defaults if file not found
        data_size = (file_path, 0, 0, 0, 0, 0)
        data_live = (file_path, 0)
        data_info = (file_path, 0, 0, 0)
        if os.path.exists(full_path):
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    loc, comment_lines, blank_lines, classes, functions = count_lines_of_code_and_metrics(content)
                    live_vars = calculate_live_variables(content)
                    fan_in, fan_out, ifm = calculate_information_flow(content)
                    data_size = (file_path, loc, comment_lines, blank_lines, classes, functions)
                    data_live = (file_path, live_vars)
                    data_info = (file_path, fan_in, fan_out, ifm)
                    print(f"✓ Scanned: {file_path}")
            except Exception as e:
                print(f"✗ Error reading {file_path}: {e}")
        else:
            print(f"⚠ File not found: {file_path}")
        metrics_size.append(data_size)
        metrics_live_vars.append(data_live)
        metrics_info_flow.append(data_info)
    return metrics_size, metrics_live_vars, metrics_info_flow

def print_size_metrics(metrics):
    print("\n" + "=" * 110)
    print(" Size Metrics (Lines of Code, Comments, Blank Lines, Classes, Methods/Functions) ")
    print("=" * 110)
    print(f"{'File':<40} {'LOC':>8} {'Comments':>10} {'Blank':>8} {'Classes':>10} {'Methods':>10}")
    print("=" * 110)
    total_loc = 0
    total_comments = 0
    total_blank = 0
    total_classes = 0
    total_methods = 0
    for file_path, loc, comments, blank, classes, methods in metrics:
        print(f"{file_path:<40} {loc:>8} {comments:>10} {blank:>8} {classes:>10} {methods:>10}")
        total_loc += loc
        total_comments += comments
        total_blank += blank
        total_classes += classes
        total_methods += methods
    print("=" * 110)
    print(f"{'TOTAL':<40} {total_loc:>8} {total_comments:>10} {total_blank:>8} {total_classes:>10} {total_methods:>10}")
    print("=" * 110)
    print()

def print_live_variable_metrics(metrics):
    print("\n" + "=" * 80)
    print(" Live Variable Metrics ")
    print("=" * 80)
    print(f"{'File':<40} {'Live Variable Count':>30}")
    print("=" * 80)
    total_live_vars = 0
    for file_path, live_vars in metrics:
        print(f"{file_path:<40} {live_vars:>30}")
        total_live_vars += live_vars
    print("=" * 80)
    print(f"{'TOTAL':<40} {total_live_vars:>30}")
    print("=" * 80)
    print()

def print_information_flow_metrics(metrics):
    print("\n" + "=" * 100)
    print(" Information Flow Metrics ")
    print("=" * 100)
    print(f"{'File':<40} {'Fan-In':>10} {'Fan-Out':>10} {'InfoFlow (F^2)':>20}")
    print("=" * 100)
    total_fan_in = 0
    total_fan_out = 0
    total_info_flow = 0
    for file_path, fan_in, fan_out, ifm in metrics:
        print(f"{file_path:<40} {fan_in:>10} {fan_out:>10} {ifm:>20}")
        total_fan_in += fan_in
        total_fan_out += fan_out
        total_info_flow += ifm
    print("=" * 100)
    print(f"{'TOTAL':<40} {total_fan_in:>10} {total_fan_out:>10} {total_info_flow:>20}")
    print("=" * 100)
    print()

def main():
    project_root = "."  # Change if needed
    print(f"\nScanning specific source files from: {os.path.abspath(project_root)}\n")
    size_metrics, live_vars_metrics, info_flow_metrics = scan_specific_files(project_root)
    print_size_metrics(size_metrics)
    print_live_variable_metrics(live_vars_metrics)
    print_information_flow_metrics(info_flow_metrics)

if __name__ == "__main__":
    main()
