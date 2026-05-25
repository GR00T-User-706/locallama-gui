import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: copyDialog
    title: "Copy Model"
    standardButtons: Dialog.Ok | Dialog.Cancel
    modal: true
    property string sourceModel: backend.currentModel
    ColumnLayout {
        Label { text: "Source: " + sourceModel }
        Label { text: "New model name:" }
        TextField { id: copyModelNameField }
    }
    onAccepted: {
        if (copyModelNameField.text.trim() !== "") {
            backend.copyModel(sourceModel, copyModelNameField.text.trim())
        }
    }
    onVisibleChanged: if (visible) copyModelNameField.text = ""
}