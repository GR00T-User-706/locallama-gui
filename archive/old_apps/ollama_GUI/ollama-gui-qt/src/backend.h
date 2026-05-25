#ifndef BACKEND_H
#define BACKEND_H

#include <QObject>
#include <QProcess>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QTimer>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QStandardPaths>
#include <QFile>
#include <QFileInfo>
#include <QDir>
#include "OllamaManager.h"

class Backend : public QObject
{
    Q_OBJECT

    Q_PROPERTY(QStringList models READ models NOTIFY modelsChanged)
    Q_PROPERTY(QString currentModel READ currentModel WRITE setCurrentModel NOTIFY currentModelChanged)
    Q_PROPERTY(QString systemPrompt READ systemPrompt WRITE setSystemPrompt NOTIFY systemPromptChanged)
    Q_PROPERTY(QString userPrompt READ userPrompt WRITE setUserPrompt NOTIFY userPromptChanged)
    Q_PROPERTY(QString outputText READ outputText NOTIFY outputTextChanged)
    Q_PROPERTY(bool responseActive READ responseActive NOTIFY responseActiveChanged)
    Q_PROPERTY(bool serverRunning READ serverRunning NOTIFY serverRunningChanged)
    Q_PROPERTY(QString serverStatusText READ serverStatusText NOTIFY serverStatusTextChanged)
    Q_PROPERTY(QString serverStatusColor READ serverStatusColor NOTIFY serverStatusColorChanged)
    Q_PROPERTY(bool onlineMode READ onlineMode WRITE setOnlineMode NOTIFY onlineModeChanged)
    Q_PROPERTY(QString temperature READ temperature NOTIFY temperatureChanged)
    Q_PROPERTY(QString topP READ topP NOTIFY topPChanged)
    Q_PROPERTY(QString numCtx READ numCtx NOTIFY numCtxChanged)

    // New properties for UI enhancements
    Q_PROPERTY(bool modelLoading READ modelLoading NOTIFY modelLoadingChanged)
    Q_PROPERTY(QString modelInfoJson READ modelInfoJson NOTIFY modelInfoJsonChanged)
    Q_PROPERTY(bool modelInfoLoading READ modelInfoLoading NOTIFY modelInfoLoadingChanged)
    Q_PROPERTY(QString pullProgressText READ pullProgressText NOTIFY pullProgressTextChanged)
    Q_PROPERTY(double pullProgressCompleted READ pullProgressCompleted NOTIFY pullProgressCompletedChanged)
    Q_PROPERTY(double pullProgressTotal READ pullProgressTotal NOTIFY pullProgressTotalChanged)
    Q_PROPERTY(bool pullInProgress READ pullInProgress NOTIFY pullInProgressChanged)
    Q_PROPERTY(QString pushProgressText READ pushProgressText NOTIFY pushProgressTextChanged)
    Q_PROPERTY(bool pushInProgress READ pushInProgress NOTIFY pushInProgressChanged)
    Q_PROPERTY(QString createProgressText READ createProgressText NOTIFY createProgressTextChanged)
    Q_PROPERTY(bool createInProgress READ createInProgress NOTIFY createInProgressChanged)

public:
    explicit Backend(QObject *parent = nullptr);
    ~Backend();

    QStringList models() const { return m_models; }
    QString currentModel() const { return m_currentModel; }
    void setCurrentModel(const QString &model);
    QString systemPrompt() const { return m_systemPrompt; }
    void setSystemPrompt(const QString &prompt);
    QString userPrompt() const { return m_userPrompt; }
    void setUserPrompt(const QString &prompt);
    QString outputText() const { return m_outputText; }
    bool responseActive() const { return m_responseActive; }
    bool serverRunning() const { return m_serverRunning; }
    QString serverStatusText() const { return m_serverStatusText; }
    QString serverStatusColor() const { return m_serverStatusColor; }
    bool onlineMode() const { return m_onlineMode; }
    void setOnlineMode(bool online);
    QString temperature() const { return m_temperature; }
    QString topP() const { return m_topP; }
    QString numCtx() const { return m_numCtx; }

