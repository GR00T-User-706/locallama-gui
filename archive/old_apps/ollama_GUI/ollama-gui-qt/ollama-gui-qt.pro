QT += qml quick widgets network core
CONFIG += c++17

TARGET = ollama-gui-qt
TEMPLATE = app

SOURCES += src/main.cpp \
           src/backend.cpp \
           src/OllamaManager.cpp

HEADERS += src/backend.h \
           src/OllamaManager.h

RESOURCES += src/resources.qrc

# Install desktop file and icon
desktop.files = assets/org.example.ollama-gui-qt.desktop
desktop.path = /usr/local/share/applications
icon.files = assets/ollama-gui-qt.png
icon.path = /usr/local/share/icons/hicolor/64x64/apps
INSTALLS += desktop icon