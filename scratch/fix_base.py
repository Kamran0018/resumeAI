import os
import re

def fix_layout():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_html_path = os.path.join(base_dir, 'templates', 'base.html')
    
    if not os.path.exists(base_html_path):
        print(f"File not found: {base_html_path}")
        return
        
    print(f"Reading {base_html_path}...")
    with open(base_html_path, 'rb') as f:
        content_bytes = f.read()
        
    # Decode with errors='ignore' to remove the corrupted character
    content = content_bytes.decode('utf-8', errors='ignore')
    
    # Define responsive styles to insert
    responsive_css = """
        /* ── Responsive Sidebar for Mobile/Tablet ── */
        @media (max-width: 850px) {
            .sidebar {
                position: fixed;
                left: -var(--sidebar-width);
                transition: transform 0.3s ease;
                z-index: 1000;
            }
            .sidebar.open {
                transform: translateX(var(--sidebar-width));
            }
            .main-area {
                margin-left: 0 !important;
                width: 100% !important;
            }
            .mobile-menu-btn {
                display: flex !important;
                align-items: center;
                justify-content: center;
            }
            .sidebar-close-btn {
                display: block !important;
            }
        }

        /* ── Sidebar Overlay Style ── */
        .sidebar-overlay {
            position: fixed;
            inset: 0;
            background: rgba(11, 15, 25, 0.5);
            backdrop-filter: blur(4px);
            z-index: 999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .sidebar-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        /* ── Sidebar Close Button Style ── */
        .sidebar-close-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 20px;
            cursor: pointer;
            padding: 8px;
            transition: color 0.2s ease;
        }
        .sidebar-close-btn:hover {
            color: var(--text-primary);
        }
    </style>
"""

    # Check if </style> is indeed missing before <body>
    if '</style>' not in content or '<body>' in content:
        # We find the corrupted body tag line: e.g. "═════<body>"
        # We replace it with our styles, </style> and <body>
        pattern = re.compile(r'[^<\n]*<body>')
        if pattern.search(content):
            print("Found <body> with leading corrupted characters. Replacing...")
            content = pattern.sub(responsive_css + '    <body>', content)
        else:
            # Fallback: simple replace of <body>
            content = content.replace('<body>', responsive_css + '    <body>')
            
    # Write back as clean UTF-8
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully fixed base.html layout and encoding!")

if __name__ == '__main__':
    fix_layout()
