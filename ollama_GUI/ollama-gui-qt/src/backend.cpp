#include "backend.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QNetworkRequest>
#include <QProcess>
#include <QTimer>
#include <QFile>
#include <QDebug>
#include <QCoreApplication>

Backend::Backend(QObject *parent)
    : QObject(parent),
      m_netManager(new QNetworkAccessManager(this)),
      m_ollama(new OllamaManager(m_netManager, this))
{
    // Connect OllamaManager signals to Backend properties/signals
    connect(m_ollama, &OllamaManager::serverRunningChanged, this, [this](bool running) {
        m_serverRunning = running;
        emit serverRunningChanged();
    });
    connect(m_ollama, &OllamaManager::serverStatusChanged, this, [this](const QString &text, const QString &color) {
        if (m_serverStatusText != text) {
            m_serverStatusText = text;
            emit serverStatusTextChanged();
        }
        if (m_serverStatusColor != color) {
            m_serverStatusColor = color;
            emit serverStatusColorChanged();
        }
    });
    connect(m_ollama, &OllamaManager::onlineModeChanged, this, [this](bool online) {
        m_onlineMode = online;
        emit onlineModeChanged();
    });
    // Models
    connect(m_ollama, &OllamaManager::modelsLoaded, this, [this](const QStringList &names) {
        if (m_models != names) {
            m_models = names;
            emit modelsChanged();
            if (!names.isEmpty()) {
                if (m_currentModel.isEmpty() || !names.contains(m_currentModel)) {
                    m_currentModel = names.first();
                    emit currentModelChanged();
                    loadModelParams(m_currentModel);
                }
            }
        }
        appendOutput("[Models loaded]\n");
        if (!names.isEmpty())
            appendOutput(QString("[Models: %1]\n").arg(names.join(", ")));
    });
    // Chat
    connect(m_ollama, &OllamaManager::chatFinished, this, [this](const QString &response, bool interrupted, const QString &error) {
        if (interrupted)
            appendOutput("\n[INTERRUPTED]\n");
        else if (!error.isEmpty())
            appendOutput("[ERROR] " + error + "\n");
        else
            appendOutput(response + "\n");
        m_responseActive = false;
        emit responseActiveChanged();
    });
    connect(m_ollama, &OllamaManager::responseActiveChanged, this, [this](bool active) {
        m_responseActive = active;
        emit responseActiveChanged();
    });
    // Pull
    connect(m_ollama, &OllamaManager::pullProgressChanged, this, [this](const QString &status, double completed, double total) {
        m_pullProgressText = status;
        m_pullProgressCompleted = completed;
        m_pullProgressTotal = total;
        m_pullInProgress = true;
        emit pullProgressTextChanged();
        emit pullProgressCompletedChanged();
        emit pullProgressTotalChanged();
        emit pullInProgressChanged();
    });
    connect(m_ollama, &OllamaManager::pullFinished, this, [this](bool success, const QString &error) {
        m_pullInProgress = false;
        emit pullInProgressChanged();
        if (success) {
            appendOutput("[Pull completed]\n");
            refreshModels();
        } else {
            appendOutput("[Pull error: " + error + "]\n");
        }
    });
    // Push
    connect(m_ollama, &OllamaManager::pushProgressChanged, this, [this](const QString &status) {
        m_pushProgressText = status;
        m_pushInProgress = true;
        emit pushProgressTextChanged();
        emit pushInProgressChanged();
    });
    connect(m_ollama, &OllamaManager::pushFinished, this, [this](bool success, const QString &error) {
        m_pushInProgress = false;
        emit pushInProgressChanged();
        if (success)
            appendOutput("[Push completed]\n");
        else
            appendOutput("[Push error: " + error + "]\n");
    });
    // Create (and copy)
    connect(m_ollama, &OllamaManager::createProgressChanged, this, [this](const QString &status) {
        m_createProgressText = status;
        m_createInProgress = true;
        emit createProgressTextChanged();
        emit createInProgressChanged();
    });
    connect(m_ollama, &OllamaManager::createFinished, this, [this](bool success, const QString &error) {
        m_createInProgress = false;
        emit createInProgressChanged();
        if (success) {
            appendOutput("[Create completed]\n");
            refreshModels();
        } else {
            appendOutput("[Create error: " + error + "]\n");
        }
    });
    // Model info
    connect(m_ollama, &OllamaManager::modelInfoReady, this, [this](const QJsonObject &info) {
        QJsonDocument doc(info);
        m_modelInfoJson = QString::fromUtf8(doc.toJson(QJsonDocument::Compact));
        m_modelInfoLoading = false;
        emit modelInfoJsonChanged();
        emit modelInfoLoadingChanged();
    });
    connect(m_ollama, &OllamaManager::modelInfoError, this, [this](const QString &error) {
        m_modelInfoLoading = false;
        emit modelInfoLoadingChanged();
        emit operationError("Model info error: " + error);
    });
    // Model delete
    connect(m_ollama, &OllamaManager::modelDeleteFinished, this, [this](const QString &model, bool success, const QString &error) {
        if (success) {
            appendOutput("[Deleted " + model + "]\n");
            refreshModels();
        } else {
            appendOutput("[Delete error: " + error + "]\n");
        }
    });
    // Embeddings
    connect(m_ollama, &OllamaManager::embeddingReady, this, [this](const QString &model, const QJsonArray &embeddings) {
        // For simplicity, show a summary in output area
        QString summary = QString("Embedding for model '%1':\n").arg(model);
        // The first embedding's vector length
        QJsonArray first = embeddings.first().toArray();
        summary += QString("Vector length: %1\n").arg(first.size());
        // Show first few elements
        QStringList truncated;
        for (int i = 0; i < qMin(10, first.size()); ++i)
            truncated << QString::number(first[i].toDouble(), 'f', 6);
        summary += "First elements: [" + truncated.join(", ") + "] ...\n";
        appendOutput(summary);
        emit embeddingResultReady(summary);
    });
    connect(m_ollama, &OllamaManager::embeddingError, this, [this](const QString &error) {
        appendOutput("[Embedding error: " + error + "]\n");
    });
    // Diagnostics
    connect(m_ollama, &OllamaManager::connectionTestResult, this, [this](bool ok, const QString &msg) {
        emit connectionTestFinished(ok, msg);
        appendOutput("[Diagnostics] " + msg + "\n");
    });

    // Initial state sync
    m_ollama->checkAndStartServer();
}

