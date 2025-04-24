import os
import re
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox

def replace_in_files(folder, old_str, new_str, replace_uuid=False, rename_folders=True):
    uuid_pattern = re.compile(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    )
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        for filename in filenames:
            new_filename = filename.replace(old_str, new_str)
            old_file_path = os.path.join(dirpath, filename)
            new_file_path = os.path.join(dirpath, new_filename)
            if new_file_path != old_file_path:
                os.rename(old_file_path, new_file_path)
            try:
                with open(new_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue
            new_content = content
            if replace_uuid:
                new_content = uuid_pattern.sub(lambda m: str(uuid.uuid4()), new_content)
            if old_str:
                new_content = new_content.replace(old_str, new_str)
            if new_content != content:
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        if rename_folders:
            for dirname in dirnames:
                new_dirname = dirname.replace(old_str, new_str)
                old_dir_path = os.path.join(dirpath, dirname)
                new_dir_path = os.path.join(dirpath, new_dirname)
                if new_dir_path != old_dir_path:
                    os.rename(old_dir_path, new_dir_path)

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def execute():
    folder = folder_entry.get()
    old_str = old_str_entry.get()
    new_str = new_str_entry.get()
    replace_uuid = uuid_var.get()
    rename_folders = rename_folders_var.get()
    if folder and (old_str or replace_uuid):
        replace_in_files(folder, old_str, new_str, replace_uuid, rename_folders)
        messagebox.showinfo("完了", "置き換えが完了しました！")
    else:
        messagebox.showwarning("警告", "フォルダと置換設定を少なくとも1つ選択してください。")

root = tk.Tk()
root.title("Text Replacer v2")

tk.Label(root, text="フォルダを選択:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="参照", command=select_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="置き換える文字列:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
old_str_entry = tk.Entry(root, width=50)
old_str_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="新しい文字列:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
new_str_entry = tk.Entry(root, width=50)
new_str_entry.grid(row=2, column=1, padx=5, pady=5)

uuid_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="ファイル内のUUIDをランダムに置き換える", variable=uuid_var).grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

rename_folders_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="フォルダー名も置き換える", variable=rename_folders_var).grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")

tk.Button(root, text="実行", command=execute).grid(row=5, column=0, columnspan=3, padx=5, pady=10)

root.mainloop()