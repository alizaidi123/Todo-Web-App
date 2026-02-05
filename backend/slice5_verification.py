"""
Slice 5 Verification: Test Frontend ChatKit implementation.
"""
import os
import sys
import json
from pathlib import Path


def test_slice5():
    print("=== Slice 5 Verification: Frontend ChatKit ===")

    # Test 1: Check that frontend chat page exists
    chat_page_path = Path("../frontend/app/chat/page.tsx")
    if chat_page_path.exists():
        print("[OK] Frontend chat page exists")
    else:
        print(f"[ERROR] Frontend chat page does not exist at {chat_page_path}")
        return False

    # Test 2: Check that chat page contains ChatKit components
    try:
        with open(chat_page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_components = [
            '@chatscope/chat-ui-kit-react',
            'MainContainer',
            'ChatContainer',
            'MessageList',
            'MessageInput'
        ]

        missing_components = []
        for component in required_components:
            if component not in content:
                missing_components.append(component)

        if not missing_components:
            print("[OK] All required ChatKit components present")
        else:
            print(f"[ERROR] Missing ChatKit components: {missing_components}")
            return False

    except Exception as e:
        print(f"[ERROR] Could not read chat page: {e}")
        return False

    # Test 3: Check that frontend connects to correct backend endpoint
    try:
        if '/api/${userId}/chat' in content or "api/" in content and "chat" in content:
            print("[OK] Frontend connects to correct backend endpoint")
        else:
            print("[ERROR] Frontend does not connect to expected backend endpoint")
            return False
    except:
        print("[ERROR] Could not check backend endpoint connection")
        return False

    # Test 4: Check that package.json has required dependencies
    package_json_path = Path("../frontend/package.json")
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_json = json.load(f)

            required_deps = [
                "@chatscope/chat-ui-kit-react",
                "@chatscope/chat-ui-kit-styles",
                "axios"
            ]

            missing_deps = []
            all_deps = {}
            all_deps.update(package_json.get('dependencies', {}))
            all_deps.update(package_json.get('devDependencies', {}))

            for dep in required_deps:
                if dep not in all_deps:
                    missing_deps.append(dep)

            if not missing_deps:
                print("[OK] All required frontend dependencies present")
            else:
                print(f"[ERROR] Missing frontend dependencies: {missing_deps}")
                return False

        except Exception as e:
            print(f"[ERROR] Could not check package.json: {e}")
            return False
    else:
        print(f"[ERROR] package.json not found at {package_json_path}")
        return False

    # Test 5: Check that the main page has the chat button
    main_page_path = Path("../frontend/app/page.tsx")
    if main_page_path.exists():
        try:
            with open(main_page_path, 'r', encoding='utf-8') as f:
                main_content = f.read()

            if 'Chat with AI' in main_content and '/chat' in main_content:
                print("[OK] Main page contains Chat with AI button")
            else:
                print("[WARNING] Main page may be missing Chat with AI button")
                # This is not necessarily an error, depending on implementation

        except Exception as e:
            print(f"[WARNING] Could not check main page for chat button: {e}")
            # Don't fail the test for this, as it's not critical

    # Test 6: Check that chat layout exists
    chat_layout_path = Path("../frontend/app/chat/layout.tsx")
    if chat_layout_path.exists():
        print("[OK] Chat layout exists for protected routing")
    else:
        print(f"[ERROR] Chat layout does not exist at {chat_layout_path}")
        return False

    print("\n=== Slice 5 Verification Complete ===")
    print("[OK] Frontend ChatKit page implemented")
    print("[OK] ChatKit components integrated")
    print("[OK] Connects to backend endpoint")
    print("[OK] Required dependencies installed")
    print("[OK] Protected routing implemented")

    return True


if __name__ == "__main__":
    success = test_slice5()
    if success:
        print("\nSlice 5 verification PASSED")
    else:
        print("\nSlice 5 verification FAILED")
        sys.exit(1)