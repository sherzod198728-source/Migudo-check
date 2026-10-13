#!/usr/bin/env bash
# Kalkulyator APK'sini yig'adi. Kerak: aapt, dalvik-exchange, zipalign, apksigner,
# android-sdk-platform-23 (Ubuntu: apt-get install aapt apksigner zipalign android-sdk-platform-23 dalvik-exchange)
# Ishlatish: KEYSTORE=kalit.jks KS_PASS=parol ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
ANDROID_JAR=/usr/lib/android-sdk/platforms/android-23/android.jar
OUT=build
rm -rf "$OUT" && mkdir -p "$OUT/gen" "$OUT/classes" "$OUT/assets"
cp ../kalkulyator.html "$OUT/assets/"

aapt package -f -m -J "$OUT/gen" -M AndroidManifest.xml -S res -I "$ANDROID_JAR" \
  -A "$OUT/assets" -F "$OUT/unsigned.apk" -0 arsc
javac -nowarn -Xlint:-options -source 8 -target 8 -bootclasspath "$ANDROID_JAR" \
  -d "$OUT/classes" $(find src "$OUT/gen" -name '*.java')
dalvik-exchange --dex --min-sdk-version=21 --output="$OUT/classes.dex" "$OUT/classes"
(cd "$OUT" && aapt add unsigned.apk classes.dex >/dev/null)

zipalign -f -p 4 "$OUT/unsigned.apk" "$OUT/aligned.apk"
apksigner sign --ks "${KEYSTORE:-kalit.jks}" --ks-pass "pass:${KS_PASS:?KS_PASS kerak}" \
  --out ../Kalkulyator.apk "$OUT/aligned.apk"
apksigner verify --print-certs ../Kalkulyator.apk | head -1
echo "Tayyor: ../Kalkulyator.apk"
