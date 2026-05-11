import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: pushDialog
    title: "Push Model"
    standardButtons: Dialog.Ok | Dialog.Cancel
    modal: true
    ColumnLayout {
        Label { text: "Model name:" }
        TextField { id: pushModelField; text: backend.currentModel }
        Label { text: "Namespace (optional):" }
        TextField { id: pushNamespaceField; placeholderText: "e.g., library" }
        BusyIndicator {
            running: backend.pushInProgress
            visible: backend.pushInProgress
        }
        Label {
            visible: backend.pushInProgress
            text: backend.pushProgressText
        }
    }
    onAccepted: {
        if (pushModelField.text.trim() !== "") {
            backend.pushModel(pushModelField.text.trim(), pushNamespaceField.text.trim())
        }
    }
    onVisibleChanged: if (visible) { pushModelField.text = backend.currentModel; pushNamespaceField.text = "" }
}