Backend::~Backend()
{
}

void Backend::setCurrentModel(const QString &model)
{
    if (m_currentModel != model) {
        m_currentModel = model;
        emit currentModelChanged();
        loadModelParams(model);
    }
}

void Backend::setSystemPrompt(const QString &prompt)
{
    if (m_systemPrompt != prompt) {
        m_systemPrompt = prompt;
        emit systemPromptChanged();
    }
}

void Backend::setUserPrompt(const QString &prompt)
{
    if (m_userPrompt != prompt) {
        m_userPrompt = prompt;
        emit userPromptChanged();
    }
}

void Backend::setOnlineMode(bool online)
{
    if (m_onlineMode != online) {
        m_onlineMode = online;
        emit onlineModeChanged();
        m_ollama->setOnlineMode(online);
    }
}

void Backend::checkAndStartServer()
{
    m_ollama->checkAndStartServer();
}

void Backend::toggleMode(bool online)
{
    m_ollama->setOnlineMode(online);
}

void Backend::restartServer()
{
    m_ollama->restartServer();
}

void Backend::refreshModels()
{
    m_modelLoading = true;
    emit modelLoadingChanged();
    m_ollama->loadModels();
    // modelsLoaded signal will reset m_modelLoading
    connect(m_ollama, &OllamaManager::modelsLoaded, this, [this]() {
        m_modelLoading = false;
        emit modelLoadingChanged();
    }, Qt::SingleShotConnection); // one-shot to avoid multiple connects
}

void Backend::runChat()
{
    if (m_responseActive) return;
    if (m_userPrompt.trimmed().isEmpty()) return;
    appendOutput(QString("\n> %1\nThinking...\n").arg(m_userPrompt.trimmed()));
    m_ollama->runChat(m_systemPrompt, m_userPrompt, m_currentModel);
}

void Backend::interruptResponse()
{
    m_ollama->interruptChat();
}

void Backend::loadSystemPromptFromFile(const QUrl &fileUrl)
{
    QString path = fileUrl.toLocalFile();
    QFile file(path);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        setSystemPrompt(file.readAll());
        appendOutput(QString("[Loaded system prompt from %1]\n").arg(path));
    }
}

