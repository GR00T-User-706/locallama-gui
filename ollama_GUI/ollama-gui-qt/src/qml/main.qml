import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtQuick.Dialogs 1.3

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 800
    height: 700
    title: "Local LLM"

    // Menu bar
    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Load System Prompt..."; onTriggered: fileDialog.open() }
            MenuSeparator {}
            MenuItem { text: "Restart Server"; onTriggered: backend.restartServer() }
            MenuItem { text: "Quit"; onTriggered: Qt.quit() }
        }
        Menu {
            title: "Edit"
            MenuItem { text: "Clear Chat"; onTriggered: backend.clearChat() }
            MenuItem { text: "Interrupt"; onTriggered: backend.interruptResponse(); enabled: backend.responseActive }
        }
        Menu {
            title: "Models"
            MenuItem { text: "Show Available Models"; onTriggered: backend.showAvailableModels() }
            MenuItem { text: "Refresh Models"; onTriggered: backend.refreshModels() }
            MenuItem { text: "Pull Model..."; onTriggered: pullModelDialog.open() }
            MenuItem { text: "Push Model..."; onTriggered: pushDialog.open() }
            MenuItem { text: "Create Model..."; onTriggered: createDialog.open() }
            MenuItem { text: "Copy Model..."; onTriggered: copyDialog.open() }
            MenuItem { text: "Delete Model..."; onTriggered: deleteConfirmation.open() }
            MenuItem { text: "Show Model Info"; onTriggered: { infoDialog.modelName = backend.currentModel; infoDialog.open() } }
            MenuSeparator {}
            Menu {
                title: "Set Parameters"
                MenuItem { text: "Temperature..."; onTriggered: paramDialog.showFor("temperature", backend.temperature) }
                MenuItem { text: "Top P..."; onTriggered: paramDialog.showFor("top_p", backend.topP) }
                MenuItem { text: "Context Length..."; onTriggered: paramDialog.showFor("num_ctx", backend.numCtx) }
            }
        }
        Menu {
            title: "Tools"
            MenuItem { text: "Generate Embeddings..."; onTriggered: embeddingDialog.open() }
            MenuItem { text: "Diagnostics..."; onTriggered: diagnosticsDialog.open() }
        }
        Menu {
            title: "Settings"
            MenuItem {
                text: "Online Mode"
                checkable: true
                checked: backend.onlineMode
                onTriggered: backend.onlineMode = checked
            }
            MenuSeparator {}
            MenuItem { text: "Server Options..."; onTriggered: serverOptionsDialog.open() }
        }
        Menu {
            title: "Help"
            MenuItem { text: "About"; onTriggered: aboutDialog.open() }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5

        // Top bar: model selector and status
        RowLayout {
            Layout.fillWidth: true
            Label { text: "Model:" }
            ComboBox {
                id: modelCombo
                model: backend.models
                Layout.fillWidth: true
                onCurrentTextChanged: backend.currentModel = currentText
                Component.onCompleted: currentIndex = (backend.currentModel !== "") ? model.indexOf(backend.currentModel) : 0
            }
            ToolButton {
                text: "↻"
                onClicked: backend.refreshModels()
                ToolTip.text: "Refresh model list"
                ToolTip.visible: hovered
            }
            BusyIndicator {
                running: backend.modelLoading
                visible: backend.modelLoading
                width: 16; height: 16
            }
            RowLayout {
                Layout.alignment: Qt.AlignRight
                Rectangle {
                    width: 12; height: 12; radius: 6; color: backend.serverStatusColor
                }
                Label {
                    text: backend.serverStatusText
                    color: backend.serverStatusColor
                }
            }
        }

        // System prompt
        Label { text: "System Prompt (optional)" }
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            TextArea {
                id: sysPromptText
                text: backend.systemPrompt
                onTextChanged: backend.systemPrompt = text
                wrapMode: TextArea.Wrap
                placeholderText: "System prompt..."
            }
        }

        // User prompt
        Label { text: "User Prompt" }
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            TextArea {
                id: userPromptText
                text: backend.userPrompt
                onTextChanged: backend.userPrompt = text
                wrapMode: TextArea.Wrap
                placeholderText: "Your message..."
                Keys.onReturnPressed: {
                    if (!(event.modifiers & Qt.ShiftModifier)) {
                        backend.runChat();
                        event.accepted = true;
                    }
                }
            }
        }

        // Run / Interrupt button
        Button {
            text: backend.responseActive ? "Interrupt" : "Run"
            enabled: backend.serverRunning
            onClicked: {
                if (backend.responseActive) {
                    backend.interruptResponse();
                } else {
                    backend.runChat();
                }
            }
        }

        // Output display
        Label { text: "Chat Output" }
        ScrollView {
            id: outputScroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            TextArea {
                id: outputArea
                text: backend.outputText
                readOnly: true
                wrapMode: TextArea.Wrap
                onTextChanged: {
                    outputScroll.ScrollBar.vertical.position = 1.0;
                }
            }
        }
    }

    // ----- Dialogs (existing + new) -----
    FileDialog {
        id: fileDialog
        title: "Load System Prompt"
        nameFilters: ["Text files (*.txt)", "All files (*)"]
        onAccepted: backend.loadSystemPromptFromFile(fileUrl)
    }

    Dialog {
        id: pullModelDialog
        title: "Pull Model"
        standardButtons: Dialog.Ok | Dialog.Cancel
        ColumnLayout {
            Label { text: "Model name:" }
            TextField { id: pullModelField }
        }
        onAccepted: {
            if (pullModelField.text.trim() !== "") {
                backend.pullModel(pullModelField.text.trim());
            }
        }
    }

    DeleteModelDialog {
        id: deleteConfirmation
        modelName: backend.currentModel
    }

    ModelInfoDialog {
        id: infoDialog
    }

    PullProgressDialog {
        id: pullProgress
    }

    PushDialog {
        id: pushDialog
    }

    CreateModelDialog {
        id: createDialog
    }

    CopyModelDialog {
        id: copyDialog
    }

    EmbeddingDialog {
        id: embeddingDialog
    }

    DiagnosticsDialog {
        id: diagnosticsDialog
    }

    Dialog {
        id: paramDialog
        title: "Set Parameter"
        standardButtons: Dialog.Ok | Dialog.Cancel
        property string paramName: ""
        property alias valueText: paramTextField.text

        ColumnLayout {
            Label { text: paramDialog.paramName + " value:" }
            TextField { id: paramTextField }
        }
        onAccepted: {
            if (paramDialog.paramName !== "" && paramTextField.text !== "") {
                backend.setParameter(paramDialog.paramName, paramTextField.text);
            }
        }

        function showFor(param, defaultValue) {
            paramName = param;
            paramTextField.text = defaultValue;
            open();
        }
    }

    Dialog {
        id: serverOptionsDialog
        title: "Server Options"
        standardButtons: Dialog.Ok
        ColumnLayout {
            Label { text: "Server Configuration"; font.bold: true }
            Label { text: "OLLAMA_HOST: 127.0.0.1:11434" }
            Label { text: "Current mode: " + (backend.onlineMode ? "online" : "offline") }
            Label { text: "Models path: " + (backend.onlineMode ? "~/.ollama/models" : "/home/lykthornyx/.ollama/models") }
            Label { text: "Server status: " + backend.serverStatusText }
        }
    }

    Dialog {
        id: aboutDialog
        title: "About"
        standardButtons: Dialog.Ok
        ColumnLayout {
            Label { text: "Developer: Zenrich ShadowStep" }
            Label { text: "Contact: crypto_code_weaver_syndicate@proton.me" }
            Label { text: "Local LLM Interface" }
            LAbel { text: "Version" + Qt.application.version }
            Label { text: "Ollama frontend" }
            Label { text: "Runs completely offline\nModels stored locally" }
        }
    }
}