
import os
import pickle
from tkinter import Tk, Label, Entry, Button, Listbox, messagebox


'''
重大更新：新增GUI窗口
'''

class PathManager:
    def __init__(self):
        self.paths = self.load_paths()

        self.root = Tk()
        self.root.title("路径管理器")

        self.label = Label(self.root, text="当前已添加的脚本或应用程序路径：")
        self.label.pack()

        self.path_listbox = Listbox(self.root)
        self.path_listbox.pack()
        self.update_path_listbox()

        self.add_button = Button(self.root, text="添加路径", command=self.add_path)
        self.add_button.pack()

        self.rename_button = Button(self.root, text="重命名路径", command=self.rename_path)
        self.rename_button.pack()

        self.remove_button = Button(self.root, text="删除路径", command=self.remove_path)
        self.remove_button.pack()

        self.launch_button = Button(self.root, text="启动路径", command=self.launch_path)
        self.launch_button.pack()

        self.save_button = Button(self.root, text="保存路径", command=self.save_paths)
        self.save_button.pack()

        self.exit_button = Button(self.root, text="退出", command=self.root.quit)
        self.exit_button.pack()

        self.root.mainloop()

    def update_path_listbox(self):
        self.path_listbox.delete(0, "end")
        for path in self.paths:
            self.path_listbox.insert("end", path[0])

    def add_path(self):
        top = Tk()
        top.title("添加路径")

        label = Label(top, text="请输入脚本或应用程序的路径：")
        label.pack()

        path_entry = Entry(top)
        path_entry.pack()

        name_label = Label(top, text="请输入路径的名称：")
        name_label.pack()

        name_entry = Entry(top)
        name_entry.pack()

        def add():
            path = path_entry.get()
            name = name_entry.get()
            if os.path.exists(path):
                self.paths.append((name, path))
                self.update_path_listbox()
                top.destroy()
            else:
                messagebox.showerror("错误", "路径不存在，请重新输入。")

        add_button = Button(top, text="添加", command=add)
        add_button.pack()

        top.mainloop()

    def rename_path(self):
        index = self.path_listbox.curselection()
        if len(index) == 0:
            messagebox.showerror("错误", "请选择要重命名的路径。")
            return
        old_name = self.path_listbox.get(index)
        old_path = None
        for path in self.paths:
            if path[0] == old_name:
                old_path = path[1]
                break
        if not old_path:
            messagebox.showerror("错误", "未找到要重命名的路径。")
            return

        top = Tk()
        top.title("重命名路径")

        label = Label(top, text="请输入新的路径名称：")
        label.pack()

        name_entry = Entry(top)
        name_entry.pack()

        def rename():
            new_name = name_entry.get()
            for i, path in enumerate(self.paths):
                if path[0] == old_name:
                    self.paths[i] = (new_name, path[1])
                    self.update_path_listbox()
                    top.destroy()
                    return

        rename_button = Button(top, text="重命名", command=rename)
        rename_button.pack()

        top.mainloop()

    def remove_path(self):
        index = self.path_listbox.curselection()
        if len(index) == 0:
            messagebox.showerror("错误", "请选择要删除的路径。")
            return
        name = self.path_listbox.get(index)

        for i, path in enumerate(self.paths):
            if path[0] == name:
                del self.paths[i]
                self.update_path_listbox()
                return

    def launch_path(self):
        index = self.path_listbox.curselection()
        if len(index) == 0:
            messagebox.showerror("错误", "请选择要启动的路径。")
            return
        name = self.path_listbox.get(index)

        for path in self.paths:
            if path[0] == name:
                if path[1].endswith('.py'):
                    os.system(f'python {path[1]}')
                else:
                    os.startfile(path[1])
                return

    def save_paths(self):
        with open('paths.pkl', 'wb') as f:
            pickle.dump(self.paths, f)

    def load_paths(self):
        if os.path.exists('paths.pkl'):
            with open('paths.pkl', 'rb') as f:
                paths = pickle.load(f)
                return paths
        else:
            return []


if __name__ == '__main__':
    path_manager = PathManager()
