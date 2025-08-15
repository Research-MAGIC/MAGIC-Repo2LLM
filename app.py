#!/usr/bin/env python3
from nicegui import ui, run, app
import requests
import zipfile
import io
import ast
import json
import tiktoken
from datetime import datetime
import re

# --- MAGIC Research Brand Colors ---
BRAND_COLORS = {
    'primary': '#5B3AFF',  # Magic purple from logo
    'primary_dark': '#4A2FE5',
    'primary_light': '#7B5FFF',
    'accent': '#6B4FFF',
    'background': '#FFFFFF',
    'surface': '#F8F7FF',
    'text_primary': '#1A1A1A',
    'text_secondary': '#6B7280',
    'border': '#E5E5E5',
    'success': '#10B981',
    'error': '#EF4444',
    'warning': '#F59E0B'
}

# --- Custom CSS for MAGIC Research Branding ---
CUSTOM_CSS = '''
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    body {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #F8F7FF 0%, #FFFFFF 100%) !important;
        min-height: 100vh;
    }
    
    /* Custom sparkle animation for logo */
    @keyframes sparkle {
        0% { opacity: 0; transform: scale(0.8) rotate(0deg); }
        50% { opacity: 1; transform: scale(1.1) rotate(180deg); }
        100% { opacity: 0; transform: scale(0.8) rotate(360deg); }
    }
    
    .sparkle {
        animation: sparkle 3s ease-in-out infinite;
    }
    
    /* Card styling */
    .magic-card {
        background: white !important;
        border: 1px solid rgba(91, 58, 255, 0.1) !important;
        box-shadow: 0 4px 6px -1px rgba(91, 58, 255, 0.1), 0 2px 4px -1px rgba(91, 58, 255, 0.06) !important;
        transition: all 0.3s ease !important;
    }
    
    .magic-card:hover {
        box-shadow: 0 10px 15px -3px rgba(91, 58, 255, 0.15), 0 4px 6px -2px rgba(91, 58, 255, 0.08) !important;
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .magic-btn {
        background: linear-gradient(135deg, #5B3AFF 0%, #7B5FFF 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .magic-btn:hover {
        background: linear-gradient(135deg, #4A2FE5 0%, #6B4FFF 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(91, 58, 255, 0.3) !important;
    }
    
    .magic-btn:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.5s, height 0.5s;
    }
    
    .magic-btn:active:before {
        width: 300px;
        height: 300px;
    }
    
    /* Secondary button styling */
    .magic-btn-secondary {
        background: white !important;
        color: #5B3AFF !important;
        border: 2px solid #5B3AFF !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .magic-btn-secondary:hover {
        background: #F8F7FF !important;
        border-color: #4A2FE5 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(91, 58, 255, 0.2) !important;
    }
    
    /* Input styling */
    .q-field--outlined .q-field__control {
        border-color: #E5E5E5 !important;
    }
    
    .q-field--outlined .q-field__control:hover {
        border-color: #5B3AFF !important;
    }
    
    .q-field--outlined.q-field--focused .q-field__control {
        border-color: #5B3AFF !important;
        box-shadow: 0 0 0 3px rgba(91, 58, 255, 0.1) !important;
    }
    
    /* Log area styling */
    .magic-log {
        background: #F8F7FF !important;
        border: 1px solid rgba(91, 58, 255, 0.1) !important;
        border-radius: 8px !important;
        font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace !important;
    }
    
    /* Textarea styling */
    .magic-output {
        background: #F8F7FF !important;
        border: 1px solid rgba(91, 58, 255, 0.1) !important;
        border-radius: 8px !important;
        font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace !important;
    }
    
    /* Badge styling */
    .magic-badge {
        background: linear-gradient(135deg, #5B3AFF 0%, #7B5FFF 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* Header gradient */
    .magic-header {
        background: linear-gradient(135deg, #5B3AFF 0%, #7B5FFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Info badge */
    .info-badge {
        background: #E0E7FF;
        color: #5B3AFF;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
</style>
'''

# --- Core Helper Functions (Preserved from original script) ---

def is_file_type(file_path: str, file_extension: str) -> bool:
    """Check if the file has the specified file extension."""
    return file_path.endswith(file_extension)


