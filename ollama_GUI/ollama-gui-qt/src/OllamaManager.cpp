#include "OllamaManager.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QNetworkRequest>
#include <QProcess>
#include <QTimer>
#include <QFile>
#include <QFileInfo>
#include <QDir>
#include <QStandardPaths>
#include <QDebug>

const QString OllamaManager::BASE_URL = QStringLiteral("http://127.0.0.1:11434/api");
const QString OllamaManager::TAGS_URL = BASE_URL + "/tags";
const QString OllamaManager::CHAT_URL = BASE_URL + "/chat";
const QString OllamaManager::SHOW_URL = BASE_URL + "/show";
const QString OllamaManager::DELETE_URL = BASE_URL + "/delete";
const QString OllamaManager::PULL_URL = BASE_URL + "/pull";
const QString OllamaManager::PUSH_URL = BASE_URL + "/push";
const QString OllamaManager::CREATE_URL = BASE_URL + "/create";
const QString OllamaManager::EMBED_URL = BASE_URL + "/embed";
const QString OllamaManager::OFFLINE_MODELS_PATH = QStringLiteral("/home/lykthornyx/.ollama/models");

OllamaManager::OllamaManager(QNetworkAccessManager *net, QObject *parent)
    : QObject(parent), m_netManager(net)
{
    updateStatus();
}

OllamaManager::~OllamaManager()
{
    stopServer();
}

// ---- Server Management ----
void OllamaManager::startOllama()
{
    stopOllama();
    m_ollamaProcess = new QProcess(this);
    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    if (!m_onlineMode) {
        env.insert("OLLAMA_HOME", OFFLINE_MODELS_PATH);
        env.insert("OLLAMA_MODELS", OFFLINE_MODELS_PATH);
    }
    env.insert("OLLAMA_HOST", "127.0.0.1:11434");
    m_ollamaProcess->setProcessEnvironment(env);
    m_ollamaProcess->start("ollama", {"serve"});
    qDebug() << "Started ollama serve";
}

void OllamaManager::stopOllama()
{
    if (m_ollamaProcess) {
        qDebug() << "Stopping ollama process";
        m_ollamaProcess->terminate();
        if (!m_ollamaProcess->waitForFinished(5000)) {
            m_ollamaProcess->kill();
            m_ollamaProcess->waitForFinished();
        }
        m_ollamaProcess->deleteLater();
        m_ollamaProcess = nullptr;
    }
    setServerRunning(false);
}

void OllamaManager::checkAndStartServer()
{
    QNetworkReply *reply = m_netManager->get(QNetworkRequest(QUrl(TAGS_URL)));
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();
        if (reply->error() == QNetworkReply::NoError) {
            setServerRunning(true);
            loadModels();
        } else {
            qDebug() << "Server not running, trying systemctl restart";
            QProcess *sysctl = new QProcess(this);
            sysctl->start("systemctl", {"reload-or-restart", "ollama"});
            connect(sysctl, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
                    this, [this, sysctl](int, QProcess::ExitStatus) {
                        sysctl->deleteLater();
                        waitForServer();
                    });
        }
    });
}

void OllamaManager::waitForServer()
{
    if (m_waitTimer) {
        m_waitTimer->stop();
        m_waitTimer->deleteLater();
    }
    m_waitCount = 0;
    m_waitTimer = new QTimer(this);
    connect(m_waitTimer, &QTimer::timeout, this, [this]() {
        m_waitCount++;
        if (m_waitCount > 20) {
            m_waitTimer->stop();
            m_waitTimer->deleteLater();
            m_waitTimer = nullptr;
            setServerRunning(false);
            updateStatus();
            qWarning() << "waitForServer timeout";
            return;
        }
        QNetworkReply *reply = m_netManager->get(QNetworkRequest(QUrl(TAGS_URL)));
        connect(reply, &QNetworkReply::finished, this, [this, reply]() {
            reply->deleteLater();
            if (reply->error() == QNetworkReply::NoError) {
                if (m_waitTimer) {
                    m_waitTimer->stop();
                    m_waitTimer->deleteLater();
                    m_waitTimer = nullptr;
                }
                setServerRunning(true);
                loadModels();
                updateStatus();
            }
        });
    });
    m_waitTimer->start(500);
}

