[app]
title = XvsO
package.name = xvso
package.domain = org.rogotuyt
source.dir = .
source.include_exts = py,png,jpg,kv,pkl
icon.filename = %(source.dir)s/icon.png
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions =
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
