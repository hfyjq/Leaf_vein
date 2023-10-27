import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def center_window(window):
    """
    将窗口居中显示在屏幕上
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def check_permission():
    """
    检查用户是否同意许可条例
    """
    if os.path.exists('permission.pkl'):
        return True  # 用户已经同意过许可条例

    root = tk.Tk()
    root.withdraw()

    # 创建一个带有滚动条和选择按钮的窗口来展示许可条例
    permission_text = "*本软件的使用受用户许可协议的约束。软件的一些功能需要网络连接。开发者在任何时候都不保证联网功能的可用性，例如高级功能的详细使用说明，某些报错的具体解析，或驱动程序支持。开发者保留修改和终止任意功能的权利。软件部分内容、技术支持请访问对应内容提供的Github或steam创意工坊页面链接。任何说明文本、软件、脚本命名若与现实世界中的地点、人物、技术或实体重名以及相似纯属巧合，并不意味着本软件有任何第三方的赞助和认可。\n" \
                      "要获取补充DLC以及其它附加内容，可能需要提供额外费用、特殊序列号。获取这些内容可能需要互联网连接，可能不适用于所有使用者。\n"\
                      "\n"\
                      "版权所有  Copyright (c) 2023 梦梦没在做梦 ，遵从Apache V2.0开源协议。任何说明文本、软件、脚本命名若与现实世界中的地点、人物、技术或实体重名以及相似纯属巧合，不含有任何暗示或煽动。开发者并不以任何形式支持、容忍或鼓励任何人将本软件用于非法用途.\n"\
                      "\n"\
                      "#请严格遵从软件内的使用说明，过失操作导致的一切损失均由您自行承担\n" \
                      "\n" \
                      "#不建议自行更改任何依赖文件，这可能导致部分功能的失效、部分文件异常或损毁"
    def confirm_permission():
        user_choice = "I AGREE" if agree_var.get() else "I DISAGREE"
        if user_choice == "I AGREE":
            with open('permission.pkl', 'wb') as f:
                pickle.dump(True, f)
            permission_window.destroy()

    permission_window = tk.Toplevel(root)
    permission_window.title("用户许可")
    permission_window.geometry("500x400")
    center_window(permission_window)

    permission_scroll = tk.Scrollbar(permission_window, orient=tk.VERTICAL)
    permission_textbox = scrolledtext.ScrolledText(
        permission_window, height=25, wrap=tk.WORD,
        yscrollcommand=permission_scroll.set)
    permission_textbox.insert(tk.END, permission_text)
    permission_textbox.config(state=tk.DISABLED)  # 禁用文本框编辑
    permission_textbox.pack(fill=tk.BOTH, expand=tk.YES)

    permission_agree_frame = tk.Frame(permission_window)
    permission_agree_frame.pack(anchor=tk.W)

    agree_var = tk.BooleanVar()
    agree_checkbox = tk.Checkbutton(
        permission_agree_frame, text="我同意", variable=agree_var)
    agree_checkbox.pack(side=tk.LEFT)

    disagree_checkbox = tk.Checkbutton(
        permission_agree_frame, text="我不同意", variable=agree_var,
        onvalue=False, offvalue=True)
    disagree_checkbox.pack(side=tk.LEFT)

    permission_confirm_button = tk.Button(
        permission_window, text="确认", command=confirm_permission)
    permission_confirm_button.pack(side=tk.BOTTOM)

    permission_scroll.config(command=permission_textbox.yview)
    permission_scroll.pack(fill=tk.Y, side=tk.RIGHT)

    root.wait_window(permission_window)  # 等待用户同意或拒绝许可条例

    if os.path.exists('permission.pkl'):
        # 用户同意了许可条例，继续执行程序逻辑
        return True
    else:
        # 用户拒绝了许可条例，退出程序
        messagebox.showerror("错误", "您必须同意许可条例才能使用本程序。")
        return False

def add_path(paths):
    """
    添加新的脚本或应用程序路径
    """
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(title='选择脚本或应用程序的路径')
    if path:
        name = input("*请输入路径的名称：")
        paths.append((name, path))
        print("*已成功添加路径！")
    else:
        print("*未选择路径。")
    return paths


def rename_path(paths):
    """
    重命名指定的脚本或应用程序路径
    """
    show_paths(paths)
    path_choice = input("*请输入要重命名的路径的编号：")
    try:
        path_index = int(path_choice)
        name = input("*请输入新的路径名称：")
        paths[path_index] = (name, paths[path_index][1])
        print("*已成功重命名路径！")
    except (ValueError, IndexError):
        print("*无效的路径编号。请重新选择。")
    return paths

def remove_path(paths):
    """
    删除指定的脚本或应用程序路径
    """
    show_paths(paths)
    path_choice = input("*请输入要删除的路径的编号：")
    try:
        path_index = int(path_choice)
        del paths[path_index]
        print("*已成功删除路径！")
    except (ValueError, IndexError):
        print("*无效的路径编号。请重新选择。")
    return paths


def remove_all_paths():
    """
    删除所有的脚本或应用程序路径
    """
    confirmation = input("*确定要删除所有路径吗？(输入 'Y' 确认): ")
    if confirmation == "Y":
        return []
    else:
        print("*操作已取消。")
        return None


def save_paths(paths):
    """
    保存路径列表到文件
    """
    with open('paths.pkl', 'wb') as f:
        pickle.dump(paths, f)


def load_paths():
    """
    加载保存在文件中的路径列表
    """
    if os.path.exists('paths.pkl'):
        with open('paths.pkl', 'rb') as f:
            paths = pickle.load(f)
            return paths
    else:
        return []


def show_paths(paths):
    """
    显示路径列表
    """
    os.system("cls" if os.name == "nt" else "clear")  # 清除之前的内容

    print("当前已添加的脚本或应用程序路径：\n")
    for i, path in enumerate(paths):
        print(f"{i}: {path[0]} - {path[1]}")


def launch_script(script_path):
    """
    执行脚本
    """
    os.system(f'python {script_path}')


def launch_program(program_path):
    """
    启动应用程序
    """
    os.startfile(program_path)


def main():
    # 检查用户是否同意许可条例
    if not check_permission():
        return

    # 加载已有路径列表或创建一个新的空列表
    paths = load_paths()

    while True:
        # 显示当前路径列表
        show_paths(paths)

        # 获取用户输入并执行对应操作
        choice = input("----------------------------------------\n"
                       "|请选择操作:                            |\n"
                       "|1. 添加新的脚本或应用程序路径          |\n"
                       "|2. 启动已添加的脚本或应用程序          |\n"
                       "|3. 重命名指定已添加的脚本或应用程序路径|\n"
                       "|4. 删除指定已添加的脚本或应用程序路径  |\n"
                       "|5. 删除所有已添加的脚本或应用程序路径  |\n"
                       "|6. 退出程序                            |\n"
                       "-----------------------------------------\n")

        if choice == '1':
            paths = add_path(paths)
            save_paths(paths)

        elif choice == '2':
            path_choice = input("*请输入要启动的路径的编号：")
            try:
                path_index = int(path_choice)
                path = paths[path_index][1]
                if path.endswith('.py'):
                    launch_script(path)
                else:
                    launch_program(path)
            except (ValueError, IndexError):
                print("*无效的路径编号。请重新选择。")

        elif choice == '3':
            paths = rename_path(paths)
            save_paths(paths)

        elif choice == '4':
            paths = remove_path(paths)
            save_paths(paths)

        elif choice == '5':
            paths = remove_all_paths()
            if paths is not None:
                save_paths(paths)

        elif choice == '6':
            break

        else:
            print("*无效的选择。请重新输入。")


if __name__ == '__main__':
    main()