    // New property getters
    bool modelLoading() const { return m_modelLoading; }
    QString modelInfoJson() const { return m_modelInfoJson; }
    bool modelInfoLoading() const { return m_modelInfoLoading; }
    QString pullProgressText() const { return m_pullProgressText; }
    double pullProgressCompleted() const { return m_pullProgressCompleted; }
    double pullProgressTotal() const { return m_pullProgressTotal; }
    bool pullInProgress() const { return m_pullInProgress; }
    QString pushProgressText() const { return m_pushProgressText; }
    bool pushInProgress() const { return m_pushInProgress; }
    QString createProgressText() const { return m_createProgressText; }
    bool createInProgress() const { return m_createInProgress; }

    Q_INVOKABLE void checkAndStartServer();
    Q_INVOKABLE void toggleMode(bool online);
    Q_INVOKABLE void runChat();
    Q_INVOKABLE void interruptResponse();
    Q_INVOKABLE void loadSystemPromptFromFile(const QUrl &fileUrl);
    Q_INVOKABLE void clearChat();
    Q_INVOKABLE void showAvailableModels();
    Q_INVOKABLE void pullModel(const QString &modelName);
    Q_INVOKABLE void pushModel(const QString &modelName, const QString &namespace_ = QString());
    Q_INVOKABLE void createModel(const QString &name, const QString &modelfile);
    Q_INVOKABLE void copyModel(const QString &source, const QString &destination);
    Q_INVOKABLE void removeModel(const QString &modelName);
    Q_INVOKABLE void showModelInfo(const QString &modelName);
    Q_INVOKABLE void setParameter(const QString &param, const QString &value);
    Q_INVOKABLE void restartServer();
    Q_INVOKABLE void showServerOptions();
    Q_INVOKABLE void about();
    Q_INVOKABLE void refreshModels();
    Q_INVOKABLE void cancelCurrentOperation();
    Q_INVOKABLE void generateEmbedding(const QString &prompt, const QString &model = QString());
    Q_INVOKABLE void testConnection();

signals:
    void modelsChanged();
    void currentModelChanged();
    void systemPromptChanged();
    void userPromptChanged();
    void outputTextChanged();
    void responseActiveChanged();
    void serverRunningChanged();
    void serverStatusTextChanged();
    void serverStatusColorChanged();
    void onlineModeChanged();
    void temperatureChanged();
    void topPChanged();
    void numCtxChanged();

    // New signals
    void modelLoadingChanged();
    void modelInfoJsonChanged();
    void modelInfoLoadingChanged();
    void pullProgressTextChanged();
    void pullProgressCompletedChanged();
    void pullProgressTotalChanged();
    void pullInProgressChanged();
    void pushProgressTextChanged();
    void pushInProgressChanged();
    void createProgressTextChanged();
    void createInProgressChanged();

    void embeddingResultReady(const QString &summary);
    void connectionTestFinished(bool ok, const QString &message);
    void operationError(const QString &message);

private:
    // Internal helpers
    void appendOutput(const QString &text);
    void loadModelParams(const QString &model);

    OllamaManager *m_ollama;
    QNetworkAccessManager *m_netManager; // kept to pass to OllamaManager

    QStringList m_models;
    QString m_currentModel;
    QString m_systemPrompt;
    QString m_userPrompt;
    QString m_outputText;
    bool m_responseActive = false;
    bool m_serverRunning = false;
    QString m_serverStatusText;
    QString m_serverStatusColor;
    bool m_onlineMode = false;
    QString m_temperature = "0.7";
    QString m_topP = "0.9";
    QString m_numCtx = "8192";

    // New state
    bool m_modelLoading = false;
    QString m_modelInfoJson;
    bool m_modelInfoLoading = false;
    QString m_pullProgressText;
    double m_pullProgressCompleted = 0;
    double m_pullProgressTotal = 0;
    bool m_pullInProgress = false;
    QString m_pushProgressText;
    bool m_pushInProgress = false;
    QString m_createProgressText;
    bool m_createInProgress = false;
};

#endif // BACKEND_H