def is_likely_useful_file(file_path: str, lang: str = "python") -> bool:
    """Determine if the file is likely to be useful by excluding common non-source directories and config files."""
    excluded_dirs = ["docs", "examples", "tests", "test", "scripts", "utils", "benchmarks"]
    utility_or_config_files = []
    github_workflow_or_docs = [".github", ".gitignore", "LICENSE"]

    if lang == "python":
        excluded_dirs.append("__pycache__")
        utility_or_config_files.extend(["hubconf.py", "setup.py"])
        github_workflow_or_docs.extend(["stale.py", "gen-card-", "write_model_card"])
    elif lang == "go":
        excluded_dirs.append("vendor")
        utility_or_config_files.extend(["go.mod", "go.sum", "Makefile"])

    if any(part.startswith(".") for part in file_path.split("/")):
        return False
    if "test" in file_path.lower():
        return False
    for excluded_dir in excluded_dirs:
        if f"/{excluded_dir}/" in file_path or file_path.startswith(excluded_dir + "/"):
            return False
    for file_name in utility_or_config_files:
        if file_name in file_path:
            return False
    for doc_file in github_workflow_or_docs:
        if doc_file in file_path:
            return False
    return True


def is_test_file(file_content: str, lang: str) -> bool:
    """Determine if the file content suggests it is a test file by checking for testing library imports."""
    test_indicators = {"python": ["unittest", "pytest"], "go": ["testing"]}.get(lang, [])

    if lang == "python":
        try:
            module = ast.parse(file_content)
            for node in ast.walk(module):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in test_indicators:
                            return True
                elif isinstance(node, ast.ImportFrom):
                    if node.module in test_indicators:
                        return True
        except SyntaxError:
            pass
    return False


# --- Token Calculation Function ---
def get_token_count(text: str) -> int:
    """Calculates the number of tokens in a string using the cl100k_base encoding."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text, disallowed_special=())
        return len(tokens)
    except Exception as e:
        print(f"Could not calculate tokens: {e}")
        return 0


# --- Helper function to extract repo name from URL ---
def get_repo_name_from_url(url: str) -> str:
    """Extract repository name from GitHub URL."""
    # Pattern to match GitHub URLs
    pattern = r'github\.com[/:]([^/]+)/([^/\.]+)'
    match = re.search(pattern, url)
    if match:
        owner = match.group(1)
        repo = match.group(2).replace('.git', '')
        return f"{owner}_{repo}"
    return "repository"


# --- Core Processing Logic (Adapted for UI Integration) ---

def download_and_process_repo(repo_url: str, branch_or_tag: str, log: ui.log) -> tuple[str | None, str]:
    """
    Downloads and processes files from a GitHub repository, logging progress to the UI.
    Returns a tuple of (concatenated content as string or None on failure, repository name).
    """
    repo_name = get_repo_name_from_url(repo_url)
    download_url = f"{repo_url}/archive/refs/heads/{branch_or_tag}.zip"
    lang = "python"

    log.push(f"🔄 Attempting to download from: {download_url}")
    try:
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.push(f"❌ Error: Failed to download the repository. {e}")
        return None, repo_name

    log.push("✅ Download successful. Processing files...")
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    
    # Add header with metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_contents = f"""# ========================================
# Repository: {repo_url}
# Branch/Tag: {branch_or_tag}
# Processed: {timestamp}
# Processed by: MAGIC-Repo2LLM
# ========================================

