import os
import shutil
from tkinter import messagebox, Tk, Checkbutton, BooleanVar, Button

# Windows에서 Documents 경로 얻기
documents_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'EA Games', 'The Sims 4')

# 심즈4 캐시 폴더 경로 설정
cache_folder = os.path.join(documents_folder, 'cache')
cachestr_folder = os.path.join(documents_folder, 'cachestr')
cache_log = documents_folder  # 로그 파일이 있는 폴더

# documents_folder의 상위 폴더인 EA Games 폴더를 기반으로 백업 폴더 설정
backup_folder = os.path.join(os.path.dirname(documents_folder), 'backup')


def backup_files():
    """백업 폴더를 생성하고 원본 파일들을 백업합니다."""
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # cache 폴더 백업
    cache_backup = os.path.join(backup_folder, 'cache')
    if os.path.exists(cache_folder):
        shutil.copytree(cache_folder, cache_backup, dirs_exist_ok=True)

    # cachestr 폴더 백업
    cachestr_backup = os.path.join(backup_folder, 'cachestr')
    if os.path.exists(cachestr_folder):
        shutil.copytree(cachestr_folder, cachestr_backup, dirs_exist_ok=True)

    # 로그 파일 백업
    log_backup = os.path.join(backup_folder, 'logs')
    if not os.path.exists(log_backup):
        os.makedirs(log_backup)
    for file_name in os.listdir(cache_log):
        if file_name.endswith('.log'):
            file_path = os.path.join(cache_log, file_name)
            shutil.copy(file_path, log_backup)


def rollback_files():
    """백업 폴더의 파일들을 원래 위치로 복원합니다."""
    # cache 폴더 복원
    cache_backup = os.path.join(backup_folder, 'cache')
    if os.path.exists(cache_backup):
        if os.path.exists(cache_folder):
            shutil.rmtree(cache_folder)
        shutil.copytree(cache_backup, cache_folder)

    # cachestr 폴더 복원
    cachestr_backup = os.path.join(backup_folder, 'cachestr')
    if os.path.exists(cachestr_backup):
        if os.path.exists(cachestr_folder):
            shutil.rmtree(cachestr_folder)
        shutil.copytree(cachestr_backup, cachestr_folder)

    # 로그 파일 복원
    log_backup = os.path.join(backup_folder, 'logs')
    if os.path.exists(log_backup):
        for file_name in os.listdir(log_backup):
            backup_file_path = os.path.join(log_backup, file_name)
            original_file_path = os.path.join(cache_log, file_name)
            shutil.copy(backup_file_path, original_file_path)


def delete_files(cache_selected, cachestr_selected, log_selected):
    deleted_files_count = 0  # 삭제된 파일의 수를 저장할 변수
    try:
        # cache 폴더의 .png 파일 삭제
        if cache_selected and os.path.exists(cache_folder):
            for file_name in os.listdir(cache_folder):
                if file_name.endswith('.png'):
                    file_path = os.path.join(cache_folder, file_name)
                    os.remove(file_path)
                    deleted_files_count += 1  # 삭제된 파일 수 증가
                    print(f"{file_path} 파일이 삭제되었습니다.")

        # cachestr 폴더 삭제
        if cachestr_selected and os.path.exists(cachestr_folder):
            # 폴더 내 파일 수 세기
            deleted_files_count += len(os.listdir(cachestr_folder))
            shutil.rmtree(cachestr_folder)
            print(f"{cachestr_folder} 폴더가 삭제되었습니다.")

        # .log 파일 삭제
        if log_selected and os.path.exists(cache_log):
            for file_name in os.listdir(cache_log):
                if file_name.endswith('.log'):
                    file_path = os.path.join(cache_log, file_name)
                    os.remove(file_path)
                    deleted_files_count += 1  # 삭제된 파일 수 증가
                    print(f"{file_path} 로그 파일이 삭제되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}. 롤백을 수행합니다.")
        rollback_files()  # 롤백 수행
        messagebox.showerror("오류", "파일 삭제 중 오류가 발생했습니다. 변경 사항을 되돌립니다.")
        return 0  # 오류 발생 시 삭제된 파일 수를 0으로 반환

    return deleted_files_count


# 삭제 확인 및 실행 함수
def confirm_delete():
    # 삭제 여부 확인
    cache_selected = cache_var.get()
    cachestr_selected = cachestr_var.get()
    log_selected = log_var.get()

    # 삭제할 항목이 선택되지 않은 경우 경고 표시
    if not cache_selected and not cachestr_selected and not log_selected:
        messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
        return

    # 삭제 확인 알림창 표시
    answer = messagebox.askyesno("삭제 확인", "선택한 항목을 삭제하시겠습니까?")

    # 사용자가 '예'를 선택한 경우 삭제 진행
    if answer:
        backup_files()  # 백업 수행
        deleted_files_count = delete_files(cache_selected, cachestr_selected, log_selected)
        if deleted_files_count > 0:
            messagebox.showinfo("삭제 완료", f"선택한 캐시 파일이 삭제되었습니다.\n총 {deleted_files_count}개의 파일이 삭제되었습니다.")
    else:
        messagebox.showinfo("취소", "삭제 작업이 취소되었습니다.")


# GUI 생성 함수
def create_gui():
    # Tkinter 기본 창 생성
    root = Tk()
    root.title("캐시 파일 삭제 프로그램")

    # 아이콘 설정 (ico 파일 경로를 설정)
    root.iconbitmap('sims4_cleaner_imgae.ico')

    # 체크박스 변수 설정
    global cache_var, cachestr_var, log_var
    cache_var = BooleanVar()
    cachestr_var = BooleanVar()
    log_var = BooleanVar()

    # 체크박스 생성
    cache_check = Checkbutton(root, text="cache 폴더의 .png 파일 삭제", variable=cache_var)
    cachestr_check = Checkbutton(root, text="cachestr 폴더 삭제", variable=cachestr_var)
    log_check = Checkbutton(root, text=".log 파일 삭제", variable=log_var)

    # 체크박스 배치
    cache_check.pack(pady=5)
    cachestr_check.pack(pady=5)
    log_check.pack(pady=5)

    # 삭제 버튼 생성
    delete_button = Button(root, text="삭제 실행", command=confirm_delete)
    delete_button.pack(pady=10)

    # Tkinter 창 실행
    root.mainloop()


# 프로그램 실행
if __name__ == "__main__":
    create_gui()