void OllamaManager::setOnlineMode(bool online)
{
    if (m_onlineMode != online) {
        m_onlineMode = online;
        emit onlineModeChanged(online);
        qDebug() << "Switching to" << (online ? "online" : "offline") << "mode";
        startOllama();
        waitForServer();
    }
}

void OllamaManager::restartServer()
{
    setOnlineMode(m_onlineMode);
}

void OllamaManager::stopServer()
{
    stopOllama();
}

void OllamaManager::setServerRunning(bool running)
{
    if (m_serverRunning != running) {
        m_serverRunning = running;
        emit serverRunningChanged(running);
        updateStatus();
    }
}

void OllamaManager::updateStatus()
{
    QString text, color;
    if (m_serverRunning) {
        text = m_onlineMode ? QStringLiteral("\xF0\x9F\x9F\xA2 Online")   // 🟢
                            : QStringLiteral("\xF0\x9F\x9F\xA1 Offline"); // 🟡
        color = m_onlineMode ? "green" : "orange";
    } else {
        text = QStringLiteral("\xE2\x9A\xAB Server stopped"); // ⚫
        color = "gray";
    }
    if (m_serverStatusText != text || m_serverStatusColor != color) {
        m_serverStatusText = text;
        m_serverStatusColor = color;
        emit serverStatusChanged(text, color);
    }
}

QString OllamaManager::modelsPath() const
{
    return m_onlineMode ? QStandardPaths::writableLocation(QStandardPaths::HomeLocation) + "/.ollama/models"
                        : OFFLINE_MODELS_PATH;
}

// ---- Models ----
void OllamaManager::loadModels()
{
    QNetworkReply *reply = m_netManager->get(QNetworkRequest(QUrl(TAGS_URL)));
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            QStringList names;
            for (const QJsonValue &val : doc.object().value("models").toArray())
                names.append(val.toObject().value("name").toString());
            emit modelsLoaded(names);
        } else {
            qWarning() << "loadModels error:" << reply->errorString();
            emit modelsLoaded({}); // empty list as error indicator
        }
    });
}

