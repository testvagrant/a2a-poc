#!/usr/bin/env python3
"""
Generate UTA Dashboard

This script generates a comprehensive dashboard for showcasing the Universal Tester-Agent system.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from reporters.dashboard_generator import generate_dashboard

def main():
    """Generate the UTA dashboard."""
    print("🚀 Generating UTA Dashboard...")
    
    try:
        dashboard_path = generate_dashboard(str(project_root), "dashboard")
        print(f"✅ Dashboard generated successfully!")
        print(f"📁 Location: {dashboard_path}")
        print(f"🌐 Open: {dashboard_path}/index.html")
        
        # List generated files
        dashboard_dir = Path(dashboard_path)
        if dashboard_dir.exists():
            files = list(dashboard_dir.glob("*.html"))
            print(f"\n📄 Generated pages:")
            for file in files:
                print(f"   - {file.name}")
        
        print(f"\n🎯 Ready for client presentations!")
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
