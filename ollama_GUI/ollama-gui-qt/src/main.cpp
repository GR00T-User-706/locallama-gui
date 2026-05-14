#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QIcon>
#include "backend.h"

int main(int argc, char *argv[])
{
    // QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling); // deprecated in Qt6
    QGuiApplication app(argc, argv);
    app.setWindowIcon(QIcon(":/assets/ollama-gui-qt.png"));
    app.setApplicationVersion("1.0.0");
    Backend backend;
    backend.checkAndStartServer(); // initial server check

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("backend", &backend);
    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}