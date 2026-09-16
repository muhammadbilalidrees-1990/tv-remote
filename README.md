# TV Remote (Samsung Tizen) — Flutter prototype

Controls Samsung smart TVs (2016+) over Wi-Fi. Android + iOS.

## What works

| Feature | How |
|---|---|
| Find TV | SSDP scan, falls back to Wi-Fi subnet scan, or manual IP |
| Pairing | TV shows "Allow" once; token saved on phone |
| Keys | D-pad, OK, back, home, settings, vol/ch (hold to repeat), mute, guide, number pad, media keys, source |
| Keyboard | Type on TV (search, email, passwords); opens by itself when a TV text field is focused (models that report it); paste, hide-text, session-only recent entries |
| Apps | Netflix, YouTube, Prime Video, Disney+, Spotify |
| Power | Off via key; on via Wake-on-LAN, then auto-reconnect |
| Auto-reconnect | On app start (last TV) and when app returns to foreground |

## Setup

```bash
flutter create tv_remote
cd tv_remote
# copy this folder's pubspec.yaml and lib/ over the generated ones
rm test/widget_test.dart          # generated test references the old counter app
flutter pub get
```

### Android — `android/app/src/main/AndroidManifest.xml`

Above `<application>`:

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE"/>
```

On the `<application ...>` tag add (older TVs use plain `ws://` / `http://`):

```xml
android:usesCleartextTraffic="true"
```

### iOS — `ios/Runner/Info.plist`

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>Used to find and control your TV on this Wi-Fi network.</string>
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsLocalNetworking</key>
  <true/>
</dict>
```

iOS asks for Local Network permission the first time. If the first scan finds nothing, allow it and tap scan again.

## Run

```bash
flutter run            # phone must be on the same Wi-Fi as the TV
```

## TV settings to check

- Settings > General > External Device Manager > Device Connection Manager: access notification ON
- Settings > General > Network > Expert Settings > **Power On with Mobile**: ON (needed to turn the TV on)

## Test checklist (real TV required)

1. First connect shows Allow on TV; press Allow; dot turns blue
2. Kill and reopen app; connects with no prompt (token reused)
3. Hold Vol +; volume keeps rising
4. Power off; wait 30 s; Power on; TV wakes and remote reconnects
5. Focus the TV's search box; keyboard sheet opens (or tap the keyboard key); typed text appears on TV
6. Each app button opens the right app (IDs vary by region; fix in `remote_screen.dart`)
7. Deny on TV; app shows the unblock instructions

## Known limits

- **iOS SSDP and Wake-on-LAN** need Apple's `com.apple.developer.networking.multicast` entitlement (request from Apple). Without it, discovery uses the subnet scan and power-on may not work.
- Pre-2016 Samsung TVs (port 55000 protocol) are not supported.
- App IDs differ by model/region.
- Auto-open keyboard depends on the TV sending focus events; some models don't, so use the keyboard button.
- Some apps (e.g. Netflix, YouTube) use their own on-screen keyboards and may ignore typed text.
- No touchpad yet.
- Store listing: don't use "Samsung" in the app name or icon.

## Files

```
lib/
  main.dart                      app + theme
  models/tv_device.dart          TV info model
  services/discovery.dart        SSDP + subnet scan + probe
  services/samsung_remote.dart   WebSocket, pairing, keys, apps, power
  services/wake_on_lan.dart      magic packet
  screens/remote_screen.dart     main remote
  screens/devices_screen.dart    pick / add TV
  widgets/remote_key.dart        key, D-pad, rocker
  widgets/keyboard_sheet.dart    type-on-TV sheet
  widgets/palette.dart           colors
```