void Backend::clearChat()
{
    m_outputText.clear();
    emit outputTextChanged();
}

void Backend::showAvailableModels()
{
    // prints to output area
    QNetworkReply *reply = m_netManager->get(QNetworkRequest(QUrl(OllamaManager::TAGS_URL)));
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();
        appendOutput("\n--- Available Models ---\n");
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
            QJsonArray arr = doc.object().value("models").toArray();
            for (const QJsonValue &v : arr)
                appendOutput(QString("  %1\n").arg(v.toObject().value("name").toString()));
        } else {
            appendOutput("[Error fetching models]\n");
        }
    });
}

void Backend::pullModel(const QString &modelName)
{
    if (modelName.trimmed().isEmpty()) return;
    appendOutput("[Pulling " + modelName + "...]\n");
    m_ollama->pullModel(modelName.trimmed());
}

void Backend::pushModel(const QString &modelName, const QString &namespace_)
{
    m_ollama->pushModel(modelName, namespace_);
}

void Backend::createModel(const QString &name, const QString &modelfile)
{
    m_ollama->createModel(name, modelfile);
}

void Backend::copyModel(const QString &source, const QString &destination)
{
    // copy is create with modelfile "FROM source"
    QString modelfile = QString("FROM %1\n").arg(source);
    m_ollama->createModel(destination, modelfile);
    // We reuse create signals; any success will refresh models.
}

void Backend::removeModel(const QString &modelName)
{
    if (modelName.trimmed().isEmpty()) return;
    m_ollama->deleteModel(modelName.trimmed());
}

void Backend::showModelInfo(const QString &modelName)
{
    if (modelName.isEmpty()) return;
    m_modelInfoLoading = true;
    m_modelInfoJson.clear();
    emit modelInfoLoadingChanged();
    emit modelInfoJsonChanged();
    m_ollama->showModelInfo(modelName);
}

void Backend::setParameter(const QString &param, const QString &value)
{
    if (m_currentModel.isEmpty()) return;
    QString base = m_ollama->modelsPath();
    QString configPath = base + "/manifests/registry.ollama.ai/library/" + m_currentModel + "/config.json";
    QFile file(configPath);
    QJsonObject cfg;
    if (file.open(QIODevice::ReadOnly)) {
        cfg = QJsonDocument::fromJson(file.readAll()).object();
        file.close();
    }
    cfg[param] = value;
    if (file.open(QIODevice::WriteOnly)) {
        file.write(QJsonDocument(cfg).toJson());
        file.close();
        appendOutput(QString("[%1=%2 saved for %3]\n").arg(param, value, m_currentModel));
        loadModelParams(m_currentModel);
    } else {
        appendOutput("[Error writing config file]\n");
    }
    qWarning() << "Direct config file modification risk: path" << configPath;
}

void Backend::loadModelParams(const QString &model)
{
    if (model.isEmpty()) return;
    QString base = m_ollama->modelsPath();
    QString configPath = base + "/manifests/registry.ollama.ai/library/" + model + "/config.json";
    QFile file(configPath);
    m_temperature = "0.7";
    m_topP = "0.9";
    m_numCtx = "8192";
    if (file.open(QIODevice::ReadOnly)) {
        QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
        file.close();
        QJsonObject cfg = doc.object();
        m_temperature = cfg.value("temperature").toString(m_temperature);
        m_topP = cfg.value("top_p").toString(m_topP);
        m_numCtx = cfg.value("num_ctx").toString(m_numCtx);
    }
    emit temperatureChanged();
    emit topPChanged();
    emit numCtxChanged();
}

void Backend::cancelCurrentOperation()
{
    m_ollama->cancelCurrentOperation();
}

void Backend::generateEmbedding(const QString &prompt, const QString &model)
{
    QString mdl = model.isEmpty() ? m_currentModel : model;
    if (mdl.isEmpty()) {
        appendOutput("[No model selected for embedding]\n");
        return;
    }
    m_ollama->generateEmbedding(prompt, mdl);
}

void Backend::testConnection()
{
    m_ollama->testConnection();
}

void Backend::showServerOptions() {}
void Backend::about() {}

void Backend::appendOutput(const QString &text)
{
    m_outputText += text;
    emit outputTextChanged();
}