void OllamaManager::deleteModel(const QString &name)
{
    QNetworkRequest req{QUrl(DELETE_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = name;
    QNetworkReply *reply = m_netManager->deleteResource(req);
    connect(reply, &QNetworkReply::finished, this, [this, name, reply]() {
        reply->deleteLater();
        bool success = (reply->error() == QNetworkReply::NoError);
        QString error = success ? QString() : reply->errorString();
        emit modelDeleteFinished(name, success, error);
    });
}

void OllamaManager::pullModel(const QString &name)
{
    if (m_pullReply) {
        qWarning() << "Pull already in progress";
        return;
    }
    QNetworkRequest req{QUrl(PULL_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = name;
    body["stream"] = true;
    m_pullReply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(m_pullReply, &QNetworkReply::finished, this, [this]() {
        if (m_pullReply) {
            QNetworkReply *reply = m_pullReply;
            m_pullReply = nullptr;
            bool success = (reply->error() == QNetworkReply::NoError);
            QString error = success ? QString() : reply->errorString();
            emit pullFinished(success, error);
            reply->deleteLater();
        }
    });
    connect(m_pullReply, &QNetworkReply::readyRead, this, &OllamaManager::onPullReadyRead);
}

void OllamaManager::onPullReadyRead()
{
    if (!m_pullReply) return;
    m_pullBuffer.append(m_pullReply->readAll());
    parseStreamResponse(m_pullReply, m_pullBuffer, [this](const QJsonObject &obj) {
        QString status = obj.value("status").toString();
        double completed = obj.value("completed").toDouble(0);
        double total = obj.value("total").toDouble(0);
        emit pullProgressChanged(status, completed, total);
    });
}

void OllamaManager::pushModel(const QString &name, const QString &namespace_)
{
    if (m_pushReply) {
        qWarning() << "Push already in progress";
        return;
    }
    QNetworkRequest req{QUrl(PUSH_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = name;
    body["stream"] = true;
    if (!namespace_.isEmpty()) body["namespace"] = namespace_;
    m_pushReply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(m_pushReply, &QNetworkReply::finished, this, [this]() {
        if (m_pushReply) {
            QNetworkReply *reply = m_pushReply;
            m_pushReply = nullptr;
            bool success = (reply->error() == QNetworkReply::NoError);
            emit pushFinished(success, success ? QString() : reply->errorString());
            reply->deleteLater();
        }
    });
    connect(m_pushReply, &QNetworkReply::readyRead, this, &OllamaManager::onPushReadyRead);
}
void OllamaManager::onChatReadyRead()
{
    if (!m_chatReply) return;
    m_chatBuffer.append(m_chatReply->readAll());
    // For streaming chat, each line is a JSON object with a "message" field.
    // We'll parse and emit incremental updates if needed.
    parseStreamResponse(m_chatReply, m_chatBuffer, [this](const QJsonObject &obj) {
        QString content = obj.value("message").toObject().value("content").toString();
        if (!content.isEmpty()) {
            emit chatOutputAppended(content);
        }
    });
}
void OllamaManager::onPushReadyRead()
{
    if (!m_pushReply) return;
    m_pushBuffer.append(m_pushReply->readAll());
    parseStreamResponse(m_pushReply, m_pushBuffer, [this](const QJsonObject &obj) {
        QString status = obj.value("status").toString();
        emit pushProgressChanged(status);
    });
}

void OllamaManager::createModel(const QString &name, const QString &modelfile)
{
    if (m_createReply) {
        qWarning() << "Create already in progress";
        return;
    }
    QNetworkRequest req{QUrl(CREATE_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = name;
    body["modelfile"] = modelfile;
    body["stream"] = true;
    m_createReply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(m_createReply, &QNetworkReply::finished, this, [this]() {
        if (m_createReply) {
            QNetworkReply *reply = m_createReply;
            m_createReply = nullptr;
            bool success = (reply->error() == QNetworkReply::NoError);
            emit createFinished(success, success ? QString() : reply->errorString());
            reply->deleteLater();
        }
    });
    connect(m_createReply, &QNetworkReply::readyRead, this, &OllamaManager::onCreateReadyRead);
}

void OllamaManager::onCreateReadyRead()
{
    if (!m_createReply) return;
    m_createBuffer.append(m_createReply->readAll());
    parseStreamResponse(m_createReply, m_createBuffer, [this](const QJsonObject &obj) {
        QString status = obj.value("status").toString();
        emit createProgressChanged(status);
    });
}

void OllamaManager::copyModel(const QString &source, const QString &destination)
{
    QString modelfile = QString("FROM %1\n").arg(source);
    createModel(destination, modelfile);
    // copyFinished will be emitted by createFinished; we could also alias signals.
    // For simplicity we reuse create progress signals; a wrapper slot will emit copyFinished.
    // We'll connect a one-shot signal.
    // Since copy uses create internally, we will emit copyFinished on createFinished.
    // However, we need a different signal. Easiest: connect a local slot.
    // Implementation below:
    // We'll set a temporary flag and in the createFinished connection emit copyFinished.
    // But to keep it clean, we'll just call createModel and in the finished connection emit copyFinished.
    // We'll handle in the finished slot.
    // Use a helper lambda.
    if (!m_createReply) {
        // createModel already started, modify finished connection later.
        // We'll rely on createFinished signal; in backend we know if it's a copy operation by context.
    }
    // For simplicity, we'll just connect the createFinished to emit copyFinished with success.
    // To avoid signal overload, we'll connect a lambda that disconnects after execution.
    // Implementation later in Backend.
}

void OllamaManager::cancelCurrentOperation()
{
    if (m_pullReply) {
        m_pullReply->abort();
        m_pullReply = nullptr;
    }
    if (m_pushReply) {
        m_pushReply->abort();
        m_pushReply = nullptr;
    }
    if (m_createReply) {
        m_createReply->abort();
        m_createReply = nullptr;
    }
    if (m_chatReply) {
        m_chatReply->abort();
        m_chatReply = nullptr;
    }
}

void OllamaManager::showModelInfo(const QString &name)
{
    QNetworkRequest req{QUrl(SHOW_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = name;
    QNetworkReply *reply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            emit modelInfoReady(doc.object());
        } else {
            emit modelInfoError(reply->errorString());
        }
    });
}

// ---- Chat ----
void OllamaManager::runChat(const QString &system, const QString &user, const QString &model)
{
    if (m_chatReply) {
        qWarning() << "Chat already active";
        return;
    }
    QNetworkRequest req{QUrl(CHAT_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject msg1, msg2;
    msg1["role"] = "system";
    msg1["content"] = system;
    msg2["role"] = "user";
    msg2["content"] = user.trimmed();
    QJsonObject body;
    body["model"] = model;
    body["messages"] = QJsonArray{msg1, msg2};
    body["stream"] = true;
    m_chatReply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(m_chatReply, &QNetworkReply::readyRead, this, &OllamaManager::onChatReadyRead);
    connect(m_chatReply, &QNetworkReply::finished, this, [this]() {
        QNetworkReply *reply = m_chatReply;
        m_chatReply = nullptr;
        QString result;
        bool interrupted = false;
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            result = doc.object().value("message").toObject().value("content").toString();
            if (result.isEmpty()) result = "[ERROR] Empty response";
        } else {
            if (reply->error() == QNetworkReply::OperationCanceledError)
                interrupted = true;
            else
                result = "[ERROR] " + reply->errorString();
        }
        emit chatFinished(result, interrupted, reply->errorString());
        emit responseActiveChanged(false);
        reply->deleteLater();
    });
    emit responseActiveChanged(true);
}

void OllamaManager::interruptChat()
{
    if (m_chatReply) {
        m_chatReply->abort();
        m_chatReply = nullptr;
        emit chatFinished(QString(), true, "Interrupted");
        emit responseActiveChanged(false);
    }
}

// ---- Embeddings ----
void OllamaManager::generateEmbedding(const QString &prompt, const QString &model)
{
    QNetworkRequest req{QUrl(EMBED_URL)};
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject body;
    body["model"] = model;
    body["input"] = prompt;
    QNetworkReply *reply = m_netManager->post(req, QJsonDocument(body).toJson());
    connect(reply, &QNetworkReply::finished, this, [this, reply, model]() {
        reply->deleteLater();
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            QJsonArray embeddings = doc.object().value("embeddings").toArray();
            if (embeddings.isEmpty()) {
                emit embeddingError("No embeddings returned");
            } else {
                emit embeddingReady(model, embeddings);
            }
        } else {
            emit embeddingError(reply->errorString());
        }
    });
}

// ---- Diagnostics ----
void OllamaManager::testConnection()
{
    QNetworkReply *reply = m_netManager->get(QNetworkRequest(QUrl(TAGS_URL)));
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();
        if (reply->error() == QNetworkReply::NoError) {
            emit connectionTestResult(true, "OLLAMA server is reachable at localhost:11434");
        } else {
            emit connectionTestResult(false, "Cannot connect to OLLAMA: " + reply->errorString());
        }
    });
}

// ---- Helper for stream parsing ----
void OllamaManager::parseStreamResponse(QNetworkReply *reply, QByteArray &buffer,
                                         const std::function<void(const QJsonObject&)> &callback)
{
    (void)reply;
    while (buffer.contains('\n')) {
        int idx = buffer.indexOf('\n');
        QByteArray line = buffer.left(idx).trimmed();
        buffer.remove(0, idx + 1);
        if (line.isEmpty()) continue;
        QJsonParseError err;
        QJsonDocument doc = QJsonDocument::fromJson(line, &err);
        if (err.error == QJsonParseError::NoError) {
            callback(doc.object());
        } else {
            qWarning() << "Stream JSON parse error:" << err.errorString();
        }
    }
}