"""

    all_files = zip_file.namelist()
    log.push(f"📊 Found {len(all_files)} total files in the archive.")

    processed_count = 0
    for file_path in all_files:
        cleaned_path = "/".join(file_path.split('/')[1:])
        if not cleaned_path or file_path.endswith("/"):
            continue

        if not is_file_type(cleaned_path, ".py") or not is_likely_useful_file(cleaned_path, lang):
            continue

        try:
            file_content = zip_file.read(file_path).decode("utf-8")
        except (UnicodeDecodeError, Exception) as e:
            log.push(f"⚠️ Skipping (read/decode error): {cleaned_path} - {e}")
            continue

        if is_test_file(file_content, lang):
            log.push(f"🧪 Skipping (test file): {cleaned_path}")
            continue

        log.push(f"📄 Processing: {cleaned_path}")
        file_contents += f"# File: {cleaned_path}\n"
        file_contents += file_content
        file_contents += "\n\n"
        processed_count += 1

    log.push(f"✨ Processing complete. Processed {processed_count} files.")
    return file_contents, repo_name


# --- NiceGUI User Interface Definition ---

@ui.page('/')
def main_page():
    """Defines the layout and functionality of the web interface."""
    
    # Store processed content and filename globally for download
    processed_data = {'content': '', 'filename': ''}

    async def process_repository():
        """Handles the button click event to start processing the repository."""
        log.clear()
        output_area.set_value('')
        token_count_label.set_text('Calculating...')
        file_size_label.set_text('Calculating...')
        process_button.set_visibility(False)
        spinner.set_visibility(True)
        download_button.set_enabled(False)
        copy_button.set_enabled(False)

        repo_url = repo_input.value
        branch = branch_input.value

        if not repo_url:
            ui.notify('Repository URL cannot be empty.', type='negative')
            process_button.set_visibility(True)
            spinner.set_visibility(False)
            return

        content, repo_name = await run.io_bound(download_and_process_repo, repo_url, branch, log)

        process_button.set_visibility(True)
        spinner.set_visibility(False)

        if content is not None:
            output_area.set_value(content)
            
            # Calculate metrics
            num_tokens = get_token_count(content)
            file_size_kb = len(content.encode('utf-8')) / 1024
            
            token_count_label.set_text(f'{num_tokens:,}')
            file_size_label.set_text(f'{file_size_kb:.2f} KB')
            
            # Store processed data for download
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            processed_data['content'] = content
            processed_data['filename'] = f"{repo_name}_{branch}_{timestamp}.txt"
            
            # Enable action buttons
            download_button.set_enabled(True)
            copy_button.set_enabled(True)
            
            ui.notify(f'✨ Repository processed successfully! Ready to download as: {processed_data["filename"]}', 
                     type='positive', position='top', timeout=5000)
        else:
            ui.notify('Failed to process repository. Check log for details.', type='negative', position='top')

    async def copy_to_clipboard():
        """Copies the output text to the user's clipboard."""
        text = output_area.value
        if not text:
            ui.notify('There is no content to copy.', type='warning', position='top')
            return
        # Use ui.run_javascript properly for clipboard access
        js_code = f'''
            navigator.clipboard.writeText({json.dumps(text)}).then(
                () => console.log("Copied to clipboard"),
                (err) => console.error("Failed to copy:", err)
            );
        '''
        await ui.run_javascript(js_code)
        ui.notify('✅ Output copied to clipboard!', type='positive', position='top')

    def download_file():
        """Triggers download of the processed content as a text file."""
        if not processed_data['content']:
            ui.notify('No content to download. Please process a repository first.', type='warning', position='top')
            return
        
        # Create download using NiceGUI's download mechanism
        ui.download(
            processed_data['content'].encode('utf-8'), 
            processed_data['filename']
        )
        ui.notify(f'📥 Downloading: {processed_data["filename"]}', type='positive', position='top')

    # --- UI Layout ---
    
    # Add custom CSS
    ui.add_head_html(CUSTOM_CSS)
    
    with ui.column().classes('w-full items-center gap-6 mx-auto p-6'):
        # Header with MAGIC branding - CENTERED
        with ui.column().classes('items-center gap-2 mb-8 w-full'):
            # SVG Logo - Centered
            ui.html('''
                <div style="display: flex; justify-content: center; width: 100%;">
                    <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <g class="sparkle">
                            <path d="M50 10 L55 25 L70 20 L60 35 L75 40 L60 45 L70 60 L55 50 L50 65 L45 50 L30 60 L40 45 L25 40 L40 35 L30 20 L45 25 Z" 
                                  fill="url(#gradient1)" opacity="0.9"/>
                        </g>
                        <g style="animation-delay: 1s" class="sparkle">
                            <path d="M20 15 L22 20 L27 18 L24 23 L29 25 L24 27 L27 32 L22 29 L20 34 L18 29 L13 32 L16 27 L11 25 L16 23 L13 18 L18 20 Z" 
                                  fill="url(#gradient2)" opacity="0.7"/>
                        </g>
                        <g style="animation-delay: 2s" class="sparkle">
                            <path d="M75 65 L77 70 L82 68 L79 73 L84 75 L79 77 L82 82 L77 79 L75 84 L73 79 L68 82 L71 77 L66 75 L71 73 L68 68 L73 70 Z" 
                                  fill="url(#gradient2)" opacity="0.7"/>
                        </g>
                        <defs>
                            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#5B3AFF;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#7B5FFF;stop-opacity:1" />
                            </linearGradient>
                            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#6B4FFF;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#8B6FFF;stop-opacity:1" />
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
            ''')
            
            # Centered text
            ui.label('MAGIC Research').classes('text-4xl font-bold magic-header text-center')
            ui.label('Repo2LLM - GitHub to LLM Converter').classes('text-xl text-gray-600 text-center')

        ui.label('Transform any GitHub repository into a single file optimized for Large Language Model analysis').classes(
            'text-center text-gray-600 mb-4 max-w-2xl')

        # Main input card
        with ui.card().classes('w-full max-w-4xl magic-card p-6'):
            ui.label('Repository Configuration').classes('text-xl font-semibold mb-4').style(f'color: {BRAND_COLORS["primary"]}')
            
            with ui.row().classes('w-full items-end gap-4'):
                repo_input = ui.input(
                    label="GitHub Repository URL",
                    placeholder="https://github.com/username/repository",
                    value="https://github.com/cognitivecomputations/github2file"
                ).props('outlined dense').classes('flex-grow').style('min-width: 400px')

                branch_input = ui.input(
                    label="Branch / Tag", 
                    placeholder="main",
                    value="master"
                ).props('outlined dense').style('width: 150px')

            with ui.row().classes('gap-3 mt-4'):
                process_button = ui.button('Process Repository', on_click=process_repository).classes('magic-btn').props('rounded size=lg icon=hub')
                spinner = ui.spinner(size='lg', color=BRAND_COLORS['primary'])
                spinner.set_visibility(False)

        # Processing log card
        with ui.card().classes('w-full max-w-4xl magic-card p-6'):
            with ui.row().classes('w-full justify-between items-center mb-3'):
                ui.label('Processing Log').classes('text-xl font-semibold').style(f'color: {BRAND_COLORS["primary"]}')
                ui.html(f'<span class="magic-badge">Live Updates</span>')
            
            log = ui.log().classes('w-full h-48 magic-log p-3')

        # Output information card
        with ui.card().classes('w-full max-w-4xl magic-card p-6'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('Analysis Metrics').classes('text-xl font-semibold').style(f'color: {BRAND_COLORS["primary"]}')
                
                with ui.row().classes('items-center gap-6'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('token', size='sm').style(f'color: {BRAND_COLORS["accent"]}')
                        ui.label('Total Tokens:').classes('text-base')
                        token_count_label = ui.label('0').classes('text-lg font-mono font-bold').style(f'color: {BRAND_COLORS["primary"]}')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('storage', size='sm').style(f'color: {BRAND_COLORS["accent"]}')
                        ui.label('File Size:').classes('text-base')
                        file_size_label = ui.label('0 KB').classes('text-lg font-mono font-bold').style(f'color: {BRAND_COLORS["primary"]}')
                    
                    ui.html(f'<span class="info-badge">cl100k_base encoding</span>')

        # Output card with action buttons
        with ui.card().classes('w-full max-w-4xl magic-card p-6'):
            with ui.row().classes('w-full justify-between items-center mb-3'):
                ui.label('Concatenated Repository Data').classes('text-xl font-semibold').style(f'color: {BRAND_COLORS["primary"]}')
                
                with ui.row().classes('gap-2'):
                    download_button = ui.button('Download TXT', icon='download', 
                                               on_click=download_file).classes('magic-btn').props('rounded')
                    download_button.set_enabled(False)
                    
                    copy_button = ui.button('Copy to Clipboard', icon='content_copy', 
                                          on_click=copy_to_clipboard).classes('magic-btn-secondary').props('rounded')
                    copy_button.set_enabled(False)

            output_area = ui.textarea().classes('w-full h-96 font-mono magic-output p-3').props(
                'outlined readonly placeholder="Processed repository content will appear here..."')

        # Footer
        with ui.row().classes('mt-12 items-center gap-4 text-gray-500'):
            ui.link('🌐 researchmagic.com', 'https://researchmagic.com/').classes('hover:text-purple-600')
            ui.label('•')
            ui.link('✉️ support@researchmagic.com', 'mailto:support@researchmagic.com').classes('hover:text-purple-600')
            ui.label('•')
            ui.label('© 2025 MAGIC Research. All rights reserved.')


# Run the NiceGUI application with star favicon
ui.run(title='MAGIC-Repo2LLM - GitHub to LLM Converter', favicon='✨', dark=False, port=8080, host='0.0.0.0')
