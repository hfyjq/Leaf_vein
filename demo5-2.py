import os
import webbrowser
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import sys
from colorama import init, Fore, Style
import gettext

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

init(autoreset=True)

# 将程序中的文本标记为待翻译的源文本，方便进行语言切换
_ = gettext.gettext

# 翻译文本
# 英文翻译
en_translations = gettext.translation('menu', localedir='locales', languages=['en'])
en_translations.install()

# 中文翻译
zh_translations = gettext.translation('menu', localedir='locales', languages=['zh'])
zh_translations.install()

def add_path(paths):
    """
    添加新的脚本或应用程序路径
    """
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(title=_('Select script or application path'))
    if path:
        name = input(_("*Please enter the name of the path:"))
        paths.append((name, path))
        print(_("*The path has been successfully added!"))
    else:
        print(_("*No path selected."))
    return paths

def rename_path(paths):
    """
    重命名指定的脚本或应用程序路径
    """
    show_paths(paths)
    path_choice = input(_("*Please enter the number of the path to be renamed:"))
    try:
        path_index = int(path_choice)
        name = input(_("*Please enter the new name of the path:"))
        paths[path_index] = (name, paths[path_index][1])
        print(_("*The path has been successfully renamed!"))
    except (ValueError, IndexError):
        print(_("*Invalid path number. Please select again."))
    return paths

def remove_path(paths):
    """
    删除指定的脚本或应用程序路径
    """
    show_paths(paths)
    path_choice = input(Fore.RED + _("*Please enter the number of the path to be deleted:") + Fore.RESET)
    try:
        path_index = int(path_choice)
        del paths[path_index]
        print(Fore.RED + _("*The path has been successfully deleted!") + Style.RESET_ALL)
    except (ValueError, IndexError):
        print(Fore.RED + _("*Invalid path number. Please select again.") + Style.RESET_ALL)
    return paths

def remove_all_paths():
    """
    删除所有的脚本或应用程序路径
    """
    confirmation = input(Fore.RED + _("Are you sure you want to delete all paths? (Enter 'Y' to confirm):") + Fore.RESET)
    if confirmation == "Y":
        return []
    else:
        print(_("*Operation canceled."))
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

    print(Fore.GREEN + "*Current added script or application paths:")
    for i, path in enumerate(paths):
        print(f"{Fore.GREEN}{i}: {path[0]} - {path[1]}{Style.RESET_ALL}")
    sys.stdout.flush()

def launch_script(script_path):
    """
    执行脚本
    """
    os.system(f'python {script_path}')

def launch_program(path):
    """
    启动应用程序
    """
    os.startfile(path)

def add_website(websites):
    """
    添加新的网址
    """
    name = input(Fore.CYAN + "*Please enter the name of the website:")
    url = input(Fore.CYAN + "*Please enter the URL of the website:")
    websites.append((name, url))
    print(Fore.CYAN + "*The website has been successfully added!" + Style.RESET_ALL)
    return websites


def remove_website(websites):
    """
    删除指定的网址
    """
    show_websites(websites)
    website_choice = input(Fore.RED + "*Please enter the number of the website to be deleted:" + Fore.RESET)
    try:
        website_index = int(website_choice)
        del websites[website_index]
        print(Fore.RED + "*The website has been successfully deleted!" + Style.RESET_ALL)
    except (ValueError, IndexError):
        print(Fore.RED + "*Invalid website number. Please select again." + Style.RESET_ALL)
    return websites


def show_websites(websites):
    """
    显示网址列表
    """
    print(_("Current added websites:"))
    for i, website in enumerate(websites):
        print(f"{i}: {website[0]} - {website[1]}")


def open_website(websites):
    """
    在浏览器打开指定的网址
    """
    show_websites(websites)
    website_choice = input(Fore.CYAN + "*Please enter the number of the website to be opened:" + Fore.RESET)
    try:
        website_index = int(website_choice)
        website_url = websites[website_index][1]
        webbrowser.open(website_url)
    except (ValueError, IndexError):
        print(Fore.RED + "*Invalid path number. Please select another path." + Style.RESET_ALL)


def main():
    # 检查用户是否同意许可条例
    if not check_permission():
        return

    # 加载已有路径列表或创建一个新的空列表
    paths = load_paths()

    # 加载已有网址列表或创建一个新的空列表
    websites = [
        (_("NVIDIA Driver Search"), "https://www.nvidia.cn/geforce/drivers/"),
        (_("AMD Driver Search"), "https://www.amd.com/zh-hans/support"),
        (_("INTEL Driver Search"), "https://www.intel.cn/content/www/cn/zh/download-center/home.html"),
        (_("Microsoft Driver Search"), "https://www.microsoft.com/zh-cn/download/drivers"),
    ]

    while True:
        # 显示当前路径列表
        print(Fore.GREEN + "\n" )
        show_paths(paths)
        print(Fore.GREEN + "\n" + Fore.CYAN)
        show_websites(websites)
        print(Fore.CYAN + "\n" + Style.RESET_ALL)

        # 获取用户输入并执行对应操作
        choice = input("----------------------------------------\n"
                       f"|{Fore.YELLOW}{_('Please select an operation:'): ^40s}{Style.RESET_ALL}|\n"
                       "|1. Add new script or application path  |\n"
                       "|2. Launch added script or application  |\n"
                       "|3. Rename specified script or application path|\n"
                       "|4. Remove specified script or application path |\n"
                       "|5. Remove all added script or application paths |\n"
                       "|6. Add new website                     |\n"
                       "|7. Remove specified website            |\n"
                       "|8. Open specified website              |\n"
                       "|9. Switch language to English          |\n"
                       "|10. 切换语言为中文                        |\n"
                       "-----------------------------------------\n")

        if choice == '1':
            paths = add_path(paths)
            save_paths(paths)

        elif choice == '2':
            path_choice = input("*Please enter the number of the path to be launched:")
            try:
                path_index = int(path_choice)
                path = paths[path_index][1]
                if path.endswith('.py'):
                    launch_script(path)
                else:
                    launch_program(path)
            except (ValueError, IndexError):
                print(Fore.RED + "*Invalid path number. Please re-select。" + Style.RESET_ALL)

        elif choice == '3':
            paths = rename_path(paths)
            save_paths(paths)

        elif choice == '4':
            paths = remove_path(paths)
            save_paths(paths)

        elif choice == '5':
            confirmation = input(
                Fore.RED + "*Are you sure you want to delete all paths? (Enter 'Y' to confirm):" + Fore.RESET)
            if confirmation == "Y":
                paths = remove_all_paths()
                if paths is not None:
                    save_paths(paths)
            else:
                print(_("*Operation canceled."))

        elif choice == '6':
            websites = add_website(websites)

        elif choice == '7':
            websites = remove_website(websites)

        elif choice == '8':
            open_website(websites)

        elif choice == '9':
            # 切换到英文
            en_translations.install()
            print(Fore.CYAN + "\n" + _("*Language has been successfully switched to English!") + Style.RESET_ALL)

        elif choice == '10':
            # 切换到中文
            zh_translations.install()
            print(Fore.CYAN + "\n" + _("*语言已成功切换为中文！") + Style.RESET_ALL)

        else:
            print(Fore.RED + "*Invalid choice. Please select again." + Style.RESET_ALL)


if __name__ == '__main__':
    main()