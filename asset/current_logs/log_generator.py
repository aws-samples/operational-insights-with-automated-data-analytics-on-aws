# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import random
from datetime import datetime, timedelta
import random
import socket
import struct

# This function is used to simulate an Application that generates logs in Apache Log Format

def random_datetime(start_datetime, end_datetime):
    time_format = "%d/%b/%Y:%H:%M:%S %z"

    start_datetime = datetime.strptime(start_datetime, time_format)
    end_datetime = datetime.strptime(end_datetime, time_format)
    time_delta = end_datetime - start_datetime
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    random_datetime = start_datetime + timedelta(seconds=random_seconds)

    return random_datetime.strftime(f"{time_format}")


constants = {
    "request": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE"],
    "endpoint": [
        "/v1/server",
        "/v1/server/admin",
        "/v1/server/admin/developer",
        "/v1/server/login",
        "/v1/server/register",
        "/v1/server/posts",
        "/v1/server/data",
        "/v1/server/playlists",
        "/v1/server/albums",
        "/v1/server/videos",
        "/v1/server/search",
    ],
    "statuscode": [
        "303",
        "404",
        "500",
        "403",
        "502",
        "304",
        "200",
        "201",
        "204",
        "302",
        "400",
        "407",
        "405",
        "504",
    ],
    "username": [
        "james",
        "adam",
        "eve",
        "alex",
        "smith",
        "isabella",
        "david",
        "angela",
        "donald",
        "hilary",
        "root",
        "warren",
        "dawson",
        "roger",
        "kaila",
        "shamar",
        "alyssa",
        "ariel",
        "albert",
        "omar",
        "kamora",
        "chase",
        "david",
        "bryce",
    ],
    "ua": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Mozilla/5.0 (Android 10; Mobile; rv:84.0) Gecko/84.0 Firefox/84.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4380.0 Safari/537.36 Edg/89.0.759.0",
        "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.12.4.5121",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329",
        "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 OPR/61.2.3076.56749",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.158 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) CriOS/91.0.4472.218 Mobile/15E148 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6; SM-G715U; Build/MOB30M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.1370.42 Mobile Safari/537.36 EdgA/106.0.1370.42",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.40 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:96.0.1) Gecko/20100101 Firefox/96.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.902.48 Safari/537.36 Edg/92.0.902.48",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) CriOS/95.0.4638.212 Mobile/15E148 Safari/537.36",
    ],
    "referrer": ["-", "www.example.com"],
}


def lambda_handler(event, context):
    for _ in range(0, 1000):
        log_line = '%s - %s [%s] "%s %s HTTP/1.1" %s %s "%s" "%s"\n' % (
            socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF))),
            random.choice(constants["username"]),
            random_datetime("01/Jan/2023:12:00:00 +1000", "31/Jul/2023:23:59:59 +1000"),
            random.choice(constants["request"]),
            random.choice(constants["endpoint"]),
            random.choice(constants["statuscode"]),
            str(int(random.gauss(5000, 50))),
            random.choice(constants["referrer"]),
            random.choice(constants["ua"]),
        )
        print(log_line)
