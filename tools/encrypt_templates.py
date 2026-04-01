import os
import sys

# 將 src/engine 加入路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src", "engine"))

from security import SecurityEngine

import argparse

def process_templates(target_dirs, mode='encrypt'):
    engine = SecurityEngine()
    total_count = 0
    
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            print(f"跳過不存在的目錄: {target_dir}")
            continue
            
        print(f"\n--- 正在{ '加密' if mode == 'encrypt' else '還原' }目錄: {target_dir} ---")
        count = 0
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if mode == 'encrypt':
                    # 僅加密 Word 與 Excel，且避開暫存檔與已加密檔
                    if file.endswith(('.docx', '.xlsx')) and not file.startswith('~') and not file.endswith('.enc'):
                        file_path = os.path.join(root, file)
                        dest_path = file_path + ".enc"
                        print(f"加密中: {file} -> {os.path.basename(dest_path)}")
                        engine.encrypt_file(file_path, dest_path)
                        os.remove(file_path)
                        count += 1
                elif mode == 'decrypt':
                    # 尋找已加密檔並還原
                    if file.endswith('.enc'):
                        file_path = os.path.join(root, file)
                        # 移除 .enc 結尾
                        dest_path = file_path[:-4]
                        print(f"還原中: {file} -> {os.path.basename(dest_path)}")
                        # 使用 BytesIO 解密並存入檔案
                        content = engine.decrypt_to_memory(file_path)
                        with open(dest_path, 'wb') as f:
                            f.write(content.getbuffer())
                        # 刪除加密檔
                        os.remove(file_path)
                        count += 1
                        
        print(f"完成！該目錄共處理 {count} 個檔案。")
        total_count += count
                
    print(f"\n總結：共處理 {total_count} 個檔案。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ISMS 範本加密/解密工具')
    parser.add_argument('--mode', choices=['encrypt', 'decrypt'], default='encrypt', help='執行模式')
    parser.add_argument('--dirs', nargs='+', help='目標目錄列表')
    parser.add_argument('--yes', action='store_true', help='跳過確認')
    
    args = parser.parse_args()
    
    # 預設目錄
    target_dirs = args.dirs or [
        os.path.join(BASE_DIR, "files", "marked"),
        os.path.join(BASE_DIR, "examples")
    ]
    
    if not args.yes:
        action = "加密並刪除明文" if args.mode == 'encrypt' else "從加密檔還原明文"
        confirm = input(f"即將於以下目錄執行 [{action}]：\n" + "\n".join([f"- {d}" for d in target_dirs]) + "\n確定嗎？(y/n): ")
        if confirm.lower() != 'y':
            print("已取消。")
            sys.exit(0)
            
    process_templates(target_dirs, mode=args.mode)
