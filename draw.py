#!/usr/bin/env python3

import os
import subprocess
import sys
from datetime import datetime, timedelta

import cv2
from tqdm import tqdm

if __name__ == "__main__":

    # Load the image and convert it to grayscale
    img = cv2.imread(sys.argv[1])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Make the start date be not last sunday, but the one before
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = today - timedelta(days=(today.isoweekday() + 1))

    # Loop through each of the pixels and work out a corresponding date
    commit_dates = []
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):

            c = img[y, x]
            d = start + timedelta(weeks=-(img.shape[1] - x), days=y)
            for i in range(c):
                commit_dates.append(d.isoformat())

    for d in tqdm(commit_dates, desc="Committing", unit="commit", dynamic_ncols=True):
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", d],
            env={
                **os.environ,
                "GIT_AUTHOR_DATE": d,
                "GIT_COMMITTER_DATE": d,
            },
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
