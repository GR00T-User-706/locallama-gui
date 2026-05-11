#ifndef OLLAMAMANAGER_H
#define OLLAMAMANAGER_H

#include <QObject>
#include <QProcess>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QTimer>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

class OllamaManager : public QObject
{
    Q_OBJECT
public:
    explicit OllamaManager(QNetworkAccessManager *net, QObject *parent = nullptr);
    ~OllamaManager();

    // Server
    Q_INVOKABLE void checkAndStartServer();
    Q_INVOKABLE void stopServer();
    Q_INVOKABLE void restartServer(); // toggleMode to its current onlineMode
    Q_INVOKABLE void setOnlineMode(bool online);

    // Models
    Q_INVOKABLE void loadModels();
    Q_INVOKABLE void deleteModel(const QString &name);
    Q_INVOKABLE void pullModel(const QString &name);
    Q_INVOKABLE void pushModel(const QString &name, const QString &namespace_ = QString());
    Q_INVOKABLE void createModel(const QString &name, const QString &modelfile);
    Q_INVOKABLE void copyModel(const QString &source, const QString &destination);
    Q_INVOKABLE void showModelInfo(const QString &name);
    Q_INVOKABLE void cancelCurrentOperation();

    // Chat
    Q_INVOKABLE void runChat(const QString &system, const QString &user, const QString &model);
    Q_INVOKABLE void interruptChat();

    // Embeddings
    Q_INVOKABLE void generateEmbedding(const QString &prompt, const QString &model);

    // Diagnostics
    Q_INVOKABLE void testConnection();

signals:
    // Server
    void serverRunningChanged(bool running);
    void serverStatusChanged(const QString &text, const QString &color);
    void onlineModeChanged(bool online);

    // Models
    void modelsLoaded(const QStringList &models);
    void modelDeleteFinished(const QString &model, bool success, const QString &error);
    void pullProgressChanged(const QString &statusText, double completed, double total);
    void pullFinished(bool success, const QString &error);
    void pushProgressChanged(const QString &statusText);
    void pushFinished(bool success, const QString &error);
    void createProgressChanged(const QString &statusText);
    void createFinished(bool success, const QString &error);
    void copyFinished(bool success, const QString &error);
    void modelInfoReady(const QJsonObject &info);
    void modelInfoError(const QString &error);

    // Chat
    void chatOutputAppended(const QString &text);
    void chatFinished(const QString &response, bool interrupted, const QString &error);
    void responseActiveChanged(bool active);

    // Embeddings
    void embeddingReady(const QString &model, const QJsonArray &embeddings);
    void embeddingError(const QString &error);

    // Diagnostics
    void connectionTestResult(bool ok, const QString &message);

private slots:
    void onPullReadyRead();
    void onPushReadyRead();
    void onCreateReadyRead();
    void onChatReadyRead();  // not used for streaming chat, kept for future

private:
    void startOllama();
    void stopOllama();
    void waitForServer();
    void setServerRunning(bool running);
    void updateStatus();
    QString modelsPath() const;
    void parseStreamResponse(QNetworkReply *reply, QByteArray &buffer,
                             const std::function<void(const QJsonObject&)> &callback);

    QNetworkAccessManager *m_netManager;
    QProcess *m_ollamaProcess = nullptr;
    QTimer *m_waitTimer = nullptr;
    int m_waitCount = 0;

    bool m_onlineMode = false;
    bool m_serverRunning = false;
    QString m_serverStatusText;
    QString m_serverStatusColor;

    // Active requests (for cancellation)
    QNetworkReply *m_pullReply = nullptr;
    QNetworkReply *m_pushReply = nullptr;
    QNetworkReply *m_createReply = nullptr;
    QNetworkReply *m_chatReply = nullptr;

    static const QString BASE_URL;
    static const QString TAGS_URL;
    static const QString CHAT_URL;
    static const QString SHOW_URL;
    static const QString DELETE_URL;
    static const QString PULL_URL;
    static const QString PUSH_URL;
    static const QString CREATE_URL;
    static const QString EMBED_URL;
    static const QString OFFLINE_MODELS_PATH;

    QByteArray m_pullBuffer;
    QByteArray m_pushBuffer;
    QByteArray m_createBuffer;
};

#endif // OLLAMAMANAGER_H