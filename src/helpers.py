import os 

import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

del_paths = []

def check_path(path: str) -> bool:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    return True

def do_download(url: str, save_path: os.PathLike) -> str:
    """
    The function that actually does the downloading part.
    Uses rich progress bar to show the progress.
    param url: The URL to download
    :return: The path to the downloaded file.
    """
    try:
        progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            transient=True,
        )
        task_id = progress.add_task(url, filename=save_path)

        with progress:

            r = requests.get(url, stream=True)

            # Getting the content length to be marked as the total length of the download
            total = int(r.headers.get("content-length"), 0)
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        progress.update(task_id, total=total, completed=f.tell())

        del_paths.append(save_path)
        return save_path
    except Exception:
        res = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(res.content)
        del_paths.append(save_path)
        return save_path

def cleanup() -> None:
    """
    Deletes all the files that were downloaded.
    """
    for path in del_paths:
        os.remove(path)