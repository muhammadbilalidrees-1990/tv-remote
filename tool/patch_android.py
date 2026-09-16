#!/usr/bin/env python3
"""Patch the AndroidManifest that `flutter create` generates."""

import re
import sys
from pathlib import Path

MANIFEST = Path("android/app/src/main/AndroidManifest.xml")

PERMISSIONS = [
    ("android.permission.INTERNET", "talk to the TV"),
    ("android.permission.ACCESS_NETWORK_STATE", "know when Wi-Fi drops"),
    ("android.permission.ACCESS_WIFI_STATE", "read the subnet for scanning"),
    ("android.permission.CHANGE_WIFI_MULTICAST_STATE", "SSDP discovery"),
]

APP_LABEL = "TV Remote"


def fail(message: str) -> None:
    print(f"patch_android: ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail(f"{MANIFEST} not found. Run `flutter create --platforms=android .` first.")

    xml = MANIFEST.read_text(encoding="utf-8")
    original = xml

    opening = re.search(r"<manifest\b[^>]*>", xml)
    if not opening:
        fail("could not find the <manifest> opening tag")

    to_add = [
        f'    <!-- {why} -->\n    <uses-permission android:name="{name}" />'
        for name, why in PERMISSIONS
        if name not in xml
    ]
    if to_add:
        block = "\n" + "\n".join(to_add) + "\n"
        xml = xml[: opening.end()] + block + xml[opening.end() :]

    if "usesCleartextTraffic" not in xml:
        xml, count = re.subn(
            r"(<application\b)",
            r'\1\n        android:usesCleartextTraffic="true"',
            xml,
            count=1,
        )
        if count == 0:
            fail("could not find the <application> tag")

    xml = re.sub(r'android:label="[^"]*"', f'android:label="{APP_LABEL}"', xml, count=1)

    if xml == original:
        print("patch_android: nothing to change, manifest already patched")
        return

    MANIFEST.write_text(xml, encoding="utf-8")
    print("patch_android: manifest patched")
    for name, _ in PERMISSIONS:
        print(f"  + {name}")
    print("  + android:usesCleartextTraffic=true")
    print(f'  + android:label="{APP_LABEL}"')


if __name__ == "__main__":
    main()
