import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: embeddingDialog
    title: "Generate Embeddings"
    standardButtons: Dialog.Ok | Dialog.Cancel
    modal: true
    ColumnLayout {
        Label { text: "Prompt:" }
        TextArea {
            id: embedPrompt
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            wrapMode: TextArea.Wrap
        }
        Label { text: "Model (empty = current):" }
        TextField { id: embedModelField; placeholderText: backend.currentModel }
        Label { text: "Result will appear in chat output." }
    }
    onAccepted: {
        var prompt = embedPrompt.text.trim()
        if (prompt !== "") {
            var model = embedModelField.text.trim() === "" ? backend.currentModel : embedModelField.text.trim()
            backend.generateEmbedding(prompt, model)
        }
    }
    onVisibleChanged: if (visible) embedPrompt.text = ""
}