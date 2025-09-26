import streamlit as st
from lexer import tokenize
from parser import parse
from semantic import semantic_check
from intermediate import generate_code
from optimizer import optimize
from codegen import generate_target
from utils import build_tree
from PIL import Image
import os
import tempfile

# Configure page
st.set_page_config(
    page_title="Compiler Phase Visualizer",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .phase-header {
        font-size: 1.5rem;
        color: #2e8b57;
        border-left: 4px solid #2e8b57;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .code-output {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 1rem;
        font-family: 'Courier New', monospace;
    }
    .error-message {
        color: #dc3545;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #155724;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

def display_output(title, content, color_class="code-output"):
    """Helper function to display output with consistent formatting"""
    st.markdown(f'<div class="phase-header">{title}</div>', unsafe_allow_html=True)
    
    if isinstance(content, list):
        if not content:
            content = ["No output generated."]
        content_str = "\n".join(str(line) for line in content)
    else:
        content_str = str(content) if content else "No output generated."
    
    st.code(content_str, language="text")

def visualize_compiler_phases(code):
    """Main function to process code through all compiler phases"""
    
    # Initialize session state for results
    if 'results' not in st.session_state:
        st.session_state.results = {}
    
    try:
        # Phase 1: Lexical Analysis
        st.markdown('<div class="phase-header">🔤 Lexical Analysis (Tokenization)</div>', unsafe_allow_html=True)
        with st.spinner("Tokenizing input..."):
            tokens = tokenize(code)
            st.session_state.results['tokens'] = tokens
            
            if tokens:
                st.code("\n".join(str(token) for token in tokens), language="text")
                st.success(f"✅ Generated {len(tokens)} tokens successfully")
            else:
                st.warning("⚠️ No tokens generated")
        
        # Phase 2: Parsing
        st.markdown('<div class="phase-header">🌳 Syntax Analysis (Parsing)</div>', unsafe_allow_html=True)
        with st.spinner("Parsing tokens..."):
            ast = parse(code)
            
            if ast is None:
                st.error("❌ Syntax Error: Could not parse the input code")
                st.session_state.results['ast'] = None
                return  # Stop further processing
            
            st.session_state.results['ast'] = ast
            st.success("✅ Abstract Syntax Tree (AST) generated successfully")
            
            # Generate and display parse tree visualization
            try:
                tree = build_tree(ast)
                
                # Use temporary directory for file operations
                with tempfile.TemporaryDirectory() as temp_dir:
                    tree_path = os.path.join(temp_dir, "ast")
                    tree.render(tree_path, format="png", cleanup=True)
                    
                    image_path = tree_path + ".png"
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        
                        # Create columns for centering the image
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.image(image, caption="Abstract Syntax Tree", use_container_width=True)
                    else:
                        st.warning("⚠️ Could not generate tree visualization")
                        
            except Exception as e:
                st.warning(f"⚠️ Tree visualization failed: {str(e)}")
        
        # Phase 3: Semantic Analysis
        st.markdown('<div class="phase-header">🔍 Semantic Analysis</div>', unsafe_allow_html=True)
        with st.spinner("Performing semantic analysis..."):
            sem_errors = semantic_check(ast)
            st.session_state.results['semantic'] = sem_errors
            
            if sem_errors:
                st.code("\n".join(str(error) for error in sem_errors), language="text")
                st.error(f"❌ Found {len(sem_errors)} semantic error(s)")
            else:
                st.success("✅ No semantic errors found")
        
        # Phase 4: Intermediate Code Generation
        st.markdown('<div class="phase-header">⚙️ Intermediate Code Generation</div>', unsafe_allow_html=True)
        with st.spinner("Generating intermediate code..."):
            ic = generate_code(ast)
            st.session_state.results['intermediate'] = ic
            
            if ic:
                st.code("\n".join(str(line) for line in ic), language="text")
                st.success(f"✅ Generated {len(ic)} lines of intermediate code")
            else:
                st.warning("⚠️ No intermediate code generated")
        
        # Phase 5: Code Optimization
        st.markdown('<div class="phase-header">🚀 Code Optimization</div>', unsafe_allow_html=True)
        with st.spinner("Optimizing code..."):
            opt = optimize(ic)
            st.session_state.results['optimized'] = opt
            
            if opt:
                st.code("\n".join(str(line) for line in opt), language="text")
                
                # Show optimization statistics
                original_lines = len(ic) if ic else 0
                optimized_lines = len(opt)
                if original_lines > optimized_lines:
                    st.success(f"✅ Optimized! Reduced from {original_lines} to {optimized_lines} lines")
                elif original_lines == optimized_lines:
                    st.info(f"ℹ️ No optimizations applied ({optimized_lines} lines)")
                else:
                    st.info(f"ℹ️ Code expanded to {optimized_lines} lines after optimization")
            else:
                st.warning("⚠️ No optimized code generated")
        
        # Phase 6: Target Code Generation
        st.markdown('<div class="phase-header">💻 Target Code Generation</div>', unsafe_allow_html=True)
        with st.spinner("Generating target code..."):
            target = generate_target(opt)
            st.session_state.results['target'] = target
            
            if target:
                st.code("\n".join(str(line) for line in target), language="asm")
                st.success(f"✅ Generated {len(target)} lines of target code")
            else:
                st.warning("⚠️ No target code generated")
                
    except Exception as e:
        st.error(f"❌ An error occurred during compilation: {str(e)}")

def main():
    # Main header
    st.markdown('<h1 class="main-header">🔧 Compiler Phase Visualizer</h1>', unsafe_allow_html=True)
    
    # Sidebar for instructions and options
    with st.sidebar:
        st.markdown("## 📝 Instructions")
        st.markdown("""
        1. Enter your source code in the text area
        2. Click **Run Compiler** to process
        3. View results for each compilation phase
        
        **Compilation Phases:**
        - **Lexical Analysis**: Tokenization
        - **Syntax Analysis**: Parse tree generation
        - **Semantic Analysis**: Type checking & validation
        - **Intermediate Code**: Three-address code
        - **Optimization**: Code improvements
        - **Target Code**: Final assembly/machine code
        """)
        
        st.markdown("## ⚙️ Options")
        show_debug = st.checkbox("Show debug information", value=False)
        auto_run = st.checkbox("Auto-run on code change", value=False)
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📄 Source Code Input")
        
        # Sample code examples
        sample_codes = {
            "Empty": "",
            "Simple Declaration": "int x;\nint y;",
            "Simple Assignment": "int x;\nint y;\nx = 10;\ny = x + 5;",
            "If Statement": "int x;\nint y;\nif (x > 0) {\n    y = x * 2;\n} else {\n    y = 0;\n}",
            #"Loop Example": "int i;\nint sum = 0;\nfor (i = 0; i < 10; i++) {\n    sum = sum + i;\n}"
        }
        
        selected_sample = st.selectbox("Load sample code:", list(sample_codes.keys()))
        if st.button("Load Sample"):
            st.session_state.input_code = sample_codes[selected_sample]
        
        # Code input area
        input_code = st.text_area(
            "Enter your source code:",
            value=st.session_state.get('input_code', ''),
            height=200,
            help="Enter the source code you want to compile"
        )
        
        # Store code in session state
        st.session_state.input_code = input_code
        
        # Run button
        run_compiler = st.button("🚀 Run Compiler", type="primary")
        
        if auto_run and input_code.strip():
            run_compiler = True
    
    with col2:
        st.markdown("### 📊 Compilation Results")
        
        if run_compiler and input_code.strip():
            visualize_compiler_phases(input_code)
        elif run_compiler and not input_code.strip():
            st.warning("⚠️ Please enter some source code to compile")
        else:
            st.info("👆 Enter source code and click 'Run Compiler' to see results")
    
    # Results summary section
    if 'results' in st.session_state and st.session_state.results:
        st.markdown("---")
        st.markdown("## 📈 Compilation Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        results = st.session_state.results
        
        with col1:
            token_count = len(results.get('tokens', []))
            st.metric("Tokens Generated", token_count)
        
        with col2:
            semantic_errors = len(results.get('semantic', []))
            st.metric("Semantic Errors", semantic_errors)
        
        with col3:
            ic_lines = len(results.get('intermediate', []))
            st.metric("Intermediate Code Lines", ic_lines)
        
        with col4:
            target_lines = len(results.get('target', []))
            st.metric("Target Code Lines", target_lines)
    
    # Debug information
    if show_debug and 'results' in st.session_state:
        with st.expander("🐛 Debug Information"):
            st.json(st.session_state.results)

if __name__ == "__main__":
    main()