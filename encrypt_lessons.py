import json
import base64

# Simple XOR encryption to obfuscate content
# Key matching the frontend 'pinegood888'
KEY = "pinegood888"

def xor_encrypt(text, key):
    if not text:
        return ""
    # Convert to bytes
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    encrypted = bytearray()
    
    for i in range(len(text_bytes)):
        encrypted.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])
        
    # Return as base64 string
    return base64.b64encode(encrypted).decode('utf-8')

def main():
    source_path = r"e:\Quant\PineScript_study\web\data\lessons.json"
    dest_path = r"e:\Quant\PineScript_study\web\data\lessons_encrypted.json"
    
    print(f"Reading from {source_path}...")
    with open(source_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("Encrypting sensitive fields for locked lessons...")
    count = 0
    
    for lesson in data.get("lessons", []):
        # Only encrypt if it is a locked lesson
        if lesson.get("isLocked", False):
            print(f"  Encrypting: {lesson.get('title', 'Unknown')}")
            
            # Fields to encrypt
            fields = ["concept", "concept_extra", "pine_code", "python_code"]
            
            for field in fields:
                if field in lesson and lesson[field]:
                    lesson[field] = "ENC:" + xor_encrypt(lesson[field], KEY)
            
            # Mark as encrypted content
            lesson["isEncrypted"] = True
            count += 1
            
    print(f"Encrypted {count} lessons.")
    
    # Save to a NEW file or overwrite (user choice, but let's overwrite for deployment simplicity usually)
    # Here we save to lessons.json directly to make deployment easy? 
    # WAIT: If we overwrite, the user loses source. 
    # Better approach: 
    # 1. We keep lessons.json as SOURCE (Source of Truth).
    # 2. We generate lessons.json for deployment.
    # But since the user wants to "upload to git", they might upload the source.
    # 
    # STRATEGY:
    # We will modify lessons.json in place BUT keep a backup? 
    # No, that's dangerous.
    # 
    # Correct Flow for User:
    # 1. lessons_source.json (Editable, Clear Text) -> KEEP THIS LOCAL
    # 2. lessons.json (Encrypted) -> PUBLIC WEB
    #
    # Action: Rename current lessons.json to lessons_source.json, then generate encrypted lessons.json
    
    import os
    import shutil
    
    source_file = r"e:\Quant\PineScript_study\web\data\lessons_source.json"
    target_file = r"e:\Quant\PineScript_study\web\data\lessons.json"
    
    # Check if we already have a source file
    if not os.path.exists(source_file):
        print("Creating source backup: lessons_source.json")
        shutil.copy(r"e:\Quant\PineScript_study\web\data\lessons.json", source_file)
    else:
        print("Using existing lessons_source.json as source.")
        
    # Read from SOURCE
    with open(source_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Encrypt
    for lesson in data.get("lessons", []):
        if lesson.get("isLocked", False):
            fields = ["concept", "concept_extra", "pine_code", "python_code"]
            for field in fields:
                if field in lesson and lesson[field]:
                    lesson[field] = "ENC:" + xor_encrypt(lesson[field], KEY)
            lesson["isEncrypted"] = True

    # Write to TARGET (lessons.json) which is used by the app
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Success! Encrypted data written to {target_file}")
    print(f"Original data preserved in {source_file}")

if __name__ == "__main__":
    main()
