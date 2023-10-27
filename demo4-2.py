
import os
import pickle
import tkinter as tk
from tkinter import filedialog


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
