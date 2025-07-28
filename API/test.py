import platform
import psutil
import shutil


def disk():
    try: 
        partitions = psutil.disk_partitions(all=False)
        # token = request.headers['Authorization']
        # check_token(token)
        if platform.system() == 'Windows':
            for partition in partitions:
                usage = shutil.disk_usage(partition.mountpoint)
                print(f"Всего: {usage.total / (2**30):.2f} GB")
                print(f"Использовано: {usage.used / (2**30):.2f} GB")
        elif platform.system() == 'Linux':
            disk_info = shutil.disk_usage('/') 
            print(f"Всего: {disk_info.total / (2**30):.2f} GB")
            print(f"Использовано: {disk_info.used / (2**30):.2f} GB")

    except Exception as e:
        print(str(e))

disk()
