
import base64
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SOURCES = [
    # Pawdroid
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",

    # Surfboard / TGParse
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/ss",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/trojan",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/vless",

    # Open proxy lists
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_BASE64.txt",

    # Iran collectors
    "https://raw.githubusercontent.com/HosseinKoofi/GO_V2rayCollector/main/mixed_iran.txt",
    "https://raw.githubusercontent.com/HosseinKoofi/GO_V2rayCollector/main/vless_iran.txt",
    "https://raw.githubusercontent.com/HosseinKoofi/GO_V2rayCollector/main/ss_iran.txt",
    "https://raw.githubusercontent.com/Stinsonysm/GO_V2rayCollector/refs/heads/main/trojan_iran.txt",

    # EbraSha
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/ss_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/V2Ray-Config-By-EbraSha.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",

    # Argh94
    "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Vmess.txt",
    "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Hysteria2.txt",
    "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Germany.txt",

    # MhdiTaheri
    "https://raw.githubusercontent.com/MhdiTaheri/V2rayCollector_Py/refs/heads/main/sub/Mix/mix.txt",
    "https://raw.githubusercontent.com/MhdiTaheri/V2rayCollector_Py/refs/heads/main/sub/United%20States/config.txt",

    # KobaBi
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub_all.txt",

    # 10ium
    "https://raw.githubusercontent.com/10ium/ScrapeAndCategorize/refs/heads/main/output_configs/Hysteria2.txt",
    "https://raw.githubusercontent.com/10ium/ScrapeAndCategorize/refs/heads/main/output_configs/Vless.txt",
    "https://raw.githubusercontent.com/10ium/ScrapeAndCategorize/refs/heads/main/output_configs/ShadowSocks.txt",
    "https://raw.githubusercontent.com/10ium/ScrapeAndCategorize/refs/heads/main/output_configs/Trojan.txt",
    "https://raw.githubusercontent.com/10ium/V2ray-Config/main/Splitted-By-Protocol/hysteria2.txt",
    "https://raw.githubusercontent.com/10ium/V2Hub3/main/merged_base64",
    "https://raw.githubusercontent.com/10ium/V2Hub3/refs/heads/main/Split/Normal/shadowsocks",
    "https://raw.githubusercontent.com/10ium/V2Hub3/refs/heads/main/Split/Normal/reality",
    "https://raw.githubusercontent.com/10ium/base64-encoder/main/encoded/10ium_mixed_iran.txt",

    # Epodonios
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub1.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub2.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/Sub3.txt",

    # barry-far
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub2.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub3.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub4.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub6.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub7.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Sub8.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub9.txt",

    # MatnOfficial
    "https://raw.githubusercontent.com/aqayerez/MatnOfficial-VPN/refs/heads/main/MatnOfficial%23MatnOfficial",

    # Other public lists
    "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs.txt",
    "https://raw.githubusercontent.com/bamdad23/JavidnamanIran/refs/heads/main/WS%2BHysteria2",
    "https://raw.githubusercontent.com/mshojaei77/v2rayAuto/refs/heads/main/telegram/popular_channels_1",
    "https://raw.githubusercontent.com/mshojaei77/v2rayAuto/refs/heads/main/telegram/popular_channels_2",
    "https://raw.githubusercontent.com/mshojaei77/v2rayAuto/refs/heads/main/subs/hysteria",
    "https://raw.githubusercontent.com/mshojaei77/v2rayAuto/refs/heads/main/subs/hy2",
    "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/speed.txt",
    "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/hys-tuic.txt",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Reality",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Vless",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet_iOS.txt",
    "https://raw.githubusercontent.com/Proxydaemitelegram/Proxydaemi44/refs/heads/main/Proxydaemi44",
    "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/refs/heads/master/collected-proxies/xray-json-full/actives_all.json",
    "https://raw.githubusercontent.com/rango-cfs/NewCollector/refs/heads/main/v2ray_links.txt",
]

SCHEMES = (
    "vmess", "vless", "trojan", "ss", "ssr",
    "hysteria", "hysteria2", "tuic", "wireguard",
    "socks", "socks5", "http", "https", "anytls"
)

URI_PATTERN = re.compile(
    r"(?i)(?:"
    + "|".join(re.escape(s) for s in SCHEMES)
    + r")://[^\s\"'<>]+"
)

MAX_SOURCE_BYTES = 2_000_000
MAX_CONFIGS = 10_000
TIMEOUT = 15


def decode_base64(text):
    text = re.sub(r"\s+", "", text)

    if len(text) < 20:
        return None

    try:
        padded = text + "=" * (-len(text) % 4)
        raw = base64.b64decode(padded, validate=True)
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return None


def extract_configs(data):
    text = data.decode("utf-8", errors="ignore")
    found = []
    seen = set()
    queue = [text]

    # Try decoding whole subscription files and individual Base64 lines.
    for _ in range(3):
        if not queue:
            break

        current = queue
        queue = []

        for content in current:
            for match in URI_PATTERN.findall(content):
                config = match.rstrip(".,;)]}\"'")
                if config and config not in seen:
                    seen.add(config)
                    found.append(config)

            compact = re.sub(r"\s+", "", content)
            decoded = decode_base64(compact)

            if decoded and decoded != content:
                queue.append(decoded)

            # Some sources encode each config on a separate line.
            for line in content.splitlines()[:20000]:
                line = line.strip()

                if not line or "://" in line:
                    continue

                if len(line) > 30 and len(line) < 20000:
                    decoded_line = decode_base64(line)
                    if decoded_line:
                        queue.append(decoded_line)

    return found


def fetch_source(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 VPN-Subscription-Collector/2.0",
            "Accept": "*/*",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if response.status != 200:
                print(f"HTTP {response.status}: {url}")
                return url, []

            data = response.read(MAX_SOURCE_BYTES)

        configs = extract_configs(data)
        print(f"OK: {len(configs)} configs | {url}")
        return url, configs

    except Exception as exc:
        print(f"FAILED: {url} | {exc}")
        return url, []


def main():
    all_configs = []
    seen = set()
    failed = []
    source_results = []

    print(f"Starting collection from {len(SOURCES)} sources...")

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(fetch_source, url)
            for url in SOURCES
        ]

        for future in as_completed(futures):
            try:
                url, configs = future.result()
            except Exception as exc:
                print(f"Worker error: {exc}")
                continue

            source_results.append((url, len(configs)))

            if not configs:
                failed.append(url)

            for config in configs:
                config = config.strip()

                if config and config not in seen:
                    seen.add(config)
                    all_configs.append(config)

    if not all_configs:
        raise SystemExit(
            "No configs found. Existing output files were left unchanged."
        )

    all_configs = all_configs[:MAX_CONFIGS]

    plain_text = "\n".join(all_configs) + "\n"
    encoded_text = base64.b64encode(
        plain_text.encode("utf-8")
    ).decode("ascii") + "\n"

    Path("sub.txt").write_text(encoded_text, encoding="utf-8")

    report = [
        f"Unique configurations collected: {len(all_configs)}",
        f"Sources configured: {len(SOURCES)}",
        f"Sources returning zero configs: {len(failed)}",
        "",
        "Source results:",
    ]

    for url, count in sorted(source_results):
        report.append(f"{count:5d} | {url}")

    Path("count.txt").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8"
    )

    print()
    print(f"SUCCESS: {len(all_configs)} unique configs")
    print(f"Sources returning zero configs: {len(failed)}")
    print("Created: sub.txt, count.txt")


if __name__ == "__main__":
    main()
