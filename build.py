
import base64
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SOURCES = [
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/vless",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/ss",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/trojan",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_BASE64.txt",
    "https://raw.githubusercontent.com/HosseinKoofi/GO_V2rayCollector/main/mixed_iran.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/V2Ray-Config-By-EbraSha.txt",
    "https://raw.githubusercontent.com/10ium/V2ray-Config/main/Splitted-By-Protocol/hysteria2.txt",
]

SCHEMES = (
    "vmess", "vless", "trojan", "ss", "ssr",
    "hysteria", "hysteria2", "tuic", "wireguard",
    "socks", "http", "https", "anytls"
)

PATTERN = re.compile(
    r"(?i)\b(?:"
    + "|".join(SCHEMES)
    + r")://[^\s\"'<>]+"
)

MAX_SOURCE_BYTES = 700_000
MAX_CONFIGS = 3000


def extract_configs(data):
    text = data.decode("utf-8", errors="ignore")
    found = PATTERN.findall(text)

    if found:
        return found

    # بعضی منابع، اشتراک را به صورت Base64 منتشر می‌کنند.
    compact = re.sub(r"\s+", "", text)

    if len(compact) > 20:
        try:
            decoded = base64.b64decode(
                compact + "=" * (-len(compact) % 4),
                validate=True
            ).decode("utf-8", errors="ignore")

            return PATTERN.findall(decoded)
        except Exception:
            pass

    return []


def fetch_source(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if response.status != 200:
                print(f"HTTP {response.status}: {url}")
                return []

            data = response.read(MAX_SOURCE_BYTES)

        configs = extract_configs(data)
        print(f"Read {len(configs)} configs: {url}")
        return configs

    except Exception as exc:
        print(f"Source failed: {url} — {exc}")
        return []


def main():
    all_configs = []
    seen = set()

    # فقط چهار منبع هم‌زمان برای کاهش فشار منابع
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(fetch_source, url)
            for url in SOURCES
        ]

        for future in as_completed(futures):
            try:
                configs = future.result()
            except Exception as exc:
                print(f"Worker error: {exc}")
                continue

            for config in configs:
                config = config.strip().rstrip("),]")

                if config and config not in seen:
                    seen.add(config)
                    all_configs.append(config)

    if not all_configs:
        raise SystemExit(
            "No configurations found. Previous output files were not changed."
        )

    all_configs = all_configs[:MAX_CONFIGS]

    plain_text = "\n".join(all_configs) + "\n"
    encoded_text = base64.b64encode(
        plain_text.encode("utf-8")
    ).decode("ascii") + "\n"

    Path("sub.txt").write_text(
        encoded_text,
        encoding="utf-8"
    )

    Path("count.txt").write_text(
        f"Configurations collected: {len(all_configs)}\n",
        encoding="utf-8"
    )

    print(f"Success: {len(all_configs)} unique configs saved.")
    print("Output files: sub.txt, count.txt")


if __name__ == "__main__":
    main()
