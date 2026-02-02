import sys
import asyncio
from requests_html import HTMLSession

def test_render_feature():
    print("--- Starting Requests-HTML Functional Verification ---")
    
    # 1. Initialize the session
    session = HTMLSession()
    
    try:
        # 2. Basic Fetch
        print("--> Fetching example.com...")
        r = session.get('https://example.com')
        
        # 3. TRIGGER THE DEP-DRIFT TRAP
        # .render() triggers pyppeteer -> urllib3 launch.
        # On urllib3 2.0+, this throws a TypeError: 'method' is an unexpected keyword.
        print("--> Launching Chromium and Rendering JavaScript...")
        r.html.render(timeout=30)
        
        # 4. Verify Content
        if "Example Domain" in r.html.text:
            print("    [✓] JavaScript rendering successful.")
        else:
            raise ValueError("Rendered content does not match expectation.")
            
        print("--- SMOKE TEST PASSED ---")
        session.close()

    except Exception as e:
        print(f"CRITICAL VALIDATION FAILURE: {str(e)}")
        # If urllib3 2.x is present, we expect a TypeError or AttributeError here.
        if session:
            try:
                session.close()
            except:
                pass
        sys.exit(1)

if __name__ == "__main__":
    test_render_feature()